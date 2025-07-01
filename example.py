import json

with open("data/extracted/layouts/page_001.json") as f:
    data = json.load(f)

# Show how one layout block looks
print(json.dumps(data[0], indent=2))
