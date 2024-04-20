"""Nalezení všech odpovídajících geolokací."""

import csv
import xml.etree.ElementTree as et
import os
import threading
from typing import Dict, Generator, Set, Tuple

import requests
import PySimpleGUI as sg

from county import COUNTY

URL = "https://api.mapy.cz/geocode"
api_key = ''
ENCODING = "cp1250"
DELIMITER = ";"
OUTPUT = "output.csv"
LAYOUT = [
    [sg.Text("Hledaný výraz:")],
    [sg.Input("firma", key="-SEARCH-")],
    [sg.Text("Adresář výstupního souboru:")],
    [sg.Input(f"{os.path.join(os.getcwd(), OUTPUT)}", key="-PATH-")],
    [sg.Text("", key="-MESSAGE-", size=(20, 1))],
    [sg.Button("Hledat"), sg.Button("Ukončit")],
]


def geocode_position(county: str, search: str) -> str:
    s = requests.Session()
    response = s.get(URL, params={"query": f"{county}, {search}"})
    if response.status_code == 200:
        return response.text


def generate_items(xml) -> Generator[Dict[str, str], None, None]:
    result = et.fromstring(xml)
    point = result.find("point")
    for item in point.findall("item"):
        yield item.attrib


def get_discovered(
    generator: Generator[Dict[str, str], None, None]
) -> Set[Tuple[str, str, str]]:
    return {(item["x"], item["y"], item["title"]) for item in generator}


def create_csv(set_discovered: Set[Tuple[str, str, str]], filepath: str) -> None:
    with open(filepath, "w", newline="", encoding=ENCODING) as f:
        writer = csv.writer(f, delimiter=DELIMITER)
        writer.writerows(set_discovered)


def search_for(search: str, filepath: str) -> None:
    set_discovered = set()
    for county in COUNTY:
        xml = geocode_position(county, search)
        set_discovered |= get_discovered(generate_items(xml))
    create_csv(set_discovered, filepath)


def search_thread(window, search: str, filepath: str) -> None:
    window["-MESSAGE-"].update(value="Hledám ...")
    search_for(search, filepath)
    window["-MESSAGE-"].update(value="Hotovo")


def main() -> None:
    window = sg.Window(title="Geocoding Mapy", layout=LAYOUT)
    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, "Ukončit"):
            break
        if 1 == 1:
            threading.Thread(
                target=search_thread,
                args=(window, values["-SEARCH-"], values["-PATH-"]),
                daemon=True,
            ).start()
    window.close()


if __name__ == "__main__":
    main()
