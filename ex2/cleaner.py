import json

with open('dataset.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

with open('clean_dataset.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)
