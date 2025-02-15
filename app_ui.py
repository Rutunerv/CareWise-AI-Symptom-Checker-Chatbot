import streamlit as st
import requests
import speech_recognition as sr
import pyttsx3
import threading
import time

# Initialize text-to-speech engine
engine = pyttsx3.init()

st.title("🩺 AI Symptom Checker Chatbot with Voice & Text")

# Initialize session state for symptoms & speech tracking
if "symptoms" not in st.session_state:
    st.session_state.symptoms = ""

if "speaking" not in st.session_state:
    st.session_state.speaking = False

# Function to recognize voice input
def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Speak your symptoms...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            symptoms = recognizer.recognize_google(audio)
            return symptoms
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand your voice."
        except sr.RequestError:
            return "Speech recognition service is unavailable."

# Function for text-to-speech response (runs in a thread)
def speak(text):
    st.session_state.speaking = True  # Set speaking state
    st.rerun()  # Refresh UI to show Stop Audio button
    engine.say(text)
    engine.runAndWait()
    st.session_state.speaking = False  # Reset state after speaking
    st.rerun()  # Refresh UI to remove Stop button

# Function to stop audio
def stop_audio():
    engine.stop()
    st.session_state.speaking = False  # Reset state
    st.rerun()  # Refresh UI to remove Stop button

# **Text input field** (updates session state when user types)
text_input = st.text_area("Enter your symptoms (or use voice input):", st.session_state.symptoms)
if text_input:
    st.session_state.symptoms = text_input  # Update session state when user types

# **Voice input button** (updates session state)
if st.button("🎙️ Speak Symptoms"):
    spoken_symptoms = get_voice_input()
    st.session_state.symptoms = spoken_symptoms
    st.write(f"🗣️ You said: {spoken_symptoms}")

# **Check diagnosis button**
if st.button("Check Diagnosis"):
    if st.session_state.symptoms.strip():
        response = requests.post("http://127.0.0.1:5000/diagnose", json={"symptoms": st.session_state.symptoms})
        diagnosis = response.json().get("diagnosis", "Error in getting diagnosis.")
        st.write("🩺 **Possible Diagnosis:**", diagnosis)

        # Run speech in a separate thread to keep UI responsive
        speech_thread = threading.Thread(target=speak, args=(diagnosis,))
        speech_thread.start()
    else:
        st.warning("Please enter or speak symptoms before checking.")

# **Show Stop Audio button only if speaking is active**
if st.session_state.speaking:
    if st.button("🛑 Stop Audio"):
        stop_audio()
