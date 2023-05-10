from flask import Flask, request, render_template, request
from dotenv import load_dotenv
import boto3
from botocore.exceptions import WaiterError
from werkzeug.utils import secure_filename
import os

load_dotenv()

app = Flask(__name__)

s3 = boto3.client('s3')
BUCKET_NAME = os.environ["BUCKET_NAME"]
FOLDER_NAME_UPLOAD = os.environ["FOLDER_NAME_UPLOAD"]
FOLDER_NAME_DOWNLOAD = os.environ["FOLDER_NAME_DOWNLOAD"]
generated_filename = None

@app.route('/')  
def home():
    return render_template("index.html")
    
@app.route('/upload', methods=['POST'])
def upload():
    global generated_filename
    if request.method == 'POST':
        pdf_upload = request.files['file']
        if pdf_upload:
            filename = secure_filename(pdf_upload.filename)
            s3.upload_fileobj(
                Fileobj=pdf_upload,
                Bucket=BUCKET_NAME,
                Key=FOLDER_NAME_UPLOAD + '/' + filename
            )
            # Esperar a que el archivo TXT esté disponible en el bucket de salida
            txt_filename = os.path.splitext(filename)[0] + '.txt'
            waiter = s3.get_waiter('object_exists')
            try:
                waiter.wait(Bucket=BUCKET_NAME, Key=FOLDER_NAME_DOWNLOAD + '/' + txt_filename)
                msg = "Upload and processing done ! "
                generated_filename = txt_filename
            except WaiterError:
                msg = "Error: Timeout waiting for TXT file to be available"
    return render_template("index.html", msg=msg)

@app.route('/download')
def download_file():
    try:
        if generated_filename:
            s3.download_file(BUCKET_NAME, FOLDER_NAME_DOWNLOAD + '/' + generated_filename, generated_filename)
            return 'File downloaded successfully'
        else:
            return 'No file has been uploaded yet'
    except NoCredentialsError:
        return 'Error: Invalid AWS credentials'
    except Exception as e:
        return f'Error: {e}'


if __name__ == "__main__":
    app.run(debug=True)