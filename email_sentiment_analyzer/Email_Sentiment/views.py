from django.shortcuts import render
from django.http import HttpResponse
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Create your views here.

def index(request):
    return HttpResponse("Test")

# def sentence_analyzer(request):
#     if request.method == "POST":
# TODO: Return OVERALL sentiment analysis (Positive, Negative, Compound, sarcasm)
# TODO: Return sentence-by-sentence analysis for sarcasm + Positivity/Negativy
# TODO: Define some classes to define the level of positivity and sarcasm.
#         return JsonResponse({"": }, status=200)

