import os
import json
import subprocess
from llama_cpp import Llama
from ctransformers import AutoModelForCausalLM

# Load model configurations from models.conf
CONFIG_FILE = "models.conf"

def load_model_config():
    """Loads model configurations from models.conf"""
    if not os.path.exists(CONFIG_FILE):
        print(f"Error: {CONFIG_FILE} not found.")
        return {}

    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

# Load models
models_config = load_model_config()
loaded_models = {}

for model_name, config in models_config.items():
    model_path = config["file"]
    
    if config["model_type"] == "ollama":
        print(f"Ollama model detected: {model_name}. No preloading required.")
    elif os.path.exists(model_path):
        print(f"Loading {model_name} from {model_path}...")
        if config["model_type"] == "mistral":
            loaded_models[model_name] = AutoModelForCausalLM.from_pretrained(
                model_path, model_type="mistral"
            )
        else:
            loaded_models[model_name] = Llama(model_path=model_path)
    else:
        print(f"Warning: Model {model_name} not found at {model_path}")

def call_ai_model(system_prompt, history, model_name="llama-2-7b"):
    """Calls the selected AI model with the system prompt and chat history."""

    if model_name not in models_config:
        return f"Error: Model '{model_name}' is not available."

    config = models_config[model_name]
    max_tokens = config["max_tokens"]

    try:
        # Format input
        full_prompt = f"<<SYS>>\n{system_prompt}\n<</SYS>>\n\n"
        for msg in history:
            full_prompt += f"User: {msg}\nAI:"

        if config["model_type"] == "ollama":
            # Call Ollama using a subprocess
            # TODO hard coding ollama path for testing, need to make this dynamic
            OLLAMA_PATH = "C:\\Users\\bigmo\\AppData\\Local\\Programs\\Ollama\\ollama.exe"

            result = subprocess.run(
                [OLLAMA_PATH, "run", config["file"], full_prompt], 
                capture_output=True, 
                text=True,
                encoding="utf-8")
            ai_text = result.stdout.strip()

        elif config["model_type"] == "mistral":
            ai_text = loaded_models[model_name](full_prompt, max_new_tokens=max_tokens).strip()

        else:
            response = loaded_models[model_name](full_prompt, max_tokens=max_tokens, stop=["\n"])
            ai_text = response["choices"][0]["text"].strip() if isinstance(response, dict) else response.strip()

        print(f"Generated AI Response: {ai_text}")  # Debugging
        return ai_text if ai_text else "Error: AI generated an empty response."

    except Exception as e:
        return f"AI Error: {str(e)}"