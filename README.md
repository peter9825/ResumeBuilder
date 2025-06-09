Project Overview

This project is an AI-powered resume generator that creates professional tech resumes in markdown format based on a given job description and personal profile. 
It utilizes Google's Gemini AI to analyze job requirements and tailor resumes accordingly. The program stores job ad data from multiple JSON files into an SQLite 
database. Upon running the program, the user can observe each job listing using an intuitive graphical user interface and save profile information into the database.
After saving multiple profiles, users can select from each saved profile in the GUI's dropdown menu to preload their data. After generating markdown resumes
and cover-letters, the program converts the markdown files to pdf versions.


Requirements

- Python 3 (I've used 3.12)

- SQLite3 

- Pycharm IDE

- pip updated to latest version

- google.generativeai library (pip install google-generativeai)

- PySimpleGUI (pip install PySimpleGUI)

- FPDF (pip install fpdf)

- API key found in secrets.txt file


Running the Program

- Open the project in Pycharm IDE

- Ensure that you have the required libraries installed

- Ensure that you have the secrets.txt file in the project files (API key included)

- Run the program, it should create the database, insert job ad data, display the GUI, and allow you to generate resumes and cover-letters for
  selected jobs. After generating your resume and cover-letter it will save them as markdown files and pdf files in the designated subfolders.
