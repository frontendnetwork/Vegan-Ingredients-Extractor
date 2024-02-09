# Vegan Ingredients Extractor

Vegan Ingredients Extractor is a Python script designed to parse through the OpenFoodFacts database [dump in jsonl-format (Direct Download, ~ 6GB gzipped, ~40GB uncompressed)](https://static.openfoodfacts.org/data/openfoodfacts-products.jsonl.gz) to identify vegan products and extract their ingredients. 

It is mainly designed to improve the Vegan Ingredients Checker on the [Veganify API](https://github.com/frontendnetwork/veganify-api) and provides an efficient way to filter through extensive datasets, leveraging labels and ingredients data to curate a list of vegan-friendly ingredients. This script can also be altered to look for other stuff. 

## How to Use

### Prerequisites:
- [Python](https://python.org)
- [OpenFoodFacts database dump](https://static.openfoodfacts.org/data/openfoodfacts-products.jsonl.gz)


### Setup:
Clone this repository to your local machine and navigate to the repository's directory in your terminal.

```bash
$ cd Vegan-Ingredients-Extractor
```

### Running the Script:
The script can be executed with or without a command-line argument for the file path. To run it with a file path argument:
```zsh
$ python3 extract_vegan_ingredients.py --path=/path/to/your/openfoodfacts-products.jsonl
```

### Output:
The script will process the specified .jsonl file to identify vegan products and extract their ingredients. It removes duplicates and cleans up the data to ensure a refined list.

Upon completion, the script outputs a file named vegan_ingredients.json containing all unique vegan ingredients extracted from the dataset.
To modify the outputs file name or path, alter Line 81:
```python
save_ingredients(ingredients, 'vegan_ingredients.json')
```

## License

This project is open-sourced under the WTFPL License. Do what the fuck you want.
