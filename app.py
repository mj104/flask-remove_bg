from flask import Flask, request, jsonify, url_for, render_template
from rembg import remove
import os
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = 'static'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image = request.files['image']

    try:
        input_data = image.read()
        output_data = remove(input_data)

        # Save file
        filename = f'removed_{datetime.now().strftime("%Y%m%d%H%M%S")}.png'
        output_path = os.path.join(UPLOAD_FOLDER, filename)

        with open(output_path, 'wb') as f:
            f.write(output_data)

        # Return image URL
        image_url = url_for('static', filename=filename, _external=True)
        return jsonify({"image_url": image_url})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
