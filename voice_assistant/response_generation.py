# voice_assistant/response_generation.py
import logging
from config import Config
# from IPython.display import Markdown, display

import logging
import sys
# from IPython.display import Markdown, display
from tools_and_assisstant.assisstant import assisstant_graph
import uuid
from tools_and_assisstant.utils import _print_event


thread_id = str(uuid.uuid4())
config = {
    "configurable": {
        # The passenger_id is used in our flight tools to
        # fetch the user's flight information
        "user_id": "anmolagarwal403@gmail.com",
        # Checkpoints are accessed by thread_id
        "thread_id": thread_id,
    }
}

_printed = set()


async def generate_response(query, local_model_path=None):
    response = assisstant_graph.stream(
        {"messages": ("user", query)}, config, stream_mode="values"
    )
    last_msg = (list(response)[-1].get("messages"))

# Extract the last AI message (which is an AIMessage instance)
    last_ai_message = last_msg[-1]

# Extract the content of the last message
    last_text_message = last_ai_message.content[0]['text']

# Print the extracted text message
    return last_text_message
