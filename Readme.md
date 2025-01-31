# LLMTestProject

LLMTestProject is a **local AI model testing tool** that allows you to run, test, and compare different **LLMs** (Large Language Models) like **Llama 2, Llama 3.2, Mistral 7B, and OpenChat (Ollama)**.

It provides a **web-based interface** where users can:
- **Select AI models dynamically**
- **Store and manage system prompts**
- **Send messages to different AI models**
- **Retrieve AI-generated responses**

---

## 🚀 Features
✅ **Run local AI models** (Llama 2, Llama 3.2, Mistral 7B, OpenChat)  
✅ **Dynamically select models from a dropdown**  
✅ **Save and retrieve system prompts with versioning**  
✅ **Supports multiple AI backends (`llama-cpp-python`, `ctransformers`, `ollama`)**  
✅ **Clean, modular, and extensible design**

---

## 📌 Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-repo/LLMTestProject.git
cd LLMTestProject
```

### 2️⃣ Install Dependencies

#### Python Dependencies
```bash
pip install -r requirements.txt
```
Ensure you have the required libraries installed:
- `llama-cpp-python` (for Llama models)
- `ctransformers` (for Mistral 7B)
- `huggingface_hub` (for downloading models)
- `ollama` (for OpenChat)

#### Install Ollama (For OpenChat)
```bash
winget install Ollama.Ollama
ollama pull openchat
```

### 3️⃣ Download AI Models
You must manually download and place AI models inside the `models/` directory.

#### Llama 2, Llama 3.2, Mistral 7B
1. Get the models from [Hugging Face](https://huggingface.co/meta-llama)  
2. Place `.gguf` files in the `models/` folder

Example:
```bash
mkdir models
wget https://huggingface.co/meta-llama/Llama-3.2-7B-GGUF/resolve/main/llama-3.2-7b.Q4_K_M.gguf -O models/llama-3.2-7b.gguf
```

### 4️⃣ Run the Server
```bash
python run_server.py
```
This will:
- Start the **PHP web server** on `http://localhost:18085`
- Start the **Python API server** on `http://localhost:18086`

---

## 🌍 API Endpoints
The Python API provides multiple endpoints for managing AI models and system prompts.

### 📌 1. Get Available AI Models
```http
GET /get_models
```
**Response:**
```json
{
    "models": ["llama-2-7b", "llama-2-13b", "mistral-7b", "llama-3.2-7b", "openchat"]
}
```

### 📌 2. Get List of System Prompts
```http
GET /get_prompts
```
**Response:**
```json
["Example_Prompt_1", "Example_Prompt_2"]
```

### 📌 3. Get the Last Used System Prompt
```http
GET /get_last_prompt
```
**Response:**
```json
{
    "last_prompt": "Example_Prompt_1"
}
```

### 📌 4. Get a Specific System Prompt
```http
GET /get_prompt?name=Example_Prompt_1&version=latest
```
**Response:**
```json
{
    "prompt": "You are an AI assistant.",
    "versions": [
        {"version": 1, "prompt": "You are an AI assistant."},
        {"version": 2, "prompt": "You are an advanced AI assistant."}
    ]
}
```

### 📌 5. Save a System Prompt
```http
POST /save_prompt
Content-Type: application/json

{
    "name": "Example_Prompt_1",
    "prompt": "You are a helpful AI."
}
```
**Response:**
```json
{
    "message": "Saved as version 3."
}
```

### 📌 6. Send a Message to an AI Model
```http
POST /send_message
Content-Type: application/json

{
    "history": ["Hello!", "How are you?"],
    "model": "llama-2-7b"
}
```
**Response:**
```json
{
    "response": "I am doing well, thank you!"
}
```

---

## 🛠 Configuration

### 🔧 `models.conf`
All available models are stored in `models.conf`.  
To add new models, edit this file:

```json
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
```

---

## 🎯 Next Steps
- **[ ] Add support for GPT4All**
- **[ ] Improve AI response tracking (tokens, latency, etc.)**
- **[ ] Implement real-time UI updates with WebSockets**
- **[ ] Add dynamic model management UI**

---

## 👨‍💻 Contributors
- **David Mulgrew**

---

## 📜 License
MIT License. Free to use, modify, and distribute.

