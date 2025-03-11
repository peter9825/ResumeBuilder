import unittest
from main import create_resume

# I used AI to help me write the Dummy class and its functionality.
# this DummyResponse class is a placeholder class used to mimic a response object.
class DummyResponse:
    pass

# this DummyChat class simulates the gemini_chat object.
# send_message returns response as the prompt
class DummyChat:
    def send_message(self, prompt):
        response = DummyResponse()
        response.text = prompt  # echo the prompt back as the response text
        return response

# tests the create_resume function from main.py
class TestCreateResumePrompt(unittest.TestCase):
    def test_prompt_includes_descriptions(self):
        """Test that create_resume's prompt contains both the job description and personal description."""
        # define sample descriptions
        job_description = "Mock Job Description"
        personal_description = "Mock Personal Information"
        # create instance of DummyChat to simulate the LLM
        dummy_chat = DummyChat()

        # return the final prompt string
        prompt_result = create_resume(dummy_chat, job_description, personal_description)

        # verify that both pieces of information are present in the prompt
        self.assertIn(job_description, prompt_result, "Job description not found in the prompt.")
        self.assertIn(personal_description, prompt_result, "Personal description not found in the prompt.")


if __name__ == '__main__':
    unittest.main()
