from LLM.llm_out import generate_llama2_response
from VectorDB_chat.access_db import search_similarity
from FireBaseDB.access_db import GetAccountDetails
from IntentClassifierRasa.intent_finder import get_intent
from fastapi.responses import JSONResponse
from FireBaseDB.write_db import save_chat_data

def get_response(user_msg, token):

    intent = get_intent(user_msg)

    # return intent

    db_context = ""
    vec_db_context = ""

    if intent == "Account_details" or intent == "Account_balance":
        db_context = GetAccountDetails(token['userId'])
    elif intent == "Transactions":
        # db_context = GetTransactionHistory(token['localId'])
        pass
    elif intent == "savings_rates":
        # db_context = GetInterestRates()
        pass
    elif intent == "fixed_rates":
        # db_context = GetInterestRates()
        pass
    elif intent == "loan_rates":
        # db_context = GetLoanRates()
        pass
    elif intent == "exchange_rates":
        # db_context = GetExchangeRates()
        pass
    elif intent == 'vectorDb':
        vec_db_context = search_similarity(user_msg)

    past_msgs = dict()

    llm_response = generate_llama2_response(user_msg, past_msgs=past_msgs, context=vec_db_context, db_ans=db_context)

    save_chat_data(User_msg=user_msg, Assistance_msg=llm_response, intent=intent, accountNumber=token['userId'])

    return llm_response