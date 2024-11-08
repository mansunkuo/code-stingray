import os

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import HarmBlockThreshold, HarmCategory

from code_stingray.llms.llm import LLM


class GoogleAILLM(LLM):
    """Concrete LLM class for Google Generative AI."""

    def __init__(self, model_name, **kwargs):
        super().__init__(model_name)

    def create(self) -> ChatGoogleGenerativeAI:
        if "GOOGLE_API_KEY" not in os.environ:
            raise ValueError("GOOGLE_API_KEY environment variable is not set.")
        safety_settings = {
            HarmCategory.HARM_CATEGORY_UNSPECIFIED: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        }
        return ChatGoogleGenerativeAI(
            model=self.model_name, safety_settings=safety_settings
        )
