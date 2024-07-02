# AI Chatbot powered by Amazon Bedrock 🚀🤖
## Overview
Sample chatbot application to experience Amazon Bedrock, using Chainlit and LangChain.

![](https://raw.githubusercontent.com/hayao-k/Bedrock-AIChatbot-Sample/main/images/overview.png)

You can interact with the AI assistant while switching between multiple models. 

![](https://raw.githubusercontent.com/hayao-k/Bedrock-AIChatbot-Sample/main/images/multiple-models.png)

Please ensure you enable access to each model in Amazon Bedrock beforehand.

## Features
- **Customizable Chat Settings**: Through Chainlit, it offers a user-friendly interface to select models and adjust settings before initializing the chat.
- **Model Selection**: Amazon Bedrock model list is automatically retrieved and can be selected.
- **Document Chat**: Please refer to the [official documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html#conversation-inference-supported-models-features) for the support status of each model.
- **Image Processing (Anthropic Models Only)**: Supports image input for Claude 3 models.

## Prerequisites
Before deploying this application, ensure you have the following:

- AWS Copilot CLI installed
- Enable access to each model in Amazon Bedrock

## Getting Started
Deploy to AWS App Runner using AWS Copilot CLI.
To deploy this application:

```
git clone https://github.com/hayao-k/Bedrock-AIChatbot-Sample
cd Bedrock-AIChatbot-Sample
export AWS_REGION=us-east-1
copilot app init bedrockchat-app
copilot deploy --name bedrockchat --env dev
```

Follow the prompts in the deployment process to set up the application.

Of course, you can also manually build a Dockerfile and deploy it to the infrastructure of your choice.

Enjoy!

## Cleanup
To delete the application and its resources:

1. Run the following command:

   ```bash
   copilot app delete
   ```

2. Follow the prompts to confirm deletion.