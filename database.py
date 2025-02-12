import sqlite3
import json

DB_NAME = "jobs.db"
# connect to the database and create table
def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # drop the jobs table if it already exists, (this avoids overwiting or duplicating data.)
    cursor.execute('''DROP TABLE IF EXISTS jobs''')
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  
            title TEXT,                            
            company TEXT,                          
            description TEXT,                  
            location TEXT,                        
            job_type TEXT,                         
            date_posted TEXT,                      
            min_amount REAL,                       
            max_amount REAL,                       
            is_remote TEXT,                        
            job_url TEXT                           
        )
    ''')
    conn.commit()
    conn.close()

# helper function to extract min-max salary
def extract_salary(salary_range):
    if salary_range:
        try:
            salary_range = salary_range.strip().replace(",", "")
            if  "-" in salary_range:
                min_salary, max_salary = salary_range.split("-")
                return float(min_salary), float(max_salary)
            else:
                return float(salary_range), float(salary_range)
        except ValueError:
            return 0, 0
    return 0, 0

# helper function to extract job url from providers list
def extract_job_url(job_providers):
    if job_providers:
        for provider in job_providers:
            if isinstance(provider, dict):
                url = provider.get("url")
                if url:
                    return url
                return None

# helper function to convert certain values to floats
def convert_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0

# helper function to convert boolean values to strings
def convert_is_remote(value):
    if isinstance(value, bool):
        return "yes" if value else "no"
    return "yes" if str(value).strip() in ["1", "True", "true"] else "no"


# function to parse data from first rabid jobs file and insert the data into the database
def save_job_data(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        data = f.read().strip()
    try:
        jobs = json.loads(data)
        if not isinstance(jobs, list):
            jobs = [jobs]
    except json.JSONDecodeError as e:
        print(f"Error parsing {json_file}: {e}")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    for job in jobs:
        min_salary, max_salary = extract_salary(job.get("salaryRange", ""))
        job_url = extract_job_url(job.get("jobProviders", []))
        cursor.execute('''
            INSERT INTO jobs (title, company, description, location, job_type, date_posted, min_amount, max_amount, is_remote, job_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            job.get("title"),
            job.get("company"),
            job.get("description"),
            job.get("location"),
            job.get("employmentType"),
            job.get("datePosted"),
            min_salary,
            max_salary,
            "no",
            job_url
        ))

    conn.commit()
    conn.close()

# function to parse data from second rabid jobs file and insert the data into the database
def save_job_data2(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        data = f.read().strip()
    try:
        jobs = json.loads(data)
        if not isinstance(jobs, list):
            jobs = [jobs]
    except json.JSONDecodeError as e:
        print(f"Error parsing {json_file}: {e}")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    for job in jobs:
        min_salary = convert_float(job.get("min_amount", "0"))
        max_salary = convert_float(job.get("max_amount", "0"))
        job_url = job.get("job_url") or job.get("job_url_direct")
        cursor.execute(''' 
            INSERT INTO jobs (title, company, description, location, job_type, date_posted, min_amount, max_amount, is_remote, job_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            job.get("title"),
            job.get("company"),
            job.get("description"),
            job.get("location"),
            job.get("job_type"),
            job.get("date_posted"),
            min_salary,
            max_salary,
            convert_is_remote(job.get("is_remote")),
            job_url
        ))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_table()
    save_job_data("job-data.json")
    save_job_data2("job-data2.json")

