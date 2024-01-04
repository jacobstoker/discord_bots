import random
import requests
from bs4 import BeautifulSoup
import csv


def update_perks_from_wiki():
    """Modify CSV with an up to date list of survivor perks by scraping the Dead by Daylight Wiki"""
    URL = "https://deadbydaylight.fandom.com/wiki/Perks"
    response = requests.get(URL)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")
    perks = []
    for header in soup.find_all("h3"):
        if "Survivor Perks" in header.get_text():
            table = header.find_next_sibling()

            for row in table.tbody.find_all("tr"):
                first_column = row.find_all("th")[1]
                perk_name = first_column.text.strip()
                perks.append(perk_name)

    if perks:
        perks.remove("Name")

        with open("perks.csv", "w", encoding="utf-8") as perk_csv:
            for perk in perks:
                perk_csv.write(f"{perk}\n")


def read_perks_from_csv() -> list[str]:
    """Return the first column of the perks csv (containing the perk names)"""
    # TODO: Initially chose to use a CSV so it can be expanded with other perk attributes, but not sure how that would that fit in with web scraping new perks??
    perks = []
    with open("perks.csv", "r") as perk_csv:
        csv_reader = csv.reader(perk_csv)
        for row in csv_reader:
            if row:
                perks.append(row[0])
    return perks


def reroll_perks(all_perks: list, current_perks: list, reroll: list) -> list:
    """Return an existing list of perks, with new random values for any specified perks"""
    missing_perks = [perk for perk in reroll if perk not in current_perks]
    if missing_perks:
        print(
            f"You tried to reroll perks ({missing_perks}) that aren't in your existing perks ({current_perks}) idiot"
        )
        return current_perks

    rerolled_perks = current_perks
    for perk in reroll:
        new_perk = perk
        while new_perk in rerolled_perks:
            new_perk = random.choice(all_perks)

        idx = rerolled_perks.index(perk)
        rerolled_perks[idx] = new_perk

    return rerolled_perks


def get_random_perks(all_perks: list, max_exhaustion: int = 4) -> list:
    """Return 4 random perks from a list of perks"""
    random_perks = random.sample(all_perks, 4)
    exhaustion_perks = [
        "Background Player",
        "Balanced Landing",
        "Dead Hard",
        "Dramaturgy",
        "Head On",
        "Lithe",
        "Overcome",
        "Smash Hit",
        "Sprint Burst",
    ]
    selected_exhaustion_perks = [
        perk for perk in random_perks if perk in exhaustion_perks
    ]

    if len(selected_exhaustion_perks) > max_exhaustion:
        non_exhaustion_perks = [
            perk for perk in all_perks if perk not in exhaustion_perks
        ]
        keep = random.sample(selected_exhaustion_perks, max_exhaustion)
        selected_exhaustion_perks = [
            perk for perk in selected_exhaustion_perks if perk not in keep
        ]
        random_perks = reroll_perks(
            non_exhaustion_perks, random_perks, selected_exhaustion_perks
        )

    return random_perks
