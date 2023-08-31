import os

from intent_classifier.dataset import load_intents_from_csv
from intent_classifier import RuleClassifier, ModelClassifier, IntentClassifier
from intent_classifier.dataset import load_intents_from_mysql, load_rules_from_mysql


str = "C:\\Users\\Sanu\\Desktop\\FinalProject\\BackEnd\\IntentClassifier\\intent_classifier\\Data\\dataset.csv"
data_bunch = load_intents_from_csv(csv_path=str, customer="common")

folder = os.path.join(os.getcwd(), "models")

model_classifier = ModelClassifier(
    folder=folder, customer="common", lang="en", n_jobs=-1
)
model_classifier.fit(data_bunch)
model_classifier.dump()

# X_tuple = tuple(data_bunch[["words", "contexts"]].to_records(index=False))
# Y = data_bunch["intents"]
# Y_np = Y["intents"].values
# model_classifier._fit(X_tuple, Y_np)
