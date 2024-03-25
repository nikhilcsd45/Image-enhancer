from flask import Flask, request, send_file, render_template, jsonify, flash, redirect
import io
from PIL import Image, ImageFilter, ImageEnhance
import base64

# Starting the app
app = Flask(__name__)

uploaded_image = None

# Render index page
@app.route('/', methods=['GET', 'POST'])
def index():
    global uploaded_image
    
    # Check if an image is uploaded
    if request.method == 'POST' and 'image' in request.files:
        file = request.files['image']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({'error': 'No selected file'})
        
        # Read the uploaded image and store it
        uploaded_image = file.read()
    
    # Convert the uploaded image to base64 encoding if available
    encoded_image = base64.b64encode(uploaded_image).decode('utf-8') if uploaded_image else ""
    
    # Render the template with the uploaded image
    return render_template('index1.html', uploaded_image=encoded_image)

# Upload image route
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

# Crop image route
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

# Rotate image route
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

# Flip image route
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

# Apply blur route
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

# Adjust contrast route
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

# Adjust brightness route
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

# About route
@app.route("/about")
def about():
    return render_template("about.html")

# Contact route
@app.route("/contact")
def contact():
    return render_template("contact.html")

# Home route
@app.route("/home")
def home():
    return render_template("index1.html")

if __name__ == "__main__":
    app.run(debug=True)
