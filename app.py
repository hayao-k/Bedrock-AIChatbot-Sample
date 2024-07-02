import mimetypes
import os
import re

from operator import itemgetter
from pathlib import Path

import boto3
import chainlit as cl
from chainlit.input_widget import Select, Slider
from langchain.memory import ConversationBufferMemory
from langchain_aws import ChatBedrockConverse
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableConfig, RunnableLambda, RunnablePassthrough

AWS_REGION = os.environ["AWS_REGION"]
EXCLUDE_MODELS = ['meta.llama2-13b-v1', 'meta.llama2-70b-v1']
PATTERN = re.compile(r'v\d+(?!.*\d[kK]$)')
PROVIDER = ""

@cl.on_chat_start
async def main():
    bedrock = boto3.client("bedrock", region_name=AWS_REGION)

    response = bedrock.list_foundation_models(
        byOutputModality="TEXT"
    )

    # オンデマンドスループットのモデル ID のみをリスト化
    model_ids = [
        item['modelId']
        for item in response["modelSummaries"]
        if PATTERN.search(item['modelId']) and item['modelId'] not in EXCLUDE_MODELS
    ]

    settings = await cl.ChatSettings(
        [
            Select(
                id="Model",
                label="Amazon Bedrock - Model",
                values=model_ids,
                initial_index=model_ids.index(
                    "anthropic.claude-3-5-sonnet-20240620-v1:0"
                ),
            ),
            Slider(
                id="Temperature",
                label="Temperature",
                initial=0.3,
                min=0,
                max=1,
                step=0.1,
            ),
            Slider(
                id="MAX_TOKEN_SIZE",
                label="Max Token Size",
                initial=2048,
                min=256,
                max=8192,
                step=256,
            ),
        ]
    ).send()
    await setup_runnable(settings)

@cl.on_settings_update
async def setup_runnable(settings):
    cl.user_session.set(
        "memory", ConversationBufferMemory(return_messages=True)
    )

    memory = cl.user_session.get("memory")

    bedrock_model_id = settings["Model"]

    llm = ChatBedrockConverse(
        model=bedrock_model_id,
        temperature=settings["Temperature"],
        max_tokens=int(settings["MAX_TOKEN_SIZE"])
    )

    global PROVIDER
    PROVIDER = bedrock_model_id.split(".")[0]

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful chatbot"),
            MessagesPlaceholder(variable_name="history"),
            MessagesPlaceholder(variable_name="human_message")
        ]
    )

    runnable = (
        RunnablePassthrough.assign(
            history=RunnableLambda(memory.load_memory_variables) | itemgetter("history")
        )
        | prompt
        | llm
        | StrOutputParser()
    )
    cl.user_session.set("runnable", runnable)

@cl.on_message
async def on_message(message: cl.Message):

    memory = cl.user_session.get("memory")
    runnable = cl.user_session.get("runnable")

    content = []
    for file in (message.elements or []):
        mime_type, _ = mimetypes.guess_type(file.name)

        file_name_path = Path(file.name)
        file_name = file_name_path.stem.replace('.', '-')
        file_format = file_name_path.suffix.lstrip('.')

        with open(file.path, "rb") as f:
            file_data = f.read()

        if mime_type:
            if mime_type.startswith("image"):
                content.append({
                    "image": {
                        "format": file_format,
                        "source": {"bytes": file_data}
                    }
                })
            elif mime_type.startswith("application") or mime_type.startswith("text"):
                content.append({
                    "document": {
                        "name": file_name,
                        "format": file_format, 
                        "source": {"bytes": file_data}
                    }
                })
    content_text = {"type": "text", "text": message.content}
    content.append(content_text)
    runnable_message_data = {"human_message": [HumanMessage(content=content)]}

    res = cl.Message(content="", author=f'Assistant: {PROVIDER.capitalize()}')

    async for chunk in runnable.astream(
        runnable_message_data,
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        await res.stream_token(chunk)

    await res.send()
    memory.chat_memory.add_user_message(message.content)
    memory.chat_memory.add_ai_message(res.content)
