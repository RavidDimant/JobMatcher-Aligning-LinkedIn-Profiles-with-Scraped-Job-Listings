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
