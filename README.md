# Ollama ChatGPT Clone - README

A fully local ChatGPT-like interface powered by Ollama and Streamlit. Chat with AI models completely offline with conversation memory and multiple model support.

## 🚀 Features

- **Local & Private**: All processing happens on your machine
- **Multiple Models**: Support for llama3, deepseek, qwen
- **Conversation Memory**: Remembers context from previous messages
- **Streaming Responses**: Real-time typing effect
- **No API Costs**: Completely free to use
- **Easy to Use**: Simple installation and intuitive interface

## 📋 Prerequisites

- Windows 10/11
- Python 3.8+
- 8GB+ RAM (16GB recommended for larger models)
- 10GB+ free storage space for models

## 🛠️ Installation

### Manual Installation

#### Step 1: Install Ollama

1. Download Ollama for Windows:
   ```bash
   # Visit the official website:
   https://ollama.com/download/OllamaSetup.exe
   
   # Or download via command line:
   curl -L -o OllamaSetup.exe https://ollama.com/download/OllamaSetup.exe
   ```

2. Run the installer and follow the prompts

3. Verify installation:
   ```bash
   ollama --version
   ```

#### Step 2: Download Models

Download models using these commands:

```bash
# Base models (recommended):
ollama pull llama3:instruct
ollama pull deepseek-r1:7b

# Additional models (optional):
ollama pull qwen3:1.7b
```

#### Step 3: Install Python Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

#### Step 4: Run the Application

```bash
# Start the chat interface
streamlit run app.py
```

## 📊 Available Models

| Model | Size | RAM Required | Best For |
|-------|------|-------------|----------|
| `llama3:instruct` | 4.7GB | 8GB+ | General purpose, instruction following |
| `deepseek-r1:7b` | 4.5GB | 8GB+ | Coding assistance, reasoning |
| `qwen3:1.7b` | 1.7GB | 4GB+ | Lightweight, fast responses |

## 🎮 Usage

### Starting the Application
Run `streamlit run app.py` in your command prompt
Make sure Ollama is running

### Using the Chat Interface

1. **Select a model** from the sidebar dropdown
2. **Adjust parameters** (temperature, max tokens) if desired
3. **Start chatting** by typing in the input box
4. **Use commands** for additional control:
   - `/clear` - Clear current conversation
   - `/save` - Save conversation
   - `/new` - Start new conversation
   - `/memory` - Toggle memory on/off

### Managing Conversations

- **View past conversations** in the sidebar
- **Switch between conversations** by clicking their titles
- **Delete conversations** using the trash can icon
- **Conversations are automatically saved**

## ⚙️ Configuration

### Memory Settings

- **Enable/Disable Memory**: Toggle context retention
- **Memory Size**: Adjust how many previous messages to remember (1-20)
- **View Memory**: Expand "View Memory Contents" to see what the AI remembers

### Model Parameters

- **Temperature**: Controls randomness (0.0 = deterministic, 1.0 = creative)
- **Max Tokens**: Limits response length

## 🔧 Troubleshooting

### Common Issues

1. **"Ollama is not recognized as a command"**
   - Restart your command prompt after installation
   - Ensure Ollama service is running: `sc query Ollama`

2. **"Error: Connection failed"**
   - Start Ollama service: `sc start Ollama`
   - Wait 10-15 seconds for service to initialize

3. **"Out of memory" errors**
   - Use smaller models (phi, qwen3:1.7b)
   - Close other memory-intensive applications
   - Reduce memory size in settings

4. **Slow responses**
   - Some models are slower than others
   - Try qwen3:1.7b or phi for faster responses

### Manual Service Control

```bash
# Check if Ollama service is running
sc query Ollama

# Start the service
sc start Ollama

# Stop the service
sc stop Ollama
```

## 📁 Project Structure

```
ollama-chatgpt-clone/
├── app.py              # Main Streamlit application  
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🚀 Performance Tips

1. **For better performance**:
   - Use smaller models if you have limited RAM
   - Close unnecessary applications while chatting
   - Disable memory for simple queries

2. **For best quality**:
   - Use llama3:instruct or deepseek-r1:7b for complex tasks
   - Enable memory for contextual conversations
   - Adjust temperature based on your needs

## 🤝 Contributing

Feel free to contribute by:
1. Reporting bugs or issues
2. Suggesting new features
3. Adding support for more models
4. Improving the documentation
---

**Note**: This application runs completely locally on your machine. No data is sent to external servers, ensuring complete privacy for your conversations..
