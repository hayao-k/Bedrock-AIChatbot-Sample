# AI Chatbot powered by Amazon Bedrock 🚀🤖

## About
Chainlit + LangChain + Bedrock なサンプルアプリケーションです。
設定パネルからモデルやパラメーターを設定できます。
Converse API を使用しており、Document Chat や Vision (画像ファイルのインプット) に対応しています。
モデルごとの対応状況については公式ドキュメントを参照してください。

[Supported models and model features](https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html#conversation-inference-supported-models-features)

### Models
ListFoundationModels API から利用可能なテキストモデルの ID を自動取得します。 
デフォルト値は Claude v3 Sonnet (`anthropic.claude-3-5-sonnet-20240620-v1:0`) です。

* Titan by Amazon
* Jurassic-2 by AI21 Labs
* Claude by Athropic
* Command by Cohere
* Llama by Meta
* Mistral by Mistral AI

### Parameters
**Temperature:** Default: 0.3  
**Max Token Size:** Default: 2048
