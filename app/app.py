import os
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
from cgi import escape
from flask_dropzone import Dropzone
import PyPDF2
import docx2txt
from tempfile import mkdtemp
from shutil import rmtree
import csv
from redislite import Redis

app = Flask(__name__)
redis_connection = Redis('/tmp/redis.db')

collegeDataset = open('collegeDataset.csv', 'r', encoding='utf-8', newline='\n')
collegeDatasetReader = csv.reader(collegeDataset)
collegeData = []
for row in collegeDatasetReader:
    collegeData.append(row)

app.config.update(
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_CUSTOM=True,
    DROPZONE_ALLOWED_FILE_TYPE='.pdf, .docx, .txt',
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_MAX_FILES=20,
    DROPZONE_UPLOAD_MULTIPLE = True,
)

dropzone = Dropzone(app)

# Read documents. The output of the documents is escaped with cgi.escape to prevent XSS. cgi.escape is used instead of flask.escape because flask.escape creates an HTML-safe object.
def readFile(filepath):
    extension = filepath.split('.')[1]
    file = filepath.split('.')[0]
    if extension == 'docx':
        text = docx2txt.process(filepath)
        return escape(text)
    if extension == 'pdf':
        pdfFileObj = open(filepath, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        text = ""
        for i in range(pdfReader.numPages):
            pageObj = pdfReader.getPage(i)
            text = text + pageObj.extractText()
        pdfFileObj.close()
        return escape(text)
    if extension == 'txt':
        txt = open(filepath, 'r')
        text = txt.read()
        txt.close()
        return escape(text)

def highlight(essay, collegeInfo):
    essay = essay.replace('\n', '<br>')

    notInfo = []
    checked = []
    redChecked = []
    for row in collegeData:
      for item in row:
        # Checks for info about wrong colleges. The not any() function checks if the wrong info is inside the right info (i.e. Georgia in Georgia Tech shouldn't be red)
        if (item not in collegeInfo) and (item not in checked) and (not any(item in s for s in collegeInfo)):
            notInfo.append(item)

    for item in sorted(notInfo, key=len, reverse=True):
        if item not in redChecked:
            essay = essay.replace(item, '<span style="background-color: #FD6164">' + item + '</span>')
            redChecked.append(item)
            # Check for singular form of team name. Wolverines --> Wolverine
            if item[-1] == "s" and item[0:-1] not in checked and (not any(item[0:-1] in s for s in collegeInfo)):
                essay = essay.replace(item[0:-1], '<span style="background-color: #FD6164">' + item[0:-1] + '</span>')


    for item in sorted(collegeInfo, key=len, reverse=True):
        if item not in checked:
            essay = essay.replace(item, '<span style="background-color: #89c057">' + item + '</span>')
            checked.append(item)
            if item[-1] == "s" and item[0:-1] not in checked:
                essay = essay.replace(item[0:-1], '<span style="background-color: #89c057">' + item[0:-1] + '</span>')

    return(essay)

@app.route('/form', methods=['POST'])
def handle_form():
    collegeName = request.form.get('selector')
    redis_connection.set('collegeName', collegeName)
    for row in collegeData:
        if row[0] == collegeName:
            for i in row:
                redis_connection.lpush('collegeInfo', i)

    return '', 204

@app.route('/', methods=['POST', 'GET'])
def upload():
    tempdir = mkdtemp()
    fileList = {}
    if request.method == 'POST':
        for key, f in request.files.items():
            if key.startswith('file'):
                filepath = os.path.join(tempdir, secure_filename(f.filename))
                f.save(filepath)
                print(filepath)
                print(readFile(filepath))
                fileList[escape(f.filename)] = readFile(filepath)
        redis_connection.hmset('fileList', fileList)
    else:
        fileList = {}
    rmtree(tempdir)
    return render_template('index.html')

@app.route('/completed')
def completed():
    print(redis_connection.keys())
    keys = [b'fileList', b'collegeInfo', b'collegeName']
    for key in keys:
        if key not in redis_connection.keys():
            return redirect("/")

    collegeInfo = []
    while(redis_connection.llen('collegeInfo')!=0):
        collegeInfo.append(redis_connection.lpop('collegeInfo').decode('utf-8'))

    collegeName = redis_connection.get('collegeName').decode('utf-8')

    fileList = {}
    for fileName, essay in redis_connection.hgetall("fileList").items():
        fileList[fileName.decode('utf-8')] = highlight(essay.decode('utf-8'),collegeInfo)

    print(collegeName, collegeInfo)
    redis_connection.flushall()

    return render_template('results.html', fileList=fileList, title=collegeName)


if __name__ == '__main__':
    app.run(debug=True)
