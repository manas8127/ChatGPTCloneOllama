import streamlit as st
import ollama
import time
from typing import List, Dict
import json
from datetime import datetime
from collections import deque

# Page configuration
st.set_page_config(
    page_title="ChatOllama - Enhanced Memory",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .chat-container {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .user-message {
        background-color: #d1ecf1;
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
    }
    .assistant-message {
        background-color: #f8d7da;
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
    }
    .stButton button {
        width: 100%;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    .memory-indicator {
        background-color: #e6f7ff;
        border-left: 4px solid #1890ff;
        padding: 10px;
        border-radius: 4px;
        margin: 10px 0;
        font-size: 0.9em;
        color: #0056b3;
    }
    .memory-disabled {
        background-color: #f8f9fa;
        border-left: 4px solid #6c757d;
        padding: 10px;
        border-radius: 4px;
        margin: 10px 0;
        font-size: 0.9em;
        color: #6c757d;
    }
    .conversation-title {
        font-weight: bold;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "model" not in st.session_state:
    st.session_state.model = "llama3:instruct"
if "conversations" not in st.session_state:
    st.session_state.conversations = {}
if "current_conversation" not in st.session_state:
    st.session_state.current_conversation = None
if "temperature" not in st.session_state:
    st.session_state.temperature = 0.7
if "max_tokens" not in st.session_state:
    st.session_state.max_tokens = 2000
if "memory_enabled" not in st.session_state:
    st.session_state.memory_enabled = True
if "memory_size" not in st.session_state:
    st.session_state.memory_size = 10
if "conversation_memory" not in st.session_state:
    st.session_state.conversation_memory = deque(maxlen=st.session_state.memory_size)

# Available models
AVAILABLE_MODELS = [
    "llama3:instruct",
    "deepseek-r1:7b",
    "qwen3:1.7b",
    "llama2",
    "mistral",
    "phi"
]

def get_ollama_models() -> List[str]:
    """Get available Ollama models"""
    try:
        models = ollama.list()
        return [model['name'] for model in models['models']]
    except:
        return AVAILABLE_MODELS

def generate_conversation_title(first_question: str) -> str:
    """Generate a title for the conversation based on the first question"""
    # Simple title generation - use first few words of the question
    words = first_question.split()
    if len(words) <= 5:
        return first_question
    else:
        return " ".join(words[:5]) + "..."

def create_new_conversation():
    """Create a new conversation"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.current_conversation = timestamp
    st.session_state.conversations[timestamp] = {
        "messages": [],
        "title": "New Conversation"
    }
    st.session_state.messages = []
    st.session_state.conversation_memory = deque(maxlen=st.session_state.memory_size)

def update_conversation_title(conversation_id: str, title: str):
    """Update the title of a conversation"""
    if conversation_id in st.session_state.conversations:
        st.session_state.conversations[conversation_id]["title"] = title

def delete_conversation(conversation_id):
    """Delete a conversation"""
    if conversation_id in st.session_state.conversations:
        del st.session_state.conversations[conversation_id]
        if st.session_state.current_conversation == conversation_id:
            create_new_conversation()

def update_memory_size():
    """Update the memory size when changed"""
    st.session_state.conversation_memory = deque(
        st.session_state.conversation_memory, 
        maxlen=st.session_state.memory_size
    )

def get_conversation_context():
    """Get the conversation context from memory"""
    if not st.session_state.memory_enabled:
        return []
    
    # Convert deque to list of messages
    context_messages = []
    for msg in st.session_state.conversation_memory:
        context_messages.append({
            'role': msg['role'],
            'content': msg['content']
        })
    
    return context_messages

def add_to_memory(role, content):
    """Add a message to the conversation memory"""
    if st.session_state.memory_enabled:
        st.session_state.conversation_memory.append({
            'role': role,
            'content': content
        })

def stream_response(prompt: str, model: str, message_placeholder, temperature=0.7, max_tokens=2000):
    """Stream response from Ollama with conversation context"""
    try:
        full_response = ""
        
        # Get conversation context from memory
        context_messages = get_conversation_context()
        
        # Add the current prompt
        context_messages.append({
            'role': 'user',
            'content': prompt
        })
        
        # Generate response
        stream = ollama.chat(
            model=model,
            messages=context_messages,
            stream=True,
            options={
                'temperature': temperature,
                'num_predict': max_tokens
            }
        )
        
        for chunk in stream:
            if 'message' in chunk and 'content' in chunk['message']:
                content = chunk['message']['content']
                full_response += content
                message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response)
        return full_response
        
    except Exception as e:
        error_msg = f"Error: {str(e)}. Make sure Ollama is running on your system."
        message_placeholder.markdown(error_msg)
        return error_msg

def get_conversation_title(conversation_data):
    """Safely get conversation title from conversation data (handles old and new formats)"""
    if isinstance(conversation_data, dict) and "title" in conversation_data:
        return conversation_data["title"]
    elif isinstance(conversation_data, list) and len(conversation_data) > 0:
        # For old format conversations, generate a title from the first user message
        for msg in conversation_data:
            if msg.get("role") == "user":
                return generate_conversation_title(msg.get("content", "Untitled Conversation"))
        return "Untitled Conversation"
    else:
        return "Untitled Conversation"

def get_conversation_messages(conversation_data):
    """Safely get messages from conversation data (handles old and new formats)"""
    if isinstance(conversation_data, dict) and "messages" in conversation_data:
        return conversation_data["messages"]
    elif isinstance(conversation_data, list):
        return conversation_data
    else:
        return []

def migrate_old_conversations():
    """Migrate old format conversations to new format"""
    for conv_id, conv_data in st.session_state.conversations.items():
        if isinstance(conv_data, list):
            # This is an old format conversation, migrate it
            title = "Untitled Conversation"
            for msg in conv_data:
                if msg.get("role") == "user":
                    title = generate_conversation_title(msg.get("content", "Untitled Conversation"))
                    break
            
            st.session_state.conversations[conv_id] = {
                "messages": conv_data,
                "title": title
            }

# Sidebar for model selection and settings
with st.sidebar:
    st.title("⚙️ ChatOllama Settings")
    
    # Model selection
    available_models = get_ollama_models()
    selected_model = st.selectbox(
        "Choose a model:",
        available_models,
        index=available_models.index(st.session_state.model) if st.session_state.model in available_models else 0
    )
    
    if selected_model != st.session_state.model:
        st.session_state.model = selected_model
    
    st.divider()
    
    # Memory settings
    st.subheader("🧠 Memory Settings")
    st.session_state.memory_enabled = st.checkbox("Enable Memory", value=st.session_state.memory_enabled)
    
    if st.session_state.memory_enabled:
        new_memory_size = st.slider("Memory Size (messages)", 1, 20, st.session_state.memory_size, 1)
        if new_memory_size != st.session_state.memory_size:
            st.session_state.memory_size = new_memory_size
            update_memory_size()
        
        # Display current memory contents
        if st.session_state.conversation_memory:
            with st.expander("View Memory Contents"):
                for i, msg in enumerate(st.session_state.conversation_memory):
                    role_emoji = "👤" if msg['role'] == 'user' else "🤖"
                    st.text(f"{role_emoji} {msg['role']}: {msg['content'][:100]}{'...' if len(msg['content']) > 100 else ''}")
    
    st.divider()
    
    # Conversation management
    st.subheader("💬 Conversations")
    
    # Migrate old format conversations if needed
    migrate_old_conversations()
    
    # Button to create new conversation
    if st.button("➕ New Conversation", use_container_width=True):
        create_new_conversation()
    
    # Display existing conversations
    if st.session_state.conversations:
        st.write("Saved conversations:")
        for conv_id in list(st.session_state.conversations.keys())[:5]:  # Show only last 5
            conv_data = st.session_state.conversations[conv_id]
            col1, col2 = st.columns([3, 1])
            with col1:
                # Display the conversation title instead of timestamp
                title = get_conversation_title(conv_data)
                if st.button(f"💬 {title}", key=f"btn_{conv_id}"):
                    st.session_state.current_conversation = conv_id
                    st.session_state.messages = get_conversation_messages(conv_data)
            with col2:
                if st.button("🗑️", key=f"del_{conv_id}"):
                    delete_conversation(conv_id)
    
    st.divider()
    
    # Model parameters
    st.subheader("🎛️ Model Parameters")
    st.session_state.temperature = st.slider("Temperature", 0.0, 1.0, st.session_state.temperature, 0.1)
    st.session_state.max_tokens = st.number_input("Max Tokens", 100, 4000, st.session_state.max_tokens)
    
    st.divider()
    
    # Information
    st.info("""
    **Note:** Make sure Ollama is running on your system.
    Start it with: `ollama serve`
    
    **Available commands:**
    - /clear - Clear current conversation
    - /save - Save current conversation
    - /new - Start new conversation
    - /memory - Toggle memory on/off
    """)

# Main chat interface
st.markdown('<h1 class="main-header">💬 ChatOllama with Memory</h1>', unsafe_allow_html=True)
st.caption("Powered by local LLMs through Ollama - Now with conversation memory")

# Memory status indicator
if st.session_state.memory_enabled:
    memory_status = f"🧠 Memory enabled (storing {len(st.session_state.conversation_memory)}/{st.session_state.memory_size} messages)"
    st.markdown(f'<div class="memory-indicator">{memory_status}</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="memory-disabled">❌ Memory disabled</div>', unsafe_allow_html=True)

# Initialize conversation if none exists
if st.session_state.current_conversation is None:
    create_new_conversation()

# Display current conversation title in the main area
if st.session_state.current_conversation in st.session_state.conversations:
    conv_data = st.session_state.conversations[st.session_state.current_conversation]
    conv_title = get_conversation_title(conv_data)
    st.subheader(f"💬 {conv_title}")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to ask?"):
    # Handle special commands
    if prompt.startswith('/'):
        if prompt == '/clear':
            st.session_state.messages = []
            st.session_state.conversation_memory.clear()
            st.rerun()
        elif prompt == '/save':
            if st.session_state.messages:
                if st.session_state.current_conversation in st.session_state.conversations:
                    st.session_state.conversations[st.session_state.current_conversation]["messages"] = st.session_state.messages
                st.success("Conversation saved!")
            else:
                st.warning("No messages to save")
        elif prompt == '/new':
            create_new_conversation()
            st.rerun()
        elif prompt == '/memory':
            st.session_state.memory_enabled = not st.session_state.memory_enabled
            st.rerun()
        else:
            st.warning("Unknown command. Available commands: /clear, /save, /new, /memory")
    else:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        add_to_memory("user", prompt)
        
        # If this is the first message, generate a title for the conversation
        if len(st.session_state.messages) == 1:  # Only one message (the current one)
            title = generate_conversation_title(prompt)
            if st.session_state.current_conversation in st.session_state.conversations:
                st.session_state.conversations[st.session_state.current_conversation]["title"] = title
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Display assistant response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            # Generate and stream response
            full_response = stream_response(
                prompt, 
                st.session_state.model, 
                message_placeholder,
                st.session_state.temperature,
                st.session_state.max_tokens
            )
        
        # Add assistant response to chat history and memory
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        add_to_memory("assistant", full_response)
        
        # Auto-save conversation
        if st.session_state.current_conversation in st.session_state.conversations:
            st.session_state.conversations[st.session_state.current_conversation]["messages"] = st.session_state.messages

# Add some useful buttons at the bottom
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("🔄 Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.conversation_memory.clear()
        st.rerun()
with col2:
    if st.button("💾 Save Conversation", use_container_width=True):
        if st.session_state.messages:
            if st.session_state.current_conversation in st.session_state.conversations:
                st.session_state.conversations[st.session_state.current_conversation]["messages"] = st.session_state.messages
                st.success("Conversation saved!")
        else:
            st.warning("No messages to save")
with col3:
    if st.button("➕ New Conversation", use_container_width=True):
        create_new_conversation()
        st.rerun()
with col4:
    memory_button_text = "❌ Disable Memory" if st.session_state.memory_enabled else "🧠 Enable Memory"
    if st.button(memory_button_text, use_container_width=True):
        st.session_state.memory_enabled = not st.session_state.memory_enabled
        st.rerun()