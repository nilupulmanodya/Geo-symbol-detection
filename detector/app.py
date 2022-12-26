import torch
import cv2
import io
import shutil
import os
# from wsgiref.simple_server import make_server
from flask import Flask, render_template, request, Markup, redirect
from PIL import Image

#loading trained model
model = torch.hub.load('ultralytics/yolov5','custom','models/best.pt')
UPLOAD_FOLDER = './upload'
RESULT_FOLDER = './static/images/results/0'


def predict_image(im_name):
    print('im_name',im_name)
    #os.remove(RESULT_FOLDER)
    shutil.rmtree(RESULT_FOLDER)
    img = Image.open(UPLOAD_FOLDER+'/'+im_name)
    results = model(img)
    results.print()
    print('results',results.xyxy[0])  # im predictions (tensor)
    print('results pandas',results.pandas().xyxy[0])  # im predictions (pandas)
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], im_name)) # deleting uploaded file if prediction success
    results.save(save_dir=RESULT_FOLDER)
    printRes = results.pandas().xyxy[0]

    LenRes = len(printRes)
    return im_name, printRes, LenRes
    

# def getTableData()


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER




#render prediction results page
@ app.route('/predictions')
def paperChartPredictions():
    title = 'Paper Chart Detector - Predictions'
    return render_template('results.html', title=title)


@app.route('/', methods=['GET', 'POST'])
def disease_prediction():
    title = 'Paper Chart Detector - Predictions'

    if request.method == 'POST':
        print('post')
        print(request.args)
        print(request.files)
        if 'file' not in request.files:
            print('no file in requiests')
            #return redirect(request.url)


        if 'file' not in request.files:
            print('there is no file1 in form!')
            return render_template('home.html', title=title)
        file1 = request.files['file']
        path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        file1.save(path)
            
        try:
            result_img, printRes, LenRes = predict_image(file1.filename)
            # print(result_img)
            return render_template('results.html', result_img=result_img, printRes= printRes, title=title, LenRes=LenRes)
        except Exception as e :
            print('tried not success', e)
            pass
    return render_template('home.html', title=title)
