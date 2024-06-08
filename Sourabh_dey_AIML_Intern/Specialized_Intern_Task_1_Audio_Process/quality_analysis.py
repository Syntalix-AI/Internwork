import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
import math

# Function to extract pitch features using Librosa
def extract_pitch(y, sr):
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    avg_pitch = librosa.feature.rms(S=magnitudes * pitches)
    return avg_pitch

# Load audio files
a1 = input("Your Original Audio File: ")
a2 = input("Your Audio file: ")
y1, sr1 = librosa.load(a1)
y2, sr2 = librosa.load(a2)

#manhatten
#jacard index
#mahalnobis


#for showing percentage
x = lambda a,b : print(f"Percentage Deviation = {abs(((a-b)/a)*100)} \n")

#lambda for calculating percentage
v = lambda a,b : abs(((a-b)/a)*100)
# Extract MFCC features
mfcc_original = librosa.feature.mfcc(y=y1, sr=sr1)
mfcc_performance = librosa.feature.mfcc(y=y2, sr=sr2)

# Extract pitch features
pitch_original = extract_pitch(y=y1, sr=sr1)
pitch_performance = extract_pitch(y=y2, sr=sr2)



print("\nDYNAMIC TIME WARP DISTANCE ANALYSIS\n")
print("----------------------------------------------------------------")
# Calculate the DTW distance between the MFCC sequences
distance_mfcc, _ = fastdtw(mfcc_original.T, mfcc_performance.T, dist=euclidean)

print("DTW Distance (MFCC):", distance_mfcc)

# Calculate the DTW distance between the pitch sequences
distance_pitch, _ = fastdtw(pitch_original.T, pitch_performance.T, dist=euclidean)
print("DTW Distance (Pitch):", distance_pitch)

print("\nTEMPO ANALYSIS\n")
print("----------------------------------------------------------------")
# Additional features
# Calculate tempo (beats per minute) using Librosa's tempo estimation
tempo_original = librosa.beat.tempo(y=y1, sr=sr1)
tempo_performance = librosa.beat.tempo(y=y2, sr=sr2)
print("Tempo (Original):", tempo_original)
print("Tempo (Performance):", tempo_performance)
x(tempo_original,tempo_performance)
v_tempo= v(tempo_original,tempo_performance)
print("\nZERO CROSSING RATE ANALYSIS\n")
print("----------------------------------------------------------------")
# Calculate zero-crossing rate (ZCR) using Librosa
zcr_original = librosa.feature.zero_crossing_rate(y=y1)
zcr_performance = librosa.feature.zero_crossing_rate(y=y2)
avg_zcr_original = np.mean(zcr_original)
avg_zcr_performance = np.mean(zcr_performance)
print("Average ZCR (Original):", avg_zcr_original)
print("Average ZCR (Performance):", avg_zcr_performance)
v_zcr = v(avg_zcr_original,avg_zcr_performance)
x(avg_zcr_original,avg_zcr_performance)



#print("\nSPECTRAL CONTRAST\n")
# Spectral Contrast
spectral_contrast_original = librosa.feature.spectral_contrast(y=y1, sr=sr1)
spectral_contrast_performance = librosa.feature.spectral_contrast(y=y2, sr=sr2)
mean_spectral_contrast_original = np.mean(spectral_contrast_original, axis=1)
mean_spectral_contrast_performance = np.mean(spectral_contrast_performance, axis=1)
#print("Mean Spectral Contrast (Original):", mean_spectral_contrast_original)
#print("Mean Spectral Contrast (Performance):", mean_spectral_contrast_performance)


print("\nENERGY ANALYSIS\n")
print("----------------------------------------------------------------")
# Energy Analysis
energy_original = librosa.feature.rms(y=y1)
energy_performance = librosa.feature.rms(y=y2)
mean_energy_original = np.mean(energy_original)
mean_energy_performance = np.mean(energy_performance)
print("Mean Energy (Original):", mean_energy_original)
print("Mean Energy (Performance):", mean_energy_performance)
v_mean_energy = v(mean_energy_original,mean_energy_performance)
x(mean_energy_original,mean_energy_performance)

#print("\nFORMANT ANALYSIS\n")
# Formant Analysis (example)
# Note: Formant analysis typically requires more specialized tools or libraries
# This is a simplified example using LPC analysis in Librosa
#formant_order = 4  # Example order for LPC analysis
#formants_original = librosa.lpc(y=y1, order=formant_order)
#formants_performance = librosa.lpc(y=y2, order=formant_order)
#print("Formants (Original):", formants_original)
#print("Formants (Performance):", formants_performance)


print("\nHARMONIC-PERCUSSIVE SOURCE SEPARATION\n")
print("----------------------------------------------------------------")
# Harmonic-Percussive Source Separation (HPSS)
y_harmonic, y_percussive = librosa.effects.hpss(y=y1)
y_harmonic_performance, y_percussive_performance = librosa.effects.hpss(y=y2)
# Example: Calculate energy of harmonic and percussive components
energy_harmonic = np.mean(librosa.feature.rms(y=y_harmonic))
energy_percussive = np.mean(librosa.feature.rms(y=y_percussive))
energy_harmonic_performance = np.mean(librosa.feature.rms(y=y_harmonic_performance))
energy_percussive_performance = np.mean(librosa.feature.rms(y=y_percussive_performance))
print("Energy Harmonic (Original):", energy_harmonic)
print("Energy Harmonic (Performance):", energy_harmonic_performance)
v_energy_harmonic = v(energy_harmonic,energy_harmonic_performance)
x(energy_harmonic,energy_harmonic_performance)
print("Energy Percussive (Original):", energy_percussive)
print("Energy Percussive (Performance):", energy_percussive_performance)
v_energy_percussive = v(energy_percussive,energy_percussive_performance)
x(energy_percussive,energy_percussive_performance)



devi = float(v_tempo) + v_zcr + v_mean_energy + v_energy_harmonic + v_energy_percussive
deviation =  devi/5
print("----------------------------------------------------------------------------------------------------------------------------------")
print(f"\nOVERALL AUDIO QUALITY  COMPARED TO THE ORIGINAL :  {abs(100 - deviation)} % \n")
print("----------------------------------------------------------------------------------------------------------------------------------")




print("\nSHOWING THE GRAPHICAL VISUAL COMPARISON\n")

# Plot comparison show
plt.figure(figsize=(14, 12))

plt.subplot(4, 2, 1)
librosa.display.waveshow(y1, sr=sr1)
plt.title(a1)
plt.xlabel('Time (seconds)')
plt.ylabel('Amplitude')

plt.subplot(4, 2, 2)
librosa.display.waveshow(y2, sr=sr2)
plt.title(a2)
plt.xlabel('Time (seconds)')
plt.ylabel('Amplitude')


plt.subplot(4, 2, 3)
librosa.display.specshow(spectral_contrast_original, x_axis='time', sr=sr1)
plt.colorbar()
plt.title('Spectral Contrast (Original)')
plt.xlabel('Time (seconds)')
plt.ylabel('Frequency Bands')

plt.subplot(4, 2, 4)
librosa.display.specshow(spectral_contrast_performance, x_axis='time', sr=sr2)
plt.colorbar()
plt.title('Spectral Contrast (Performance)')
plt.xlabel('Time (seconds)')
plt.ylabel('Frequency Bands')


# Plot MFCC, pitch, and spectral contrast
plt.subplot(4, 2, 5)
librosa.display.specshow(mfcc_original, x_axis='time', sr=sr1)
plt.colorbar()
plt.title('MFCC (Original)')
plt.xlabel('Time (seconds)')
plt.ylabel('MFCC Coefficients')

plt.subplot(4, 2, 6)
librosa.display.specshow(mfcc_performance, x_axis='time', sr=sr2)
plt.colorbar()
plt.title('MFCC (Performance)')
plt.xlabel('Time (seconds)')
plt.ylabel('MFCC Coefficients')


#voice modulation - give more weight


plt.tight_layout()
plt.show()






