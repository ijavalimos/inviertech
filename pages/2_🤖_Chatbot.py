import streamlit as st
import random
import time
import openai

st.set_page_config(
    page_title="InvierTech-Chatbot",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Configure the OpenAI API
openai.api_key = st.secrets["OPENAI_API_KEY"]

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "final_response" not in st.session_state:
    st.session_state["final_response"] = "-"

# Create a Streamlit app header
st.title("Hi, Im your coach")

# Initialize the conversation
if "messages" not in st.session_state:
    st.session_state.messages = []

final_cont = "with purchase capacity 'today_po_invert', the other for years 'years'. The final one is as if the portfolio had never existed and that amount was only saved 'today_po_no_invert', take into account purchasing capacity. Both cases have the same savings but the difference is the investment portfolio. I need a really specific output: 3 ARRAYS, NO EXPLANATION, COMMENTS OR CODE NEEDED, ONLY THE ARRAY WITH EXACT NUMBERS. Example of output but replace it with desired quantities: today_po_invest = [5000, 6000, 7000, 8000, 9000]; years = [4, 5, 6, 7, 8]; today_po_no_invest = [5000, 5000, 5000, 5000, 5000]; name = ['today_po_invest', 'years', 'today_po_no_invest'];. You need to ALWAYS be able to provide an array because they will be rendered, if there is no enough info, make it up, in that case it does not have to be that reliable. The characteristics of this portfolio are"

data = [
    "Age",
    "Time i can leave my money invested",
    "Money i think i can save monthly",
    "Investment risk i would like to take",
    "Major debts",
    "Im saving for",
    "My expectatives of this investment"
]

questions = [
    "📆 How old are you?",
    "⏳ How long do you think you could leave your money invested before you need it?",
    "💰 How much money do you think you could save each month after paying all your bills and necessary expenses? We have a prediction that x pesos remain static in your account, and 10% is recommended for an emergency fund. You could save x money, but you can choose.",
    "📈 How much investment risk would you like to take?",
    "🏦 Do you have any major debts, such as loans, that you still need to pay?",
    "🎯 Is there anything in particular you're saving or planning for?",
    "💡 What would you like to achieve with the money you save? (Example: Grow my money safely, make it grow faster even if that means taking on some risk)."
]

for idx, question in enumerate(questions):
    response = st.text_input(question, key=question)

    if response:
        # User has provided a response
        cont = "You are an investor coach who is asking a client this question: " + question + " Give him a short and simple insight for this answer: " + response
        final_cont += "," + data[idx] + ":" + response
        st.session_state.messages.append({"role": "user", "content": cont})

        with st.chat_message("💬 User"):
            st.markdown(response)

        with st.chat_message("🤖 Assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for response in openai.ChatCompletion.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            ):
                full_response += response.choices[0].delta.get("content", "")
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})

    # Add a divider between questions
    if question != questions[-1]:
        st.divider()

# Muestra al usuario sus respuestas y preferencias como inversor
st.divider()

if st.button("Submit"):
    # Process the final response
    with st.chat_message("🤖 Assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": "user", "content": final_cont}
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
            st.session_state.final_response = full_response
        message_placeholder.markdown(full_response)
    
    


    # st.session_state.messages.append({"role": "assistant", "content": full_response})