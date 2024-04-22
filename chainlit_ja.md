# AI Chatbot powered by Amazon Bedrock 🚀🤖

## About
Chainlit + LangChain + Bedrock なサンプルアプリケーションです。
設定パネルからモデルやパラメーターを設定できます。
Claude 3 のみマルチモーダル (画像ファイルのインプット) に対応しています。

### Models
ListFoundationModels API から利用可能なテキストモデルの ID を自動取得します。 
デフォルト値は Claude v3 Sonnet (`anthropic.claude-3-sonnet-20240229-v1:0`) です。

* Titan by Amazon
* Jurassic-2 by AI21 Labs
* Claude by Athropic
* Command by Cohere
* Llama by Meta
* Mistral by Mistral AI

### Parameters
**Temperature:** Default: 0.3  

**Max Token Size:** Default: 1024  
