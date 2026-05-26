from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename


app = Flask(__name__)

# 4MB Limit
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST' and 'file' in request.files:
        f = request.files['file']

        #only allow .pdf
        if f.filename.endswith('.pdf'):

            filename = secure_filename(f.filename)

#            Upload saved to "uploads" folder in 'static'
            f.save("static/uploads/" + filename)
#            Display the filename and that it has been uploaded sucessfully
            return f'File "{filename}" uploaded successfully.'
#            Else display "only pdf files accepted"        
        else: 
            return "Only PDF files allowed.."
  

if __name__ == '__main__':
    app.run(debug=True)