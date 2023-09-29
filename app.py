import os
from langchain.prompts import PromptTemplate 
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.llms.bedrock import Bedrock
import chainlit as cl
from chainlit.input_widget import Select, Slider

aws_region = os.environ["AWS_REGION"]

@cl.author_rename
def rename(orig_author: str):
    mapping = {
        "ConversationChain": bedrock_model_id
    }
    return mapping.get(orig_author, orig_author)

@cl.on_chat_start
async def main():
    settings = await cl.ChatSettings(
        [
            Select(
                id="Model",
                label="Amazon Bedrock - Model",
                values=[
                    "anthropic.claude-v2", 
                    "ai21.j2-ultra", 
                    "amazon.titan-text-express-v1"
                ],
                initial_index=0,
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
        region_name=aws_region,
        model_id=bedrock_model_id,
        model_kwargs={"temperature": settings["Temperature"]}
    )
    
    base_template = """\n
    {history}
    Human: {input}
    Assistant:"""
    
    intruction_message = "ユーザーの指示には注意深く従ってください"
    
    provider = bedrock_model_id.split(".")[0]
    # Slider の設定値の型が float のため、明示的に int にする
    MAX_TOKEN_SIZE = int(settings["MAX_TOKEN_SIZE"])
    
    # モデルによってトークンサイズの指定方法が異なる
    if provider == "anthropic":
        llm.model_kwargs["max_tokens_to_sample"] = MAX_TOKEN_SIZE
    elif provider == "ai21":
        llm.model_kwargs["maxTokens"] = MAX_TOKEN_SIZE
    elif provider == "amazon":
        # Titan supports English only
        intruction_message = "Please pay close attention to my instructions."
        llm.model_kwargs["maxTokenCount"] = MAX_TOKEN_SIZE

    template = intruction_message + base_template
    
    prompt = PromptTemplate(
        template=template,
        input_variables=["history", "input"],
    )
    
    conversation = ConversationChain(
        prompt=prompt, 
        llm=llm, 
        memory=ConversationBufferMemory(
            # Anthropic requires the prefix to be "Assistant":
            ai_prefix="Assistant"
        ),
        verbose=True
    )
    # Store the chain in the user session
    cl.user_session.set("llm_chain", conversation)


@cl.on_message
async def main(message: str):
    # Retrieve the chain from the user session
    conversation = cl.user_session.get("llm_chain") 

    # Call the chain asynchronously
    res = await conversation.acall(
        message, 
        callbacks=[cl.AsyncLangchainCallbackHandler()]
    )
    
    await cl.Message(content=res["response"]).send()
