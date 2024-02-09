import json
import time
import os
import re
import argparse

def is_vegan(product):
    labels_tags = product.get('labels_tags', [])
    labels = product.get('labels', [])
    if not isinstance(labels, list):
        labels = [labels]  # Ensure it's a list
    all_labels = labels_tags + labels
    return any('vegan' in label.lower() for label in all_labels)

def sanitize_ingredient(ingredient):
    # Normalize and remove \r\n
    ingredient = ingredient.replace('\r\n', ', ').replace('\n', ', ')
    # Remove percentages and non-ingredient notes
    ingredient = re.sub(r'\(\s*\d+%?\s*\)', '', ingredient)
    ingredient = re.sub(r'\d+%', '', ingredient)
    ingredient = re.sub(r'\*.*$', '', ingredient)  # Removes notes starting with *
    # Balance parentheses
    open_braces = ingredient.count('(')
    close_braces = ingredient.count(')')
    if open_braces != close_braces:
        ingredient = ingredient.replace('(', '').replace(')', '')
    return [i.strip().strip('_').replace('_', ' ') for i in re.split(r',|\.', ingredient) if i.strip()]

def count_lines(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return sum(1 for _ in file)

def process_file(file_path, total_lines):
    start_time = time.time()
    vegan_ingredients = set()
    vegan_products_count = 0
    print("\033[36m[ℹ︎] Estimating remaining time...", end='\r')
    with open(file_path, 'r', encoding='utf-8') as file:
        for i, line in enumerate(file):
            if i > 0 and i % 10000 == 0:
                elapsed_time = time.time() - start_time
                lines_per_second = i / elapsed_time
                estimated_time = (total_lines - i) / lines_per_second
                if i == 10000 or i % 100000 == 0:
                    print(' ' * 60, end='\r')
                    formatted_i = f"{i:,}"
                    estimated_minutes = estimated_time / 60
                    print(f"\033[36m[ℹ︎] Processed {formatted_i} lines. Estimated time: {estimated_minutes:,.2f} minutes.", end='\r')
            
            product = json.loads(line)
            if is_vegan(product):
                vegan_products_count += 1
                ingredients_text = product.get('ingredients_text', '')
                for ingredient in sanitize_ingredient(ingredients_text):
                    vegan_ingredients.add(ingredient)
    
    vegan_ingredients = list(filter(None, vegan_ingredients))  # Remove empty strings
    return vegan_ingredients, vegan_products_count

def save_ingredients(ingredients, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(ingredients, file, ensure_ascii=False, indent=2)

def get_args():
    parser = argparse.ArgumentParser(description='Extract Vegan Ingredients from OpenFoodFacts Database Dump.')
    parser.add_argument('--path', type=str, required=True, help='Path to the "openfoodfacts-products.jsonl" file.')
    return parser.parse_args()

def main():
    args = get_args()
    file_path = args.path
    
    print("\033[1m\033[93m[ℹ︎] Veganify: Extracting Vegan Ingredients from OpenFoodFacts Database Dump\033[0m")
    
    if os.path.exists(file_path) and file_path.endswith('.jsonl'):
        print("\033[36m[ℹ︎] Calculating total lines..", end='\r')
        total_lines = count_lines(file_path)
        print(f'\n\033[92m[✔] Total lines calculated: {total_lines:,}\033[0m')
        start_time = time.time()
        ingredients, vegan_products_count = process_file(file_path, total_lines)
        save_ingredients(ingredients, 'vegan_ingredients.json')
        elapsed_time = time.time() - start_time
        print(f'\n\033[92m[✔] Finished processing in {elapsed_time:.2f} seconds. Extracted {len(ingredients):,} unique ingredients from {vegan_products_count:,} products identified as vegan.\033[0m')
    else:
        print("\033[91m[✖] Error: File does not exist or is not a .jsonl file.\033[0m")

if __name__ == "__main__":
    main()
