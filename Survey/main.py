import streamlit as st
import pandas as pd
import os

# Define the correct path for responses.csv inside the Survey folder
RESPONSES_FILE = "Survey/responses.csv"

# Function to check if CSV exists and initialize if necessary
def ensure_csv_exists():
    """Creates an empty CSV file with headers if it does not exist or is empty."""
    if not os.path.exists(RESPONSES_FILE) or os.stat(RESPONSES_FILE).st_size == 0:
        df = pd.DataFrame(columns=[
            "LinkedIn",
            "Top_3_Skills",
            "experience_description",
            "Job_Type",
            "Hobbies",
        ])
        df.to_csv(RESPONSES_FILE, index=False)
        print(f"✅ Created new CSV file: {RESPONSES_FILE}")  # Debug message

# Call this function at the start
ensure_csv_exists()

# Function to load CSV with error handling
def load_responses():
    """Loads the responses CSV, handling empty files properly."""
    try:
        return pd.read_csv(RESPONSES_FILE)
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=["LinkedIn", "Top_3_Skills", "experience_description", "Job_Type", "Hobbies"])

# Manage submission state
if "submitted" not in st.session_state:
    st.session_state["submitted"] = False

if not st.session_state["submitted"]:
    st.title("📋 Job Matching Survey")

    # Form for collecting responses
    with st.form("survey_form"):
        LinkedIn = st.text_input("🔗 LinkedIn Profile URL:")
        skill1 = st.text_input("Skill 1: ")
        skill2 = st.text_input("Skill 2: ")
        skill3 = st.text_input("Skill 3: ")
        skills = ", ".join(filter(None, [skill1, skill2, skill3]))

        description = st.text_area("📌 Tell us about an interesting project you worked on lately:")

        Job_Type = st.selectbox(
            "💼 Looking for work as:",
            ["full time", "part time", "freelance", "internship"]
        )

        hobby1 = st.text_input("Hobby 1: ")
        hobby2 = st.text_input("Hobby 2: ")
        hobby3 = st.text_input("Hobby 3: ")
        hobbies = ", ".join(filter(None, [hobby1, hobby2, hobby3]))

        submitted = st.form_submit_button("🚀 Submit Response")

        if submitted:
            if not LinkedIn:
                st.error("❌ LinkedIn profile URL is required.")
            else:
                ensure_csv_exists()  # Ensure the file exists before writing

                existing_responses = load_responses()

                new_response = pd.DataFrame({
                    "LinkedIn": [LinkedIn],
                    "Top_3_Skills": [skills],
                    "experience_description": [description],
                    "Job_Type": [Job_Type],
                    "Hobbies": [hobbies],
                })

                # Append new response and save to CSV
                updated_responses = pd.concat([existing_responses, new_response], ignore_index=True)
                
                # Debug: Print the updated dataframe
                print("📝 Updated Responses:")
                print(updated_responses)

                # Save to CSV
                updated_responses.to_csv(RESPONSES_FILE, index=False)
                print(f"✅ Successfully updated {RESPONSES_FILE}")

                # Update state and rerun
                st.session_state["submitted"] = True
                st.experimental_rerun()

else:
    st.success("✅ Thank you! Your response has been recorded.")

# Option to display all responses
if st.checkbox("📊 Show all responses"):
    df = load_responses()
    if df.empty:
        st.warning("⚠️ No responses recorded yet.")
    else:
        st.dataframe(df)

# import streamlit as st
# import pandas as pd
# import os
# import base64

# def get_base64_image(image_path):
#     with open(image_path, "rb") as img_file:
#         return base64.b64encode(img_file.read()).decode()

# RESPONSES_FILE = "responses.csv"

# # Ensure the CSV file exists with correct columns
# if not os.path.exists(RESPONSES_FILE):
#     df = pd.DataFrame(columns=[
#         "LinkedIn",
#         "Top_3_Skills",
#         "experience_description",
#         "Job_Type",
#         "Hobbies",
#     ])
#     df.to_csv(RESPONSES_FILE, index=False)

# if "submitted" not in st.session_state:
#     st.session_state["submitted"] = False

# if not st.session_state["submitted"]:
#     image_path = "https://raw.githubusercontent.com/RavidDimant/JobMatcher-Aligning-LinkedIn-Profiles-with-Scraped-Job-Listings/main/Survey/logo.png"

#     st.markdown(
#         f"""
#         <div style="text-align: center; margin-top: 20px;">
#             <img src="{image_path}" alt="Career Cupid Logo" 
#             style="width: 100%; max-width: 800px; height: auto; border-radius: 20px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);">
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

#     with st.form("survey_form"):
#         # Define a style for labels
#         LABEL_STYLE = """
#         <style>
#             .stTextInput > label, .stSelectbox > label, .stSlider > label, .stRadio > label {
#                 font-size: 18px;
#                 font-family: Arial, Helvetica, sans-serif;
#                 font-weight: bold;
#             }
#         </style>
#         """
#         st.markdown(LABEL_STYLE, unsafe_allow_html=True)

#         LinkedIn = st.text_input("Please provide a link to your LinkedIn profile:")

#         st.markdown(
#             """
#             <div style="text-align: center; font-size: 18px; font-weight: bold;">
#                 Enter your top 3 professional skills:
#             </div>
#             """,
#             unsafe_allow_html=True,
#         )
#         skill1 = st.text_input("Skill 1: ")
#         skill2 = st.text_input("Skill 2: ")
#         skill3 = st.text_input("Skill 3: ")

#         skills = ", ".join(filter(None, [skill1, skill2, skill3]))  # Remove empty inputs
        
#         description = st.text_area("Tell us about an interesting project you worked on lately:")

#         Job_Type = st.selectbox(
#             "I looking to work:",
#             ["full time", "part time", "freelance", "internship"]
#         )

#         st.markdown(
#             """
#             <div style="text-align: center; font-size: 18px; font-weight: bold;">
#                 Enter your top 3 hobbies:
#             </div>
#             """,
#             unsafe_allow_html=True,
#         )
#         hobby1 = st.text_input("Hobby 1: ")
#         hobby2 = st.text_input("Hobby 2: ")
#         hobby3 = st.text_input("Hobby 3: ")

#         hobbies = ", ".join(filter(None, [hobby1, hobby2, hobby3]))  # Remove empty inputs

#         # Ensure the submit button is within the form
#         submitted = st.form_submit_button("Submit")

#         if submitted:
#             if not LinkedIn:
#                 st.error("LinkedIn is a required field.")
#             else:
#                 new_response = pd.DataFrame({
#                     "LinkedIn": [LinkedIn],
#                     "Top_3_Skills": [skills],
#                     "experience_description": [description],
#                     "Job_Type": [type],
#                     "Hobbies": [hobbies],
#                 })

#                 existing_responses = pd.read_csv(RESPONSES_FILE)
#                 updated_responses = pd.concat([existing_responses, new_response], ignore_index=True)
#                 updated_responses.to_csv(RESPONSES_FILE, index=False)

#                 st.session_state["submitted"] = True
#                 st.experimental_rerun()

# else:
#     st.markdown(
#         """
#         <div style="text-align: center; margin-top: 50px; padding: 20px; border: 2px solid #FFA500; border-radius: 15px; background-color: #FFF5E6;">
#             <h1 style="color: #FF4500;">✨ Thanks! Your response has been submitted successfully ✨</h1>
#         </div>
#         """,
#         unsafe_allow_html=True
#     )
