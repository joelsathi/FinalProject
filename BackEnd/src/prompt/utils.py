from LLM.llm_out import generate_llama2_response
from VectorDB_chat.access_db import search_similarity
from FireBaseDB.access_db import GetAccountDetails,read_last_transactions,Get_Saving_Interest_Rates,Get_Fixed_Interset_Rates,Get_Loan_Rates,Get_Exchange_Rates
from IntentClassifierRasa.intent_finder import get_intent
from fastapi.responses import JSONResponse
from FireBaseDB.write_db import save_chat_data
from googletrans import Translator

def translator_util(message:str, translate_from:str, translate_to:str):
    if translate_from == "English":
        translate_from = "en"
    elif translate_from == "Tamil":
        translate_from = "ta"
    elif translate_from == "Sinhala":
        translate_from = "si"
    
    if translate_to == "English":
        translate_to = "en"
    elif translate_to == "Tamil":
        translate_to = "ta"
    elif translate_to == "Sinhala":
        translate_to = "si"
    
    return translate_to_lang(message, translate_from, translate_to)

def translate_to_lang(message: str, translate_from: str, translate_to: str):
    if translate_from == translate_to:
        return message
    translator = Translator()
    translation = translator.translate(message, dest=translate_to, src=translate_from)
    return translation.text

def get_response(user_msg, token, language):

    user_msg = translator_util(user_msg, language, "English")

    intent = get_intent(user_msg)

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

    past_msgs = dict()

    llm_response = generate_llama2_response(user_msg, past_msgs=past_msgs, context=vec_db_context, db_ans=db_context)

    save_chat_data(User_msg=user_msg, Assistance_msg=llm_response, intent=intent, accountNumber=token['userId'])

    llm_response = translator_util(llm_response, "English", language)

    return llm_response