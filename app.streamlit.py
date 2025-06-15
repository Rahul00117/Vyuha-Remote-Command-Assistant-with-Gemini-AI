import paramiko
import google.generativeai as genai
import streamlit as st
import os

# Gemini API setup
api_key = "Hide"
model_name = "gemini-1.5-flash"
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name)

def yoursarthi(prompt):
    response = model.generate_content(
        f'''You are a Linux engineer. Convert the user prompt into a single Linux command.
        Do not use quotes or bash script, only single command like: date, ls, etc.
        Prompt: {prompt}'''
    )
    command = response.text.strip()
    return command

def execute_remote_command(host, port, username, password, command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, port, username, password)
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()
        return output, error
    except Exception as e:
        return None, str(e)
    finally:
        ssh.close()

# Streamlit UI
st.set_page_config(page_title="Vyuh: Remote Command Assistant", layout="wide")
st.markdown("""
    <h1 style="text-align: center; color: #4a90e2; font-family: sans-serif; font-weight: bold;">
        Vyuh: Remote Command Assistant
    </h1>
    """, unsafe_allow_html=True)

with st.expander("🔒 Remote Server Login"):
    host = st.text_input("Remote IP")
    port = st.number_input("Port", value=22, min_value=1, max_value=65535)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    st.info("Enter your remote server details to proceed.")

with st.expander("💬 Enter Task Prompt"):
    prompt = st.text_area("Describe your task (e.g., 'tell me today's date', 'list files')")
    if st.button("Generate & Execute Command"):
        if prompt:
            command = yoursarthi(prompt)
            st.session_state.command = command
            st.success(f"Generated Linux command: `{command}`")

            # Automatically execute if server details are available
            if host and username and password:
                output, error = execute_remote_command(host, port, username, password, command)
                if output:
                    st.code(output, language="bash")
                if error:
                    st.error(error)
            else:
                st.error("Please enter server details first.")
        else:
            st.error("Please enter a task prompt.")

# Extra Features
with st.expander("📁 File Management Tools (Coming Soon)"):
    st.info("Future features: file upload/download, directory listing, and more!")

with st.expander("🌐 Multilingual Support"):
    lang = st.radio("Language", ["English", "हिंदी"])
    if lang == "हिंदी":
        st.write("भविष्य में हिंदी में पूरा इंटरफेस उपलब्ध होगा।")
    else:
        st.write("Full multilingual support coming soon!")

st.markdown("---")
st.write("© 2025 Vyuh: Remote Command Assistant")
