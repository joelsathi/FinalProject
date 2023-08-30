import sys

# sys.path.append("C:\\University\\Academics_5th_sem\\7. Data Science & Engineering Project\\FinalProject\\BackEnd\\VectorDB_chat\\access_db.py")
# sys.path.append("C:\\University\\Academics_5th_sem\\7. Data Science & Engineering Project\\FinalProject\\BackEnd\\LLM\\llm_out.py")

# from VectorDB_chat.access_db import search_similarity
# from LLM.llm_out import generate_llama2_response

from BackEnd.VectorDB_chat.access_db import search_similarity
from BackEnd.LLM.llm_out import generate_llama2_response
from BackEnd.FireBaseDB.access_db import GetAccount
from BackEnd.intent_classifier.load_classifier import get_intent


def get_response(user_msg, past_msgs):
    # use the intent classifier to get the intent of the user message
    # intent = get_intent(user_msg)

    # if intent == "firebase":
    #    # use the firebase to get the answer
    # elif intent == "vectorDb":
    #   # use the vectorDb to get the answer
    # else:
    #   # use the LLM to get the answer

    # similarity search
    # similarity_context, doc = search_similarity(user_msg)

    db_ans = GetAccount("ACC6")

    out = generate_llama2_response(user_msg, past_msgs, db_ans=db_ans)

    # answer = ""

    # for item in out:
    #     answer += item

    return out


# past_msgs = [
#     {"role": "Assistant", "content": "How can I help you today?"},
# ]
# user_msg = "List out some transaction accounts."

# out = get_response(user_msg, past_msgs)

# print(out)
