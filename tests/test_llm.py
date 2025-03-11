"""
test_llm_response.py

This module contains unit tests for verifying that the create_resume function from main.py
returns a valid, non-empty response from the language model (LLM). It uses MagicMock from
the unittest.mock module to simulate the behavior of the LLM without making an actual API call.
"""
import unittest
from unittest.mock import MagicMock
from main import create_resume


# I used AI to help me with MagickMock its functionality.
# it checks that the response from the AI is not empty
# since we are not using web api's this is a way of confirming 200/ok

class TestLLMResponse(unittest.TestCase):
    """
    Unit test class for verifying that the create_resume function returns a non-empty response.
    This test simulates confirming a successful (200/OK) response from the LLM.
    """
    def test_llm_response_is_not_empty(self):
        """
        Test that create_resume returns a non-empty response from the LLM.
        This verifies that when the LLM is queried, it provides some output.
        """
        dummy_chat = MagicMock()

        dummy_chat.send_message.return_value.text = "This is a dummy resume response."

        job_description = "Test Job Description"
        personal_description = "Test Personal Information"

        response_text = create_resume(dummy_chat, job_description, personal_description)

        self.assertTrue(len(response_text) > 0, "LLM response should not be empty.")

if __name__ == '__main__':
    unittest.main()
