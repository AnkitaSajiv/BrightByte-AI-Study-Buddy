import streamlit as st
from google import genai
from dotenv import load_dotenv
import os
import time

# Load API key
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# --- FULL DARK MODE CSS ---
st.markdown(
    """
    <style>
    /* Main background */
    body, .block-container {
        background-color: #121212;
        color: #e0e0e0;
    }

    /* Sidebar (feature selector light) */
    .css-1d391kg, .css-1d391kg button, .css-1d391kg select {
        background-color: #f5f5f5 !important;
        color: #000000 !important;
    }

    .css-1d391kg:hover {
        background-color: #e0e0e0 !important;
    }

    /* Buttons */
    button, .stButton>button {
        background-color: #1e1e1e;
        color: #e0e0e0;
        border: 1px solid #444;
    }
    button:hover, .stButton>button:hover {
        background-color: #333333;
    }

    /* Text inputs */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #1e1e1e !important;
        color: #ffffff !important;
        border: 1px solid #444 !important;
    }

    /* Headers */
    h1, h2, h3, h4, h5 {
        color: #ffffff !important;
    }

    /* Motivational quote at bottom-right */
    .quote {
        position: fixed;
        bottom: 10px;
        right: 10px;
        color: #00ffcc;
        font-size: 16px;
        font-style: italic;
        opacity: 0.7;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Page settings
st.set_page_config(page_title="BrightByte!", layout="wide", initial_sidebar_state="expanded")
st.title("BrightByte!")
st.markdown("Your AI assistant for your path to success!")

# Sidebar menu (ligh colored)
option = st.sidebar.selectbox(
    "Choose a feature",
    ["Explain Topic", "Summarize Notes", "Generate Quiz/Flashcards", "Pomodoro Timer", "Notepad"]
)

# Helper function
def get_gemini_response(prompt):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text

# ----------------- Features -------------------

# Explain Topic
if option == "Explain Topic":
    st.subheader("📚 Topic Explainer")
    topic = st.text_input("Enter topic to explain:")
    if st.button("Explain"):
        if topic.strip() != "":
            prompt = f"Explain the topic '{topic}' in simple terms for a student."
            explanation = get_gemini_response(prompt)
            st.success("Explanation:")
            st.write(explanation)
        else:
            st.warning("Please enter a topic.")

# Summarize Notes
elif option == "Summarize Notes":
    st.subheader("📝 Notes Summarizer")
    notes = st.text_area("Paste your study notes:")
    if st.button("Summarize"):
        if notes.strip() != "":
            prompt = f"Summarize the following notes in a concise way:\n{notes}"
            summary = get_gemini_response(prompt)
            st.success("Summary:")
            st.write(summary)
        else:
            st.warning("Please paste your notes.")

# Generate Quiz / Flashcards
elif option == "Generate Quiz/Flashcards":
    st.subheader("🧠 Quiz / Flashcards Generator")
    topic = st.text_input("Enter topic for quiz/flashcards:")
    if st.button("Generate"):
        if topic.strip() != "":
            prompt = f"Create 5 multiple-choice questions with answers and 5 flashcards for the topic '{topic}'."
            result = get_gemini_response(prompt)
            st.success("Quiz / Flashcards:")
            st.write(result)
        else:
            st.warning("Please enter a topic.")

# Pomodoro Timer with live countdown
elif option == "Pomodoro Timer":
    st.subheader("🍅 Pomodoro Timer")
    work_minutes = st.number_input("Work duration (minutes):", min_value=1, max_value=120, value=25)
    break_minutes = st.number_input("Break duration (minutes):", min_value=1, max_value=60, value=5)

    # Placeholders
    timer_placeholder = st.empty()
    progress_bar = st.progress(0)

    if st.button("Start Pomodoro"):
        st.success("Pomodoro started! Focus on work session.")

        # Work session countdown
        total_work_seconds = work_minutes * 60
        for i in range(total_work_seconds, -1, -1):
            mins, secs = divmod(i, 60)
            timer_placeholder.markdown(f"**Work Time:** {mins:02d}:{secs:02d}")
            progress_bar.progress(int((total_work_seconds - i) / total_work_seconds * 100))
            time.sleep(1)

        st.info("Work session done! Take a break now.")
        progress_bar.progress(0)

        # Break session countdown
        total_break_seconds = break_minutes * 60
        for i in range(total_break_seconds, -1, -1):
            mins, secs = divmod(i, 60)
            timer_placeholder.markdown(f"**Break Time:** {mins:02d}:{secs:02d}")
            progress_bar.progress(int((total_break_seconds - i) / total_break_seconds * 100))
            time.sleep(1)

        st.success("Pomodoro cycle completed!")
        progress_bar.progress(0)

# Notepad / Word
elif option == "Notepad":
    st.subheader("📝 Notepad")
    notes = st.text_area("Write your notes here:", height=400)
    if st.button("Save Notes"):
        with open("my_notes.txt", "w", encoding="utf-8") as f:
            f.write(notes)
        st.success("Notes saved as 'my_notes.txt'.")

# ----------------- Motivational Quote -------------------
st.markdown('<div class="quote">“Dream it. Wish it. Do it.”</div>', unsafe_allow_html=True)
