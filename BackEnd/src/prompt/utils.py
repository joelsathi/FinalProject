from LLM.llm_out import generate_llama2_response
from VectorDB_chat.access_db import search_similarity
from FireBaseDB.access_db import GetAccountDetails,read_last_transactions,Get_Saving_Interest_Rates,Get_Fixed_Interset_Rates,Get_Loan_Rates,Get_Exchange_Rates
from IntentClassifierRasa.intent_finder import get_intent
from fastapi.responses import JSONResponse

def get_response(user_msg, token):

    # return user_msg

    intent = get_intent(user_msg)

    # return intent

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

    return llm_response