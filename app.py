import streamlit as st
import ollama

MODEL_NAME = "llama3.2:3b"

SYSTEM_PROMPT = """
You are InnerSpace AI, a non-clinical emotional-fitness reflection assistant for university students.

You are not a therapist, counsellor, doctor, crisis service, or medical system.
Your role is to help users reflect on emotions, organise thoughts, and identify safe next steps.

Core rules:
1. Do not diagnose mental-health conditions.
2. Do not provide medical, clinical, legal, or therapeutic advice.
3. Do not claim to replace professional or human support.
4. Use reflective listening and neutral validation.
5. Ask short reflective questions instead of giving commands.
6. Encourage user agency and independent judgement.
7. Avoid asking for unnecessary personal or identifiable information.
8. If the user appears to be in crisis, at risk of harm, or mentions self-harm, stop normal reflection and signpost emergency or professional support.
9. Keep responses short, calm, and non-authoritative.
10. Remind users that the tool is for general reflection only when appropriate.
"""

CRISIS_KEYWORDS = [
    "kill myself", "suicide", "hurt myself", "harm myself", "end my life",
    "self harm", "self-harm", "i want to die", "i might hurt myself"
]

CLINICAL_KEYWORDS = [
    "do i have depression", "diagnose me", "am i depressed",
    "do i have anxiety", "what medication", "should i take medication",
    "am i mentally ill"
]

PRIVACY_KEYWORDS = [
    "personal details", "my address", "my phone number", "my full name",
    "confidential", "private information", "sensitive information"
]

TONE_INSTRUCTIONS = {
    "Calm": "Use a calm, gentle, reflective tone. Keep the response soft and steady.",
    "Motivational": "Use an encouraging tone, focused on small manageable next steps.",
    "Direct": "Use a concise, practical tone. Be clear but not harsh."
}


def check_guardrails(user_input: str):
    text = user_input.lower()

    if any(keyword in text for keyword in CRISIS_KEYWORDS):
        return """
I’m sorry you’re feeling this way. I can’t provide crisis support or continue reflective coaching for this situation.

Please contact emergency services or a crisis support service now. If you are in the UK, you can call Samaritans on 116 123 or contact emergency services on 999 if you are in immediate danger.

If possible, reach out to someone you trust nearby and do not stay alone with this.
"""

    if any(keyword in text for keyword in CLINICAL_KEYWORDS):
        return """
I can’t diagnose mental-health conditions or provide clinical advice.

What I can do is help you reflect on what you are experiencing in general terms. If this has been persistent, intense, or affecting your daily life, it would be best to speak with a GP, university wellbeing service, counsellor, or another qualified professional.
"""

    if any(keyword in text for keyword in PRIVACY_KEYWORDS):
        return """
You do not need to share identifiable or highly sensitive personal information here.

For privacy, keep your reflection general. For example, you could describe the situation without names, addresses, phone numbers, student numbers, or confidential details.
"""

    return None


def generate_response(user_input: str, tone: str):
    guardrail_response = check_guardrails(user_input)

    if guardrail_response:
        return guardrail_response

    tone_instruction = TONE_INSTRUCTIONS.get(tone, TONE_INSTRUCTIONS["Calm"])

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT + "\n\nTone instruction: " + tone_instruction
        },
        {
            "role": "user",
            "content": user_input
        }
    ]

    response = ollama.chat(
        model=MODEL_NAME,
        messages=messages
    )

    return response["message"]["content"]


st.set_page_config(
    page_title="InnerSpace AI",
    page_icon="🧠",
    layout="centered"
)

st.title("InnerSpace AI")
st.subheader("Privacy-first emotional fitness reflection demo")

st.info(
    """
    InnerSpace AI is a non-clinical reflection prototype. 
    It is not a therapist, counsellor, doctor, crisis service, or replacement for professional support.
    
    This local demo is designed for general emotional-fitness reflection only.
    Do not enter identifiable, confidential, emergency, or highly sensitive information.
    """
)

st.markdown("### Select response tone")
tone = st.selectbox(
    "Choose how you want the assistant to respond:",
    ["Calm", "Motivational", "Direct"]
)

st.markdown("### Reflection input")
user_input = st.text_area(
    "Write a short reflection. Keep it general and avoid personal identifiers.",
    placeholder="Example: I feel overwhelmed with coursework and I do not know where to start."
)

if st.button("Generate reflection"):
    if not user_input.strip():
        st.warning("Please enter a short reflection first.")
    else:
        with st.spinner("Generating local response..."):
            output = generate_response(user_input, tone)

        st.markdown("### InnerSpace AI response")
        st.write(output)

        st.caption(
            "Local demo: response generated using Python + Ollama. No persistent storage is used in this prototype."
        )

st.markdown("---")
st.caption(
    "Prototype for academic demonstration only. Designed to show reflective dialogue, tone selection, privacy-first framing, and non-therapeutic guardrails."
)
