#! /usr/bin/env python3

from scripts.webscraping.site_scrapers.pokemonzone import scrape as scrape_pokemonzone


print(f"\nStarting data scraping procedure...\n")

# scrape_ptcgpocket()
scrape_pokemonzone()

print(f"\nData scraping procedure complete.\n")