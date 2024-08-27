from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
import nltk

from nltk.sentiment.vader import SentimentIntensityAnalyzer
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
    message = 'sdsdsdsdsd'
    return render(request, "Email_Sentiment/index.html", {'message': message})

def analyze(request):
    if request.method == "POST":
        data = json.loads(request.body)
        text_to_analyze = data.get("data")
        
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
        
        overall_sentiment = (sum(numeric_values) / len(numeric_values)) * 10

        print(overall_sentiment)

        if overall_sentiment < 0:
            overall_sentiment = f'{abs(overall_sentiment):.1f}% Negative'
        else:
            overall_sentiment = f'{abs(overall_sentiment):.1f}% Positive'
        
        print(overall_sentiment)
        
        


        token_dict = dict(zip(tokens, token_values))


        print(token_dict)
       
        # print(pol_scores)
        


# TODO: Return OVERALL sentiment analysis (Positive, Negative, Compound, sarcasm)
# TODO: Return sentence-by-sentence analysis for sarcasm + Positivity/Negativy
# TODO: Define some classes to define the level of positivity and sarcasm.

        return JsonResponse({"sentences": token_dict, "overall_sentiment": overall_sentiment}, status=200)
    

