from ...LLM.llm_out import generate_llama2_response
from ...VectorDB_chat.access_db import search_similarity
from ...FireBaseDB.access_db import GetAccountDetails
from ...IntentClassifierRasa.intent_finder import get_intent

async def get_response(user_msg, token):

    intent = get_intent(user_msg)

    db_context = ""
    vec_db_context = ""

    if intent == "Account_details":
        db_context = GetAccountDetails(token['localId'])
    elif intent == "Transaction_history":
        # db_context = GetTransactionHistory(token['localId'])
        pass
    elif intent == "Interest_rates":
        # db_context = GetInterestRates()
        pass
    elif intent == "Loan_rates":
        # db_context = GetLoanRates()
        pass
    elif intent == "Exchange_rates":
        # db_context = GetExchangeRates()
        pass
    elif intent == 'vectorDb':
        vec_db_context = search_similarity(user_msg)

    past_msgs = dict()

    llm_response = generate_llama2_response(user_msg, past_msgs=past_msgs, context=vec_db_context, db_ans=db_context)