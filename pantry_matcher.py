import pandas as pd
import re

LANG_DATA = [
    {'code': 'en', 'ingredient_cols': ['Ingredients_English', 'ingredients_en'], 'name_cols': ['Name', 'name']},
    {'code': 'ta', 'ingredient_cols': ['Ingredients_Tamil', 'ingredients_ta'], 'name_cols': ['TamilName', 'tamilname']},
    {'code': 'hn', 'ingredient_cols': ['ingredients_hn'], 'name_cols': ['hindiName']},
    {'code': 'kl', 'ingredient_cols': ['ingredients_kl'], 'name_cols': ['malayalamName']},
    {'code': 'kn', 'ingredient_cols': ['ingredients_kn'], 'name_cols': ['kannadaName']},
    {'code': 'te', 'ingredient_cols': ['ingredients_te'], 'name_cols': ['teluguName']},
    {'code': 'french', 'ingredient_cols': ['ingredients_french'], 'name_cols': ['frenchName']},
    {'code': 'spanish', 'ingredient_cols': ['ingredients_spanish'], 'name_cols': ['spanishName']},
    {'code': 'german', 'ingredient_cols': ['ingredients_german'], 'name_cols': ['germanName']},
]

LANG_UNICODE_RANGES = {
    'ta': (0x0B80, 0x0BFF),
    'hn': (0x0900, 0x097F),
    'kl': (0x0D00, 0x0D7F),
    'kn': (0x0C80, 0x0CFF),
    'te': (0x0C00, 0x0C7F),
    'en': (0x0000, 0x007F),
}

def detect_language_of_text(text):
    for lang, (start, end) in LANG_UNICODE_RANGES.items():
        for char in text:
            if start <= ord(char) <= end:
                return lang
    return 'en'

def clean_for_match(text):
    text = re.sub(r'\([^)]*\)', '', text)
    text = re.sub(r'\d+', '', text)
    units = [
        'cup', 'cups', 'tbsp', 'tablespoon', 'tablespoons', 'tsp', 'teaspoon',
        'teaspoons', 'kg', 'g', 'grams', 'ml', 'ltr', 'spoon', 'oz', 'lb', 'lbs',
        'ஸ்பூன்', 'கப்', 'கிலோ', 'ഗ്രാം', 'കപ്പ്', 'चम्मच', 'కప్పు', 'स्पून', 'कप'
    ]
    for u in units:
        text = text.replace(u, '')
    return text.strip(' .,-')

def tokenize_ingredient(item):
    item = clean_for_match(item)
    tokens = re.split(r'[\s,;-]+', item)
    return set([t for t in tokens if t])

def preprocess_ingredient_line(text):
    if pd.isna(text):
        return []
    items = [i.strip().lower() for i in re.split(r',|\n', str(text)) if i.strip()]
    return items

def load_recipe_data_per_language(excel_path):
    xls = pd.ExcelFile(excel_path)
    all_recipes = []
    for sheet in xls.sheet_names:
        df = pd.read_excel(excel_path, sheet_name=sheet)
        for lang in LANG_DATA:
            name_col = None
            for nc in lang['name_cols']:
                if nc in df.columns:
                    name_col = nc
                    break
            ing_col = None
            for ic in lang['ingredient_cols']:
                if ic in df.columns:
                    ing_col = ic
                    break
            if not name_col or not ing_col:
                continue
            for _, row in df.iterrows():
                recipe_name = row.get(name_col)
                ing_list = preprocess_ingredient_line(row.get(ing_col, ""))
                if recipe_name and ing_list:
                    tokens = set()
                    for i in ing_list:
                        tokens.update(tokenize_ingredient(i))
                    all_recipes.append({
                        'sheet': sheet,
                        'lang': lang['code'],
                        'recipe_name': recipe_name,
                        'ingredients': tokens
                    })
    print(f"Loaded {len(all_recipes)} recipes with per-language separation.")
    return all_recipes

def match_recipes_per_language(pantry_list, recipes):
    lang_to_pantry = {}
    for item in pantry_list:
        lang = detect_language_of_text(item)
        lang_to_pantry.setdefault(lang, []).append(item)

    results = []
    for lang, pantry_items in lang_to_pantry.items():
        pantry_tokens = set()
        for item in pantry_items:
            pantry_tokens |= tokenize_ingredient(item)
        for rec in recipes:
            if rec['lang'] != lang:
                continue
            available = pantry_tokens & rec['ingredients']
            missing = rec['ingredients'] - pantry_tokens
            match_ratio = len(available) / len(rec['ingredients']) if rec['ingredients'] else 0
            score = match_ratio - 0.1 * len(missing)
            results.append({
                'recipe_name': rec['recipe_name'],
                'cuisine': rec['sheet'],
                'lang': lang,
                'available_ingredients': sorted(available),
                'missing_ingredients': sorted(missing),
                'match_ratio': round(match_ratio, 3),
                'missing_count': len(missing),
                'score': round(score, 3)
            })
    results.sort(key=lambda x: (-x['score'], x['missing_count']))
    return results
