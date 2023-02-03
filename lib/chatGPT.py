from revChatGPT.Official import Chatbot
from src.utils import get_config


def chatGPT(prompt: str) -> str:
    api_key = get_config().chatGPT
    chatbot = Chatbot(api_key=api_key)
    return chatbot.ask(prompt)["choices"][0]["text"]
