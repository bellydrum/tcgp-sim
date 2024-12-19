#! /usr/bin/env python3

from scripts.webscraping.site_scrapers.ptcgpocket import scrape as scrape_ptcgpocket


print(f"\nStarting data scraping procedure...\n")

scrape_ptcgpocket()

print(f"\nData scraping procedure complete.\n")