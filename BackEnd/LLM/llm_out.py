import replicate
import os

REPLICATE_API_TOKEN = "r8_4XLZPiv7b4U25JHazYOny8Nglja2o8C22WWwf"
os.environ['REPLICATE_API_TOKEN'] = REPLICATE_API_TOKEN

def get_output_llm(prompt, temperature=0.5, top_p=0.8, max_length=512, repetition_penalty=1):
    llm = 'a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea'

    output = replicate.run(llm, 
                           input={"prompt": prompt,
                                  "temperature":temperature, "top_p":top_p, "max_length":max_length, "repetition_penalty":repetition_penalty})
    return output

# Function for generating LLaMA2 response
def generate_llama2_response(user_input, past_msgs ,context="", db_ans=""):

    answer_using_context_template = """
                                    {chat_history}
                                    User: {user_msg}
                                    You should use the following context to answer the question
                                    Context: {context}
                                    Finish the Answer as the assistant:
                                    Assistant:
                                    """
    
    answer_using_database_answer_template = """
                                    {chat_history}
                                    User: {user_msg}
                                    The following context is provided to you to answer the question
                                    Context: {db_ans}
                                    Formulate the answer using the context provided. Finish the Answer as the assistant:
                                    Assistant:
                                    """
    
    answer_using_llm = """
                        {chat_history}
                        User: {user_msg}
                        You should only answer this question if this question is in the banking domain as the assistant.
                        If this question is not in the banking domain, you should reply, 'I am a banking chatbot, I am not trained to answer this question.', and you should not provide information more on that subject.
                        Assistant:
                        """

    l = len(past_msgs)
    cnt = 0
    chat_history = ""
    for dict_message in past_msgs:
        if dict_message["role"] == "user":
            if l - cnt <= 6:
                chat_history += "User: " + dict_message["content"] + "\n\n"
        else:
            if l - cnt <= 6:
                chat_history += "Assistant: " + dict_message["content"] + "\n\n"
        cnt += 1
    
    if context != "":
        string_dialogue = answer_using_context_template.format(chat_history=chat_history, user_msg=user_input, context=context)
    elif db_ans != "":
        string_dialogue = answer_using_database_answer_template.format(chat_history=chat_history, user_msg=user_input, db_ans=db_ans)
    else:
        string_dialogue = answer_using_llm.format(chat_history=chat_history, user_msg=user_input)

    output = get_output_llm(prompt=string_dialogue)

    return output