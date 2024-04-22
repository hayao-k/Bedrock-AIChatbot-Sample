import io
import os
import re

from base64 import b64encode
from operator import itemgetter

import boto3
from PIL import Image
import chainlit as cl
from chainlit.input_widget import Select, Slider
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
from langchain.schema.runnable.config import RunnableConfig
from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage

AWS_REGION = os.environ["AWS_REGION"]
PATTERN = re.compile(r'v\d+(?!.*\d[kK]$)')
PROVIDER = ""

TOKEN_PARAM_BY_PROVIDER = {
    "ai21": "maxTokens",
    "amazon": "maxTokenCount",
    "meta": "max_gen_len",
    "default": "max_tokens"  # Anthropic, Cohere, Mistral
}

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
        if PATTERN.search(item['modelId'])
    ]

    settings = await cl.ChatSettings(
        [
            Select(
                id="Model",
                label="Amazon Bedrock - Model",
                values=model_ids,
                initial_index=model_ids.index(
                    "anthropic.claude-3-sonnet-20240229-v1:0"
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
                initial=1024,
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

    llm = ChatBedrock(
        model_id=bedrock_model_id,
        model_kwargs={"temperature": settings["Temperature"]}
    )

    # モデルによってトークンサイズの指定方法が異なる
    global PROVIDER
    PROVIDER = bedrock_model_id.split(".")[0]

    token_param = TOKEN_PARAM_BY_PROVIDER.get(
        PROVIDER, TOKEN_PARAM_BY_PROVIDER["default"]
    )

    llm.model_kwargs[token_param] = int(settings["MAX_TOKEN_SIZE"])

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

def encode_image_to_base64(image, image_format):
    buffer = io.BytesIO()
    image.save(buffer, format=image_format)
    return b64encode(buffer.getvalue()).decode("utf-8")

@cl.on_message
async def on_message(message: cl.Message):

    memory = cl.user_session.get("memory")
    runnable = cl.user_session.get("runnable")

    # Anthropic モデルの場合のみ、画像を処理する
    if PROVIDER == "anthropic":
        content = []

        for file in (message.elements or []):
            if file.path and "image" in file.mime:
                image = Image.open(file.path)
                bs64 = encode_image_to_base64(
                    image,
                    file.mime.split('/')[-1].upper() # 画像フォーマットを渡す
                )
                content.append({
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": file.mime,
                        "data": bs64
                    }
                })

        content_text = {"type": "text", "text": message.content}
        content.append(content_text)
        runnable_message_data = {"human_message": [HumanMessage(content=content)]}
    else:
        runnable_message_data = {"human_message": [HumanMessage(content=message.content)]}

    res = cl.Message(content="", author=f'Chatbot: {PROVIDER.capitalize()}')

    async for chunk in runnable.astream(
        runnable_message_data,
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        await res.stream_token(chunk)

    await res.send()
    memory.chat_memory.add_user_message(message.content)
    memory.chat_memory.add_ai_message(res.content)
