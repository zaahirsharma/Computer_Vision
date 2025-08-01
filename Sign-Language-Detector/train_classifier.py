import pickle

# Training a random forest classifier to detect sign language gestures
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

import numpy as np


# Load the data from the pickle file
data_dict = pickle.load(open('./data.pickle', 'rb'))

# Extract data and labels, converted to numpy array bc data is in form of lists
data = np.asarray(data_dict['data'])
labels = np.asarray(data_dict['labels'])

# Split data into training and testing sets
# Keeping 20% of the data for testing
# x = data, y = labels
# Keep same proportion of labels in both training and testing sets
x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, shuffle=True, stratify=labels)


# Create model
model = RandomForestClassifier()

# Train model
model.fit(x_train, y_train)

# Predict on the test set
y_predict = model.predict(x_test)

# Check accuracy of the model
score = accuracy_score(y_predict, y_test)

# Print the accuracy of the model, output was 100% when run
print(f'Accuracy of the model: {score * 100:.2f}%')

# Save the model to a pickle file
f = open('model.pickle', 'wb')
pickle.dump({'model': model}, f)
f.close()

