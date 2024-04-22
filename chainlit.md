# AI Chatbot powered by Amazon Bedrock 🚀🤖

## About
Sample chatbot application to experience Amazon Bedrock, using Chainlit and LangChain.  
You can interact with the AI assistant while switching between multiple models.
Only Claude 3 supports multimodal input (image files).

### Models
Automatically retrieves the IDs of text models available from the ListFoundationModels API. 
The default value is Claude v3 Sonnet (`anthropic.claude-3-sonnet-20240229-v1:0`).

* Titan by Amazon
* Jurassic-2 by AI21 Labs
* Claude by Athropic
* Command by Cohere
* Llama by Meta
* Mistral by Mistral AI

### Parameters
**Temperature:** Default: 0.3  

**Max Token Size:** Default: 1024  
