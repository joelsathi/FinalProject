from LLM.llm_out import generate_llama2_response
from VectorDB_chat.access_db import search_similarity
from FireBaseDB.access_db import GetAccountDetails,read_last_transactions,Get_Saving_Interest_Rates,Get_Fixed_Interset_Rates,Get_Loan_Rates,Get_Exchange_Rates, get_latest_chat_history
from IntentClassifierRasa.intent_finder import get_intent
from fastapi.responses import JSONResponse
from FireBaseDB.write_db import save_chat_data
from .google_translator import translate_text

def translator_util(message:str, translate_to:str):
    if translate_to == "English":
        translate_to = "en"
    elif translate_to == "Tamil":
        translate_to = "ta"
    elif translate_to == "Sinhala":
        translate_to = "si"
    
    return translate_text(message, translate_to)


def get_response(user_msg, token, language):

    print(user_msg)
    user_msg = translator_util(user_msg, "English")

    intent = get_intent(user_msg)
    print(intent)

    db_context = ""
    vec_db_context = ""

    if intent == "Account_details" or intent == "Account_balance":
        db_context = GetAccountDetails(token['userId'])
    elif intent == "Transactions":
        db_context = read_last_transactions(token['localId'])
        pass
    elif intent == "savings_rates":
        db_context = Get_Saving_Interest_Rates()
        pass
    elif intent == "fixed_rates":
        db_context = Get_Fixed_Interset_Rates()
        pass
    elif intent == "loan_rates":
        db_context = Get_Loan_Rates()
        pass
    elif intent == "exchange_rates":
        db_context = Get_Exchange_Rates()
        pass
    elif intent == 'vectorDb':
        vec_db_context = search_similarity(user_msg)
    
    # past_msgs = get_latest_chat_history(token['userId'], limit=1)
    past_history = ""
    # if past_msgs is not None:
    #     chat_history = past_msgs['chats']
    #     for msg in chat_history:
    #         if msg['role'] == 'user':
    #             past_history += f"<s>\n[INST]\n{msg['content']}\n[/INST]\n"
    #         else:
    #             past_history += f"{msg['content']}\n</s>\n"

    print(f"User Message: {user_msg} \nPast History: {past_history} \nDB Context: {db_context} \nVec DB Context: {vec_db_context}")
    llm_response = generate_llama2_response(user_msg, past_msgs=past_history, context=vec_db_context, db_ans=db_context)
    print("Generated LLM Response")
    save_chat_data(User_msg=user_msg, Assistance_msg=llm_response, intent=intent, accountNumber=token['userId'])

    llm_response = translator_util(llm_response, language)
    print(f"{llm_response}")
    return llm_response