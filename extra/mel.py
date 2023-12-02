# import librosa
# import librosa.display
# import matplotlib.pyplot as plt

# def plot_mel_spectrogram(audio_path, save_path=None):
#     # Load audio file
#     y, sr = librosa.load(audio_path, sr=None)

#     # Generate Mel spectrogram
#     mel_spectrogram = librosa.feature.melspectrogram(y, sr=sr, n_fft=2048, hop_length=512, n_mels=128)

#     # Convert to decibels
#     mel_spectrogram_db = librosa.amplitude_to_db(mel_spectrogram, ref=np.max)

#     # Plot the Mel spectrogram
#     plt.figure(figsize=(10, 5))
#     librosa.display.specshow(mel_spectrogram_db, x_axis='time', y_axis='mel', sr=sr, hop_length=512, cmap='viridis')
#     plt.colorbar(format='%+2.0f dB')
#     plt.title('Mel Spectrogram')
#     plt.xlabel('Time (s)')
#     plt.ylabel('Frequency (Hz)')

#     # Save the plot if a save_path is provided
#     if save_path:
#         plt.savefig(save_path, bbox_inches='tight')

#     # Display the plot
#     plt.show()

# # Example usage
# input_audio_file = '/home/mayank/Monke/wheeze.wav'
# output_plot_path = '/home/mayank/Monke/plot.png'
# plot_mel_spectrogram(input_audio_file, save_path=output_plot_path)

import numpy as np
import librosa
import matplotlib.pyplot as plt

def plot_amplitude_vs_time(audio_path, save_path=None):
    # Load audio file
    y, sr = librosa.load(audio_path, sr=None)

    # Calculate time values
    time = np.arange(0, len(y)) / sr

    # Plot amplitude vs time
    plt.figure(figsize=(10, 4))
    plt.plot(time, y, color='b')
    plt.title('Amplitude vs Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.grid(True)

    # Save the plot if a save_path is provided
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')

    # Display the plot
    plt.show()

# Example usage
input_audio_file = '/home/mayank/Monke/wheeze.wav'  # Adjust the file path if needed
output_plot_path = '/home/mayank/Monke/plot.png'  # Adjust the output plot path if needed
plot_amplitude_vs_time(input_audio_file, save_path=output_plot_path)
