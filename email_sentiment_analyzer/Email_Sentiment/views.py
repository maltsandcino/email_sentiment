from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
import nltk

from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')

class_dict = {
    8: "Top",
    7: "Top1",
    5: "Top2",
    3: "Top3",
    0: "Neutral",
    -3: "worstm3",
    -5: "Worstm2",
    -7: "Worstm1",
    -8: "Worst"
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
        
        for item in tokens:
            value = analyzer.polarity_scores(item)['compound']
            value = round(value, 1) * 10
            for level in class_dict:
                if value < level:
                    continue
                else:
                    value = level
                    break

            value = class_dict[value]
            token_values.append(value)
        


        token_dict = dict(zip(tokens, token_values))


        print(token_dict)
       
        # print(pol_scores)
        


# TODO: Return OVERALL sentiment analysis (Positive, Negative, Compound, sarcasm)
# TODO: Return sentence-by-sentence analysis for sarcasm + Positivity/Negativy
# TODO: Define some classes to define the level of positivity and sarcasm.

        return JsonResponse({"sentences": token_dict}, status=200)
    

