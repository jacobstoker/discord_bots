# discord_bots
Collection of weird little discord bots

Each bot will need a .env in its directory with an accompanying discord token, formatted as seen in the .env_example

## Random DBD Perks ## 
- Scrapes the Dead by Daylight Wiki to get the latest list of perks
- Assigns any discord user 4 perks with the !get_random_perks command
- Can reroll any of the perks with !reroll. This is currently inflexible - case and spaces need to be matched exactly, with a comma and a space separating different perks.
    - eg. "!reroll Borrowed Time, Tenacity"