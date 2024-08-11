from flask import Flask, request, jsonify
from flask_cors import CORS
from deepface import DeepFace

app = Flask(__name__)
CORS(app)

global model_name
model_name = "Facenet"


@app.route("/")
def index():
    return jsonify("Hello, World!"), 200


@app.route("/compare", methods=["POST"])
def compare():
    if "img1" not in request.files or "img2" not in request.files:
        return jsonify({"message": "Missing images", "status_code": 400}), 400

    img1 = request.files["img1"]
    img2 = request.files["img2"]

    img1.save("temp_img1.png")
    img2.save("temp_img2.png")

    try:
        resp = DeepFace.verify(
            img1_path="temp_img1.png", img2_path="temp_img2.png", model_name=model_name
        )
        distance = resp["distance"]
        similarity_percentage = round((1 - distance) * 100, 0)

        if similarity_percentage < 50:
            verified = False
            status_code = 200
            result = {
                "verified": verified,
                "similarity_percentage": similarity_percentage,
                "status_code": status_code,
            }
        else:
            verified = True
            status_code = 200
            result = {
                "verified": verified,
                "similarity_percentage": similarity_percentage,
                "status_code": status_code,
            }

        return jsonify(result), status_code
    except Exception as e:
        status_code = 400
        result = {
            "message": "Invalid detection faces",
            "status_code": status_code,
        }
        return jsonify(result), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
