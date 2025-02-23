"""
tests/test_gui.py

This module contains unit tests for gui functionality and database insertion.

Test 1: when a user selects a job from Job Listings,
all the data is returned to be displayed in Job Details.

Test 2: when the user saves their profile, their information
gets inserted into the database properly.
"""
import os
import sqlite3
import tempfile
import time
import unittest
import gui

# Test 1
class TestFormatJobDetails(unittest.TestCase):
    """Unit tests to display all job info."""
    def test_format_job_details(self):
        """Unit test to retrieve full info from selected job in the list."""
        # create a sample job tuple representing a job entry from the database

        job = (
            1,
            "Test Job",
            "Test Company",
            "Test description",
            "Test Location",
            "Full-Time",
            "2025-01-01",
            50000.0,
            70000.0,
            "yes",
            "http://example.com"
        )

        # expected formatted string for the job details
        expected = (
            "ID: 1\n"
            "Title: Test Job\n"
            "Company: Test Company\n"
            "Description: Test description\n"
            "Location: Test Location\n"
            "Job Type: Full-Time\n"
            "Date Posted: 2025-01-01\n"
            "Min Salary: 50000.0\n"
            "Max Salary: 70000.0\n"
            "Is Remote: yes\n"
            "Job URL: http://example.com\n"
        )

        # assert that the formatted details match the expected string.
        self.assertEqual(gui.format_job_details(job), expected)

# Test 2
# following similar logic from previous database testing
class TestUserProfileInsertion(unittest.TestCase):
    """Unit tests to ensure that user data is saved to the database properly."""
    def setUp(self):
        """Create a temporary database file and initialize the user_profiles table."""
        # creates a temporary database file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as tmp:
            self.db_path = tmp.name
        # override jobs.db to temp db
        gui.DB_NAME = self.db_path

        # drop the user_profiles table if it exists
        conn = sqlite3.connect(self.db_path)
        conn.execute("DROP TABLE IF EXISTS user_profiles")
        conn.commit()
        conn.close()

        # call function create user_profiles table
        gui.create_user_profiles_table()

        # verify table exists.
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_profiles'")
        table = cursor.fetchone()
        self.assertIsNotNone(table, "user_profiles table was not created in setUp")
        conn.close()

    def tearDown(self):
        """Delete the temporary database file after each test."""
        # wait briefly to allow connections to close before removing temp db.
        for _ in range(3):
            try:
                os.remove(self.db_path)
                break
            except PermissionError:
                time.sleep(0.5)

    def test_save_user_profile(self):
        """Test that saving a user profile inserts the correct data into the database."""
        # similar to the mock json from previous test, create mock sample_profile
        sample_profile = {
            "full_name": "John Doe",
            "email": "john@example.com",
            "phone": "123-456-7890",
            "githubID": "johndoe",
            "linkedin": "https://www.linkedin.com/in/johndoe",
            "projects": "Project A, Project B",
            "relevant_courses": "CS101, CS102",
            "other_info": "Additional details"
        }

        # save the user profile to the database.
        gui.save_user_profile(sample_profile)

        # connect to temp db and query the user_profiles table.
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT full_name, email, phone, githubID, linkedin, projects,
                   relevant_courses, other_info
            FROM user_profiles
            """
        )
        # retrieve mock user profile
        record = cursor.fetchone()
        conn.close()

        # expected output based on sample_profile.
        expected = (
            "John Doe",
            "john@example.com",
            "123-456-7890",
            "johndoe",
            "https://www.linkedin.com/in/johndoe",
            "Project A, Project B",
            "CS101, CS102",
            "Additional details"
        )

        # assert that the record matches the expected output.
        self.assertEqual(record, expected)


if __name__ == "__main__":
    unittest.main()
