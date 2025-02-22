import PySimpleGUI as sg
import sqlite3
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
            relevant_courses TEXT
        )
        """
    )
    conn.commit()
    conn.close()

def get_jobs():
    """
    Retrieve all job entries from the 'jobs' table, returning (id, title).
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

def save_user_profile(data):
    """
    Insert a new user into the user_profiles table using the data dictionary.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO user_profiles (
            full_name, email, phone, githubID, linkedin, projects, relevant_courses
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data["full_name"],
            data["email"],
            data["phone"],
            data["githubID"],
            data["linkedin"],
            data["projects"],
            data["relevant_courses"],
        ),
    )
    conn.commit()
    conn.close()

def main():
    """
    Main function to build and display the GUI for job listings and user profile input.
    """
    # call function to create new table in jobs.db
    create_user_profiles_table()

    # get all job listings from database, with their id and title
    jobs = get_jobs()
    job_list = [f"{job[0]}: {job[1]}" for job in jobs]

    # color theme of the gui
    sg.theme("NeonGreen1")

    # layout for job listings and details
    job_layout = [
        [sg.Text("Job Listings")],
        [
            sg.Listbox(
                values=job_list,   # id: title strings
                size=(50, 10),     # size of the listbox
                key="-JOB_LIST-",  # key used to retrieve selected job
                enable_events=True # enable event when a user selects a job
            )
        ],
        [sg.Text("Job Details")],
        [sg.Multiline("", size=(60, 10), key="-JOB_DETAILS-")]
    ]

    # layout for user profile input fields, consists of label and input field
    profile_layout = [
        [
            sg.Text("Full Name", size=(15,1)),
            sg.InputText(key="-FULL_NAME-", size=(30,1))
        ],
        [
            sg.Text("Email Address", size=(15,1)),
            sg.InputText(key="-EMAIL-", size=(30,1))
        ],
        [
            sg.Text("Phone Number", size=(15,1)),
            sg.InputText(key="-PHONE-", size=(30,1))
        ],
        [
            sg.Text("GitHub ID", size=(15,1)),
            sg.InputText(key="-GITHUB-", size=(30,1))
        ],
        [
            sg.Text("LinkedIn", size=(15,1)),
            sg.InputText(key="-LINKEDIN-", size=(30,1))
        ],
        [
            sg.Text("Projects", size=(15,1)),
            sg.Multiline("", size=(30,4), key="-PROJECTS-")
        ],
        [
            sg.Text("Relevant Courses", size=(15,1)),
            sg.Multiline("", size=(30,4), key="-COURSES-")
        ],
        [sg.Button("Save Profile", size=(15,1))]  # save button
    ]

    # create vertical separator for better user experience
    layout = [
        [sg.Column(job_layout), sg.VerticalSeparator(), sg.Column(profile_layout)]
    ]

    # main window
    window = sg.Window("Job Finder", layout, finalize=True)

    # loop to read events from the window
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break  # exit loop if the window is closed

        # event when user selects job listing
        if event == "-JOB_LIST-":
            selected = values["-JOB_LIST-"]  # get the selected job
            if selected:
                # split id and title at ":"
                job_id_str = selected[0].split(":")[0]
                try:
                    job_id = int(job_id_str)
                    job = get_job_details(job_id)  # fetch job details from the database
                    if job:
                        # format details in the job details box
                        details = (
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
                        # update multiline field with the formatted details
                        window["-JOB_DETAILS-"].update(details)
                    else:
                        # error handling
                        window["-JOB_DETAILS-"].update("Job details not found.")
                except ValueError:

                    window["-JOB_DETAILS-"].update("Invalid job selection.")

        # event when user clicks the "Save Profile" button
        if event == "Save Profile":
            # put the input data into a dictionary
            profile_data = {
                "full_name": values["-FULL_NAME-"],
                "email": values["-EMAIL-"],
                "phone": values["-PHONE-"],
                "githubID": values["-GITHUB-"],
                "linkedin": values["-LINKEDIN-"],
                "projects": values["-PROJECTS-"],
                "relevant_courses": values["-COURSES-"],
            }
            # basic input validation for full name and email
            if not profile_data["full_name"] or not profile_data["email"]:
                sg.popup("Full Name and Email are required.")
            else:
                # save profile to database
                save_user_profile(profile_data)
                sg.popup("Profile saved successfully!")

    window.close()

if __name__ == "__main__":
    main()
