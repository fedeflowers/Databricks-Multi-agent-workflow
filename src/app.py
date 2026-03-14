import streamlit as st
import time
from orchestrator import run_agent

# Page Config
st.set_page_config(page_title="Prada PLSA Assistant", page_icon="👜", layout="wide")

# Custom CSS for Premium Design
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #1a1a1a 0%, #0d0d0d 100%);
        color: #f5f5f5;
    }
    .stChatMessage {
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 10px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(5px);
    }
    .stChatInputContainer {
        border-radius: 30px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    h1 {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        letter-spacing: -1px;
        background: linear-gradient(90deg, #ffffff, #888888);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Prada Localized Shop Analytics")
st.caption("v2.0 - Powered by Mosaic AI Agent Framework & Unity Catalog")

# Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if query := st.chat_input("Ask about inventory, guidelines, or sales..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # Process Query
    with st.chat_message("assistant"):
        # Simulated Thinking/MLflow Trace
        with st.status("🧠 Analyzing request...", expanded=True) as status:
            time.sleep(0.5)
            
            # Start workflow
            status.update(label="🧠 Routing to specialist...", state="running")
            result = run_agent(query)
            
            # Show routing decision
            routed_to = result.get("next_step", "general")
            st.write(f"✅ Routed to: **{routed_to.title()} Agent**")
            
            # Show steps/messages
            for msg in result.get("messages", []):
                if msg["role"] == "assistant" and msg.get("name"):
                    st.write(f"⚡ *Step: {msg['name']} executed*")
            
            status.update(label="🧠 Analysis complete", state="complete")
        
        # Display Final Response
        final_answer = result.get("final_response", "I'm sorry, I couldn't process that request.")
        st.markdown(final_answer)
        
        # Add to session state
        st.session_state.messages.append({"role": "assistant", "content": final_answer})
