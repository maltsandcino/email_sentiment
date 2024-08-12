from django.shortcuts import render
from django.http import HttpResponse
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer


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
#     if request.method == "POST":
# TODO: Return OVERALL sentiment analysis (Positive, Negative, Compound, sarcasm)
# TODO: Return sentence-by-sentence analysis for sarcasm + Positivity/Negativy
# TODO: Define some classes to define the level of positivity and sarcasm.

#         return JsonResponse({"": }, status=200)
    pass

