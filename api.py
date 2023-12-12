from flask import Flask, jsonify

app = Flask(__name__)

# Load the generated URLs from the JSON file
with open("generated_urls.json", "r") as json_file:
    generated_urls = json.load(json_file)


# Flask route to serve the generated URLs
@app.route('/api/generated_urls', methods=['GET'])
def get_generated_urls():
    return "My Api Route"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

