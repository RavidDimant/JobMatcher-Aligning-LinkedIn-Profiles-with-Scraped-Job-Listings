import streamlit as st
import pandas as pd
import os
import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

RESPONSES_FILE = "responses.csv"

if not os.path.exists(RESPONSES_FILE):
    df = pd.DataFrame(columns=[
        "LinkedIn",
        "Top_3_Skills",
        "Years_of_Experience",
        "experience_description",
        "Preferred_Work_Style",
        "Highest_Education",
        "Willingness_to_Learn",
        "Work_Environment_Preference",
        "Preferred_Work_Location",
        "Pay_Range",
        "Hobbies",
    ])
    df.to_csv(RESPONSES_FILE, index=False)

if "submitted" not in st.session_state:
    st.session_state["submitted"] = False

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

        education = st.selectbox(
            "What is your highest level of education?",
            ["High School", "Undergraduate", "Bachelor's", "Master's", "PhD", "Other"]
        )

        st.markdown(
            """
            <div style="text-align: center; font-size: 18px; font-weight: bold;">
                Enter your top 3 professional skills:
            </div>
            """,
            unsafe_allow_html=True,
        )
        skill1 = st.text_input("1. ")
        skill2 = st.text_input("2. ")
        skill3 = st.text_input("3. ")

        skills = f"{skill1}, {skill2}, {skill3}"

        experience = st.slider("How many years of experience do you have in your field?", 0, 40, 0)

        description = st.text_input("Tell us about an interesting project you worked on lately:")

        work_style = st.selectbox(
            "Do you prefer working independently, collaboratively, or in a leadership role?",
            ["Independently", "Collaboratively", "Leadership"]
        )

        st.markdown(
            """
            <div style="text-align: center; font-size: 18px; font-weight: bold;">
                What are your favorite hobbies?
            </div>
            """,
            unsafe_allow_html=True,
        )
        hobbies = st.text_input("")
        hobby1 = st.text_input("1. ")
        hobby2 = st.text_input("2. ")
        hobby3 = st.text_input("3. ")

        hobbies = f"{hobby1}, {hobby2}, {hobby3}"
        learning = st.radio(
            "Are you interested in learning new skills or technologies regularly?",
            ["Yes", "No"]
        )

        work_env = st.selectbox(
            "What type of work environment do you prefer?",
            ["Quiet", "Collaborative", "Fast-Paced", "Flexible"]
        )

        location = st.selectbox(
            "I prefer working:",
            ["Remotely", "In-Office", "Hybrid"]
        )

        pay_range = st.selectbox(
            "What is your expected pay range?",
            ["Doesn't Matter", "$40,000–$60,000", "$60,000–$80,000", "$80,000–$100,000", "$100,000+"]
        )

        submitted = st.form_submit_button("Submit")

        if submitted:
            if not LinkedIn:
                st.error("LinkedIn is a required field.")
            else:
                new_response = pd.DataFrame({
                    "LinkedIn": [LinkedIn],
                    "Top_3_Skills": [skills],
                    "Years_of_Experience": [experience],
                    "experience_description": [description],
                    "Preferred_Work_Style": [work_style],
                    "Highest_Education": [education],
                    "Willingness_to_Learn": [learning],
                    "Work_Environment_Preference": [work_env],
                    "Preferred_Work_Location": [location],
                    "Pay_Range": [pay_range],
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
            <h1 style="color: #FF4500;">✨ Dream Job Loading... ✨</h1>
            <p style="font-size: 18px; color: #666;">Please wait while we match your answers to the perfect job opportunities! 🧑‍💻</p>
        </div>
        """,
        unsafe_allow_html=True
    )
