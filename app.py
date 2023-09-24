import streamlit as st

# Define the color palette
colors = {
    'background': '#071E22',
    'text': '#F4C095',
    'button_bg': '#1D7874',
    'button_text': '#FFFFFF'
}

# Set the page title and background color
st.set_page_config(
    page_title="Investment Coaching App",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Create the Streamlit menu
st.title("Welcome to the Investment Coaching App")
st.markdown("Get started by selecting an option below:")

# Create a button to take the user to the investor profile chatbot
if st.button("Investor Profile Chatbot", key="chatbot_button"):
    # You can add the code to launch the chatbot or navigate to the chatbot page here
    st.write("Redirecting to the Investor Profile Chatbot...")

# Create a button to take the user to their investment stats
if st.button("Investment Stats", key="stats_button"):
    # You can add the code to navigate to the investment stats page here
    st.write("Redirecting to Investment Stats...")

# Add some additional content or description here if needed
st.write("Explore our investment coaching services to help you make informed decisions.")

# Set the background color and text color
st.markdown(
    f"""
    <style>
        .reportview-container {{
            background-color: {colors['background']};
            color: {colors['text']};
        }}
        .stButton > button {{
            background-color: {colors['button_bg']};
            color: {colors['button_text']};
        }}
    </style>
    """,
    unsafe_allow_html=True
)
