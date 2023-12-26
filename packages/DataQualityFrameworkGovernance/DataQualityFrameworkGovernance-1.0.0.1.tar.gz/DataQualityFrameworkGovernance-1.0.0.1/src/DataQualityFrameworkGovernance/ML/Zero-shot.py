from transformers import pipeline
import pandas as pd

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

sequence_to_classify = "I am so gratitude with the opportunity given with the wonderful career opportunity it has got!"
candidate_labels = ['Happy', 'Sad', 'Satisified', 'May leave the organisation']
sentiment = ['positive','neutral','negative']

a = classifier(sequence_to_classify, candidate_labels)
b = classifier(sequence_to_classify, sentiment)

print('category')
print (a)
print('sentiment')
print (b)



#{'labels': ['travel', 'dancing', 'cooking'],
# 'scores': [0.9938651323318481, 0.0032737774308770895, 0.002861034357920289],
# 'sequence': 'one day I will see the world'}
