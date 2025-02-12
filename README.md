Project Overview

This project is an AI-powered resume generator that creates professional tech resumes in markdown format based on a given job description and personal profile. 
It utilizes Google's Gemini AI to analyze job requirements and tailor resumes accordingly. The program stores job ad data from multiple JSON files into an SQLite 
database to be observed by the user.

Why Gemini?

I decided to use Google's Gemini as my model of choice because of it's
easy setup and user friendly code functionality. 

Prompt

"Create a professional resume in markdown format based on the following information:
(personal and job description)
Format the resume to highlight relevant skills and experience that match the job requirements.
Include sections for summary, skills, experience, and education."

I've noticed through various testing prompts that a more effective approach was to tune the system prompt to specialize 
in writing resumes tailored for software engineering and edit the prompt to be less lengthy for the best results. 
The more constraints I gave in the prompt the less optimal my results were as the model did not format certain areas 
of the markdown and even left out entire sections for technical projects along with failing to mention technologies 
that were specific to my job description.


Requirements

- Python 3 (I've used 3.12)

- SQLite3 

- Pycharm IDE

- pip updated to latest version

- google.generativeai library (pip install google-generativeai)

- API key found in secrets.txt file


Running the Program

- Open the project in Pycharm IDE

- Ensure that you have the google.generativeai library installed

- Ensure that you have the secrets.txt file in the project files (API key included)

- Run the program, it should output the resume on the command line and save it as a text file in the project directory.
