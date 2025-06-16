
import os
import shutil
import streamlit as st
import speech_recognition as sr
from pathlib import Path

# ---------- UI Styling ----------
st.set_page_config(page_title="AI File Explorer", layout="wide")
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🗂️ Smart File Explorer with Voice Control</h1>", unsafe_allow_html=True)

# ---------- Voice Recognition Function ----------
def listen_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening... Speak your command")
        try:
            audio = r.listen(source, timeout=5)
            command = r.recognize_google(audio).lower()
            st.success(f"✅ You said: {command}")
            return command
        except sr.WaitTimeoutError:
            st.error("⏱️ Timeout! Please speak again.")
        except sr.UnknownValueError:
            st.error("❌ Could not understand the audio.")
        except sr.RequestError:
            st.error("⚠️ Speech service error.")
    return ""

# ---------- File Operations ----------
def list_files(directory):
    return os.listdir(directory)

def delete_file(path):
    os.remove(path)

def rename_file(old_path, new_path):
    os.rename(old_path, new_path)

# ---------- Directory Input ----------
directory = st.text_input("📁 Enter a directory path", value=os.getcwd())

if os.path.isdir(directory):
    files = list_files(directory)
    st.success("✅ Directory found")

    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("📄 Files and Folders")
        for file in files:
            st.markdown(f"🔹 {file}")
    with col2:
        st.subheader("🎤 Voice Command")
        if st.button("Start Voice Command"):
            command = listen_command()

            if "show files" in command:
                st.rerun()

            elif "delete file" in command:
                file_to_delete = command.replace("delete file", "").strip()
                file_path = os.path.join(directory, file_to_delete)
                if os.path.exists(file_path):
                    delete_file(file_path)
                    st.success(f"🗑️ Deleted: {file_to_delete}")
                else:
                    st.error(f"❌ File not found: {file_to_delete}")

            elif "rename file" in command:
                try:
                    parts = command.split("rename file")[1].strip().split(" to ")
                    old_name = parts[0].strip()
                    new_name = parts[1].strip()
                    old_path = os.path.join(directory, old_name)
                    new_path = os.path.join(directory, new_name)
                    if os.path.exists(old_path):
                        rename_file(old_path, new_path)
                        st.success(f"✏️ Renamed {old_name} to {new_name}")
                    else:
                        st.error("❌ Old file not found.")
                except:
                    st.error("⚠️ Please use command like: rename file abc.txt to xyz.txt")

        st.markdown("🗣️ **Try Commands**:")
        st.markdown("- 'show files'")
        st.markdown("- 'delete file filename.txt'")
        st.markdown("- 'rename file old.txt to new.txt'")
else:
    st.error("🚫 Invalid directory path.")
