from BackEnd.VectorDB_chat.access_db import search_similarity
from BackEnd.LLM.llm_out import generate_llama2_response
from BackEnd.FireBaseDB.access_db import GetAccountDetails,GetBalance
from lang_tranlsator import translate_to_lang
from BackEnd.IntentClassifierRasa.intent_finder import get_intent


def get_response(user_msg, past_msgs, token, translate_to="si"):

    intent = get_intent(user_msg)

    db_context = ""
    vec_db_context = ""

    if intent == "Account_details":
        temp = GetAccountDetails(token["localId"])
        db_context = f"your Account Number is {temp['account_number']}. Your Account User Name is {temp['name']} And Account Type is {temp['account_type']}.Your current Account Balance is Rs.{temp['balance']}."
    elif intent == "Account_balance":
        balnce = GetBalance(token["localId"])
        db_context = f"Rs .{balnce}"
    elif intent == "vectorDb":
        vec_db_context, doc = search_similarity(user_msg)
    # out = generate_llama2_response(user_msg, past_msgs, db_ans=db_context, context=vec_db_context)

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
    
    # db_context = GetAccount("ACC1")
    eng_response = generate_llama2_response(user_msg, past_msgs, context="", db_ans="")

    # if translate_to == "en":
    #     cur_out = eng_response
    # else:
    #     cur_out = translate_to_lang(eng_response, translate_from="en", translate_to=translate_to)
    print(db_context)

    return db_context,db_context

past_msgs = [{"role":"Assistant", "content":"How can I help you today?"},]
user_msg = "Account balnce."

# intent = get_response(user_msg, past_msgs, "token", translate_to="si")

# print(intent)