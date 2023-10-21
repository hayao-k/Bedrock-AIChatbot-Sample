import os
import boto3
from langchain.prompts import PromptTemplate 
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.llms.bedrock import Bedrock
import chainlit as cl
from chainlit.input_widget import Select, Slider
from prompt_template import get_template

AWS_REGION = os.environ["AWS_REGION"]

@cl.author_rename
def rename(orig_author: str):
    mapping = {
        "ConversationChain": bedrock_model_id
    }
    return mapping.get(orig_author, orig_author)

@cl.on_chat_start
async def main():
    bedrock = boto3.client("bedrock", region_name=AWS_REGION)
    
    response = bedrock.list_foundation_models(
        byOutputModality="TEXT"
    )
    
    model_ids = []
    for item in response["modelSummaries"]:
        model_ids.append(item['modelId'])
    
    settings = await cl.ChatSettings(
        [
            Select(
                id="Model",
                label="Amazon Bedrock - Model",
                values=model_ids,
                initial_index=10,
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
                max=4096,
                step=256,
            ),
        ]
    ).send()
    await setup_agent(settings)

@cl.on_settings_update
async def setup_agent(settings):
    global bedrock_model_id
    bedrock_model_id = settings["Model"]
    
    # Instantiate the chain for user session
    llm = Bedrock(
        region_name=AWS_REGION,
        model_id=bedrock_model_id,
        model_kwargs={"temperature": settings["Temperature"]}
    )
    
    ai_prefix="AI"
    provider = bedrock_model_id.split(".")[0]
    # Slider の設定値の型が float のため、明示的に int にする
    MAX_TOKEN_SIZE = int(settings["MAX_TOKEN_SIZE"])
    
    # モデルによってトークンサイズの指定方法が異なる
    if provider == "anthropic":
        llm.model_kwargs["max_tokens_to_sample"] = MAX_TOKEN_SIZE
        ai_prefix="Assistant"
    elif provider == "ai21":
        llm.model_kwargs["maxTokens"] = MAX_TOKEN_SIZE
    elif provider == "cohere":
        llm.model_kwargs["max_tokens"] = MAX_TOKEN_SIZE    
    elif provider == "amazon":
        llm.model_kwargs["maxTokenCount"] = MAX_TOKEN_SIZE

    prompt = PromptTemplate(
        template=get_template(provider),
        input_variables=["history", "input"],
    )
    
    conversation = ConversationChain(
        prompt=prompt, 
        llm=llm, 
        memory=ConversationBufferMemory(
            ai_prefix=ai_prefix
        ),
        verbose=True
    )
    # Store the chain in the user session
    cl.user_session.set("llm_chain", conversation)

@cl.on_message
async def main(message: cl.Message):
    # Retrieve the chain from the user session
    conversation = cl.user_session.get("llm_chain") 

    # Call the chain asynchronously
    res = await conversation.acall(
        message.content, 
        callbacks=[cl.AsyncLangchainCallbackHandler()]
    )
    
    await cl.Message(content=res["response"]).send()
