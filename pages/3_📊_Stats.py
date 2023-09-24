import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from PIL import Image

st.set_page_config(
    page_title="InvierTech-Stats",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "final_response" not in st.session_state:
    st.session_state["final_response"] = "-"

# Create a Streamlit app header
st.title("My money")
st.divider()

expenses = pd.read_csv("data/expenses.csv")
income = pd.read_csv("data/income.csv")

sub_expenses = expenses.iloc[1:100]
sub_income = income.iloc[1:100]

st.header("What could've been and what wasn't")

if True:
    today_po_invest = []
    years = []
    today_po_no_invest = []
    name = []

    # Split the string by semicolons to separate assignments
    assignments = st.session_state.final_response.split(";")

    # Iterate through assignments and extract the arrays
    for assignment in assignments:
        # Split each assignment by '=' to separate variable and value
        parts = assignment.strip().split('=')
        if len(parts) == 2:
            variable_name = parts[0].strip()
            variable_value = parts[1].strip()
            
            # Check if the value is a list enclosed in brackets
            if variable_value.startswith("[") and variable_value.endswith("]"):
                try:
                    # Use eval to convert the string to a list
                    variable_list = eval(variable_value)
                    if isinstance(variable_list, list):
                        # Assign the list to the appropriate variable
                        if variable_name == "today_po_invest":
                            today_po_invest = variable_list
                        elif variable_name == "years":
                            years = variable_list
                        elif variable_name == "today_po_no_invest":
                            today_po_no_invest = variable_list
                        elif variable_name == "name":
                            name = variable_list
                except Exception as e:
                    print(f"Error parsing assignment: {assignment}")
                    print(e)

    chart_data = pd.DataFrame(
    {
       "Time": [1, 2, 3, 4, 5, 1, 2, 3, 4, 5] ,
       "Portfolio Value": [4000, 4000, 4000, 4000, 4000, 5000, 6000, 8000, 10000, 12000],
       "col3": ["If invested"] * 5 + ["If not invested"] * 5,
    })

    st.area_chart(chart_data, x="Time", y="Portfolio Value", color="col3")

elif False:
    st.write("Please go talk with your coach first 🤖")

st.divider()

expenses_df = expenses['category'].value_counts()
st.header("Expenses and categories")
fig1, ax1= plt.subplots(figsize=(2, 1))
patches, texts, pcts = ax1.pie(expenses_df, labels=expenses_df.index, autopct='%.1f')

plt.setp(texts, color="white", size=2)
plt.setp(pcts, color="white", size=2)

plt.savefig('pie.png', transparent=True, dpi=800)

image = Image.open('pie.png')

st.image(image)

st.divider()

st.header("How much money will I have tomorrow? And the day after?")

image = Image.open('data/prediction.jpeg')

st.image(image)