from flask import Flask, request, render_template, jsonify
from pantry_matcher import load_recipe_data_per_language, match_recipes_per_language

app = Flask(__name__)

DATA_FILE = "Recipe App Dataset.xlsx"
recipes = load_recipe_data_per_language(DATA_FILE)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/match", methods=["POST"])
def match():
    data = request.get_json()
    pantry_input = data.get("ingredients", "")
    pantry_list = [i.strip() for i in pantry_input.split(',') if i.strip()]
    if not pantry_list:
        return jsonify({"error": "No ingredients provided."}), 400
    matches = match_recipes_per_language(pantry_list, recipes)
    return jsonify(matches[:10])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
