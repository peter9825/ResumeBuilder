"""
main.py

This module sets up the generative AI model, creates a resume based on a job
description and personal description, and saves the generated resume to a file.
"""

import os
import google.generativeai as genai
import database

# setup code from the aistudio.google.com website
def setup_model():
    """Set up the generative AI model using an API key from secrets.txt."""
    # use API key from secrets file
    with open("secrets.txt", "r", encoding="utf-8") as file:
        api_key = file.read().strip()
        genai.configure(api_key=api_key)

    # model configuration
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    # modified system instructions to yield better prompting results
    model = genai.GenerativeModel(  # pylint: disable=no-member
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
        system_instruction=(
            "Your job is to create professional tech resumes in markdown format based on a "
            "personal description provided to you. Your tone should be professional and cater "
            "to software development jobs."
        ),
    )

    return model.start_chat(history=[])

# function create_resume prompts the ai to create professional resume based on job
# and personal description
def create_resume(gemini_chat, job_description, personal_description):
    """Prompt the AI to create a professional resume in markdown format."""
    prompt = (
        "Create a professional resume in markdown format based on the following info:\n\n"
        "Job Description:\n"
        f"{job_description}\n\n"
        "Personal Description:\n"
        f"{personal_description}\n\n"
        "Format the resume to highlight relevant skills and experience that match the job "
        "requirements. Include sections for summary, skills, experience, and education."
    )
    response = gemini_chat.send_message(prompt)
    return response.text

# save_resume function saves resume and sets filename and renames new versions
# to prevent overwriting resumes
def save_resume(resume):
    """Save the generated resume to a file and prevent overwriting by renaming."""
    filename = "resume.txt"
    counter = 1

    # if file already exists, name it something different
    while os.path.exists(filename):
        filename = f"resume{counter}.txt"
        counter += 1

    # write file with universal newlines and UTF-8 encoding to work on different machines
    with open(filename, "w", encoding="utf-8", newline="\n") as file:
        # normalize line endings to \n
        normalize_text = resume.replace("\r\n", "\n").replace("\r", "\n")
        file.write(normalize_text)

    return filename

def output():
    """
    Main function that creates the database, sets up the model, generates a resume,
    saves it, and prints it to the command line.
    """
    try:
        # Shortened Adobe job description to avoid long lines
        job_description = (
            "Our Company: Adobe is a global leader in digital experiences. "
            "Join our Managed Services Engineering team to develop cloud-native apps "
            "using Agile methodologies."
        )
        personal_description = (
            "I am a Computer Science major at Bridgewater State University (Class of 2025). "
            "I have experience in Data Structures, Web Development, and Software Engineering, "
            "and I am proficient in Python, Java, and C++."
        )

        # call functions to create database
        database.create_table()
        database.save_job_data("job-data.json")
        database.save_job_data2("job-data2.json")
        print("database created successfully.")

        # call function to setup the model
        print("waiting for your resume assistant...")
        gemini_chat = setup_model()

        # call function create_resume
        print("\nbuilding your resume...")
        resume = create_resume(gemini_chat, job_description, personal_description)

        # call function save_resume
        filename = save_resume(resume)
        print(f"\nresume has been saved as: {filename}")

        # display resume on the command line
        print("\nYour Resume:")
        print("-" * 100)
        print(resume)

    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"\nerror occurred: {str(e)}")
        print("please make sure your secrets.txt file contains a valid API key and try again.")

if __name__ == "__main__":
    output()
