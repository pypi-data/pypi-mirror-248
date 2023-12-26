
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score, classification_report

def train_and_classify(input_csv_file_path, result_csv_file_path, new_feedback):
    # Load data from the CSV file
    data = pd.read_csv(input_csv_file_path, encoding='latin-1')

    # Split the data into features and labels
    X = data['Feedback']
    y = data['Category']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=36)

    # Create a text classifier pipeline using Naive Bayes
    classifier = make_pipeline(TfidfVectorizer(), MultinomialNB())

    # Train the classifier
    classifier.fit(X_train, y_train)

    # Predict the test set
    predicted = classifier.predict(X_test)

    # Evaluate the model
    accuracy = accuracy_score(y_test, predicted)
    print(f"Accuracy: {accuracy:.2f}")

    # Classification report
    print("Classification Report:")
    print(classification_report(y_test, predicted))

    # Predict sentiments of new feedback
    predicted_probabilities = classifier.predict_proba(new_feedback)
    predicted_sentiments = classifier.predict(new_feedback)

    # Extract the confidence percentage for the predicted class
    confidence_percentage = [max(probs) * 100 for probs in predicted_probabilities]

    # Store results in a DataFrame
    new_results = pd.DataFrame({'Feedback': new_feedback, 'Category': predicted_sentiments, 'Confidence': confidence_percentage})

    # Save the updated DataFrame to a CSV file
    new_results.to_csv(result_csv_file_path, index=False)

    return new_results

# Usage example:

input_path = '/Users/rajithprabhakaran/Library/Mobile Documents/com~apple~CloudDocs/Documents/Python/Python Package/src/DataQualityFrameworkGovernance/Files/en_model_positive_neutral_negative.csv'
result_path = '/Users/rajithprabhakaran/Library/Mobile Documents/com~apple~CloudDocs/Documents/Python/Python Package/src/DataQualityFrameworkGovernance/Files/Result_Feedback_in_text.csv'

new_feedback_to_classify = [
    "Peron was rude and unpleasant",
    "He was so excited and happy to fetch us",
    "It was an okay place",
    "I am having some trouble with this product. I am not sure if I am using it correctly.",
    "That is crazy!  Who are they to say someone cannot own a knife?!  I imagine about 99% of people who own a knife like the one in this video would never even think of hurting another human being.",
    "where the fuck is my fully automatic shotgun which shoots out hamburgers",
    "How dare a leader put his own country first.",
    "Every country needs leaders like this.",
    "Its high time europe must understand this. And according to current changes happening in europe most of European are leaning toward conservation. In Germany people are also leaning towards conservatives.",
    "LIfe is full of stones, it upto you whether you choose diamonds or rocks",
    "I am done",
    "I am so done",
    "I feel so done",
    "I am so done with everything",
    "I think I am fine",
    "I need a break",
    "I feel drained and exhausted, i cant do it anymore",
    "I feel drained",
    "Its always faliures",
    "i am drained, but I dont know why",
    "My energy feels drained",
    "I feel exhausted",
    "Its elegant",
    "He is in a meeting",
    "Kid is playing with a toy",
    "She is sitting there with a bomb",
    "He is carrying a gun",
    "He is carrying a gun to protect the civilians",
    "Policeman is carrying a gun to protect the community",
    "Policeman is carrying a gun"
]

train_and_classify(input_path, result_path, new_feedback_to_classify)
