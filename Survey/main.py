import streamlit as st
import pandas as pd
import requests
import base64
import json

# GitHub Repo Details (Extracted from your image)
GITHUB_USERNAME = "RavidDimant"
REPO_NAME = "JobMatcher-Aligning-LinkedIn-Profiles-with-Scraped-Job-Listings"
FILE_PATH = "Survey/responses.csv"
GITHUB_TOKEN = "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"

# GitHub API URL for the file
API_URL = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{FILE_PATH}"

def get_github_file():
    """Fetch responses.csv file from GitHub (if exists)."""
    response = requests.get(API_URL, headers={"Authorization": f"token {GITHUB_TOKEN}"})
    
    if response.status_code == 200:
        file_data = response.json()
        return file_data["sha"], base64.b64decode(file_data["content"]).decode()
    return None, None  # File does not exist

def create_github_file():
    """Create a new responses.csv file on GitHub if missing."""
    initial_data = pd.DataFrame(columns=["LinkedIn", "Top_3_Skills", "experience_description", "Job_Type", "Hobbies"])
    csv_content = initial_data.to_csv(index=False)
    encoded_content = base64.b64encode(csv_content.encode()).decode()

    commit_data = {
        "message": "Created responses.csv",
        "content": encoded_content,
        "branch": "main"
    }

    response = requests.put(API_URL, headers={"Authorization": f"token {GITHUB_TOKEN}"}, data=json.dumps(commit_data))
    
    if response.status_code in [200, 201]:
        st.success("✅ responses.csv has been created on GitHub!")
    else:
        st.error("❌ Failed to create responses.csv on GitHub.")

def update_github_file(new_data):
    """Update responses.csv on GitHub by appending new responses."""
    sha, existing_content = get_github_file()
    
    if existing_content:
        df = pd.read_csv(pd.compat.StringIO(existing_content))  # Load existing CSV
    else:
        create_github_file()  # Create file if missing
        df = pd.DataFrame(columns=["LinkedIn", "Top_3_Skills", "experience_description", "Job_Type", "Hobbies"])

    # Append new data
    df = pd.concat([df, pd.DataFrame(new_data)], ignore_index=True)

    # Convert DataFrame to CSV string and encode it to Base64
    csv_content = df.to_csv(index=False)
    encoded_content = base64.b64encode(csv_content.encode()).decode()

    # Prepare commit payload
    commit_data = {
        "message": "Updated survey responses",
        "content": encoded_content,
        "branch": "main",
    }
    
    if sha:
        commit_data["sha"] = sha  # Required for updating an existing file

    response = requests.put(API_URL, headers={"Authorization": f"token {GITHUB_TOKEN}"}, data=json.dumps(commit_data))
    
    if response.status_code in [200, 201]:
        st.success("✅ Your response has been saved to GitHub!")
    else:
        st.error("❌ Failed to update responses on GitHub.")

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
        st.markdown("### Please fill out the survey below:")

        LinkedIn = st.text_input("Please provide a link to your LinkedIn profile:")

        st.markdown("**Enter your top 3 professional skills:**")
        skill1 = st.text_input("Skill 1: ")
        skill2 = st.text_input("Skill 2: ")
        skill3 = st.text_input("Skill 3: ")

        skills = ", ".join(filter(None, [skill1, skill2, skill3]))  # Remove empty inputs

        description = st.text_area("Tell us about an interesting project you worked on lately:")

        Job_Type = st.selectbox(
            "I am looking to work:",
            ["Full-time", "Part-time", "Freelance", "Internship"]
        )

        st.markdown("**Enter your top 3 hobbies:**")
        hobby1 = st.text_input("Hobby 1: ")
        hobby2 = st.text_input("Hobby 2: ")
        hobby3 = st.text_input("Hobby 3: ")

        hobbies = ", ".join(filter(None, [hobby1, hobby2, hobby3]))  # Remove empty inputs

        submitted = st.form_submit_button("Submit")

        if submitted:
            if not LinkedIn:
                st.error("LinkedIn is a required field.")
            else:
                new_response = {
                    "LinkedIn": [LinkedIn],
                    "Top_3_Skills": [skills],
                    "experience_description": [description],
                    "Job_Type": [Job_Type],
                    "Hobbies": [hobbies],
                }

                # Save response directly to GitHub
                update_github_file(new_response)

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
