import paramiko
import google.generativeai as genai

api_key = "hide"
model_name = "gemini-1.5-flash"
# custom_base_url = "https://generativelanguage.googleapis.com/v1beta/"  # Not always supported

# If you want to use custom base URL, set environment variable (experimental)
# import os
# os.environ["GOOGLE_API_BASE"] = custom_base_url

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

print("\t\t Welcome to Vyuha")

host = input("Enter remote IP: ")
port = 22
username = input("Enter remote username: ")
password = input("Enter remote password: ")

prompt = input("Enter your task (e.g., 'tell me today's date', 'list files'): ")
command = yoursarthi(prompt)
print("Generated Linux command:", command)

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    ssh.connect(host, port, username, password)
    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode()
    error = stderr.read().decode()
    print("Output:", output)
    if error:
        print("Error:", error)
except Exception as e:
    print("Error:", str(e))
finally:
    ssh.close()
