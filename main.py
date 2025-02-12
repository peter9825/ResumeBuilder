"""
main.py

This file sets up the generative AI model, creates a resume based on a job
description and personal description, and saves the generated resume to a file.
"""

import os
import google.generativeai as genai
import database


def setup_model():
    """
    Set up the generative AI model using an API key from secrets.txt.

    Returns:
        A chat session object from the generative model.
    """
    # setup code from the aistudio.google.com website
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
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
        system_instruction=(
            "Your job is creating professional tech resumes in markdown format based on a personal description "
            "provided to you. Your tone should be professional and cater to jobs in the software development field."
        ),
    )

    return model.start_chat(history=[])


def create_resume(gemini_chat, job_description, personal_description):
    """
    Prompt the AI to create a professional resume in markdown format.

    Args:
        gemini_chat: The generative AI chat session.
        job_description: A string containing the job description.
        personal_description: A string containing the personal description.

    Returns:
        The text of the generated resume.
    """
    prompt = f"""
    Create a professional resume in markdown format based on the following information:

    Job Description:
    {job_description}

    Personal Description:
    {personal_description}

    Format the resume to highlight relevant skills and experience that match the job requirements.
    Include sections for summary, skills, experience, and education.
    """
    response = gemini_chat.send_message(prompt)
    return response.text


def save_resume(resume):
    """
    Save the generated resume to a file and prevent overwriting by renaming files.

    Args:
        resume: The resume text to be saved.

    Returns:
        The filename that the resume was saved as.
    """
    filename = "resume.txt"
    counter = 1

    # if file already exists, name it something different
    while os.path.exists(filename):
        filename = f"resume{counter}.txt"
        counter += 1

    # write file with universal newlines and UTF-8 encoding for cross-platform compatibility
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
        # software development engineer at Adobe description copied from job-data.json
        job_description = """
        "Our Company
        Changing the world through digital experiences is what Adobe’s all about. We give everyone—from emerging artists to global brands—everything they need to design and deliver exceptional digital experiences! We’re passionate about empowering people to create beautiful and powerful images, videos, and apps, and transform how companies interact with customers across every screen.
        We’re on a mission to hire the very best and are committed to creating exceptional employee experiences where everyone is respected and has access to equal opportunity. We realize that new ideas can come from everywhere in the organization, and we know the next big idea could be yours!
        Job Description
        As a member of the Managed Services Engineering team, we are looking for an individual who is passionate about designing, developing, and delivering cloud-native applications using DevOps principles. The team operates using Agile principles, planning sprint tasks, and helping each other succeed. We use a wide range of tools and technologies including Python, Go, Terraform, New Relic, Salt, and AI tools in a multi-cloud environment (AWS and Azure). Our team is driven to help customers benefit from the products and services Adobe offers. You will also play a key role in innovating, executing, and bringing bold ideas to life, transforming them into impactful solutions for our customers.
        We are seeking a forward-thinking software engineer with tight-knit collaboration skills who is open about progress on tasks, seeks feedback early, and often, works optimally across organizational boundaries. The successful candidate will love working on a team where you constantly learn, experiment, and iterate quickly.
        What you'll Do
        • Use high level product requirements to design, develop, and test software through taking peer review feedback, and resolving defects.
        • Develop rapid prototypes of new ideas and concepts and champion team discussions about ways to productize features, implement new technologies and improve products.
        • Experiment with emerging technologies to envision and deliver innovative solutions, driving new possibilities from concept to execution.
        • Work with multi-functional team members to ensure a superb end-to-end user experience for our customers.
        • Follow DevOps principles, engaging and implementing application lifecycle management - from inception and design, through deployment, operations, and refinement.
        • Demonstrate and apply knowledge of software engineering practices, metrics, quality and testing procedures, process creation, and enablement.
        What you need to succeed
        • Bachelor’s Degree in Computer Science or equivalent and 5 years of relevant work experience.
        • Ability to plan, develop, test, and support applications in one or more of the following: Python or Go.
        • A passion for innovation, strong problem-solving skills, and the ability to implement ideas through rapid experimentation and collaboration with multi-functional teams.
        • Experience in developing distributed cloud-native applications.
        • Experience with AWS and/or Azure stack.
        • Experience with AI technologies is a strong plus.
        Our compensation reflects the cost of labor across several U.S. geographic markets, and we pay differently based on those defined markets. The U.S. pay range for this position is $113,400 -- $206,300 annually. Pay within this range varies by work location and may also depend on job-related knowledge, skills, and experience. Your recruiter can share more about the specific salary range for the job location during the hiring process.
        At Adobe, for sales roles starting salaries are expressed as total target compensation (TTC = base + commission), and short-term incentives are in the form of sales commission plans. Non-sales roles starting salaries are expressed as base salary and short-term incentives are in the form of the Annual Incentive Plan (AIP).
        In addition, certain roles may be eligible for long-term incentives in the form of a new hire equity award.
        Adobe will consider qualified applicants with arrest or conviction records for employment in accordance with state and local laws and “fair chance” ordinances.
        Adobe is proud to be an Equal Employment Opportunity and affirmative action employer. We do not discriminate based on gender, race or color, ethnicity or national origin, age, disability, religion, sexual orientation, gender identity or expression, veteran status, or any other applicable characteristics protected by law. Learn more.
        Adobe aims to make Adobe.com accessible to any and all users. If you have a disability or special need that requires accommodation to navigate our website or complete the application process, email accommodations@adobe.com or call (408) 536-3015.
        Adobe values a free and open marketplace for all employees and has policies in place to ensure that we do not enter into illegal agreements with other companies to not recruit or hire each other’s employees."
        """

        personal_description = """
        I am a Computer Science major at Bridgewater State University class of 2025. I am interested in breaking into the field 
        of software engineering, my relevant course work includes Data Structures and Algorithms, Web Application Development, 
        Software Engineering, Database Systems, Analysis of Algorithms, Computer Architecture, Operating Systems, and Foundations 
        of Modern AI. I have worked on several technical projects utilizing Agile methodologies and various programming tools and 
        languages such as Java, C, C++, C#, Python, HTML, CSS, Javascript, React, Node.js, PostgreSQL, SQLite, MySQL, Intellij, 
        Pycharm, VSCode, Git, and Microsoft Visual Studio.
        """

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

    except Exception as e:
        print(f"\nerror occurred: {str(e)}")
        print("please make sure your secrets.txt file contains a valid API key and try again.")


if __name__ == "__main__":
    output()
