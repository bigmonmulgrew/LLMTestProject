import http.server
import json
import os
import logging
from ai_handler import call_ai_model, models_config

# Configuration
PROMPT_DIR = "prompts"
LAST_PROMPT_FILE = "last_prompt.txt"

LOG_FILE = "server.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def read_file(file_path, default_value=""):
    """Reads a file and returns its content, or a default value if the file is missing."""
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return f.read().strip()
    return default_value

def read_json_file(file_path):
    """Reads a JSON file and returns its content, or None if the file is missing."""
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return None

def write_json_file(file_path, data):
    """Writes a dictionary to a JSON file with proper indentation."""
    try:
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        logging.error(f"Failed to write JSON file '{file_path}': {e}")


class HttpRequestHandler(http.server.BaseHTTPRequestHandler):
    def _set_headers(self, content_type="application/json"):
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        """Handle CORS preflight request."""
        self._set_headers()
        self.end_headers()

    def do_GET(self):
        if self.path == "/get_models":
            self.do_GET_models()
        elif self.path == "/get_prompts":
            self.do_GET_prompts()
        elif self.path == "/get_last_prompt":
            self.do_GET_last_prompt()
        elif self.path.startswith("/get_prompt"):
            self.do_GET_prompt()
    
    def do_GET_models(self):
        models_list = list(models_config.keys())  # Extract model names
        self._set_headers()
        self.wfile.write(json.dumps({"models": models_list}).encode("utf-8"))

    def do_GET_prompts(self):
        prompts = [f.replace(".json", "") for f in os.listdir(PROMPT_DIR) if f.endswith(".json")]
        self._set_headers()
        self.wfile.write(json.dumps(prompts).encode("utf-8"))

    def do_GET_last_prompt(self):
        """Handles missing last prompt file gracefully."""
        last_prompt = read_file(LAST_PROMPT_FILE)

        self._set_headers()
        self.wfile.write(json.dumps({"last_prompt": last_prompt}).encode("utf-8"))

    def do_GET_prompt(self):
        query = self.path.split("?name=")
        if len(query) < 2:
            self.send_response(400)
            self.end_headers()
            return
        
        prompt_name = query[1].split("&")[0]
        version_param = query[1].split("&version=")[-1] if "&version=" in query[1] else "latest"
        file_path = os.path.join(PROMPT_DIR, f"{prompt_name}.json")

        prompt_data = read_json_file(file_path)
        if prompt_data is None:
            logging.warning(f"GET request failed: Prompt file '{file_path}' not found.")
            self.send_response(404)
            self.end_headers()
            return

        latest_version = prompt_data["versions"][-1] if version_param == "latest" else \
                next((v for v in prompt_data["versions"] if str(v["version"]) == version_param), prompt_data["versions"][-1])

        logging.info(f"Serving prompt '{prompt_name}' version {version_param}")
        self._set_headers()
        self.wfile.write(json.dumps({"prompt": latest_version["prompt"], "versions": prompt_data["versions"]}).encode("utf-8"))

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)

        if not post_data:  # Prevents empty request crash
            logging.error("POST request failed: Received empty request body.")
            self.send_response(400)
            self.end_headers()
            return
        
        try:
            data = json.loads(post_data.decode("utf-8"))

            if self.path == "/save_prompt":  
                self.do_POST_save_prompt(data)            
            elif self.path == "/send_message":  
                self.do_POST_send_message(data)
            else:  
                self.send_response(404)
                self.end_headers()

        except Exception as e:
            logging.error(f"Error in POST request handling: {e}")  
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

    def do_POST_save_prompt(self, data):
        prompt_name = data.get("name", "").strip().replace(" ", "_")
        new_prompt = data.get("prompt", "").strip()

        if not prompt_name:
            logging.error("Missing prompt name in request.")
            self.send_response(400)
            self.end_headers()
            return

        if not new_prompt:
            logging.error("Missing prompt text in request.")
            self.send_response(400)
            self.end_headers()
            return

        # Proceed with saving prompt
        file_path = os.path.join(PROMPT_DIR, f"{prompt_name}.json")
        prompt_data = read_json_file(file_path) or {"name": prompt_name, "versions": []}
        
        last_prompt = prompt_data["versions"][-1]["prompt"] if prompt_data["versions"] else ""
        if last_prompt == new_prompt:
            self._set_headers()
            self.wfile.write(json.dumps({"message": "No changes detected."}).encode("utf-8"))
            return
        
        # Increment version and save new entry
        new_version = len(prompt_data["versions"]) + 1
        prompt_data["versions"].append({"version": new_version, "prompt": new_prompt})

        write_json_file(file_path, prompt_data)

        # Save last used prompt only if it's a new prompt
        if data.get("name"):
            write_json_file(LAST_PROMPT_FILE, prompt_name)

        self._set_headers()
        self.wfile.write(json.dumps({"message": f"Saved as version {new_version}."}).encode("utf-8"))

    def do_POST_send_message(self, data):
        history = data.get("history", [])
        model_name = data.get("model", "llama-2-7b")

        # Handle missing last prompt file
        last_prompt = read_file(LAST_PROMPT_FILE)
        
        prompt_file = os.path.join(PROMPT_DIR, f"{last_prompt}.json")
        prompt_data = read_json_file(prompt_file)

        if prompt_data:
            system_prompt = prompt_data["versions"][-1]["prompt"]
        else:
            system_prompt = "You are an AI assistant."

        logging.info(f"Processing AI request with system prompt: {system_prompt[:50]}...")  # Trim long prompts for logging
        logging.info(f"Using model: {model_name}")

        # Use AI model
        ai_response = call_ai_model(system_prompt, history, model_name)

        self._set_headers()
        self.wfile.write(json.dumps({"response": ai_response}).encode("utf-8"))


