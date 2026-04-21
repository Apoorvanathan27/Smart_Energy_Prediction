import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib
import os

# Get current directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load dataset
data_path = os.path.join(BASE_DIR, '..', 'data', 'energy_data.csv')
data = pd.read_csv(data_path)

# Example fields
X = data[['field1','field2','field3']]
y = data['field4']

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2)

model = LinearRegression()
model.fit(X_train,y_train)

# Save model in model folder
model_path = os.path.join(BASE_DIR, 'model.pkl')
joblib.dump(model, model_path)

print("Model Trained Successfully")
print("Model saved at:", model_path)