import requests
import numpy as np
import scipy.io.wavfile as wav
from scipy.signal import butter, filtfilt
CHANNEL_ID = '2267841'  
READ_API_KEY = 'QG66B54E37LPZ9WZ'
url = f'https://api.thingspeak.com/channels/{CHANNEL_ID}/fields/4.json?api_key={READ_API_KEY}'
response = requests.get(url)
data = response.json()
time_values = []
intensity_values = []
for entry in data['feeds']:
    intensity = entry.get('field4')
    if intensity is not None:
        try:
            intensity = float(intensity)
            time_values.append(entry['created_at'])
            intensity_values.append(intensity)
        except ValueError:
            print(f"Skipping non-numeric value: {entry['field4']}")

if not intensity_values:
    print("No valid intensity values found in the data.")
else:
    sample_rate = 44100 
    duration = 10 
    normalized_intensity = np.array(intensity_values) / np.max(np.abs(intensity_values))
    lowcut = 20  
    highcut = 1000 
    nyquist = 0.5 * sample_rate
    low = lowcut / nyquist
    high = highcut / nyquist
    order = 6 
    b, a = butter(order, [low, high], btype='band')
    filtered_intensity = filtfilt(b, a, normalized_intensity)
    num_samples = int(duration * sample_rate)
    filtered_intensity = np.resize(filtered_intensity, num_samples)
    audio_waveform = np.int16(filtered_intensity * 32767)
    wav.write('output_audio.wav', sample_rate, audio_waveform)


