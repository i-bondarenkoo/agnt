from langchain_gigachat import GigaChat
from config import settings

llm_model = GigaChat(
    model="GigaChat-2",
    verify_ssl_certs=False,
    credentials=settings.gigachat_credentials,
)
