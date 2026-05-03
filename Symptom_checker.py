import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
from Symptom_Checker.prompt import SYSTEM_PROMPT
import time

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


st.set_page_config(page_title="AI Symptom Checker", page_icon="🩺", layout="centered")


st.markdown("""
<style>
body {
    background-color: #0e1117;
}
.main-title {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    color: #00d4ff;
}
.card {
    background-color: #1c1f26;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 0px 10px rgba(0,0,0,0.5);
    margin-top: 20px;
}
.fade-in {
    animation: fadeIn 1.5s ease-in;
}
@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}
</style>
""", unsafe_allow_html=True)


st.markdown('<div class="main-title">🩺 AI Symptom Checker</div>', unsafe_allow_html=True)
st.write("💡 Enter your symptoms and get AI-powered health insights")


with st.container():
    col1, col2 = st.columns([3,1])

    with col1:
        symptoms = st.text_area("Describe your symptoms:", height=150, placeholder="e.g. fever, headache, fatigue...")

    with col2:
        st.markdown("### Tips")
        st.write("✔ Be specific")
        st.write("✔ Mention duration")
        st.write("✔ Add severity")


if st.button("🔍 Check Symptoms"):

    if not symptoms.strip():
        st.warning("⚠️ Please enter symptoms.")
    else:
        with st.spinner("🧠 AI is analyzing your symptoms..."):
            time.sleep(1.5)  # smooth animation feel

            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": symptoms}
                    ],
                    temperature=0.3
                )

                result = response.choices[0].message.content

                
                st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
                st.subheader("🧠 Analysis")
                st.write(result)
                st.markdown('</div>', unsafe_allow_html=True)

          
                if "High" in result:
                    st.error("🚨 High Severity Detected — Consider immediate medical attention")
                elif "Medium" in result:
                    st.warning("⚠️ Medium Severity — Monitor symptoms carefully")
                elif "Low" in result:
                    st.success("✅ Low Severity — Likely manageable")

               
                st.info("⚠️ This is not a medical diagnosis. Consult a doctor for professional advice.")

            except Exception as e:
                st.error(f"Error: {str(e)}")