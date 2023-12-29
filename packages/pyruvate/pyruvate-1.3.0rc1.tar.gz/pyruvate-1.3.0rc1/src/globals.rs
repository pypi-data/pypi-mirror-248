use log::{debug, error};
use pyo3::prelude::*;
use pyo3::types::{PyDict, PyModule, PyString};
use std::sync::Arc;
use std::time::Duration;

use crate::transport::SharedConnectionOptions;

pub struct WSGIOptions {
    pub server_name: String,
    pub server_port: String,
    pub script_name: String,
    pub io_module: Py<PyModule>,
    pub sys_module: Py<PyModule>,
    pub wsgi_module: Option<Py<PyModule>>,
    pub wsgi_environ: Py<PyDict>,
    pub peer_addr_key: Py<PyString>,
    pub content_length_key: Py<PyString>,
    pub wsgi_input_key: Py<PyString>,
    pub chunked_transfer: bool,
    pub qmon_warn_threshold: Option<usize>,
    pub send_timeout: Duration,
}

impl WSGIOptions {
    pub fn new(
        server_name: String,
        server_port: String,
        script_name: String,
        chunked_transfer: bool,
        qmon_warn_threshold: Option<usize>,
        send_timeout: Duration,
        py: Python,
    ) -> WSGIOptions {
        // XXX work around not being able to import wsgi module from tests
        let wsgi_module: Option<Py<PyModule>> = match py.import("pyruvate") {
            Ok(pyruvate) => Some(pyruvate.into()),
            Err(_) => {
                error!("Could not import WSGI module, so no FileWrapper");
                // PyErr::fetch(py);
                None
            }
        };
        let sys_module = py.import("sys").expect("Could not import module sys");
        let wsgi_environ = Self::prepare_wsgi_environ(
            &server_name,
            &server_port,
            &script_name,
            sys_module,
            wsgi_module.as_ref(),
            py,
        )
        .expect("Could not create wsgi environ template");
        let io_module = py.import("io").expect("Could not import module io");
        WSGIOptions {
            server_name,
            server_port,
            script_name,
            io_module: io_module.into(),
            sys_module: sys_module.into(),
            wsgi_module,
            wsgi_environ,
            peer_addr_key: PyString::new(py, "REMOTE_ADDR").into(),
            content_length_key: PyString::new(py, "CONTENT_LENGTH").into(),
            wsgi_input_key: PyString::new(py, "wsgi.input").into(),
            chunked_transfer,
            qmon_warn_threshold,
            send_timeout,
        }
    }

    fn prepare_wsgi_environ(
        server_name: &str,
        server_port: &str,
        script_name: &str,
        sys: &PyModule,
        wsgi: Option<&Py<PyModule>>,
        py: Python,
    ) -> PyResult<Py<PyDict>> {
        let environ = PyDict::new(py);
        environ.set_item("SERVER_NAME", server_name)?;
        environ.set_item("SERVER_PORT", server_port)?;
        environ.set_item("SCRIPT_NAME", script_name)?;
        environ.set_item("wsgi.errors", sys.getattr("stderr")?)?;
        environ.set_item("wsgi.version", (1, 0))?;
        environ.set_item("wsgi.multithread", false)?;
        environ.set_item("wsgi.multiprocess", true)?;
        environ.set_item("wsgi.run_once", false)?;
        environ.set_item("wsgi.url_scheme", "http")?;
        if let Some(wsgi) = wsgi {
            debug!("Setting FileWrapper in environ");
            environ.set_item("wsgi.file_wrapper", wsgi.getattr(py, "FileWrapper")?)?;
        }
        Ok(environ.into())
    }
}

pub type SharedWSGIOptions = Arc<WSGIOptions>;

pub fn shared_wsgi_options(
    server_name: String,
    server_port: String,
    script_name: String,
    chunked_transfer: bool,
    qmon_warn_threshold: Option<usize>,
    send_timeout: Duration,
    py: Python,
) -> SharedWSGIOptions {
    Arc::new(WSGIOptions::new(
        server_name,
        server_port,
        script_name,
        chunked_transfer,
        qmon_warn_threshold,
        send_timeout,
        py,
    ))
}

pub struct ServerOptions {
    pub num_workers: usize,
    pub max_number_headers: usize,
    pub connection_options: SharedConnectionOptions,
    pub wsgi_options: SharedWSGIOptions,
}

#[cfg(test)]
mod tests {
    use crate::globals::WSGIOptions;
    use log::debug;
    use pyo3::Python;
    use std::time::Duration;

    #[test]
    fn test_creation() {
        Python::with_gil(|py| {
            let sn = String::from("127.0.0.1");
            let sp = String::from("7878");
            let script = String::from("/foo");
            let pypath = py.import("sys").unwrap().getattr("path").unwrap();
            debug!("sys.path: {:?}", pypath);
            let got = WSGIOptions::new(
                sn.clone(),
                sp.clone(),
                script.clone(),
                false,
                None,
                Duration::from_secs(60),
                py,
            );
            assert!(got.server_name == sn);
            assert!(got.server_port == sp);
            assert!(got.script_name == script);
        });
    }
}
