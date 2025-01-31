import socketserver
import subprocess
import logging
import atexit
import socket
from http_handler import HttpRequestHandler

# Configuration
PHP_PORT = 18085
PYTHON_PORT = 18086

# Configure logging
LOG_FILE = "server.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

logging.info("Server is starting...")

def cleanup():
    logging.info("Shutting down servers...")
    php_process.terminate()

# Ensure cleanup runs when the script exits
atexit.register(cleanup)

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("0.0.0.0", port)) == 0

if is_port_in_use(PHP_PORT):
    logging.error(f"Port {PHP_PORT} is already in use. Exiting...")
    exit(1)

if is_port_in_use(PYTHON_PORT):
    logging.error(f"Port {PYTHON_PORT} is already in use. Exiting...")
    exit(1)

try:
    # Start PHP Server
    logging.info(f"Starting PHP server on http://localhost:{PHP_PORT}")
    php_process = subprocess.Popen(["php", "-S", f"0.0.0.0:{PHP_PORT}", "-t", "public"])
except Exception as e:
    logging.error(f"Error starting PHP server: {e}")
    exit(1)  # Exit if PHP server fails to start

try:
    # Start Python API Server
    with socketserver.TCPServer(("0.0.0.0", PYTHON_PORT), HttpRequestHandler) as httpd:
        logging.info(f"Python API server running on http://localhost:{PYTHON_PORT}")
        httpd.serve_forever()
except Exception as e:
    logging.error(f"Error starting Python API server: {e}")
    cleanup()  # Ensure PHP server stops
    exit(1)