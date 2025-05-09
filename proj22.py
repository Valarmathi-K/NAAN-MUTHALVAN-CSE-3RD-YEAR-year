import librosa
import numpy as np
import matplotlib.pyplot as plt
from hmmlearn import hmm
import os
import soundfile as sf

# Load audio file
def load_audio(file_path):
    y, sr = librosa.load(file_path, sr=None)
    return y, sr

# Basic noise reduction (using spectral gating)
def reduce_noise(y, sr):
    y_trimmed, _ = librosa.effects.trim(y, top_db=20)
    return y_trimmed

# Voice Activity Detection using energy thresholding
def apply_vad(y, frame_length=2048, hop_length=512, energy_threshold=0.02):
    energies = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]
    frames = librosa.util.frame(y, frame_length=frame_length, hop_length=hop_length)
    voiced_frames = [frames[:, i] for i in range(frames.shape[1]) if energies[i] > energy_threshold]
    return np.concatenate(voiced_frames) if voiced_frames else y

# Feature Extraction - MFCCs
def extract_features(y, sr):
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return mfcc.T  # Transpose to shape (frames, features)

# Train HMM model
def train_hmm(features_list, n_components=4):
    model = hmm.GaussianHMM(n_components=n_components, covariance_type='diag', n_iter=1000)
    lengths = [len(f) for f in features_list]
    X = np.vstack(features_list)
    model.fit(X, lengths)
    return model

# Prediction
def predict(model, features):
    return model.score(features)

# --- Example Usage ---
if _name_ == "_main_":
    # Directory containing speech samples
    sample_dir = "samples/"
    speaker_models = {}
    
    # Train one HMM per speaker
    for speaker in os.listdir(sample_dir):
        speaker_path = os.path.join(sample_dir, speaker)
        if not os.path.isdir(speaker_path):
            continue
        features_list = []
        for file in os.listdir(speaker_path):
            if file.endswith(".wav"):
                y, sr = load_audio(os.path.join(speaker_path, file))
                y = reduce_noise(y, sr)
                y = apply_vad(y)
                features = extract_features(y, sr)
                features_list.append(features)
        speaker_models[speaker] = train_hmm(features_list)

    # Test on a new audio
    test_file = "test.wav"
    y, sr = load_audio(test_file)
    y = reduce_noise(y, sr)
    y = apply_vad(y)
    test_features = extract_features(y, sr)

    # Predict speaker
    scores = {speaker: predict(model, test_features) for speaker, model in speaker_models.items()}
    predicted_speaker = max(scores, key=scores.get)

    print("Predicted Speaker:", predicted_speaker)
