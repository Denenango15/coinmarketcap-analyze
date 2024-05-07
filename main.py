"""
Script for scraping and writing data of top cryptocurrencies from CoinMarketCap.

This script utilizes Selenium and BeautifulSoup to scrape data from CoinMarketCap's website.
It then writes the extracted data into a CSV file named "Top100 <current_time>.csv".

Functions:
    - get_html(): Opens the CoinMarketCap website using Selenium and scrolls down to load more data.
                  Returns the HTML content of the page.
    - get_content(html_text): Parses the HTML content using BeautifulSoup and extracts information about
                               cryptocurrency names, market capitalization, and market percentage.
                               Returns a list of tuples containing this information.
    - write_cmc_top(): Calls get_html() and get_content() functions to get the data and then writes
                       the data into a CSV file.

Example:
    To use this script, simply call the write_cmc_top() function.
"""
import time
from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import datetime


def get_html():
    """
       Opens the CoinMarketCap website using Selenium and scrolls down to load more data.
       Returns:
           str: The HTML content of the page.
    """
    URL = 'https://coinmarketcap.com/'
    edge = webdriver.Edge()
    edge.get(URL)
    for i in range(10):
        edge.execute_script('window.scrollBy(0,window.innerHeight)')
        time.sleep(1)
    html_text = edge.page_source
    edge.quit()
    return html_text


def get_content(html_text):
    """
        Parses the HTML content using BeautifulSoup and extracts information about
        cryptocurrency names, market capitalization, and market percentage.
        Args:
            html_text (str): The HTML content of the page.
        Returns:
            list: A list of tuples containing cryptocurrency information.
                  Each tuple contains (name, market_cap, market_percentage).
    """
    soup = BeautifulSoup(html_text, 'html.parser')
    table = soup.find('tbody')
    coin_name_tags = table.find_all('p', {'class': 'sc-4984dd93-0 kKpPOn'})
    capitalization_tags = table.find_all('span', {'class': 'sc-7bc56c81-1 bCdPBp'})

    coins_info = []
    total_market_cap = 0

    for cap_tag in capitalization_tags:
        cap_str = cap_tag.text.strip().replace('$', '').replace(',', '')
        total_market_cap += float(cap_str)

    for name_tag, cap_tag in zip(coin_name_tags, capitalization_tags):
        coin_name = name_tag.text.strip()
        coin_cap = float(cap_tag.text.strip().replace('$', '').replace(',', ''))
        market_percentage = (coin_cap / total_market_cap) * 100
        coins_info.append((coin_name, coin_cap, market_percentage))

    return coins_info


def write_cmc_top():
    """
        Writes the extracted cryptocurrency data into a CSV file.
        The file is named "Top100 <current_time>.csv".
    """
    html_text = get_html()
    coins_info = get_content(html_text)

    now = datetime.datetime.now().strftime("%H.%M %d.%m.%Y")
    filename = f"Top100 {now}.csv"

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Name', 'MC', 'MP'])
        for coin_info in coins_info:
            writer.writerow(coin_info)


write_cmc_top()
