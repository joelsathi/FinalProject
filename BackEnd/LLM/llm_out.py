import replicate
import os
# from stop_word_remover import prompt_without_stop_words
from .configure import REPLICATE_API_TOKEN

os.environ['REPLICATE_API_TOKEN'] = REPLICATE_API_TOKEN

def get_output_llm(prompt, temperature=0.1, top_p=0.8, max_length=512, repetition_penalty=1):
    llm = 'a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea'
    # llm = "joehoover/zephyr-7b-alpha:14ec63365a1141134c41b652fe798633f48b1fd28b356725c4d8842a0ac151ee"
    # llm = "a16z-infra/llama-2-13b-chat:9dff94b1bed5af738655d4a7cbcdcde2bd503aa85c94334fe1f42af7f3dd5ee3"

    # prompt_after_removing_stop_words = prompt_without_stop_words(prompt)

    output = replicate.run(llm, 
                           input={"prompt": prompt,
                                  "temperature":temperature, "top_p":top_p, "max_length":max_length, "repetition_penalty":repetition_penalty})
    return output

# Function for generating LLaMA2 response
def generate_llama2_response(user_input, past_msgs ,context="", db_ans=""):

    answer_using_context_template = """
                                    {chat_history}
                                    <s>[INST]
                                    <<SYS>>
                                    Use to answer the question. You are a helpful and truthful banking assistant.
                                    Context: {context}
                                    <</SYS>>
                                    {user_msg}
                                    [/INST]
                                    """
    
    answer_using_database_answer_template = """
                                    {chat_history}
                                    <s>[INST]
                                    <<SYS>>
                                    Use to answer the question. You are a helpful and truthful banking assistant.
                                    Context: {db_ans}
                                    <</SYS>>
                                    {user_msg}
                                    [/INST]
                                    """

    check_context_template = """
                            <s>[INST]
                            <<SYS>>
                            Is this related to banking domain? Give Yes or No
                            <</SYS>>
                            {user_msg}
                            [/INST]
                            """
    
    answer_using_llm = """
                            {chat_history}
                            <s>[INST]
                            <<SYS>>
                            You should only answer this question if this question is in the banking domain as the assistant.
                            If this question is not in the banking domain, you should reply, 'I am a banking chatbot, I am not trained to answer this question.', and you should not provide information more on that subject.
                            If this question is a basic banking calculation, do the calculation and provide the answer. If it is 
                            <</SYS>>
                            {user_msg}
                            [/INST]
                            """

    l = len(past_msgs)
    cnt = 0
    chat_history = ""
    answer_flag = True
    # for dict_message in past_msgs:
    #     if dict_message["role"] == "user":
    #         if l - cnt <= 2:
    #             chat_history += "User: " + dict_message["content"] + "\n\n"
    #     else:
    #         if l - cnt <= 2:
    #             chat_history += "Assistant: " + dict_message["content"] + "\n\n"
    #     cnt += 1
    # chat_history = ""
    if context != "":
        string_dialogue = answer_using_context_template.format(chat_history=chat_history, user_msg=user_input, context=context)
    elif db_ans != "":
        string_dialogue = answer_using_database_answer_template.format(chat_history=chat_history, user_msg=user_input, db_ans=db_ans)
    else:
        context_check = get_output_llm(prompt=check_context_template.format(user_msg=user_input))
        context_out = ""
        for item in context_check:
            context_out += str(item)
        if "yes" in context_out.lower():
            string_dialogue = answer_using_llm.format(chat_history=chat_history, user_msg=user_input)
        else:
            print("This is not in the banking domain")
            response = "I am a banking chatbot, I am not trained to answer this question."
            answer_flag = False

    if answer_flag:
        output = get_output_llm(prompt=string_dialogue)
        response = ""
        for item in output:
            response += str(item)
    return response