from fastui_chat import ChatUI, basic_chat_handler
from langchain.chat_models import ChatOllama
from langchain.memory import ChatMessageHistory

history = ChatMessageHistory()
handler = basic_chat_handler(
    llm=ChatOllama(model="nous-hermes2", stop=["<|im_end|>"]),
    chat_history=history,
)

history.add_ai_message("How can I help you today?")

app = ChatUI(
    chat_history=history,
    chat_handler=handler,
)

app.start_with_uvicorn()
