import streamlit as st
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
import time
from scipy.ndimage import gaussian_filter1d

# Function to load and preprocess audio
def load_audio(file):
    y, sr = librosa.load(file, sr=None)
    return y, sr

# Function to compute and plot spectrogram
def plot_spectrogram(y, sr, ax, title):
    S = librosa.stft(y)
    S_dB = librosa.amplitude_to_db(np.abs(S), ref=np.max)
    img = librosa.display.specshow(S_dB, sr=sr, x_axis='time', y_axis='log', ax=ax)
    ax.set_title(title)
    return img

# Streamlit app
st.title('Real-Time Audio Frequency Comparison')

# Initialize session state for controlling real-time analysis
if 'analyzing' not in st.session_state:
    st.session_state.analyzing = False

# File upload
uploaded_file1 = st.file_uploader("Upload Your Original Audio File", type=["wav", "mp3"])
uploaded_file2 = st.file_uploader("Upload Your Audio File", type=["wav", "mp3"])

# Set up buttons to start and stop the real-time comparison
if uploaded_file1 and uploaded_file2:
    y1, sr1 = load_audio(uploaded_file1)
    y2, sr2 = load_audio(uploaded_file2)

    st.subheader('Real-Time Frequency Comparison')

    # Create placeholders for the plots
    fig, ax = plt.subplots(2, 1, figsize=(10, 8))
    img1 = plot_spectrogram(y1[:sr1 * 5], sr1, ax[0], 'Original Audio')
    img2 = plot_spectrogram(y2[:sr2 * 5], sr2, ax[1], 'Performance Audio')

    placeholder = st.pyplot(fig)

    if st.button('Start Real-Time Comparison'):
        st.session_state.analyzing = True

    if st.button('Stop Real-Time Comparison'):
        st.session_state.analyzing = False

    # Real-time comparison loop
    if st.session_state.analyzing:
        hop_length = sr1 // 2  # Half-second hop length for smoother transitions
        window_length = sr1 * 5  # 5-second window length

        for start in range(0, min(len(y1), len(y2)) - window_length, hop_length):
            if not st.session_state.analyzing:
                break

            y1_segment = y1[start:start + window_length]
            y2_segment = y2[start:start + window_length]

            # Clear the axes
            ax[0].cla()
            ax[1].cla()

            # Plot the updated spectrograms
            plot_spectrogram(y1_segment, sr1, ax[0], 'Original Audio')
            plot_spectrogram(y2_segment, sr2, ax[1], 'Performance Audio')

            # Update the plot
            placeholder.pyplot(fig)

            # Wait for a short interval to simulate real-time update
            time.sleep(0.5)

