
from flask import Flask, request, send_file, render_template, jsonify
import io
from PIL import Image, ImageFilter, ImageEnhance, ImageOps, ImageDraw
import os
import tempfile  
from tkinter import Tk, Canvas, Button, NW, filedialog
from PIL import Image, ImageTk
import base64
from io import BytesIO



# Starting the app
app = Flask(__name__)

uploaded_image = None

@app.route('/')
def index():
    return render_template('index1.html', uploaded_image=uploaded_image)

@app.route('/upload', methods=['POST','GET'])
def upload_image():
    global uploaded_image
    img = request.files['image']
    uploaded_image = img.read()  # Store the image data
    
    # Convert the image to JPEG format
    img_pil = Image.open(io.BytesIO(uploaded_image))
    img_pil = img_pil.convert("RGB")  # Convert to RGB format (required for JPEG)
    
    # Save the image as JPEG
    with io.BytesIO() as output:
        img_pil.save(output, format="JPEG")
        jpeg_data = output.getvalue()
    
    encoded_image = base64.b64encode(jpeg_data).decode('utf-8')
    
    return render_template('index1.html', uploaded_image=encoded_image)
    

@app.route('/crop', methods=['POST'])
def crop_image():
    global uploaded_image
    crop_type = request.form['crop_type']
    img = Image.open(io.BytesIO(uploaded_image))
    img = img.convert("RGB")

    if crop_type == 'JEE':
        img = img.resize((350, 450))
        img_io = io.BytesIO()
        img.save(img_io, format='JPEG', quality=95)
        img_io.seek(0)
        return send_file(img_io, mimetype='image/jpeg')
    elif crop_type == 'NEET':
        img = img.resize((1000, 1500))
        img_io = io.BytesIO()
        img.save(img_io, format='JPEG', quality=95)
        img_io.seek(0)
        return send_file(img_io, mimetype='image/jpeg')
    elif crop_type == 'Aadhaar':
        img = img.resize((350, 450))
        img_io = io.BytesIO()
        img.save(img_io, format='JPEG', quality=95)
        img_io.seek(0)
        return send_file(img_io, mimetype='image/jpeg')
    elif crop_type == 'PAN':
        img = img.resize((350, 250))
        img_io = io.BytesIO()
        img.save(img_io, format='JPEG', quality=95)
        img_io.seek(0)
        return send_file(img_io, mimetype='image/jpeg')

@app.route("/rotate", methods=["POST"])
def rotate_image():
    global uploaded_image
    rotation_angle = int(request.form["rotation_angle"])
    image = Image.open(io.BytesIO(uploaded_image))
    rotated_image = image.rotate(rotation_angle, expand=True)
    img_io = io.BytesIO()
    rotated_image.save(img_io, format='PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

@app.route("/flip", methods=["POST"])
def flip_image():
    global uploaded_image
    flip_type = request.form["flip_type"]
    image = Image.open(io.BytesIO(uploaded_image))
    if flip_type == "Horizontal":
        flipped_image = image.transpose(Image.FLIP_LEFT_RIGHT)
    elif flip_type == "Vertical":
        flipped_image = image.transpose(Image.FLIP_TOP_BOTTOM)
    img_io = io.BytesIO()
    flipped_image.save(img_io, format='PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

@app.route("/blur", methods=["POST"])
def apply_blur():
    global uploaded_image
    blur_type = request.form["blur_type"]
    image = Image.open(io.BytesIO(uploaded_image))
    if blur_type == "BoxBlur":
        modified_image = image.filter(ImageFilter.BoxBlur(5))
    elif blur_type == "NormalBlur":
        modified_image = image.filter(ImageFilter.BLUR)
    img_io = io.BytesIO()
    modified_image.save(img_io, format='PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

@app.route("/contrast", methods=["POST"])
def adjust_contrast():
    global uploaded_image
    contrast_factor = float(request.form["contrast_factor"])
    image = Image.open(io.BytesIO(uploaded_image))
    enhancer = ImageEnhance.Contrast(image)
    modified_image = enhancer.enhance(contrast_factor)
    img_io = io.BytesIO()
    modified_image.save(img_io, format='PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

@app.route('/bright', methods=['POST'])
def adjust_brightness():
    global uploaded_image

    # Retrieve brightness level from form
    brightness = float(request.form['brightness'])  # Corrected to 'brightness' instead of 'brightness_factor'
    
    # Open the uploaded image using PIL
    img = Image.open(io.BytesIO(uploaded_image))
    
    # Adjust the brightness of the image
    enhancer = ImageEnhance.Brightness(img)
    modified_image = enhancer.enhance(brightness)
    
    # Save the modified image to a byte stream
    img_io = io.BytesIO()
    modified_image.save(img_io, format='JPEG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')
    
    # Encode the modified image as base64
    # modified_image_data = base64.b64encode(img_io.getvalue()).decode()
    
    # # Encode the original image as base64
    # original_img_io = io.BytesIO(uploaded_image)
    # original_image_data = base64.b64encode(original_img_io.getvalue()).decode()
    
    # # Return the modified image data and original image data as JSON response
    # return jsonify({'img_data': modified_image_data, 'orig_img_data': original_image_data})

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")
@app.route("/home")
def home() :
    return render_template("index1.html")

if __name__ == "__main__":
    app.run(debug=True)







