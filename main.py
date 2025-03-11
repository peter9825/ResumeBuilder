"""
main.py

This module sets up the generative AI model, creates a resume and cover letter
based on a job description and personal description, saves them as Markdown files
in a subfolder (markdown_files), and converts those Markdown files to PDF files
in a separate subfolder (pdf_files). The AI is instructed to output only the
resume/cover letter text, with no additional commentary or explanations.
"""
import os
import google.generativeai as genai
from fpdf import FPDF
import database
import gui


# subfolder names for Markdown and PDF files
MARKDOWN_FOLDER = "markdown_files"
PDF_FOLDER = "pdf_files"

# setup code from the aistudio.google.com website
def setup_model():
    """Set up the generative AI model using an API key from secrets.txt."""
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

    # modified system instructions to yield better prompting results.
    model = genai.GenerativeModel(  # pylint: disable=no-member
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
        system_instruction=(
            "You are to produce only the requested content (resume or cover letter) in Markdown, "
            "with no additional commentary, analysis, or key improvements. Do not include anything "
            "beyond the final text."
        ),
    )
    return model.start_chat(history=[])

# function create_resume prompts the ai to create professional resume based on job
# and personal_description
def create_resume(gemini_chat, job_description, personal_description):
    """
    Prompt the AI to create a professional resume in markdown format.
    Instruct the model explicitly to output only the resume content,
    with no additional commentary or analysis.
    """
    prompt = (
        "Create a professional resume in markdown format based on the following info.\n\n"
        "Do NOT include any commentary, key improvements, or "
        "explanations only the final resume text.\n\n"
        "Job Description:\n"
        f"{job_description}\n\n"
        "Personal Description:\n"
        f"{personal_description}\n\n"
        "Format the resume to highlight relevant skills and experience. "
        "Include sections for summary, skills, experience, and education.\n"
        "Do not add any extra text or commentary beyond the resume itself."
    )
    response = gemini_chat.send_message(prompt)
    return response.text

# save_resume function saves resume, sets the filename and renames newer versions
# to prevent overwriting resumes
# it saves files to subfolders depending on the extension for organization
def save_resume(resume):
    """
    Save the generated resume to a Markdown file in MARKDOWN_FOLDER,
    and return the path to that file.
    """
    os.makedirs(MARKDOWN_FOLDER, exist_ok=True)
    base_name = "resume"
    extension = ".md"
    filename = os.path.join(MARKDOWN_FOLDER, base_name + extension)

    counter = 1
    while os.path.exists(filename):
        filename = os.path.join(MARKDOWN_FOLDER, f"{base_name}{counter}{extension}")
        counter += 1

    with open(filename, "w", encoding="utf-8", newline="\n") as file:
        normalized_text = resume.replace("\r\n", "\n").replace("\r", "\n")
        file.write(normalized_text)
    return filename

# function create_cover_letter prompts the ai to create a professional cover letter based on job
# and personal_description
def create_cover_letter(gemini_chat, job_description, personal_description):
    """
    Prompt the AI to create a professional cover letter in Markdown format.
    Instruct the model explicitly to output only the cover letter text,
    with no additional commentary or analysis.
    """
    prompt = (
        "Create a professional cover letter in markdown format based on the following info.\n\n"
        "Do NOT include any commentary, key improvements, or explanations "
        "only the final cover letter text.\n\n"
        "Job Description:\n"
        f"{job_description}\n\n"
        "Personal Information:\n"
        f"{personal_description}\n\n"
        "Explain why you are an ideal candidate for this role and highlight your key "
        "qualifications.\n"
        "Do not add any extra text or commentary beyond the cover letter itself."
    )
    response = gemini_chat.send_message(prompt)
    return response.text

# save_cover_letter function saves cover letter, sets the filename and renames newer versions
# to prevent overwriting cover letters
# it saves files to subfolders depending on the extension for organization
def save_cover_letter(cover_letter):
    """
    Save the generated cover letter to a Markdown file in MARKDOWN_FOLDER,
    and return the path to that file.
    """
    os.makedirs(MARKDOWN_FOLDER, exist_ok=True)
    base_name = "cover_letter"
    extension = ".md"
    filename = os.path.join(MARKDOWN_FOLDER, base_name + extension)

    counter = 1
    while os.path.exists(filename):
        filename = os.path.join(MARKDOWN_FOLDER, f"{base_name}{counter}{extension}")
        counter += 1

    with open(filename, "w", encoding="utf-8", newline="\n") as file:
        normalized_text = cover_letter.replace("\r\n", "\n").replace("\r", "\n")
        file.write(normalized_text)
    return filename

# function to convert markdown files to pdf, saves to pdf subfolder
def convert_text_to_pdf(text_filepath):
    """
    Convert the given Markdown file to a PDF file using the FPDF module.
    The PDF file is saved in the PDF_FOLDER subfolder.
    Before writing, replace problematic Unicode characters with ASCII equivalents.
    """
    os.makedirs(PDF_FOLDER, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(text_filepath))[0]
    pdf_filename = os.path.join(PDF_FOLDER, base_name + ".pdf")
    counter = 1
    while os.path.exists(pdf_filename):
        pdf_filename = os.path.join(PDF_FOLDER, f"{base_name}{counter}.pdf")
        counter += 1

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    with open(text_filepath, "r", encoding="utf-8") as f:
        content = f.read()
    # replace problematic Unicode characters
    content = content.replace("\u2013", "-")
    content = content.replace("\u2019", "'")

    pdf.multi_cell(0, 10, content)
    pdf.output(pdf_filename)
    return pdf_filename


def output():
    """
    Main function that calls create database and gui with AI setup functionality.
    After the GUI interaction, it converts all generated resume and cover letter Markdown files
    in MARKDOWN_FOLDER to PDF files in PDF_FOLDER.
    """
    try:
        database.create_table()
        database.save_job_data("job-data.json")
        database.save_job_data2("job-data2.json")
        gui.main()

    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"\nerror occurred: {str(e)}")
        print("please make sure your secrets.txt file contains a valid API key and try again.")

if __name__ == "__main__":
    output()
