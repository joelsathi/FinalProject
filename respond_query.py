import sys

sys.path.append("C:\\University\\Academics_5th_sem\\7. Data Science & Engineering Project\\FinalProject\\BackEnd\\VectorDB_chat\\access_db.py")
sys.path.append("C:\\University\\Academics_5th_sem\\7. Data Science & Engineering Project\\FinalProject\\BackEnd\\LLM\\llm_out.py")

# from VectorDB_chat.access_db import search_similarity
# from LLM.llm_out import generate_llama2_response

from BackEnd.VectorDB_chat.access_db import search_similarity
from BackEnd.LLM.llm_out import generate_llama2_response
# from BackEnd.FireBaseDB.access_db import get_intent
from BackEnd.FireBaseDB.access_db import GetAccount,GetBalance


def get_response(user_msg, past_msgs):
    # return GetAccount("ACC1"),GetBalance("ACC1")

    # use the intent classifier to get the intent of the user message
    # intent = get_intent(user_msg)

    # if intent == "firebase":
    #    # use the firebase to get the answer
    # elif intent == "vectorDb":
    #   # use the vectorDb to get the answer
    # else:
    #   # use the LLM to get the answer

    # similarity search
    similarity_context, doc = search_similarity(user_msg)

    # out = generate_llama2_response(user_msg, past_msgs)

    # answer = ""

    # for item in out:
    #     answer += item

    return similarity_context

# past_msgs = [{"role":"Assistant", "content":"How can I help you today?"},]
# user_msg = "List out some transaction accounts."

# out,balance = get_response(user_msg, past_msgs)

# print(out)
# print(f"balance is {balance}")