from flask import Flask, request, Response, jsonify, render_template, send_file, make_response
from hide_plate import hide_image_plate
import numpy as np
from PIL import Image
import cv2

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


# No caching at all for API endpoints.
@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

@app.route("/")
def index():
    return render_template('index.html', title="home", username=None)

@app.route("/api/hide", methods=["POST"])
def post_api_hide():
    file = request.files['image']
    image = Image.open(file.stream)
    # process the image
    hide_image_plate(image)
    # build a response dict to send back to client
    return send_file('static/results/result.jpg', mimetype="image/jpg"), 200

@app.route("/hide", methods=["POST"])
def post_hide():
    file = request.files['image']
    image = Image.open(file.stream)
    # process the image
    hide_image_plate(image)
    # build a response dict to send back to client
    return render_template('result.html')

# Run flask app
app.run(host="0.0.0.0", port=5000)