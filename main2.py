# from flask import Flask, render_template, request
# from flask_wtf import FlaskForm
# from wtforms import FileField, SubmitField
# from werkzeug.utils import secure_filename
# import os
# from wtforms.validators import InputRequired

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'supersecretkey'
# app.config['UPLOAD_FOLDER'] = 'static/files'

# class UploadFileForm(FlaskForm):
#     file = FileField("WAV File", validators=[InputRequired()])
#     submit = SubmitField("Upload File")

# @app.route('/', methods=['GET', 'POST'])
# @app.route('/home', methods=['GET', 'POST'])
# def home():
#     form = UploadFileForm()
#     filename = None
#     message = None

#     if form.validate_on_submit():
#         file = form.file.data
#         filename = secure_filename(file.filename)
#         file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], filename)
#         file.save(file_path)
#         message = "File is uploaded!"

#     return render_template('index.html', form=form, filename=filename, message=message)

# if __name__ == '__main__':
#     app.run(debug=True)

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import spectrogram
from flask import Flask, render_template
from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps 
from wtforms.validators import InputRequired
from flask import send_file
import wave
import numpy as np
import scipy.signal as signal
from flask import request
from pydub import AudioSegment
import librosa
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import InputRequired
class PatientDetailsForm(FlaskForm):
    patientName = StringField('Name', validators=[InputRequired()])
    patientAge = StringField('Age', validators=[InputRequired()])
    patientGender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
                                validators=[InputRequired()])
    patientMobile = StringField('Mobile Number', validators=[InputRequired()])
    patientAddress = TextAreaField('Address', validators=[InputRequired()])
    submit = SubmitField('Submit')
def generate_mel_spectrogram_and_save(audio_file_path, output_folder='./static'):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Load audio file and its sample rate using librosa
    audio_samples, sample_rate = librosa.load(audio_file_path, sr=None)

    # Calculate the Mel spectrogram
    mel_spectrogram = librosa.feature.melspectrogram(y=audio_samples, sr=sample_rate)
    
    # Convert the power spectrogram to decibels
    mel_spectrogram_db = librosa.power_to_db(mel_spectrogram, ref=np.max)

    # Save the Mel spectrogram as an image
    spectrogram_image_path = os.path.join(output_folder, 'mel_spectrogram.png')
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(mel_spectrogram_db, x_axis='time', y_axis='mel')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Mel Spectrogram')
    plt.savefig(spectrogram_image_path)
    plt.close()

    return spectrogram_image_path 
def plot_waveform(audio_data, sample_rate, output_image_path):
    duration = len(audio_data) / sample_rate
    time = np.linspace(0., duration, len(audio_data))
    plt.figure(figsize=(12, 4))
    plt.plot(time, audio_data, lw=1)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.title("Waveform")
    plt.tight_layout()
    
    # Save the waveform plot as an image in the specified directory
    plt.savefig(output_image_path)
    plt.close()
def denoise_lung_sounds(input_file, output_file, lowcut, highcut, sample_rate=44100):
    # Read the input WAV file
    input_wav = wave.open(input_file, 'rb')
    rate = input_wav.getframerate()
    n_channels = input_wav.getnchannels()
    sample_width = input_wav.getsampwidth()
    frames = input_wav.getnframes()
    data = np.frombuffer(input_wav.readframes(frames), dtype=np.int16)
    input_wav.close()

    # Design bandpass filter
    nyquist = 0.5 * sample_rate
    low = (lowcut - 10) / nyquist
    high = (highcut + 10) / nyquist
    order = 3
    b, a = signal.butter(order, [low, high], btype='band')
    
    # Apply bandpass filter to the data
    filtered_data = signal.filtfilt(b, a, data)
    
    # Save the filtered audio to a new WAV file using wave module
    output_wav = wave.open(output_file, 'wb')
    output_wav.setnchannels(1)  # Assuming mono audio
    output_wav.setsampwidth(sample_width)
    output_wav.setframerate(rate)
    output_wav.writeframes(filtered_data.astype('int16').tobytes())
    output_wav.close()
    print("OK")
def generate_amplitude_time_graph(file_path, image_path):
    # Read the .wav file
    sample_rate, data = wavfile.read(file_path)

    # Calculate time array for x-axis
    duration = len(data) / sample_rate  # Calculate the duration of the audio in seconds
    time = np.linspace(0, duration, len(data))  # Create time array corresponding to the audio data

    # Plot amplitude vs. time
    plt.figure(figsize=(10, 5))
    plt.plot(time, data, color='blue')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.title('Amplitude vs. Time Graph')
    plt.grid(True)
    plt.tight_layout()

    # Save the generated amplitude vs. time graph
    output_image_path = image_path  # Set the output image path
    plt.savefig(output_image_path)
    plt.close()
    
    return output_image_path
app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'

class UploadFileForm(FlaskForm):
    file = FileField("WAV File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = UploadFileForm()
    patient_form = PatientDetailsForm()  # Create an instance of the patient details form
    filename = None

    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)
        file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        send_file(file_path, as_attachment=True)
        denoise_lung_sounds(file_path,"./static/output.wav",100,800)
        audio = AudioSegment.from_wav(file_path)
        sample_rate = audio.frame_rate
        audio_data = np.array(audio.get_array_of_samples())
        plot_waveform(audio_data, sample_rate,"./static/image1.png")
        audio = AudioSegment.from_wav("./static/output.wav")
        sample_rate = audio.frame_rate
        audio_data = np.array(audio.get_array_of_samples())
        plot_waveform(audio_data, sample_rate,"./static/image2.png")
        # return redirect(url_for('success', output_location="./static/output.wav", input_file_path=file_path))
        return redirect(url_for('result',
                                patient_name=patient_form.patientName.data,
                                patient_age=patient_form.patientAge.data,
                                patient_gender=patient_form.patientGender.data,
                                patient_mobile=patient_form.patientMobile.data,
                                patient_address=patient_form.patientAddress.data,
                                output_location="./static/output.wav",
                                input_file_path=file_path))
    
    return render_template('main.html', form=form,patient_form=patient_form, filename=filename)
results = []
@app.route('/success')
def success():
    # Retrieve the arguments sent to the 'success' endpoint
    output_location = request.args.get('output_location', default='Not specified')
    input_file_path = request.args.get('output_file_path', default='Not specified')
    imageinputpath = "./static/image1.png"
    imageoutpupath = "./static/image2.png"
    return render_template('display_images.html', input_image=imageinputpath, output_image=imageoutpupath)
# @app.route('/gotomainpage', methods=['POST'])
# def go_to_generate():
#     return render_template('/main.html')
@app.route('/process_ml', methods=['GET'])
@app.route('/process_multiple_ml', methods=['GET'])
def process_multiple_ml():
    np.set_printoptions(suppress=True)
    
    # Load the model
    model = load_model("./static/keras_model.h5", compile=False)
    
    # Load the labels
    class_names = open("./static/labels.txt", "r").readlines()
    
    ml_folder = "./static/ML"
    
    for filename in os.listdir(ml_folder):
        if filename.endswith(".png"):
            image_path = os.path.join(ml_folder, filename)
            
            # Load and preprocess the image
            image = Image.open(image_path).convert("RGB")
            size = (224, 224)
            image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
            image_array = np.asarray(image)
            normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
            
            # Create the array of the right shape to feed into the keras model
            data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
            data[0] = normalized_image_array
            
            # Predict using the model
            prediction = model.predict(data)
            index = np.argmax(prediction)
            class_name = class_names[index].strip()  # Remove newline characters from class name
            # confidence_score = prediction[0][index]
            
            # Append results to a list
            results.append({
                'image_path': image_path,
                'class_name': class_name,
                # 'confidence_score': confidence_score
            })

    return render_template('result.html', results=results)
@app.route('/result', methods=['GET', 'POST'])
def result():

    # Retrieve patient details from the URL parameters
    patient_name = request.form.get('patientName', default='Not specified')
    patient_age = request.form.get('patientAge', default='Not specified')
    patient_gender = request.form.get('patientGender', default='Not specified')
    patient_mobile = request.form.get('patientMobile', default='Not specified')
    patient_address = request.form.get('patientAddress', default='Not specified')
     # Retrieve the uploaded file
    uploaded_file = request.files['fileToUpload']

    # Save the file to the current folder
    file_name = uploaded_file.filename
    file_path = os.path.join('./static/files', file_name)
    uploaded_file.save(file_path)
    # send_file(uploaded_file, as_attachment=True)
    denoise_lung_sounds(file_path,"./static/output.wav",100,800)
    audio = AudioSegment.from_wav(file_path)
    sample_rate = audio.frame_rate
    audio_data = np.array(audio.get_array_of_samples())
    plot_waveform(audio_data, sample_rate,"./static/image1.png")
    audio = AudioSegment.from_wav("./static/output.wav")
    sample_rate = audio.frame_rate
    audio_data = np.array(audio.get_array_of_samples())
    plot_waveform(audio_data, sample_rate,"./static/image2.png")
    imageinputpath = "./static/image1.png"
    imageoutputpath = "./static/image2.png"
    # ... (existing code to retrieve other parameters)

    return render_template('result.html',
                           patient_name=patient_name,
                           patient_age=patient_age,
                           patient_gender=patient_gender,
                           patient_mobile=patient_mobile,
                           patient_address=patient_address,
                           input_image=imageinputpath,
                           output_image=imageoutputpath,
                           input_audio_file_path = file_path
                           )
if __name__ == '__main__':
    app.run(debug=True,port=8332)
