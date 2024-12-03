from langchain_anthropic import ChatAnthropic
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableConfig
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import tools_condition
from datetime import datetime  # Import the datetime module
from tools_and_assisstant.utils import *
from datetime import datetime  # Import the datetime module
# from tools_and_assisstant.product_comparision import compare_products
from tools_and_assisstant.product_lookup import product_list_lookup
from tools_and_assisstant.specific_product import specific_product_info
from tools_and_assisstant.reviews_product import specific_product_review
from tools_and_assisstant.user_engage import user_engager
from tools_and_assisstant.state import *
from langchain_openai import AzureChatOpenAI
from config import Config


class Assistant:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def __call__(self, state: State, config: RunnableConfig):
        while True:
            configuration = config.get("configurable", {})
            user_id = configuration.get("user_id", None)
            state = {**state, "user_info": user_id}
            result = self.runnable.invoke(state)
            # If the LLM happens to return an empty response
            if not result.tool_calls and (
                not result.content
                or isinstance(result.content, list)
                and not result.content[0].get("text")
            ):
                messages = state["messages"] + \
                    [("user", "Respond with a real output.")]
                state = {**state, "messages": messages}
            else:
                break
        return {"messages": result}


# Haiku is faster and cheaper, but less accurate
llm = ChatAnthropic(model="claude-3-haiku-20240307",
                    # # llm = ChatAnthropic(model="claude-3-sonnet-20240229",
                    streaming=True, temperature=1)

primary_assistant_prompt = ChatPromptTemplate.from_messages(
    [
        (

            "system",
            """You are an AI-powered voice agent capable of simulating a knowledgeable seller for Flipkart that engages in real-time voice conversations with customers, 
mimicking the style and knowledge of a product seller, providing real-time product information.
Adapts its speaking style to match different seller personalities (e.g., tech seller, fashion consultant) depending on the prodect requiement in context
Offers relevant deals, bank offer and other offer details on the product you recommened.
When engaging with customers, aim to build a conversation gradually rather than overwhelming them with too much information or questions at once.
Keep your responses conversational."""

            """Use the tools provided to delegate the tasks accordingly.
When a user comes querying about a product, you should gather some detail about the product by asking the user first and then move for any tool call.
Once you satisfied with the keywords, call the product_list_lookup tool and collects the list of the links of similar product. 
If the user asks for comparision between two products, first gather the information of the product and then compare accordingly using specific_product_info tool. 
You also have the access for the reviews of the specific product using the specific_product_review tool.
"""
            """When searching, be persistent. Expand your query bounds if the first search returns no results. 
If a search comes up empty, expand your search before giving up.
\n\nCurrent user:\n\n{user_info}\n
\nCurrent time: {time}.""",

        ),

        ("placeholder", "{messages}"),
    ]
).partial(time=datetime.now())

main_tools = [
    product_list_lookup,
    specific_product_info,
    specific_product_review,
    user_engager
]
assistant_runnable = primary_assistant_prompt | llm.bind_tools(
    main_tools)

builder = StateGraph(State)

builder.add_node("assistant", Assistant(assistant_runnable))
builder.add_node("tools", create_tool_node_with_fallback(main_tools))
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    tools_condition,
)
builder.add_edge("tools", "assistant")

memory = MemorySaver()
assisstant_graph = builder.compile(checkpointer=memory)
