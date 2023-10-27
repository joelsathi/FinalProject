# Localized Chatbot for Banking domain

The Localized Chatbot for Bank Customer Care project aims to develop an intelligent and interactive chatbot system to enhance customer support services for users who communicate in the native Sri Lankan (Sinhala or Tamil) language. This innovative chatbot will serve as a virtual assistant, providing quick and efficient assistance to customers seeking information regarding various banking services, account-related queries, and general inquiries.

- Language Adaptability: The primary objective of this project is to build a chatbot that can seamlessly understand and respond in either Sinhala or Tamil language. By ensuring linguistic fluency, the chatbot will enable users to interact comfortably and receive accurate and contextually appropriate responses.

- Automated Customer Support: The chatbot will act as a virtual customer support representative, automating responses to frequently asked questions and routine inquiries. By leveraging natural language processing (NLP) techniques, the chatbot will provide instant and accurate information on topics such as account balances, transaction history, loan applications, card services, and other common banking processes.

- Personalization and Context Awareness: To enhance customer satisfaction, the chatbot will be designed to recognize returning customers and retrieve their historical data. This will enable personalized assistance based on individual preferences and past interactions, creating a more personalized and engaging customer experience.

- Security and Compliance: Data security and privacy will be of paramount importance. The chatbot will be developed with robust encryption protocols to protect customer information and adhere to banking regulations and privacy laws.

- 24/7 Service:This chatbot is capable of providing 24 hour service and reduces workload for the bank staff. This will enable customers to interact with the bank even when the bank staff are not available.

## Group Members

- Sanujen Premkumar(200583P)
- Joel Sathiyendra Thiyaheswaran(200590J)
- Sandaruth Siriwardana(200607V)

## Features

- Can be used in Sinhala or Tamil or English.
- Connected to real time database. Users can ask questions about their account details.
- Users can ask questions about the bank services. The static data (i.e Data which does not change with time. Eg. Bank account opening procedures, loan procedures, bank history etc.) is stored in the vector database.
- Chatbot is restricted to the banking domain. It will not answer questions which are not related to banking.
  (Sometimes, the LLM might hallucinate and answer questions which are not related to banking. We are working on it)

## Screenshots of Application

### English

![English](./screenshots/english.png)

<table align="center">
  <tr>
    <td align="center">
     <h1 style="text-align:center;">Sinhala</h1>
      <img src="https://github.com/joelsathi/FinalProject/blob/7b482f5839a221fc5951182e53ac2ede3e80e1a4/screenshots/sinhala.png" width="450" alt="Image 1">     
    </td>
    <td align="center">
      <h1 style="text-align:center;">Tamil</h1>
      <img src="https://github.com/joelsathi/FinalProject/blob/7b482f5839a221fc5951182e53ac2ede3e80e1a4/screenshots/tamil.png" width="450" alt="Image 2">
    </td>
  </tr>
</table>

<!--### Sinhala
![Sinhala](./screenshots/sinhala.png)

### Tamil
![Tamil](./screenshots/tamil.png)  -->

## Get Started

### Prerequisites

Python <br>
Anaconda <br>
Firebase account

### Installation

create a new conda environment with python version 3.8

```bash
conda create -n chatbot python=3.8
```

Activate the conda environment

```bash
conda activate chatbot
```

Install the requirements.txt file using the following command.

```bash
pip install -r requirements.txt
```

## Usage

Login details for the chatbot

Email:

```bash
sada@gmail.com
```

<br>

Password:

```bash
 123456
```

<br>

Replicate API TOKEN:

```bash
r8_....
```

Open a command prompt

```bash
cd BackEnd\IntentClassifierRasa\
```

Run the following command to start the Rasa server for the chatbot.

```bash
rasa run --enable-api -m models/20230901-131720-reduced-shark.tar.gz
rasa run --enable-api -m models/20231026-164413-clean-outlet.tar.gz
rasa run --enable-api -m models/20231027-141720-flat-range.tar.gz
```

Open a new command prompt and run the following command to start the action server.

```bash
streamlit run streamlit_app.py
```

## Contributing
