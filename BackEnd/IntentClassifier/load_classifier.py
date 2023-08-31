import os

# from intent_classifier.dataset import load_intents_from_csv
from intent_classifier import RuleClassifier, ModelClassifier, IntentClassifier

# from intent_classifier.dataset import load_intents_from_mysql, load_rules_from_mysql

model_classifier = ModelClassifier(
    folder="models", customer="common", lang="en", n_jobs=-1
)

model_classifier.load(clf_id="20230830212659")

intent_classifier = IntentClassifier(
    rule_classifier=None, model_classifier=model_classifier
)


def get_intent(text):
    intent_labels = intent_classifier.predict(words=text, context={})
    return intent_labels


prompt = input("Enter the words: ")
intent_labels = intent_classifier.predict(words=prompt, context={})

print(intent_labels)
