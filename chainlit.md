# AI Chatbot powered by Amazon Bedrock 🚀🤖

## About
Sample chatbot application to experience Amazon Bedrock, using Chainlit and LangChain.  
You can interact with the AI assistant while switching between multiple models.
The Converse API supports Document Chat and Vision (image file input). 
Please refer to the official documentation for the support status of each model.

[Supported models and model features](https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html#conversation-inference-supported-models-features)

### Models
Automatically retrieves the IDs of text models available from the ListFoundationModels API. 
The default value is Claude v3 Sonnet (`anthropic.claude-3-5-sonnet-20240620-v1:0`).

* Titan by Amazon
* Jurassic-2 by AI21 Labs
* Claude by Athropic
* Command by Cohere
* Llama by Meta
* Mistral by Mistral AI

### Parameters
**Temperature:** Default: 0.3  
**Max Token Size:** Default: 2048
