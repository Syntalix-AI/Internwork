import os
import numpy as np
import librosa
from sklearn.preprocessing import StandardScaler
from pyod.models.iforest import IForest

def extract_features(file_path):
    """Extract MFCC features from an audio file."""
    y, sr = librosa.load(file_path, sr=None)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return np.mean(mfccs.T, axis=0)

def load_data(directory):
    """Load audio data and extract features from a directory."""
    features = []
    for root, _, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith('.wav'):
                file_path = os.path.join(root, file_name)
                print(f"Loading file: {file_path}")  # Debug print
                features.append(extract_features(file_path))
    if not features:
        print(f"No .wav files found in directory: {directory}")  # Debug print
    return np.array(features)

def train_model(train_data_dir):
    """Train an Isolation Forest model on the training data."""
    train_features = load_data(train_data_dir)
    if len(train_features) == 0:
        raise ValueError("No training data loaded. Check directory and file format.")
    
    scaler = StandardScaler()
    train_features = scaler.fit_transform(train_features)
    
    model = IForest()
    model.fit(train_features)
    
    return model, scaler

def detect_anomalies(directory, model, scaler):
    """Detect anomalies in the audio data using the provided Isolation Forest model."""
    test_features = load_data(directory)
    test_features = scaler.transform(test_features)
    anomaly_scores = model.decision_function(test_features)
    is_anomalies = model.predict(test_features)
    return is_anomalies, anomaly_scores

def print_results(directory, is_anomalies, scores):
    """Print the results of the anomaly detection."""
    file_names = []
    for root, _, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith('.wav'):
                file_names.append(file_name)

    for file_name, is_anomaly, score in zip(file_names, is_anomalies, scores):
        print(f"File: {file_name}, Anomaly: {is_anomaly}, Score: {score}")

# Specify the paths to your directories
train_data_dir = r'C:\Users\Pratyusha Chatterjee\Downloads\dev_data_fan\fan\train'
source_test_data_dir = r'C:\Users\Pratyusha Chatterjee\Downloads\dev_data_fan\fan\source_test'
target_test_data_dir = r'C:\Users\Pratyusha Chatterjee\Downloads\dev_data_fan\fan\target_test'

# Train the Isolation Forest model on the training data
try:
    model, scaler = train_model(train_data_dir)
except ValueError as e:
    print(f"Error: {e}")
    # Exit or handle the error gracefully

# Example: Detect anomalies in source test data
source_is_anomalies, source_scores = detect_anomalies(source_test_data_dir, model, scaler)

# Example: Detect anomalies in target test data
target_is_anomalies, target_scores = detect_anomalies(target_test_data_dir, model, scaler)

# Example: Print results for source test data
print("Source Test Results:")
print_results(source_test_data_dir, source_is_anomalies, source_scores)

# Example: Print results for target test data
print("\nTarget Test Results:")
print_results(target_test_data_dir, target_is_anomalies, target_scores)
