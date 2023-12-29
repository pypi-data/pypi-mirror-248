#![allow(clippy::transmute_ptr_to_ptr, clippy::zero_ptr)]
// suppress warnings in py_class invocation
use log::error;
use pyo3::prelude::*;
use pyo3::types::PyList;
use pyo3::{PyObject, PyResult, Python};
use std::cell::{Cell, RefCell};
use std::cmp;

use crate::request::CONTENT_LENGTH_HEADER;

type WSGIHeaders = Vec<(String, Vec<(String, String)>)>;

#[pyclass]
pub struct StartResponse {
    pub environ: RefCell<PyObject>,
    headers_set: RefCell<WSGIHeaders>,
    headers_sent: RefCell<WSGIHeaders>,
    content_length: Cell<Option<usize>>,
    content_bytes_written: Cell<usize>,
}

#[pymethods]
impl StartResponse {
    #[new]
    fn __new__(environ: PyObject) -> Self {
        Self {
            environ: RefCell::new(environ),
            headers_set: RefCell::new(Vec::new()),
            headers_sent: RefCell::new(Vec::new()),
            content_length: Cell::new(None),
            content_bytes_written: Cell::new(0),
        }
    }

    #[pyo3(signature = (status, headers, exc_info=None))]
    fn __call__(
        &self,
        py: Python,
        status: PyObject,
        headers: PyObject,
        exc_info: Option<PyObject>,
    ) -> PyResult<PyObject> {
        let response_headers: &PyList = headers.extract(py)?;
        if exc_info.is_some() {
            error!(
                "exc_info from application: {:?}",
                exc_info.into_py(py).to_string()
            );
        }
        let mut rh = Vec::<(String, String)>::new();
        for ob in response_headers.iter() {
            rh.push((ob.get_item(0)?.to_string(), ob.get_item(1)?.to_string()));
        }
        self.headers_set.replace(vec![(status.to_string(), rh)]);
        Ok(py.None())
    }

    pub fn get_environ(&self, py: Python) -> PyResult<PyObject> {
        Ok(self.environ.borrow().clone_ref(py))
    }

    fn get_content_length(&self) -> PyResult<Option<usize>> {
        Ok(self.content_length.get())
    }

    fn set_content_length(&self, value: Option<usize>) -> PyResult<()> {
        self.content_length.replace(value);
        Ok(())
    }

    fn get_content_bytes_written(&self) -> PyResult<usize> {
        Ok(self.content_bytes_written.get())
    }

    fn set_content_bytes_written(&self, value: usize) -> PyResult<()> {
        self.content_bytes_written.replace(value);
        Ok(())
    }
}

pub trait WriteResponse {
    // Put this in a trait for more flexibility.
    // rust-cpython can't handle some types we are using here.
    #[allow(clippy::new_ret_no_self)]
    fn new(environ: PyObject, headers_set: WSGIHeaders) -> PyResult<StartResponse>;
    fn content_complete(&self) -> bool;
    fn write(
        &self,
        data: &[u8],
        output: &mut Vec<u8>,
        close_connection: bool,
        chunked_tranfer: bool,
        py: Python,
    );
    fn environ(&self, py: Python) -> PyObject;
    fn content_length(&self, py: Python) -> Option<usize>;
    fn content_bytes_written(&self, py: Python) -> usize;
    fn headers_not_sent(&self, py: Python) -> bool;
}

impl WriteResponse for StartResponse {
    fn new(environ: PyObject, headers_set: WSGIHeaders) -> PyResult<StartResponse> {
        Ok(StartResponse {
            environ: RefCell::new(environ),
            headers_set: RefCell::new(headers_set),
            headers_sent: RefCell::new(Vec::new()),
            content_length: Cell::new(None),
            content_bytes_written: Cell::new(0),
        })
    }

    fn content_complete(&self) -> bool {
        if let Some(length) = self.content_length.get() {
            self.content_bytes_written.get() >= length
        } else {
            false
        }
    }

    fn write(
        &self,
        data: &[u8],
        output: &mut Vec<u8>,
        close_connection: bool,
        chunked_transfer: bool,
        py: Python,
    ) {
        if self.headers_not_sent(py) {
            if self.headers_set.borrow().is_empty() {
                error!("write() before start_response()")
            }
            // Before the first output, send the stored headers
            self.headers_sent.replace(self.headers_set.borrow().clone());
            let respinfo = self.headers_set.borrow_mut().pop(); // headers_sent|set should have only one element
            match respinfo {
                Some(respinfo) => {
                    let response_headers: Vec<(String, String)> = respinfo.1;
                    let status: String = respinfo.0;
                    output.extend(b"HTTP/1.1 ");
                    output.extend(status.as_bytes());
                    output.extend(b"\r\n");
                    let mut maybe_chunked = true;
                    for header in response_headers.iter() {
                        let headername = &header.0;
                        output.extend(headername.as_bytes());
                        output.extend(b": ");
                        output.extend(header.1.as_bytes());
                        output.extend(b"\r\n");
                        if headername.to_ascii_uppercase() == CONTENT_LENGTH_HEADER {
                            match header.1.parse::<usize>() {
                                Ok(length) => {
                                    let _ = self.set_content_length(Some(length));
                                    // no need to use chunked transfer encoding if we have a valid content length header,
                                    // see e.g. https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Transfer-Encoding#Chunked_encoding
                                    maybe_chunked = false;
                                }
                                Err(e) => error!("Could not parse Content-Length header: {:?}", e),
                            }
                        }
                    }
                    output.extend(b"Via: pyruvate\r\n");
                    if close_connection {
                        output.extend(b"Connection: close\r\n");
                    } else {
                        output.extend(b"Connection: keep-alive\r\n");
                    }
                    if maybe_chunked && chunked_transfer {
                        output.extend(b"Transfer-Encoding: chunked\r\n");
                    }
                }
                None => {
                    error!("write(): No respinfo!");
                }
            }
            output.extend(b"\r\n");
        }
        match self.content_length(py) {
            Some(length) => {
                let cbw = self.content_bytes_written(py);
                if length > cbw {
                    let num = cmp::min(length - cbw, data.len());
                    if num > 0 {
                        output.extend(&data[..num]);
                        let _ = self.set_content_bytes_written(cbw + num);
                    }
                }
            }
            None => {
                // no content length header, use
                // chunked transfer encoding if specified
                let cbw = self.content_bytes_written(py);
                let length = data.len();
                if length > 0 {
                    if chunked_transfer {
                        output.extend(format!("{length:X}").as_bytes());
                        output.extend(b"\r\n");
                        output.extend(data);
                        output.extend(b"\r\n");
                    } else {
                        output.extend(data);
                    }
                    let _ = self.set_content_bytes_written(cbw + length);
                }
            }
        }
    }

    fn environ(&self, py: Python) -> PyObject {
        self.environ.borrow().clone_ref(py)
    }

    fn content_length(&self, py: Python) -> Option<usize> {
        match self.get_content_length() {
            Ok(opt) => opt,
            Err(e) => {
                error!("Could not get content_length, {e}");
                PyErr::fetch(py);
                None
            }
        }
    }

    fn content_bytes_written(&self, py: Python) -> usize {
        match self.get_content_bytes_written() {
            Ok(val) => val,
            Err(e) => {
                error!("Could not get content_bytes_written, {e}");
                PyErr::fetch(py);
                0
            }
        }
    }

    fn headers_not_sent(&self, _py: Python) -> bool {
        self.headers_sent.borrow().is_empty()
    }
}

#[cfg(test)]
mod tests {
    use log::LevelFilter;
    use pyo3::types::PyDict;
    use pyo3::Python;
    use simplelog::{Config, WriteLogger};
    use std::env::temp_dir;
    use std::fs::File;
    use std::io::Read;

    use crate::startresponse::{StartResponse, WriteResponse};

    #[test]
    fn test_write() {
        Python::with_gil(|py| {
            let environ = PyDict::new(py);
            let headers = vec![(
                "200 OK".to_string(),
                vec![("Content-type".to_string(), "text/plain".to_string())],
            )];
            let data = b"Hello world!\n";
            let sr = StartResponse::new(environ.into(), headers).unwrap();
            assert_eq!(sr.content_length(py), None);
            assert_eq!(WriteResponse::content_length(&sr, py), None);
            assert!(!sr.content_complete());
            let mut output: Vec<u8> = Vec::new();
            sr.write(data, &mut output, true, false, py);
            let expected =
                b"HTTP/1.1 200 OK\r\nContent-type: text/plain\r\nVia: pyruvate\r\nConnection: close\r\n\r\nHello world!\n";
            assert!(output.iter().zip(expected.iter()).all(|(p, q)| p == q));
            assert!(!sr.content_complete());
            // chunked transfer requested and no content length header
            // The final chunk will be missing; it's written in WSGIResponse::write_chunk
            let expected =
                b"HTTP/1.1 200 OK\r\nContent-type: text/plain\r\nVia: pyruvate\r\nConnection: close\r\nTransfer-Encoding: chunked\r\n\r\nD\r\nHello world!\n";
            let environ = PyDict::new(py);
            let headers = vec![(
                "200 OK".to_string(),
                vec![("Content-type".to_string(), "text/plain".to_string())],
            )];
            let sr = StartResponse::new(environ.into(), headers).unwrap();
            let mut output: Vec<u8> = Vec::new();
            assert!(!sr.content_complete());
            sr.write(data, &mut output, true, true, py);
            assert!(output.iter().zip(expected.iter()).all(|(p, q)| p == q));
            assert!(!sr.content_complete());
        });
    }

    #[test]
    fn test_honour_content_length_header() {
        Python::with_gil(|py| {
            let environ = PyDict::new(py);
            let headers = vec![(
                "200 OK".to_string(),
                vec![
                    ("Content-type".to_string(), "text/plain".to_string()),
                    ("Content-length".to_string(), "5".to_string()),
                ],
            )];
            let sr = StartResponse::new(environ.into(), headers).unwrap();
            let mut output: Vec<u8> = Vec::new();
            let data = b"Hello world!\n";
            assert!(!sr.content_complete());
            sr.write(data, &mut output, true, false, py);
            let expected =
                b"HTTP/1.1 200 OK\r\nContent-type: text/plain\r\nContent-length: 5\r\nVia: pyruvate\r\nConnection: close\r\n\r\nHello";
            assert_eq!(sr.content_length(py), Some(5));
            assert_eq!(WriteResponse::content_length(&sr, py), Some(5));
            assert_eq!(sr.content_bytes_written(py), 5);
            assert!(sr.content_complete());
            assert!(expected.iter().zip(output.iter()).all(|(p, q)| p == q));
            // chunked transfer set - ignored if content length header available
            let environ = PyDict::new(py);
            let headers = vec![(
                "200 OK".to_string(),
                vec![
                    ("Content-type".to_string(), "text/plain".to_string()),
                    ("Content-length".to_string(), "5".to_string()),
                ],
            )];
            let sr = StartResponse::new(environ.into(), headers).unwrap();
            let mut output: Vec<u8> = Vec::new();
            assert!(!sr.content_complete());
            sr.write(data, &mut output, true, true, py);
            let expected =
                b"HTTP/1.1 200 OK\r\nContent-type: text/plain\r\nContent-length: 5\r\nVia: pyruvate\r\nConnection: close\r\n\r\nHello";
            assert_eq!(sr.content_length(py), Some(5));
            assert_eq!(sr.content_bytes_written(py), 5);
            assert!(sr.content_complete());
            assert!(expected.iter().zip(output.iter()).all(|(p, q)| p == q));
        });
    }

    #[test]
    fn test_exc_info_is_none() {
        // do not display an error message when exc_info passed
        // by application is None
        Python::with_gil(|py| {
            let locals = PyDict::new(py);
            let pycode = py.run(
                r#"
status = '200 OK'
response_headers = [('Content-type', 'text/plain'), ("Expires", "Sat, 1 Jan 2000 00:00:00 GMT")]
exc_info = 'Foo'
"#,
                None,
                Some(&locals),
            );
            match pycode {
                Ok(_) => {
                    let status = locals.get_item("status").unwrap().unwrap();
                    let headers = locals.get_item("response_headers").unwrap().unwrap();
                    let exc_info = locals.get_item("exc_info").unwrap().unwrap();
                    let environ = PyDict::new(py);
                    // create logger
                    let mut path = temp_dir();
                    path.push("foo42.log");
                    let path = path.into_os_string();
                    WriteLogger::init(
                        LevelFilter::Info,
                        Config::default(),
                        File::create(&path).unwrap(),
                    )
                    .unwrap();

                    let sr = StartResponse::new(environ.into(), Vec::new()).unwrap();
                    match sr.__call__(py, status.into(), headers.into(), None) {
                        Ok(pynone) if pynone.is_none(py) => {
                            let mut errs = File::open(&path).unwrap();
                            let mut got = String::new();
                            errs.read_to_string(&mut got).unwrap();
                            assert!(!got.contains("exc_info"));
                            assert!(!got.contains("Foo"));
                        }
                        _ => assert!(false),
                    }
                    match sr.__call__(py, status.into(), headers.into(), Some(exc_info.into())) {
                        Ok(pynone) if pynone.is_none(py) => {
                            let mut errs = File::open(&path).unwrap();
                            let mut got = String::new();
                            errs.read_to_string(&mut got).unwrap();
                            assert!(got.len() > 0);
                            assert!(got.contains("exc_info"));
                            assert!(got.contains("Foo"));
                        }
                        _ => assert!(false),
                    }
                }
                _ => assert!(false),
            }
        });
    }
}
