# Pantry-Based Recipe Finder

A web application to find recipes based on the ingredients you have in your pantry. It supports multiple languages and helps you discover recipes you can make with available ingredients and see what you’re missing.

This project uses a multi-sheet Excel dataset with recipes containing ingredients and names in multiple languages (English, Tamil, Hindi, Malayalam, Kannada, Telugu, French, Spanish, German). It processes pantry inputs, detects language, matches recipes, and ranks them based on ingredient availability.

---

## Features

- Language-aware ingredient and recipe matching
- Multi-sheet Excel data source for recipes
- Simple and responsive web interface using Flask
- Shows available and missing ingredients for each matched recipe
- Scores and ranks recipes based on pantry coverage and missing ingredients

---

## Project Structure

pantry_recipe_finder/
├── app.py # Flask backend API and frontend server
├── pantry_matcher.py # Core pantry matching logic and data processing
├── Recipe App Dataset.xlsx # Excel dataset with recipes
├── templates/
│ └── index.html # Frontend HTML page for user interaction
└── static/
└── style.css # (Optional) CSS for styling


---

## Requirements

- Python 3.7+
- Flask
- pandas
- openpyxl

Install dependencies:

---

## How To Run

1. Place `Recipe App Dataset.xlsx` in the root project folder.
2. Run the Flask app:

python app.py


3. Open your browser and go to: http://127.0.0.1:5000/

4. Enter your pantry ingredients as comma-separated values (e.g. `tomato, water, egg`).
5. View the top matched recipes with scores, available and missing ingredients.

---

## How It Works

1. **Data Loading:** Loads recipe data with ingredient and recipe name columns for multiple languages from the Excel file.
2. **Language Detection:** Determines the input ingredient language based on Unicode blocks for proper matching.
3. **Ingredient Processing:** Cleans and tokenizes ingredient text into normalized tokens for comparison.
4. **Matching Algorithm:**  
- Builds pantry tokens from user input.  
- For each recipe (in matched language), finds ingredient intersection and missing items.  
- Calculates a score as `match_ratio - 0.1 * missing_count`.  
- Returns sorted top matches.
5. **Web Interface:** User enters pantry items; results displayed dynamically with available/missing ingredients and scores.

---

## Supported Languages and Columns

| Language | Ingredient Columns               | Recipe Name Columns                |
| -------- | -------------------------------| ---------------------------------|
| English  | `Ingredients_English`, `ingredients_en` | `Name`, `name`                  |
| Tamil    | `Ingredients_Tamil`, `ingredients_ta`   | `TamilName`, `tamilname`        |
| Hindi    | `ingredients_hn`                  | `hindiName`                      |
| Malayalam| `ingredients_kl`                  | `malayalamName`                  |
| Kannada  | `ingredients_kn`                  | `kannadaName`                   |
| Telugu   | `ingredients_te`                  | `teluguName`                    |
| French   | `ingredients_french`              | `frenchName`                    |
| Spanish  | `ingredients_spanish`             | `spanishName`                   |
| German   | `ingredients_german`              | `germanName`                    |

---

## Notes

- Make sure ingredient names supplied in the frontend match the language and form in your dataset for best results.
- Modify or extend the language columns or Unicode blocks as per your recipe dataset.
- You can customize the scoring function in `pantry_matcher.py` if needed.
- The dataset should be cleaned and structured appropriately with ingredient columns filled.

---

## Acknowledgements

- This app was built using Flask and pandas.
- Inspired by user requests for pantry-to-recipe matching functionality supporting multilingual data.
