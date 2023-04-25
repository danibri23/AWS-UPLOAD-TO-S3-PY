from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import boto3
# from dotenv import load_dotenv
# load_dotenv()


app = Flask(__name__)

s3 = boto3.client('s3')
BUCKET_NAME='mydaniaws2'


@app.route('/')  
def home():
    return render_template("index.html")
    

@app.route('/upload',methods=['post'])
def upload():
    if request.method == 'POST':
        pdf_upload = request.files['file']
        if pdf_upload:
                filename = secure_filename(pdf_upload.filename)
                pdf_upload.save(filename)
                s3.upload_file(
                    Filename=filename,
                    Bucket = BUCKET_NAME,
                    Key = 'pdf_input/'+ filename
                )
                msg = "Upload Done ! "
    return render_template("index.html",msg =msg)

if __name__ == "__main__":
    
    app.run(debug=True)