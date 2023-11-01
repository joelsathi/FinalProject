from BackEnd.VectorDB_chat.access_db import search_similarity
from BackEnd.LLM.llm_out import generate_llama2_response
from BackEnd.FireBaseDB.access_db import (
    GetAccountDetails,
    GetBalance,
    GetAccountType,
    GetAccountNumber,
    GetAccountName,
    GetAccountEmail,
)
from lang_tranlsator import translate_to_lang
from BackEnd.IntentClassifierRasa.intent_finder import get_intent


def get_response(user_msg, past_msgs, token, translate_to="en"):
    intent = get_intent(user_msg)

    db_context = ""
    vec_db_context = ""

    if intent == "Account_details":
        temp = GetAccountDetails(token["localId"])
        db_context = f"your Account Number is {temp['account_number']}. Your Account User Name is {temp['name']} And Account Type is {temp['account_type']}.Your current Account Balance is Rs.{temp['balance']}."
    elif intent == "Account_balance":
        balance = GetBalance(token["localId"])
        db_context = f"Rs .{balance}"
    # elif intent == "Account_type":
    #     db_context = GetAccountType(token["localId"])
    elif intent == "Account_number":
        db_context = GetAccountNumber(token["localId"])
    elif intent == "Account_holder_name":
        db_context = GetAccountName(token["localId"])
    elif intent == "Account_emailaddress":
        db_context = GetAccountEmail(token["localId"])
    elif intent == "vectorDb":
        vec_db_context = search_similarity(user_msg)

    print("Before generating response")
    print("Intent", intent)
    print("Db context",db_context)
    print("Veco DB context",vec_db_context)

    eng_response = generate_llama2_response(
        user_msg, past_msgs, context=vec_db_context, db_ans=db_context
    )

    if translate_to == "en":
        cur_out = eng_response
    else:
        cur_out = translate_to_lang(
            eng_response, translate_from="en", translate_to=translate_to
        )

    return cur_out, db_context
