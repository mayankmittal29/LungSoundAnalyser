from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
from flask import send_file
app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'
class UploadFileForm(FlaskForm):
    file = FileField("WAV File", validators=[InputRequired()])
    submit = SubmitField("Upload File")


@app.route('/', methods=['GET',"POST"])
@app.route('/home', methods=['GET',"POST"])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)
        file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return send_file(file_path, as_attachment=True)
    return render_template('main.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)

# from flask import Flask, render_template, jsonify
# from flask_wtf import FlaskForm
# from wtforms import FileField, SubmitField
# from werkzeug.utils import secure_filename
# import os
# from wtforms.validators import InputRequired
# from flask import send_file

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
#     if form.validate_on_submit():
#         file = form.file.data
#         filename = secure_filename(file.filename)
#         file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], filename)
#         file.save(file_path)

#         # Trigger the file download using JavaScript
#         return render_template('index.html', form=form, filename=filename, js_download=True)

#     return render_template('index.html', form=form)

# @app.route('/download/<filename>')
# def download_file(filename):
#     file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#     return send_file(file_path, as_attachment=True)

# if __name__ == '__main__':
#     app.run(debug=True)








# from flask import Flask, render_template, send_file
# from flask_wtf import FlaskForm
# from wtforms import FileField, SubmitField
# from werkzeug.utils import secure_filename
# import os
# from wtforms.validators import InputRequired

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'supersecretkey'
# app.config['UPLOAD_FOLDER'] = 'static/files'

# # Check if the UPLOAD_FOLDER exists, and create it if it doesn't
# if not os.path.exists(app.config['UPLOAD_FOLDER']):
#     os.makedirs(app.config['UPLOAD_FOLDER'])

# class UploadFileForm(FlaskForm):
#     file = FileField("WAV File", validators=[InputRequired()])
#     submit = SubmitField("Upload File")

# @app.route('/', methods=['GET', 'POST'])
# @app.route('/home', methods=['GET', 'POST'])
# def home():
#     form = UploadFileForm()
#     success_message = None

#     if form.validate_on_submit():
#         file = form.file.data
#         filename = secure_filename(file.filename)
#         file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], filename)
#         file.save(file_path)
#         success_message = f"File '{filename}' uploaded and downloaded successfully."

#     return render_template('tempclassifi.html', form=form, success_message=success_message)

# if __name__ == '__main__':
#     app.run(debug=True,port=5500)



# from flask import Flask, render_template, send_file
# from flask_wtf import FlaskForm
# from wtforms import FileField, SubmitField
# from werkzeug.utils import secure_filename
# import os
# from wtforms.validators import InputRequired
# from flask import send_file

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'supersecretkey'
# app.config['UPLOAD_FOLDER'] = 'static/files'

# # # Check if the UPLOAD_FOLDER exists, and create it if it doesn't
# # if not os.path.exists(app.config['UPLOAD_FOLDER']):
# #     os.makedirs(app.config['UPLOAD_FOLDER'])

# class UploadFileForm(FlaskForm):
#     file = FileField("WAV File", validators=[InputRequired()])
#     submit = SubmitField("Upload File")

# # @app.route('/', methods=['GET', 'POST'])
# # @app.route('/home', methods=['GET', 'POST'])
# # def home():
# #     form = UploadFileForm()
# #     success_message = None

# #     if form.validate_on_submit():
# #         file = form.file.data
# #         filename = secure_filename(file.filename)
# #         file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], filename)
# #         file.save(file_path)
# #         success_message = f"File '{filename}' uploaded and downloaded successfully."

#     return render_template('tempclassifi.html', form=form, success_message=success_message)

# if __name__ == '__main__':
#     app.run(debug=True)
