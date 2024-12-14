from langchain_openai import ChatOpenAI
import os
from utility_tools import make_images_api, tool_mapping, search_in_web
from langchain_core.messages import HumanMessage, SystemMessage
from dataclass_utility import ChatResponse
from utility import handle_image_response, get_retriver
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()
llm = ChatOpenAI(model="gpt-3.5-turbo")
llm_with_tools = llm.bind_tools([make_images_api, search_in_web])

system_prompt = SystemMessage(content="""
    You are an intelligent assistant capable of handling a variety of tasks. Your main goal is to understand the user's query and act accordingly. 
    If the user asks to generate an image, make sure to call the appropriate image generation tools. If the user provides a file path for image extraction or processing, follow these steps for efficient extraction:

    1. **Detect image generation requests:** If the user asks to generate or create an image, check if the description is provided. Use the appropriate tool to generate the image, and return the generated file path as:
        STRICTLY use: FILE_PATH: "<path_to_generated_image>" format no other format
    2. **Handle image file paths:** If the user provides a file path (e.g., text responses, image paths, or specific directories for processing), extract and respond with the file path efficiently. Ensure that the path is clear and formatted correctly for further processing.
    3. **Understand user intent:** Ensure that you correctly interpret whether the query is about generating an image, querying an existing one, or dealing with file paths. Always ask for clarification if necessary.
""")

def answer_question(user_question: str, documet_count_inmenory : bool = False, is_web_needed : bool = False) -> ChatResponse:
    if documet_count_inmenory:
        retriver = get_retriver()
        qa_chain = create_retrieval_chain(
            retriever = retriver,
            combine_docs_chain=create_stuff_documents_chain(
                llm=llm,
                prompt = ChatPromptTemplate.from_messages([
                    ("system", """You are a helpful AI assistant. answer the user question from the given context"""
                    ),
                    ("human", "Use the following context to answer the question:\n\nContext: {context}\n\nQuestion: {input}"),
                ])
            )
        )
        result = qa_chain.invoke({"input": user_question})
        return ChatResponse(question=user_question, answer=result.get("answer", ""), document_path="")
    
    current_tools = ""
    messages = [system_prompt, HumanMessage(user_question)]
    ai_msg = llm_with_tools.invoke(messages)
    messages.append(ai_msg)
    if ai_msg.tool_calls is not None:
        for tool_call in ai_msg.tool_calls:
            selected_tool = tool_mapping[tool_call["name"].lower()]
            current_tools = tool_call["name"].lower()
            tool_msg = selected_tool.invoke(tool_call)
            messages.append(tool_msg)

    res = llm.invoke(messages)
    if current_tools.lower() == "make_images_api":
        return handle_image_response(res=res.content, user_question=user_question)
    elif current_tools.lower() == "search_in_web":
        return ChatResponse(question=user_question, answer=res.content, document_path="")
    else:
        answer = ai_msg.content
        return ChatResponse(question=user_question, answer=answer, document_path="")

