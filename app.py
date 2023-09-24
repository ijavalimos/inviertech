import streamlit as st
import random
import time


palette = ["#071E22", "#1D7874", "#679289", "#F4C095", "#EE2E31"]

st.markdown(
    f"""
    <style>
    .reportview-container {{
        background: linear-gradient(180deg, {palette[0]} 0%, {palette[1]} 100%);
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Create a Streamlit app header
st.title("Investment Coaching App")

# Check if the "Start Chatbot" button is clicked
if st.button("Start Chatbot"):
    # Set a session variable to hide the main menu
    st.session_state.show_main_menu = False
    # Redirect to a new page with the chatbot
    st.experimental_set_query_params(chatbot=True)

# Check if the "chatbot" query parameter is set (indicating chatbot page)
if st.experimental_get_query_params().get("chatbot"):
    # Hide the main menu for the chatbot page
    st.session_state.show_main_menu = False

    # Create a button to go back to the main menu
    if st.button("Back to Main Menu"):
        # Clear chatbot responses
        if "messages" in st.session_state:
            st.session_state.messages = []
        # Show the main menu again
        st.session_state.show_main_menu = True
        # Redirect to the main menu
        st.experimental_set_query_params()

# Check if the main menu should be shown
if st.session_state.get("show_main_menu", True):
    # Create a button to view investment stats
    if st.button("Investment Stats"):
        # Redirect to a new page with investment stats
        st.experimental_set_query_params(investment_stats=True)

# Check if the "investment_stats" query parameter is set (indicating investment stats page)
if st.experimental_get_query_params().get("investment_stats"):
    # Hide the main menu for the investment stats page
    st.session_state.show_main_menu = False

# Show the main menu if the session variable allows
if st.session_state.get("show_main_menu", True):
    # Add some text or instructions
    st.write("Welcome to the Investment Coaching App!")
    st.write("Please select an option above to get started.")

# Check if the "chatbot" query parameter is set (indicating chatbot page)
if st.experimental_get_query_params().get("chatbot"):
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What is up?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            assistant_response = random.choice(
                [
                    "Hello there! How can I assist you today?",
                    "Hi, human! Is there anything I can help you with?",
                    "Do you need help?",
                ]
            )
            # Simulate stream of response with milliseconds delay
            for chunk in assistant_response.split():
                full_response += chunk + " "
                time.sleep(0.05)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})

