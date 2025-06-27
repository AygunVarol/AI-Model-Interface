# AI Model Interface 🤖

A beautiful web interface for interacting with multiple AI models via Ollama. Switch between different models seamlessly with a modern, responsive UI supporting both light and dark themes.

## ✨ Features

- **Multiple AI Models**: Support for 4 different models (Phi-4, DeepSeek R1, Dolphin Mixtral, Llama2 Uncensored)
- **Real-time Streaming**: Live response streaming for immediate feedback
- **Modern UI**: Clean, responsive design with dark/light theme toggle
- **Model Information**: Dynamic model descriptions and parameter counts
- **Easy Setup**: Simple installation process with clear instructions

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** installed on your system
2. **Ollama** installed and running ([Download Ollama](https://ollama.ai))

### Installation Steps

1. **Clone or download the project files**
   ```bash
   git clone <your-repo-url>
   cd ai-model-interface
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install AI models** (choose the ones you want)
   ```bash
   # Install all models (recommended)
   ollama pull phi4
   ollama pull deepseek-r1:14b
   ollama pull dolphin-mixtral:8x7b
   ollama pull llama2-uncensored
   
   # Or install just one to get started
   ollama pull phi4
   ```

5. **Start the application**
   ```bash
   python app.py
   ```

6. **Open your browser** and go to: `http://localhost:5000`

## 📁 Project Structure

```
ai-model-interface/
├── app.py              # Flask backend application
├── requirements.txt    # Python dependencies
├── templates/
│   └── index2.html    # Web interface
└── README.md          # This file
```

## 🤖 Supported Models

| Model | Size | Description |
|-------|------|-------------|
| **Phi-4 Mini** | 3.8B | Microsoft's compact reasoning model |
| **DeepSeek R1** | 14B | Advanced reasoning model with strong performance |
| **Dolphin Mixtral** | 8x7B | Uncensored fine-tune of Mixtral mixture of experts |
| **Llama2 Uncensored** | 7B | Uncensored version of Meta's Llama2 |

## 🛠️ Usage

1. **Select a Model**: Choose from the dropdown menu
2. **Enter Your Prompt**: Type your question or request
3. **Submit**: Click submit or press Enter (Shift+Enter for new lines)
4. **Watch the Response**: See the AI response stream in real-time

## 🎨 Interface Features

- **Theme Toggle**: Switch between light and dark modes
- **Model Information**: See model details when you select different options
- **Responsive Design**: Works great on desktop, tablet, and mobile
- **Keyboard Shortcuts**: Enter to submit, Shift+Enter for new lines
- **Real-time Streaming**: Watch responses appear as they're generated

## 🔧 Troubleshooting

### Model Not Found Error
If you see "model not found" errors:
```bash
# Check what models you have installed
ollama list

# Install missing models
ollama pull <model-name>
```

### Ollama Connection Issues
Make sure Ollama is running:
```bash
# Check if Ollama is running
ollama list

# If not running, start it
ollama serve
```

### Port Already in Use
If port 5000 is busy, change it in `app.py`:
```python
app.run(host="0.0.0.0", port=5001)  # Use port 5001 instead
```

## 🔍 API Endpoints

- `GET /` - Web interface
- `POST /api/infer` - Submit prompts and get streaming responses
- `GET /api/models` - Check available models

### API Usage Example
```bash
curl -X POST http://localhost:5000/api/infer \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello, how are you?", "model": "phi4"}'
```

## 🎯 Tips for Best Results

1. **Start with Phi-4**: It's fast and works well for most tasks
2. **Use DeepSeek R1**: For complex reasoning and analysis
3. **Try Dolphin Mixtral**: For creative and uncensored responses
4. **Clear Prompts**: Be specific about what you want
5. **Model Selection**: Different models excel at different tasks

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve this interface!

## 📄 License

This project is open source. Feel free to modify and distribute.

## 🆘 Support

If you encounter issues:

1. Check that Ollama is running: `ollama list`
2. Verify models are installed: `ollama pull <model-name>`
3. Check the console output for error messages
4. Ensure Python dependencies are installed: `pip install -r requirements.txt`

---

**Enjoy chatting with AI! 🚀**
