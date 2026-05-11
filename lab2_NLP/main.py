import os
import warnings

from sklearn.exceptions import UndefinedMetricWarning
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import f1_score, accuracy_score, recall_score
import torch
from torch.utils.data import DataLoader
import numpy as np

from config import EMB_PATH
from dataloading import SentenceDataset
from models import BaselineDNN, LSTM
from training import train_dataset, eval_dataset
from utils.load_datasets import load_MR, load_Semeval2017A
from utils.load_embeddings import load_word_vectors
from training import torch_train_val_split
from early_stopper import EarlyStopper
from attention import SimpleSelfAttentionModel, MultiHeadAttentionModel, TransformerEncoderModel

from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore", category=UndefinedMetricWarning)


########################################################
# Configuration
########################################################


# Download the embeddings of your choice
# for example http://nlp.stanford.edu/data/glove.6B.zip

# 1 - point to the pretrained embeddings file (must be in /embeddings folder)
EMBEDDINGS = os.path.join(EMB_PATH, "glove.6B.50d.txt")

# 2 - set the correct dimensionality of the embeddings
EMB_DIM = 50

EMB_TRAINABLE = False
BATCH_SIZE = 128
EPOCHS = 50
DATASET = "MR"  # options: "MR", "Semeval2017A"

# if your computer has a CUDA compatible gpu use it, otherwise use the cpu
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# DEVICE = "cpu"

########################################################
# Define PyTorch datasets and dataloaders
########################################################

# load word embeddings
print("loading word embeddings...")
word2idx, idx2word, embeddings = load_word_vectors(EMBEDDINGS, EMB_DIM)

# load the raw data
if DATASET == "Semeval2017A":
    X_train, y_train, X_test, y_test = load_Semeval2017A()
elif DATASET == "MR":
    X_train, y_train, X_test, y_test = load_MR()
else:
    raise ValueError("Invalid dataset")

# convert data labels from strings to integers
label_encoder = LabelEncoder()

y_train = label_encoder.fit_transform(y_train)  # EX1
y_test =  label_encoder.fit_transform(y_test)  # EX1
n_classes = label_encoder.classes_.size  # EX1 - LabelEncoder.classes_.size

print("First 10 labels (coded):", y_train[:10])
print("Corresponding labels:", label_encoder.inverse_transform(y_train[:10]))


# Define our PyTorch-based Dataset
train_set = SentenceDataset(X_train, y_train, word2idx)
test_set = SentenceDataset(X_test, y_test, word2idx)

#Print first 10 exapmles #EX2
for i in range(10):
    print(f"Example {i+1}:")
    print("Token indices:", train_set.data[i])
    print("Label:", train_set.labels[i])
    print()

for i in range(min(5, len(train_set))):
    original_sentence = train_set.data[i]
    original_label_str = train_set.labels[i]
    processed_example, label, length = train_set[i]
    example_str = "[ " + " ".join(str(num) for num in processed_example) + "]"
    print(f'\ndataitem = "{original_sentence}", label = "{original_label_str}"')
    print("Return values:")
    print(f"example = {example_str}")
    print(f"label = {label}")
    print(f"length = {length}")

# EX7 - Define our PyTorch-based DataLoader
#train_loader = DataLoader(train_set, batch_size= BATCH_SIZE, shuffle=True) # EX7
test_loader = DataLoader(test_set, batch_size=BATCH_SIZE, shuffle=False)  #EX7

#2.1 added
train_loader, val_loader = torch_train_val_split(train_set, BATCH_SIZE, BATCH_SIZE)


#############################################################################
# Model Definition (Model, Loss Function, Optimizer)
#############################################################################
# model = BaselineDNN(output_size= n_classes,  # EX8
#                     embeddings=embeddings,
#                     trainable_emb=EMB_TRAINABLE)

model = TransformerEncoderModel(output_size=n_classes, embeddings=embeddings, n_head = 9, n_layer = 6)

# model = LSTM(output_size= n_classes,  # EX8
#                     embeddings=embeddings,
#                     trainable_emb=EMB_TRAINABLE, bidirectional= True)

# move the mode weight to cpu or gpu
model.to(DEVICE)
print(model)

# We optimize ONLY those parameters that are trainable (p.requires_grad==True)
# if (n_classes == 2):
#     criterion = torch.nn.BCEWithLogitsLoss()  # EX8
# else:

#only keep this
criterion = torch.nn.CrossEntropyLoss()

parameters = filter(lambda p: p.requires_grad, model.parameters())  # EX8
optimizer = torch.optim.Adam(parameters, lr=1e-4)  # 10x smaller

#############################################################################
# Training Pipeline
#############################################################################
total_train_losses = []
total_test_losses = []
total_train_accuracy = []
total_test_accuracy = []
total_test_recall = []
total_train_recall = []
total_train_f1 = []
total_test_f1 = []

save_path = f'{DATASET}_{model.__class__.__name__}.pth'
early_stopper = EarlyStopper(model, save_path, patience=5) 

for epoch in range(1, EPOCHS + 1):
    # train the model for one epoch
    train_dataset(epoch, train_loader, model, criterion, optimizer)

    # evaluate the performance of the model, on both data sets
    train_loss, (y_train_gold, y_train_pred) = eval_dataset(train_loader,
                                                            model,
                                                            criterion)

    test_loss, (y_test_gold, y_test_pred) = eval_dataset(test_loader,
                                                         model,
                                                         criterion)
    
        
    # evaluate the performance of the model, on both data sets
    valid_loss, (y_valid_gold, y_valid_pred) = eval_dataset(val_loader,
                                                            model,
                                                            criterion)
    

    if early_stopper.early_stop(valid_loss):
        EPOCHS = epoch - 1
        print('Early Stopping was activated.')
        print(f'Epoch {epoch-1}/{EPOCHS}, Loss at training set: {train_loss}\n\tLoss at validation set: {valid_loss}')
        print('Training has been completed.\n')
        print("My test loss is :", test_loss)
        # print("Accuracy for train:" , accuracy_score(y_train_true, y_train_pred))
        # print("Accuracy for test:" , accuracy_score(y_test_true, y_test_pred))
        # print("F1 score for train:", f1_score(y_train_true, y_train_pred, average='macro'))
        # print("F1 score for test:", f1_score(y_test_true, y_test_pred, average='macro'))
        # print("Recall score for train:", recall_score(y_train_true, y_train_pred, average='macro'))
        # print("Recall score for test:", recall_score(y_test_true, y_test_pred, average='macro'))
        break
    
    total_train_losses.append(train_loss)
    total_test_losses.append(test_loss)
    # Convert preds and golds in a list.
    y_train_true = np.concatenate( y_train_gold, axis=0 )
    y_test_true = np.concatenate( y_test_gold, axis=0 )
    y_train_pred = np.concatenate( y_train_pred, axis=0 )
    y_test_pred = np.concatenate( y_test_pred, axis=0 )
    print("My train loss is :" , train_loss)
    print("My test loss is :", test_loss)
    total_train_accuracy.append(accuracy_score(y_train_true, y_train_pred))
    print("Accuracy for train:" , accuracy_score(y_train_true, y_train_pred))
    total_test_accuracy.append(accuracy_score(y_test_true, y_test_pred))
    print("Accuracy for test:" , accuracy_score(y_test_true, y_test_pred))
    total_train_f1.append(f1_score(y_train_true, y_train_pred))
    print("F1 score for train:", f1_score(y_train_true, y_train_pred, average='macro'))
    total_test_f1.append(f1_score(y_test_true, y_test_pred))
    print("F1 score for test:", f1_score(y_test_true, y_test_pred, average='macro'))
    total_train_recall.append(recall_score(y_train_true, y_train_pred, average='macro'))
    print("Recall score for train:", recall_score(y_train_true, y_train_pred, average='macro'))
    total_test_recall.append(recall_score(y_test_true, y_test_pred, average='macro'))
    print("Recall score for test:", recall_score(y_test_true, y_test_pred, average='macro'))

# Plot
import matplotlib.pyplot as plt

fig, axs = plt.subplots(2, 2, figsize=(14, 10))
epochs = range(1, EPOCHS + 1)

# Loss
axs[0, 0].plot(epochs, total_train_losses, label="Training Loss")
axs[0, 0].plot(epochs, total_test_losses, label="Validation Loss", color="orange")
axs[0, 0].set_title("Loss")
axs[0, 0].set_xlabel("Epoch")
axs[0, 0].set_ylabel("Loss")
axs[0, 0].legend()
axs[0, 0].grid(True)

# Accuracy
axs[0, 1].plot(epochs, total_train_accuracy, label="Training Accuracy")
axs[0, 1].plot(epochs, total_test_accuracy, label="Validation Accuracy", color="orange")
axs[0, 1].set_title("Accuracy")
axs[0, 1].set_xlabel("Epoch")
axs[0, 1].set_ylabel("Accuracy")
axs[0, 1].legend()
axs[0, 1].grid(True)

# Recall
axs[1, 0].plot(epochs, total_train_recall, label="Training Recall")
axs[1, 0].plot(epochs, total_test_recall, label="Validation Recall", color="orange")
axs[1, 0].set_title("Recall")
axs[1, 0].set_xlabel("Epoch")
axs[1, 0].set_ylabel("Recall")
axs[1, 0].legend()
axs[1, 0].grid(True)

# F1 Score
axs[1, 1].plot(epochs, total_train_f1, label="Training F1")
axs[1, 1].plot(epochs, total_test_f1, label="Validation F1", color="orange")
axs[1, 1].set_title("F1 Score")
axs[1, 1].set_xlabel("Epoch")
axs[1, 1].set_ylabel("F1 Score")
axs[1, 1].legend()
axs[1, 1].grid(True)

# Layout
plt.tight_layout()
plt.suptitle("Training vs Validation Metrics", fontsize=16, y=1.02)
plt.show()

plt.savefig("training_metrics.png", dpi=300, bbox_inches='tight')