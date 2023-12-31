# AI Chatbot powered by Amazon Bedrock 🚀🤖
## Overview
Sample chatbot application to experience Amazon Bedrock, using Chainlit and LangChain.

![](https://raw.githubusercontent.com/hayao-k/Bedrock-AIChatbot-Sample/main/images/overview.png)

You can interact with the AI assistant while switching between multiple models. 

![](https://raw.githubusercontent.com/hayao-k/Bedrock-AIChatbot-Sample/main/images/multiple-models.png)

Please ensure you enable access to each model in Amazon Bedrock beforehand.

## Getting Started
Deploy to AWS App Runner using AWS Copilot CLI.

```
export AWS_REGION=us-east-1
copilot app init bedrockchat-app
copilot deploy --name bedrockchat --env dev
```

Of course, you can also manually build a Dockerfile and deploy it to the infrastructure of your choice.

Enjoy!