import os
from flask import Flask, request, jsonify, render_template
import ollama

app = Flask(__name__)

# Create a global Ollama client for reuse
ollama_client = ollama.Client()

# Model mapping from frontend values to Ollama model names
MODEL_MAP = {
    'phi4': 'phi4',
    'deepseek-r1:14b': 'deepseek-r1:14b',
    'dolphin-mixtral:8x7b': 'dolphin-mixtral:8x7b',
    'dolphin-mixtral:8x22b': 'dolphin-mixtral:8x22b',
    'llama2-uncensored': 'llama2-uncensored',
    'llama2-uncensored:70b': 'llama2-uncensored:70b'
}

# Model information for validation and display
MODEL_INFO = {
    'phi4': {
        'name': 'Phi-4 Mini Instruct',
        'size': '3.8B',
        'description': 'Microsoft\'s compact reasoning model'
    },
    'deepseek-r1:14b': {
        'name': 'DeepSeek R1',
        'size': '14B',
        'description': 'Advanced reasoning model with strong performance'
    },
    'dolphin-mixtral:8x7b': {
        'name': 'Dolphin Mixtral',
        'size': '8x7B',
        'description': 'Uncensored fine-tune of Mixtral mixture of experts'
    },
    'dolphin-mixtral:8x22b': {
        'name': 'Dolphin Mixtral',
        'size': '8x22B',
        'description': 'Larger uncensored fine-tune of Mixtral mixture of experts'
    },
    'llama2-uncensored': {
        'name': 'Llama2 Uncensored',
        'size': '7B',
        'description': 'Uncensored version of Meta\'s Llama2'
    },
    'llama2-uncensored:70b': {
        'name': 'Llama2 Uncensored',
        'size': '70B',
        'description': 'Large uncensored version of Meta\'s Llama2'
    }
}

@app.route('/')
def index():
    return render_template('index.html')  # Updated to use your new HTML file

@app.route('/api/models', methods=['GET'])
def get_available_models():
    """Endpoint to check which models are available in Ollama"""
    try:
        models = ollama_client.list()
        available_models = []
        
        for model_key, ollama_name in MODEL_MAP.items():
            is_available = any(
                ollama_name in model['name'] or model['name'] == ollama_name 
                for model in models['models']
            )
            
            model_data = MODEL_INFO[model_key].copy()
            model_data['key'] = model_key
            model_data['ollama_name'] = ollama_name
            model_data['available'] = is_available
            available_models.append(model_data)
        
        return jsonify({'models': available_models})
    
    except Exception as e:
        return jsonify({'error': f'Error checking models: {str(e)}'}), 500

def generate_response(prompt, model_name):
    """Generate streaming response using the specified model"""
    first_token = True
    try:
        print(f"Generating response with model: {model_name}")
        
        # Start generation in streaming mode
        token_generator = ollama_client.generate(
            model=model_name,
            prompt=prompt,
            stream=True
        )
        
        for token in token_generator:
            # Extract the response text if available; otherwise fallback to str(token)
            token_text = token.response if hasattr(token, "response") and token.response is not None else str(token)
            
            # Skip if token_text is empty
            if not token_text.strip():
                continue
                
            if first_token:
                yield token_text.encode('utf-8')
                first_token = False
            else:
                # Split the token text into words and yield each word individually,
                # prepending a space for separation.
                words = token_text.split()
                for word in words:
                    yield (" " + word).encode('utf-8')
                    
    except ollama.ResponseError as e:
        error_msg = f"\nModel error: {str(e)}"
        if "model not found" in str(e).lower():
            error_msg += f"\nPlease run: ollama pull {model_name}"
        yield error_msg.encode('utf-8')
    except Exception as e:
        yield f"\nError during streaming: {str(e)}".encode('utf-8')

@app.route('/api/infer', methods=['POST'])
def infer():
    try:
        data = request.get_json(force=True)
        prompt = data.get("prompt", "")
        model_key = data.get("model", "phi4")  # Default to phi4 if not specified
        
        if not prompt:
            return jsonify({"response": "No prompt provided."}), 400
        
        # Validate model selection
        if model_key not in MODEL_MAP:
            return jsonify({"response": f"Invalid model selection: {model_key}"}), 400
        
        # Get the actual Ollama model name
        ollama_model_name = MODEL_MAP[model_key]
        
        print(f"Request received - Model: {model_key} ({ollama_model_name}), Prompt length: {len(prompt)}")
       
        # Return a streaming plain-text response
        return app.response_class(
            generate_response(prompt, ollama_model_name), 
            mimetype='text/plain'
        )
   
    except ollama.OllamaError as e:
        return jsonify({"response": f"Ollama error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"response": f"Unexpected error: {str(e)}"}), 500

def verify_models():
    """Check which models are available and provide helpful information"""
    try:
        models = ollama_client.list()
        available_model_names = [model['name'] for model in models['models']]
        
        print("=== Model Status Check ===")
        print(f"Available models in Ollama: {len(available_model_names)}")
        
        for model_key, ollama_name in MODEL_MAP.items():
            is_available = any(
                ollama_name in model_name or model_name == ollama_name 
                for model_name in available_model_names
            )
            
            status = "✅ Available" if is_available else "❌ Not found"
            print(f"{MODEL_INFO[model_key]['name']} ({ollama_name}): {status}")
            
            if not is_available:
                print(f"   To install: ollama pull {ollama_name}")
        
        print("=" * 27)
        
        # Check if at least one model is available
        available_count = sum(
            1 for model_key, ollama_name in MODEL_MAP.items()
            if any(ollama_name in model_name or model_name == ollama_name 
                   for model_name in available_model_names)
        )
        
        if available_count == 0:
            print("⚠️  WARNING: No configured models found!")
            print("Please install at least one model using 'ollama pull <model_name>'")
        else:
            print(f"✅ {available_count}/{len(MODEL_MAP)} models are ready to use")
            
    except Exception as e:
        print(f"Error checking models: {e}")
        print("Make sure Ollama is running and accessible")

if __name__ == '__main__':
    print("🚀 Starting AI Model Interface Server...")
    verify_models()
    print("🌍 Server starting on http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)