"""
gui.py

This module creates the application's graphical user interface(GUI)
and inserts saved user profile data into the database.
"""

import PySimpleGUI as sg
import sqlite3
from main import setup_model, create_resume, save_resume

DB_NAME = "jobs.db"

def create_user_profiles_table():
    """
    Create the user_profiles table in the database.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS user_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT,
            email TEXT,
            phone TEXT,
            githubID TEXT,
            linkedin TEXT,
            projects TEXT,
            relevant_courses TEXT,
            other_info TEXT
        )
        """
    )
    conn.commit()
    conn.close()

def get_jobs():
    """
    Retrieve all job entries from the 'jobs' table, returning (id,title).
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title FROM jobs")
    jobs = cursor.fetchall()
    conn.close()
    return jobs

def get_job_details(job_id):
    """
    Retrieve a single job entry by its ID, returning all fields from the 'jobs' table.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
    job = cursor.fetchone()
    conn.close()
    return job

def get_user_profiles():
    """
    Retrieve all user profiles from the user_profiles table.
    Each profile is returned as a tuple:
    (id, full_name, email, phone, githubID, linkedin, projects, relevant_courses, other_info)
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, full_name, email, phone, githubID, linkedin, projects, relevant_courses, other_info
        FROM user_profiles
        """
    )
    profiles = cursor.fetchall()
    conn.close()
    return profiles

def save_user_profile(data):
    """
    Insert a new user into the user_profiles table using the data dictionary.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Insert the user profile data into the user_profiles table.
    cursor.execute(
        """
        INSERT INTO user_profiles (
            full_name, email, phone, githubID, linkedin, projects, relevant_courses, other_info
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data["full_name"],
            data["email"],
            data["phone"],
            data["githubID"],
            data["linkedin"],
            data["projects"],
            data["relevant_courses"],
            data["other_info"],
        ),
    )
    conn.commit()
    conn.close()

def format_job_details(job):
    """
    Format the job details into a string for display.

    Assumes job is a tuple in the following order:
    (id, title, company, description, location, job_type, date_posted,
     min_amount, max_amount, is_remote, job_url)
    """
    return (
        f"ID: {job[0]}\n"
        f"Title: {job[1]}\n"
        f"Company: {job[2]}\n"
        f"Description: {job[3]}\n"
        f"Location: {job[4]}\n"
        f"Job Type: {job[5]}\n"
        f"Date Posted: {job[6]}\n"
        f"Min Salary: {job[7]}\n"
        f"Max Salary: {job[8]}\n"
        f"Is Remote: {job[9]}\n"
        f"Job URL: {job[10]}\n"
    )

def main():
    """
    Main function to build and display the GUI for job listings and user profile input.
    """
    # call function to create new table in jobs.db
    create_user_profiles_table()

    # get all job listings from database, with their id and title
    jobs = get_jobs()
    job_list = [f"{job[0]}: {job[1]}" for job in jobs]

    # get saved profiles for the dropdown menu
    profiles = get_user_profiles()
    profile_options = [f"{p[0]}: {p[1]}" for p in profiles]

    # color theme of the gui
    sg.theme("NeonGreen1")

    # layout for job listings and details.
    job_layout = [
        [sg.Text("Job Listings")],
        [
            sg.Listbox(
                values=job_list,
                size=(50, 10),
                key="-JOB_LIST-",
                enable_events=True
            )
        ],
        [sg.Text("Job Details")],
        [sg.Multiline("", size=(60, 10), key="-JOB_DETAILS-")]
    ]

    profile_layout = [
        [
            sg.Text("Select Profile", size=(15, 1)),
            sg.Combo(profile_options, key="-PROFILE_SELECT-", enable_events=True, size=(30, 1))
        ],
        [sg.Text("Full Name", size=(15, 1)), sg.InputText(key="-FULL_NAME-", size=(30, 1))],
        [sg.Text("Email Address", size=(15, 1)), sg.InputText(key="-EMAIL-", size=(30, 1))],
        [sg.Text("Phone Number", size=(15, 1)), sg.InputText(key="-PHONE-", size=(30, 1))],
        [sg.Text("GitHub ID", size=(15, 1)), sg.InputText(key="-GITHUB-", size=(30, 1))],
        [sg.Text("LinkedIn", size=(15, 1)), sg.InputText(key="-LINKEDIN-", size=(30, 1))],
        [sg.Text("Projects", size=(15, 1)), sg.Multiline("", size=(30, 4), key="-PROJECTS-")],
        [sg.Text("Relevant Courses", size=(15, 1)), sg.Multiline("", size=(30, 4), key="-COURSES-")],
        [sg.Text("Other", size=(15, 1)), sg.Multiline("", size=(30, 4), key="-OTHER-")],
        # Add two buttons: one to save profile and one to generate resume
        [sg.Button("Save Profile", size=(15, 1)), sg.Button("Generate Resume", size=(15, 1))]
    ]

    # create vertical seperator for better user experience
    layout = [
        [sg.Column(job_layout), sg.VerticalSeparator(), sg.Column(profile_layout)]
    ]

    window = sg.Window("Job Finder", layout, finalize=True)

    # loop to read events from the window
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break

        # when a job is selected, update the job details display.
        if event == "-JOB_LIST-":
            selected = values["-JOB_LIST-"]
            if selected:
                job_id_str = selected[0].split(":")[0]
                try:
                    job_id = int(job_id_str)
                    job = get_job_details(job_id)
                    if job:
                        # Use the helper function to format job details.
                        details = format_job_details(job)
                        window["-JOB_DETAILS-"].update(details)
                    else:
                        window["-JOB_DETAILS-"].update("Job details not found.")
                except ValueError:
                    window["-JOB_DETAILS-"].update("Invalid job selection.")

        # when a saved profile is selected, autofill the profile fields.
        if event == "-PROFILE_SELECT-":
            selected_profile = values["-PROFILE_SELECT-"]
            if selected_profile:
                profile_id = int(selected_profile.split(":")[0])
                # get the latest profile
                profiles = get_user_profiles()
                for p in profiles:
                    if p[0] == profile_id:
                        window["-FULL_NAME-"].update(p[1])
                        window["-EMAIL-"].update(p[2])
                        window["-PHONE-"].update(p[3])
                        window["-GITHUB-"].update(p[4])
                        window["-LINKEDIN-"].update(p[5])
                        window["-PROJECTS-"].update(p[6])
                        window["-COURSES-"].update(p[7])
                        window["-OTHER-"].update(p[8])
                        break

        # when "Save Profile" is clicked, save the profile and update the dropdown.
        if event == "Save Profile":
            profile_data = {
                "full_name": values["-FULL_NAME-"],
                "email": values["-EMAIL-"],
                "phone": values["-PHONE-"],
                "githubID": values["-GITHUB-"],
                "linkedin": values["-LINKEDIN-"],
                "projects": values["-PROJECTS-"],
                "relevant_courses": values["-COURSES-"],
                "other_info": values["-OTHER-"],
            }
            if not profile_data["full_name"] or not profile_data["email"]:
                sg.popup("Full Name and Email are required.")
            else:
                save_user_profile(profile_data)
                sg.popup("Profile saved successfully!")
                profiles = get_user_profiles()
                profile_options = [f"{p[0]}: {p[1]}" for p in profiles]
                window["-PROFILE_SELECT-"].update(values=profile_options)

        # When "Generate Resume" is clicked, generate a resume using AI.
        if event == "Generate Resume":
            # Check if a job is selected.
            selected = values["-JOB_LIST-"]
            if not selected:
                sg.popup("Please select a job from the list.")
                continue
            job_id_str = selected[0].split(":")[0]
            try:
                job_id = int(job_id_str)
            except ValueError:
                sg.popup("Invalid job selection.")
                continue

            job = get_job_details(job_id)
            if not job:
                sg.popup("Job details not found.")
                continue

            # provide the AI with description from gui.
            job_description = job[3]
            # combine profile inputs to form a personal description.
            personal_description = (
                f"Full Name: {values['-FULL_NAME-']}\n"
                f"Email: {values['-EMAIL-']}\n"
                f"Phone: {values['-PHONE-']}\n"
                f"GitHub: {values['-GITHUB-']}\n"
                f"LinkedIn: {values['-LINKEDIN-']}\n"
                f"Projects: {values['-PROJECTS-']}\n"
                f"Relevant Courses: {values['-COURSES-']}\n"
                f"Other Info: {values['-OTHER-']}"
            )

            # Check that required profile fields are filled.
            if not values["-FULL_NAME-"] or not values["-EMAIL-"]:
                sg.popup("Please fill in your Full Name and Email before generating a resume.")
                continue

            # set up the AI model.
            sg.popup("Generating resume, please wait...")
            gemini_chat = setup_model()
            # generate resume using the selected job description and user profile info.
            resume = create_resume(gemini_chat, job_description, personal_description)
            # save the resume to a file.
            filename = save_resume(resume)
            sg.popup(f"Resume generated and saved as: {filename}")
            # display the resume.
            sg.popup_scrolled(resume, title="Generated Resume")

    window.close()

if __name__ == "__main__":
    main()
