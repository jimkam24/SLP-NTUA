from transformers import pipeline
from sklearn.preprocessing import LabelEncoder
from tqdm import tqdm
from utils.load_datasets import load_MR, load_Semeval2017A
from training import get_metrics_report
import torch

# Label mappings for each dataset and model
LABELS_MAPPING = {
    'MR': {
        'siebert/sentiment-roberta-large-english': {
            'POSITIVE': 'positive',  # Positive sentiment
            'NEGATIVE': 'negative',  # Negative sentiment
        },
        'distilbert-base-uncased-finetuned-sst-2-english': {
            'POSITIVE': 'positive',  # Positive sentiment
            'NEGATIVE': 'negative',  # Negative sentiment
        },
        'textattack/bert-base-uncased-SST-2': {
            'LABEL_0': 'negative',  # Negative sentiment
            'LABEL_1': 'positive',  # Positive sentiment
        }
    },
    'Semeval2017A': {
        'finiteautomata/bertweet-base-sentiment-analysis': {
            'NEG': 'negative',  # Negative sentiment
            'NEU': 'neutral',   # Neutral sentiment
            'POS': 'positive',  # Positive sentiment
        },
        'cardiffnlp/twitter-roberta-base-sentiment': {
            'LABEL_0': 'negative',  # Negative sentiment
            'LABEL_1': 'neutral',   # Neutral sentiment
            'LABEL_2': 'positive',  # Positive sentiment
        },
        'j-hartmann/sentiment-roberta-large-english-3-classes': {
            'negative': 'negative',
            'neutral': 'neutral',
            'positive': 'positive',
        }
    }
}

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# Datasets
DATASETS = ['MR', 'Semeval2017A']
MODEL_NAMES = {
    'MR': ['siebert/sentiment-roberta-large-english', 'distilbert-base-uncased-finetuned-sst-2-english', 'textattack/bert-base-uncased-SST-2'],
    'Semeval2017A': ['finiteautomata/bertweet-base-sentiment-analysis', 'cardiffnlp/twitter-roberta-base-sentiment','j-hartmann/sentiment-roberta-large-english-3-classes']
}

if __name__ == '__main__':
    # Loop through each dataset
    for dataset in DATASETS:
        # Load the appropriate dataset
        if dataset == "Semeval2017A":
            X_train, y_train, X_test, y_test = load_Semeval2017A()
        elif dataset == "MR":
            X_train, y_train, X_test, y_test = load_MR()
        else:
            raise ValueError("Invalid dataset")

        # Encode labels
        le = LabelEncoder()
        le.fit(list(set(y_train)))  # Fit label encoder to the training labels
        y_train = le.transform(y_train)
        y_test = le.transform(y_test)
        n_classes = len(list(le.classes_))

        # Loop through each model
        for model_name in MODEL_NAMES[dataset]:
            print(f"Evaluating model: {model_name}")
            
            # Define the sentiment-analysis pipeline for the model
            sentiment_pipeline = pipeline("sentiment-analysis", model=model_name, device=DEVICE)

            y_pred = []

            # Using tqdm for progress bar that updates in place
            for x in tqdm(X_test, desc=f"Processing {model_name}", leave=True):  # The 'desc' is the description for the progress bar
                # Get the label using the defined pipeline
                result = sentiment_pipeline(x)[0]
                label = result['label']
                

                y_pred.append(LABELS_MAPPING[dataset][model_name][label])

            # Ensure the predictions are transformed using the same encoder
            y_pred_enc = le.transform(y_pred)  # Transform predictions using the encoder
            
            # Print evaluation metrics
            print(f'\nDataset: {dataset}\nPre-Trained model: {model_name}\nTest set evaluation\n{get_metrics_report([y_test], [y_pred_enc])}')
