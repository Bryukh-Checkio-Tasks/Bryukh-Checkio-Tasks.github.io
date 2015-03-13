import csv
from collections import namedtuple
from languages_codes import LANG_DICT
from jinja2 import Template, Environment, FileSystemLoader


def read_data(filename):
    with open(filename) as f:
        data = csv.reader(f, delimiter=';')
        names = next(data)
        Mission = namedtuple("Mission", names)
        missions = []
        for m in data:
            missions.append(Mission(*m))
    return missions


def collect_language_info(missions):
    info = {}
    for m in missions:
        mission_languages = m.languages.split(", ")
        for lang in mission_languages:
            info[lang] = info.get(lang, set())
            info[lang].add(m.title)
    return info


def order_languages(lang_dict):
    return sorted([k for k in lang_dict.keys() if k in LANG_DICT.keys()],
                  key=lambda k: len(lang_dict[k]), reverse=True)


def generate_table(missions, languages):
    table = []
    for m in missions:
        row = {
            "title": m.title,
            "slug": m.slug,
            "languages": []
        }
        for lang in languages:
            row["languages"].append(lang in m.languages)
        table.append(row)
    return table


def generate_html(data, language_names, template="translations.html", res_file="index.html"):
    env = Environment(loader=FileSystemLoader('./templates'))
    t = env.get_template(template)
    with open(res_file, "w") as f:
        f.write(t.render(languages=language_names, data=data))


if __name__ == "__main__":
    mission_data = read_data("tasks_info.csv")
    languages_info = collect_language_info(mission_data)
    table = generate_table(mission_data, order_languages(languages_info))
    lang_names = [LANG_DICT[code] for code in order_languages(languages_info)]
    generate_html(table, lang_names)