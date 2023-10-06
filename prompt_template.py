def get_template(provider):
    templates = {
        "anthropic": """The following is a friendly conversation between a Human and an AI.
                        The AI is talkative and provides lots of specific details from its context, in its original language. If the AI does not know the answer to a question, it truthfully says it does not know.
                        <conversation_history>
                        {history}
                        </conversation_history>
    
                        <human_reply>
                        Human: {input}
                        </human_reply>
    
                        Assistant:""",

        "ai21": """You are an excellent assistant.
                    The following is a friendly conversation between a Human and an Assistant.
                    The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.
                    
                    {history}
                    
                    Answer the question inside the <q></q>< XML tags. 
                    Do not use any XML tags in the answer.

                    <q>{input}</q>
                    """,
        
        "amazon": """The following is a friendly conversation between a Human and an AI.
                    The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.
                    Answer the question inside the <human_reply></human_reply> XML tags. 
                    Do not use any XML tags in the answer.

                    {history}
    
                    <human_reply>
                    User: {input}
                    </human_reply>
                    
                    AI:""",
                    
        "cohere": """The following is a friendly conversation between a Human and an AI.
                    The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.
                    Answer the question inside the <human_reply></human_reply> XML tags. 
                    Do not use any XML tags in the answer.

                    {history}
    
                    <human_reply>
                    Human: {input}
                    </human_reply>
                    
                    AI:"""
    }
    
    return templates.get(provider, "anthropic")
    