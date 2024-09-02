from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import os
import copy

with open('Email_Sentiment\\assets\\tokenize.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

model = tf.keras.models.load_model('Email_Sentiment\\assets\\model.keras')

nltk.download('vader_lexicon')

class_dict = {
    10: "AbsoluteTop",
    8: "Top",
    7: "Top1",
    5: "Top2",
    3: "Top3",
    0: "Neutral",
    -3: "worstm3",
    -5: "Worstm2",
    -7: "Worstm1",
    -8: "Worst",
    -10: "ReallyWorst"
}

# We need to have this set of models to tokenize our sentences.
try:
    nltk.data.find('tokenizers/punkt')
    print("Present")
except LookupError:
    print("Aquiring Models")
    nltk.download('punkt')
    

def index(request):
    nums = []
    for i in range(1,12):
        nums.append(i)
    return render(request, "Email_Sentiment/index.html", {'nums': nums})

def analyze(request):
    if request.method == "POST":
        data = json.loads(request.body)
        text_to_analyze = data.get("data")
        
        ##We first are looking at the sentiment

        tokens = nltk.tokenize.sent_tokenize(text_to_analyze)
        analyzer = SentimentIntensityAnalyzer()
        
        token_values = []
        numeric_values = []
        
        for item in tokens:
            value = analyzer.polarity_scores(item)['compound']
            value = round(value, 1) * 10
            numeric_values.append(value)
            numeric_value = value
            for level in class_dict:
                if value < level:
                    continue
                else:
                    value = level
                    break
            value = class_dict[value]
            token_values.append(value)
        
        # Getting an overall reading of the submitted text by looking at the average compound value:

        overall_sentiment = (sum(numeric_values) / len(numeric_values)) * 10

        if overall_sentiment < 0:
            overall_sentiment = f'{abs(overall_sentiment):.1f}% Negative'
        else:
            overall_sentiment = f'{abs(overall_sentiment):.1f}% Positive'
        
        token_dict = dict(zip(tokens, token_values))

        #Below we are running the same data though the sarcasm model

        max_length = 100
        trunc_type='post'
        padding_type='post'

        sequences = tokenizer.texts_to_sequences(tokens)
        padded = pad_sequences(sequences, maxlen=max_length, padding=padding_type, truncating=trunc_type)
        predictions = model.predict(padded)

        #During development, I want to keep these separate for data safety and debugging later.

        sarcasm_predictions = copy.deepcopy(token_dict)

        # The model is only about 70% accurate, and I want to set a fairly high threshold for considering something possibly sarcastic.
        total_sarcastic = 0
        for_index = list(sarcasm_predictions.keys())
        for sentence, prediction in zip(tokens, predictions):
            if prediction > 0.7:
                sarcasm_predictions[sentence] = [sarcasm_predictions[sentence], "Sarcastic", numeric_values[for_index.index(sentence)]]
                total_sarcastic += 1                
            else:
                sarcasm_predictions[sentence] = [sarcasm_predictions[sentence], "NotSarcastic", numeric_values[for_index.index(sentence)]]
        
        print(sarcasm_predictions)
        if total_sarcastic == 1:
            total_sarcastic = f"{total_sarcastic} instance"
        else:
            total_sarcastic = f"{total_sarcastic} instances"
       
        # print(pol_scores)
        


# TODO: Return OVERALL sentiment analysis (Positive, Negative, Compound, sarcasm)
# TODO: Return sentence-by-sentence analysis for sarcasm + Positivity/Negativy
# TODO: Define some classes to define the level of positivity and sarcasm.

        return JsonResponse({"sentences": sarcasm_predictions, "overall_sentiment": overall_sentiment, "overall_sarcastic": total_sarcastic}, status=200)
    

