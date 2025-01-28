import streamlit as st
import pandas as pd
import os

# Define the correct CSV file path inside the "Survey" folder
RESPONSES_FILE = "Survey/responses.csv"

# Ensure the CSV file exists with the correct column headers
if not os.path.exists(RESPONSES_FILE):
    df = pd.DataFrame(columns=[
        "LinkedIn",
        "Top_3_Skills",
        "experience_description",
        "Job_Type",
        "Hobbies",
    ])
    df.to_csv(RESPONSES_FILE, index=False)

# Manage submission state
if "submitted" not in st.session_state:
    st.session_state["submitted"] = False

if not st.session_state["submitted"]:
    # Display the image from GitHub repo
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

    # Form to collect user responses
    with st.form("survey_form"):
        st.markdown("### **📄 Please fill out the survey**")

        # User input fields
        LinkedIn = st.text_input("🔗 LinkedIn Profile URL:")
        
        st.markdown("### **🛠 Enter your top 3 professional skills:**")
        skill1 = st.text_input("Skill 1: ")
        skill2 = st.text_input("Skill 2: ")
        skill3 = st.text_input("Skill 3: ")
        skills = ", ".join(filter(None, [skill1, skill2, skill3]))  # Remove empty inputs
        
        description = st.text_area("📌 Tell us about an interesting project you worked on lately:")

        Job_Type = st.selectbox(
            "💼 Looking for work as:",
            ["full time", "part time", "freelance", "internship"]
        )

        st.markdown("### **🎭 Enter your top 3 hobbies:**")
        hobby1 = st.text_input("Hobby 1: ")
        hobby2 = st.text_input("Hobby 2: ")
        hobby3 = st.text_input("Hobby 3: ")
        hobbies = ", ".join(filter(None, [hobby1, hobby2, hobby3]))  # Remove empty inputs

        # Submit button inside the form
        submitted = st.form_submit_button("🚀 Submit Response")

        if submitted:
            # Ensure LinkedIn is not empty
            if not LinkedIn:
                st.error("❌ LinkedIn profile URL is required.")
            else:
                # Read existing responses
                if os.path.exists(RESPONSES_FILE):
                    existing_responses = pd.read_csv(RESPONSES_FILE)
                else:
                    existing_responses = pd.DataFrame(columns=[
                        "LinkedIn", "Top_3_Skills", "experience_description", "Job_Type", "Hobbies"
                    ])

                # Create new response as DataFrame
                new_response = pd.DataFrame({
                    "LinkedIn": [LinkedIn],
                    "Top_3_Skills": [skills],
                    "experience_description": [description],
                    "Job_Type": [Job_Type],  # FIXED: Used correct variable instead of "type"
                    "Hobbies": [hobbies],
                })

                # Append new response & save to CSV
                updated_responses = pd.concat([existing_responses, new_response], ignore_index=True)
                updated_responses.to_csv(RESPONSES_FILE, index=False)

                # Update session state to prevent resubmission
                st.session_state["submitted"] = True
                st.experimental_rerun()

else:
    # Thank you message after submission
    st.markdown(
        """
        <div style="text-align: center; margin-top: 50px; padding: 20px; 
                    border: 2px solid #FFA500; border-radius: 15px; background-color: #FFF5E6;">
            <h1 style="color: #FF4500;">✨ Thanks! Your response has been submitted successfully ✨</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

# Option to display all responses (for admin purposes)
if st.checkbox("📊 Show all responses"):
    if os.path.exists(RESPONSES_FILE):
        df = pd.read_csv(RESPONSES_FILE)
        st.dataframe(df)
    else:
        st.warning("⚠️ No responses recorded yet.")
