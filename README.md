#### Sentiment and Sarcasm Analyzer

## Rationale:

I wanted to create a tool to help decide whether messages for colleagues or friends could be interpreted negatively or sarcastically by the receiver. This is especially helpful for communication via text-based methods, and for those who may find discerning sentiment difficult in a general context (such as, those with some type of neurodivergence).

## What It Does:

The app is fairly basic. It takes a string of text, tokenizes them to sentences, and then returns the values to the user based on its backend anaylsis of the text. Colors are used to indicate whether a sentence has a a positive sentiment (the left-most color on the scale is the most positive) or a negative sentement. A red underline goes under sentences that have triggered the sarcasm detector, and warrant a second look as well.

## How does it do that?

We send the string to the backend with a promise, and the backend processes it using the sent_tokenizer from NLTK. It then uses the VADER module from NLTK to get the compound sentiment for each sentence, and coverts it to a useable number between 10 and -10. It then gets the average sentiment.

We use the tokenzied sentences with a second tokenizer, based on a model I trained on a dataset of 1,3 million reddit comments, classified for sarcasm. We use this model to determine whether the string is likely to be sarcastic. It has around a 70% accuracy rate, which is considerably better than chance, but since there is room for error, I set a high threshold to classify each string as sarcastic, to avoid too many false positives.

A dict with strings, their sarcasm and sentiment levels, an overall number of sarcastic instances, and the overall sentiment are then sent back to the promise, and processed there by adding particular classes to the elements that are created with the results.


## Future 

There is some room for improvement. For instance, sentences have to be different in order to work within a dictionary, because keys have to be unique. There is also room for more styling.

