import evaluate

# Load the ROUGE evaluation metric
rouge = evaluate.load('rouge')

# Define the candidate predictions and reference sentences
predictions = []
references = ["Hello! How can I assist you with your banking-related questions or concerns today?", 
              "Your current account balance, Sanda, is $1,800 in your savings account. If you have any more questions or need assistance with anything else related to your account, please feel free to ask.",
              """To determine how much money you'll have if you convert your $1,800 in your U.S. savings account to Sri Lankan Rupees (LKR), you can use the provided exchange rates:
                - Buy rate: 322.3488 LKR per 1 USD
                - Sell rate: 332.6334 LKR per 1 USD
                To calculate, you can multiply your account balance by the buy rate to get an estimate of the amount you'll receive when converting to LKR:
                $1,800 (USD) * 322.3488 (LKR/USD) = 579,227.84 LKR
                So, if you convert your $1,800 to Sri Lankan Rupees at the given buy rate, you would have approximately 579,227.84 LKR. Please note that actual rates and fees may vary depending on the bank or currency exchange service you use.""",
                ""
            ]

# Compute the ROUGE score
results = rouge.compute(predictions=predictions, references=references)

# Print the results
print(results)