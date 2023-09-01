# Localized Chatbot for Banking domain

The Localized Chatbot for Bank Customer Care project aims to develop an intelligent and interactive chatbot system to enhance customer support services for users who communicate in the native Sri Lankan (Sinhala or Tamil) language. This innovative chatbot will serve as a virtual assistant, providing quick and efficient assistance to customers seeking information regarding various banking services, account-related queries, and general inquiries. 

- Language Adaptability: The primary objective of this project is to build a chatbot that can seamlessly understand and respond in either  Sinhala or Tamil language. By ensuring linguistic fluency, the chatbot will enable users to interact comfortably and receive accurate and contextually appropriate responses.

- Automated Customer Support: The chatbot will act as a virtual customer support representative, automating responses to frequently asked questions and routine inquiries. By leveraging natural language processing (NLP) techniques, the chatbot will provide instant and accurate information on topics such as account balances, transaction history, loan applications, card services, and other common banking processes.

- Personalization and Context Awareness: To enhance customer satisfaction, the chatbot will be designed to recognize returning customers and retrieve their historical data. This will enable personalized assistance based on individual preferences and past interactions, creating a more personalized and engaging customer experience.

- Security and Compliance: Data security and privacy will be of paramount importance. The chatbot will be developed with robust encryption protocols to protect customer information and adhere to banking regulations and privacy laws.

- 24/7 Service:This chatbot is capable of providing 24 hour service and reduces workload for the bank staff. This will enable customers to interact with the bank even when the bank staff are not available.

## Group Members

- Sanujen Premkumar(200583P)
- Joel Sathiyendra Thiyaheswaran(200590J)
- Sandaruth Siriwardana(200607V)


## Get Started

### Prerequisites

Python <br>
Anaconda <br>
Firebase account

### Installation

create a new conda environment with python version 3.8

``` bash
conda create -n chatbot python=3.8
```

Activate the conda environment

``` bash
conda activate chatbot
```

Install the requirements.txt file using the following command.

``` bash
pip install -r requirements.txt
```

## Usage

Login details for the chatbot

Email:
``` bash
sada@gmail.com  
```
<br>

Password:
``` bash
 123456
```

<br>

Replicate API TOKEN: 
``` bash
r8_3HKUEnH4PKx42QQIVjSLRyxhuXLimLL39mBtL 
```

Open a command prompt

``` bash
cd BackEnd\IntentClassifierRasa\
```

Run the following command to start the Rasa server for the chatbot.

``` bash
rasa run --enable-api -m models/20230901-131720-reduced-shark.tar.gz
 ```

Open a new command prompt and run the following command to start the action server.

``` bash
streamlit run streamlit_app.py 
```

## Contributing