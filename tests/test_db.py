"""
tests/test_db.py

This module contains unit tests for the database module functions.
It tests the creation of the jobs table and the insertion of job data.
"""

import os
import sqlite3
import json
import tempfile
import time
import unittest
import database


# I don't have much experience with writing tests, so I used AI to help me with this portion.
class TestDatabaseFunctions(unittest.TestCase):
    """Unit tests for database functions."""

    def setUp(self):
        """Create a temporary database file and initialize the jobs table."""
        # creates a temporary database file, original database references it.
        with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as tmp:
            self.db_path = tmp.name
        database.DB_NAME = self.db_path

        # creates the jobs table in the temporary database.
        database.create_table()

    def tearDown(self): # pylint:disable=duplicate-code
        """Delete the temporary database file after each test."""
        # Attempt to delete the temporary database file,
        # retrying if it's still locked by another process.
        for _ in range(3):
            try:
                os.remove(self.db_path)
                break
            except PermissionError:
                time.sleep(0.5)

    # test: connect to the database and check that the 'jobs' table exists.
    def test_create_table(self):
        """Test that the 'jobs' table exists in the database."""
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='jobs'"
            )
            self.assertIsNotNone(cur.fetchone(), "jobs table was not created")

    # test: test the method that gets the data from the file, upload file to database.
    def test_save_job_data2(self):
        """Test that save_job_data2 correctly inserts job records into the database."""
        # create sample job data matching the job-data2.json format.
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
                "job_url": "http://example.com/1",
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
                "job_url_direct": "http://example.com/2",
            },
        ]

        # write the sample data to a temporary json file.
        with tempfile.NamedTemporaryFile(
            delete=False, mode="w", suffix=".json"
        ) as temp_json:
            json.dump(sample_data, temp_json)
            json_file_path = temp_json.name

        # process json file to insert the data into the database.
        database.save_job_data2(json_file_path)
        os.remove(json_file_path)

        # query the database to check the inserted data.
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT title, company, min_amount, max_amount, is_remote, job_url
                FROM jobs ORDER BY id
                """
            )
            rows = cur.fetchall()

        # expected output
        expected1 = (
            "Job1",
            "Company1",
            50000.0,
            70000.0,
            "yes",
            "http://example.com/1",
        )
        expected2 = ("Job2", "Company2", 40000.0, 60000.0, "no", "http://example.com/2")

        self.assertEqual(len(rows), 2, "Expected 2 job records in the database")
        self.assertEqual(rows[0], expected1)
        self.assertEqual(rows[1], expected2)


if __name__ == "__main__":
    unittest.main()
