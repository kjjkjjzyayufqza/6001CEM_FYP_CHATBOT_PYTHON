import random
import json
import torch
from model import NeuralNet
from nltk_utils import bag_of_words,tokenize
import os

def ChatBot(Message):
    current_path = os.path.dirname(__file__) + '/'
    with open(current_path + 'intents.json', 'r') as f:
        intents = json.load(f)

    FILE = "data.pth"
    data = torch.load(current_path + FILE)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    input_size = data["input_size"]
    hidden_size = data["hidden_size"]
    output_size = data["output_size"]
    all_words = data['all_words']
    tags = data['tags']
    model_state = data["model_state"]
    print(input)
    model = NeuralNet(input_size, hidden_size, output_size).to(device)
    model.load_state_dict(model_state)
    model.eval()

    bot_name = "Johnson"
    print("Let's chat! type 'quit' to exit!")
    sentence = Message
    sentence = tokenize(sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)
    
    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.98:
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                return (f"{bot_name}: {random.choice(intent['responses'])}")
    else:
        return (f"{bot_name}: I do not understand...")

if __name__ == '__main__':
    ChatBot()