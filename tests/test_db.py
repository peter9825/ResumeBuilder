"""
tests/test_db.py

This module contains unit tests for the database module functions.
It tests the creation of the jobs table, the insertion of job data,
and that every inserted job record has a non-empty 'company' field.
"""

import os
import sqlite3
import json
import tempfile
import time
import unittest
import database

class TestDatabaseFunctions(unittest.TestCase):
    """Unit tests for database functions."""

    def setUp(self):
        """Create a temporary database file and initialize the jobs table."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as tmp:
            self.db_path = tmp.name
        database.DB_NAME = self.db_path
        database.create_table()

    def tearDown(self):
        """Delete the temporary database file after each test."""
        for _ in range(3):
            try:
                os.remove(self.db_path)
                break
            except PermissionError:
                time.sleep(0.5)

    def test_create_table(self):
        """Test that the 'jobs' table exists in the database."""
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='jobs'")
            self.assertIsNotNone(cur.fetchone(), "jobs table was not created")

    def test_save_job_data2(self):
        """Test that save_job_data2 correctly inserts job records into the database."""
        # Create sample job data matching job-data2.json format.
        sample_data = [
            {
                "title": "Job1",
                "company": "Company1",
                "description": "Desc1",
                "location": "Loc1",
                "job_type": "Full-Time",
                "date_posted": "2025-01-01",
                "min_amount": "50000",
                "max_amount": "70000",
                "is_remote": "True",
                "job_url": "http://example.com/1"
            },
            {
                "title": "Job2",
                "company": "Company2",
                "description": "Desc2",
                "location": "Loc2",
                "job_type": "Part-Time",
                "date_posted": "2025-02-01",
                "min_amount": "40000",
                "max_amount": "60000",
                "is_remote": "False",
                "job_url_direct": "http://example.com/2"
            }
        ]
        with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix=".json") as temp_json:
            json.dump(sample_data, temp_json)
            json_file_path = temp_json.name

        database.save_job_data2(json_file_path)
        os.remove(json_file_path)

        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT title, company, min_amount, max_amount, is_remote, job_url
                FROM jobs ORDER BY id
            """)
            rows = cur.fetchall()

        expected1 = ("Job1", "Company1", 50000.0, 70000.0, "yes", "http://example.com/1")
        expected2 = ("Job2", "Company2", 40000.0, 60000.0, "no", "http://example.com/2")
        self.assertEqual(len(rows), 2, "Expected 2 job records in the database")
        self.assertEqual(rows[0], expected1)
        self.assertEqual(rows[1], expected2)

    # personal test of my choosing, testing save_job_data production function
    def test_company_field_not_empty(self):
        """
        Test that each job record inserted into the database has a non-empty 'company' field.
        This test uses sample data with various 'company' values and verifies that records with
        an empty or missing 'company' field are skipped.
        """
        sample_data = [
            {
                "title": "Job1",
                "company": "Company1",  # valid
                "description": "Desc1",
                "location": "Loc1",
                "employmentType": "Full-Time",
                "datePosted": "2025-01-01",
                "salaryRange": "50000-70000",
                "jobProviders": [{"url": "http://example.com/1"}]
            },
            {
                "title": "Job2",
                "company": "",  # invalid: empty company
                "description": "Desc2",
                "location": "Loc2",
                "employmentType": "Part-Time",
                "datePosted": "2025-02-01",
                "salaryRange": "40000-60000",
                "jobProviders": [{"url": "http://example.com/2"}]
            },
            {
                "title": "Job3",
                # missing 'company' key altogether should be skipped.
                "description": "Desc3",
                "location": "Loc3",
                "employmentType": "Contract",
                "datePosted": "2025-03-01",
                "salaryRange": "30000-50000",
                "jobProviders": [{"url": "http://example.com/3"}]
            }
        ]

        # write the sample data to a temporary JSON file.
        # follows similar logic to previous test.
        with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix=".json") as temp_json:
            json.dump(sample_data, temp_json)
            json_file_path = temp_json.name

        # process the JSON file to insert data.
        database.save_job_data(json_file_path)
        os.remove(json_file_path)

        # connect to the database and fetch all job records.
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT company FROM jobs")
            rows = cur.fetchall()

        # check that each job record in the database has a non-empty 'company' field.
        for (company,) in rows:
            self.assertTrue(company, "A job record has an empty 'company' field.")

if __name__ == "__main__":
    unittest.main()
