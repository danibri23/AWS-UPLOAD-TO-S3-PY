from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import boto3
import os
load_dotenv()


app = Flask(__name__)

s3 = boto3.client('s3',
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                aws_session_token=os.getenv('AWS_DEFAULT_REGION')
                    )
BUCKET_NAME='mydaniaws2'


@app.route('/')  
def home():
    return render_template("index.html")
    

@app.route('/upload',methods=['post'])
def upload():
    if request.method == 'POST':
        img = request.files['file']
        if img:
                filename = secure_filename(img.filename)
                img.save(filename)
                s3.upload_file(
                    Filename=filename,
                    Bucket = BUCKET_NAME,
                    Key = filename
                )
                msg = "Upload Done ! "
    return render_template("index.html",msg =msg)

if __name__ == "__main__":
    
    app.run(debug=True)