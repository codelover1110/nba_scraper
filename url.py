import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import logging as log
import json
from bs4 import BeautifulSoup

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz

from datetime import datetime, timedelta, date

from sqlalchemy import create_engine
import pandas as pd
import psycopg2

log.basicConfig(level=log.INFO)

# Set up the connection parameters
conn_params = {
    "host": "localhost",
    "port": "5432",
    "database": "postgres",
    "user": "postgres",
    "password": "Foryoureyesonly11",
    "sslmode": "prefer",
    "connect_timeout": "10"
}

# Connect to the database
conn = psycopg2.connect(**conn_params)
engine = create_engine(
    f'postgresql://{conn_params["user"]}:{conn_params["password"]}@{conn_params["host"]}:{conn_params["port"]}/{conn_params["database"]}')

# Create a cursor object
cur = conn.cursor()


# initial setup of selenium
class GameScrap:
    def __init__(self):
        self.driver = None
        self.actions = None
        pass

    # set up driver
    def configure_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(options=options)
        self.actions = ActionChains(self.driver)

    # function to wait for an element to be visible on the page before performing an action
    def wait_for_element(self, by, value, wait=20):
        wait = WebDriverWait(self.driver, wait)
        element = wait.until(EC.visibility_of_element_located((by, value)))
        return element

    # function to navigate to a URL
    def navigate_to_url(self, url):
        self.driver.get(url)

    # function to select an element by a specific selector
    def select_element(self, by, value):
        element = self.driver.find_element(by, value)
        return element


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


game_data_detail = []
# driver setup
gs = GameScrap()
gs.configure_driver()
actions = gs.actions


def main():
    global game_data_detail
    game_data_detail = []
    gameid = 0

    start_date = date(2022, 10, 18)
    print("Start date", start_date)
    end_date = date.today()
    print("End date", end_date)

    for single_date in daterange(start_date, end_date):
        print(single_date.strftime("%Y-%m-%d"))
        url = 'https://www.nba.com/games?date=' + str(single_date.strftime("%Y-%m-%d"))
        print(url)
        gs.navigate_to_url(url)
        time.sleep(20)

        try:
            gs.select_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]').click()
        except:
            pass

        gs.wait_for_element(By.XPATH, './/div[@class="GamesView_gameCardsContainer__c_9fB"]')
        url_elements = gs.select_element(By.XPATH,
                                         './/div[@class="GamesView_gameCardsContainer__c_9fB"]').find_elements(By.XPATH,
                                                                                                               './/div[@class="GameCard_gc__UCI46 GameCardsMapper_gamecard__pz1rg"]')
        print(url_elements)
        for match in url_elements:
            nba_url_data = {}
            print(match)

            try:
                teams = match.find_elements(By.CLASS_NAME, 'MatchupCardTeamName_base__PBkuX')
                print(teams)
                g = 0
                for team in teams:
                    if g == 0:
                        away = team.text
                        print(away)
                    else:
                        home = team.text
                        print(home)
                    g = g + 1
            except:
                print("Cant capture teams")

            game_url = match.find_elements(By.TAG_NAME, 'a')

            gameid = gameid + 1
            nba_url_data['gameid'] = gameid
            nba_url_data['url'] = game_url[0].get_attribute('href')
            nba_url_data['away'] = away
            nba_url_data['home'] = home
            nba_url_data['date'] = single_date.strftime("%Y-%m-%d")
            print(nba_url_data)
            data = pd.json_normalize(nba_url_data)
            table_name = 'nba_url_details'
            data.to_sql(table_name, engine, if_exists='append', index=False)


def work():
    main()
    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%d-%H-%M-%S")

    # data = pd.json_normalize(game_data_detail)
    #
    # table_name = 'nba_game_url'
    # data.to_sql(table_name, engine, if_exists='replace', index=False)


if __name__ == '__main__':
    work()
    # scheduler = BlockingScheduler()
    #
    # # scrap every 30 seconds
    # scheduler.add_job(work, 'interval', seconds=10)
    # scheduler.start()
    pass
