LLMTestProject
LLMTestProject is a local AI model testing tool that allows you to run, test, and compare different LLMs (Large Language Models) like Llama 2, Llama 3.2, Mistral 7B, and OpenChat (Ollama).

It provides a web-based interface where users can:

Select AI models dynamically
Store and manage system prompts
Send messages to different AI models
Retrieve AI-generated responses
Features

Run local AI models (Llama 2, Llama 3.2, Mistral 7B, OpenChat)
Dynamically select models from a dropdown
Save and retrieve system prompts with versioning
Supports multiple AI backends (llama-cpp-python, ctransformers, ollama)
Clean, modular, and extensible design
Installation

Clone the Repository
git clone https://github.com/your-repo/LLMTestProject.git
cd LLMTestProject

Install Dependencies

Python Dependencies
pip install -r requirements.txt

Ensure you have the required libraries installed:

llama-cpp-python (for Llama models)
ctransformers (for Mistral 7B)
huggingface_hub (for downloading models)
ollama (for OpenChat)
Install Ollama (For OpenChat)
winget install Ollama.Ollama
ollama pull openchat

Download AI Models
You must manually download and place AI models inside the models/ directory.
Llama 2, Llama 3.2, Mistral 7B

Get the models from Hugging Face (https://huggingface.co/meta-llama)
Place .gguf files in the models/ folder
Example:
mkdir models
wget https://huggingface.co/meta-llama/Llama-3.2-7B-GGUF/resolve/main/llama-3.2-7b.Q4_K_M.gguf -O models/llama-3.2-7b.gguf

Run the Server
python run_server.py
This will:

Start the PHP web server on http://localhost:18085
Start the Python API server on http://localhost:18086
API Endpoints

Get Available AI Models
GET /get_models
Response:
{
"models": ["llama-2-7b", "llama-2-13b", "mistral-7b", "llama-3.2-7b", "openchat"]
}
Purpose: Returns a list of available AI models.

Get List of System Prompts
GET /get_prompts
Response:
["Example_Prompt_1", "Example_Prompt_2"]
Purpose: Returns a list of stored system prompts.

Get the Last Used System Prompt
GET /get_last_prompt
Response:
{
"last_prompt": "Example_Prompt_1"
}
Purpose: Retrieves the name of the last system prompt used.

Get a Specific System Prompt
GET /get_prompt?name=Example_Prompt_1&version=latest
Response:
{
"prompt": "You are an AI assistant.",
"versions": [
{"version": 1, "prompt": "You are an AI assistant."},
{"version": 2, "prompt": "You are an advanced AI assistant."}
]
}
Purpose: Retrieves the latest or a specific version of a system prompt.

Save a System Prompt
POST /save_prompt
Content-Type: application/json
{
"name": "Example_Prompt_1",
"prompt": "You are a helpful AI."
}

Response:
{
"message": "Saved as version 3."
}
Purpose: Saves a new system prompt or a new version if the text has changed.

Send a Message to an AI Model
POST /send_message
Content-Type: application/json
{
"history": ["Hello!", "How are you?"],
"model": "llama-2-7b"
}

Response:
{
"response": "I am doing well, thank you!"
}
Purpose: Sends a conversation history to the selected AI model and returns a response.

Configuration

models.conf
All available models are stored in models.conf.
To add new models, edit this file:

{
"llama-2-7b": {
"file": "models/llama-2-7b-chat.gguf",
"max_tokens": 512,
"model_type": "llama"
},
"llama-3.2-7b": {
"file": "models/llama-3.2-7b.gguf",
"max_tokens": 1024,
"model_type": "llama"
},
"openchat": {
"file": "openchat",
"max_tokens": 512,
"model_type": "ollama"
}
}

Next Steps

Add support for GPT4All
Improve AI response tracking (tokens, latency, etc.)
Implement real-time UI updates with WebSockets
Add dynamic model management UI
Contributors

[Your Name]
[Other Contributors]
License
MIT License. Free to use, modify, and distribute.