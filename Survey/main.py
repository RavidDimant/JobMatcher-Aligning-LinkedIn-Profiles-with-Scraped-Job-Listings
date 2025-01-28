import streamlit as st
import pandas as pd
import os
import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

RESPONSES_FILE = "responses.csv"

# Ensure the CSV file exists with correct columns
if not os.path.exists(RESPONSES_FILE):
    df = pd.DataFrame(columns=[
        "LinkedIn",
        "Top_3_Skills",
        "experience_description",
        "Preferred_Work_Location",
        "Hobbies",
    ])
    df.to_csv(RESPONSES_FILE, index=False)

if "submitted" not in st.session_state:
    st.session_state["submitted"] = False

if not st.session_state["submitted"]:
    image_path = "https://raw.githubusercontent.com/RavidDimant/JobMatcher-Aligning-LinkedIn-Profiles-with-Scraped-Job-Listings/main/Survey/logo.png"

    st.markdown(
        f"""
        <div style="text-align: center; margin-top: 20px;">
            <img src="{image_path}" alt="Career Cupid Logo" 
            style="width: 100%; max-width: 800px; height: auto; border-radius: 20px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);">
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("survey_form"):
        # Define a style for labels
        LABEL_STYLE = """
        <style>
            .stTextInput > label, .stSelectbox > label, .stSlider > label, .stRadio > label {
                font-size: 18px;
                font-family: Arial, Helvetica, sans-serif;
                font-weight: bold;
            }
        </style>
        """
        st.markdown(LABEL_STYLE, unsafe_allow_html=True)

        LinkedIn = st.text_input("Please provide a link to your LinkedIn profile:")

        st.markdown(
            """
            <div style="text-align: center; font-size: 18px; font-weight: bold;">
                Enter your top 3 professional skills:
            </div>
            """,
            unsafe_allow_html=True,
        )
        skill1 = st.text_input("Skill 1: ")
        skill2 = st.text_input("Skill 2: ")
        skill3 = st.text_input("Skill 3: ")

        skills = ", ".join(filter(None, [skill1, skill2, skill3]))  # Remove empty inputs
        
        description = st.text_area("Tell us about an interesting project you worked on lately:")

        location = st.selectbox(
            "I prefer working:",
            ["Remotely", "In-Office", "Hybrid"]
        )

        st.markdown(
            """
            <div style="text-align: center; font-size: 18px; font-weight: bold;">
                Enter your top 3 hobbies:
            </div>
            """,
            unsafe_allow_html=True,
        )
        hobby1 = st.text_input("Hobby 1: ")
        hobby2 = st.text_input("Hobby 2: ")
        hobby3 = st.text_input("Hobby 3: ")

        hobbies = ", ".join(filter(None, [hobby1, hobby2, hobby3]))  # Remove empty inputs

        # Ensure the submit button is within the form
        submitted = st.form_submit_button("Submit")

        if submitted:
            if not LinkedIn:
                st.error("LinkedIn is a required field.")
            else:
                new_response = pd.DataFrame({
                    "LinkedIn": [LinkedIn],
                    "Top_3_Skills": [skills],
                    "experience_description": [description],
                    "Preferred_Work_Location": [location],
                    "Hobbies": [hobbies],
                })

                existing_responses = pd.read_csv(RESPONSES_FILE)
                updated_responses = pd.concat([existing_responses, new_response], ignore_index=True)
                updated_responses.to_csv(RESPONSES_FILE, index=False)

                st.session_state["submitted"] = True
                st.experimental_rerun()

else:
    st.markdown(
        """
        <div style="text-align: center; margin-top: 50px; padding: 20px; border: 2px solid #FFA500; border-radius: 15px; background-color: #FFF5E6;">
            <h1 style="color: #FF4500;">✨ Thanks! Your response has been submitted successfully ✨</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
