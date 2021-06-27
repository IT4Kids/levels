import json


def main():
    with open('summary.json', 'r', encoding='u8') as f:
        c = json.load(f)

    new = []
    for d in c:
        temp = {
            "rating": d['rating'],
            "filename": d['filename'],
            "solution_exists": d['solution_exists'],
            "template_exists": d["template_exists"],
            "title": {
                "de": d["title"],
                "en": d["title"],
                "nl": d["title"],
                "fr": d["title"]
            },
            "description": {
                "de": d["description"],
                "en": d["description"],
                "nl": d["description"],
                "fr": d["description"]
            }
        }
        new.append(temp)

    with open('new_summary.json', 'w', encoding='u8') as f:
        json.dump(new, f)


if __name__ == '__main__':
    main()
