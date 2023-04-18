import logging as log
from datetime import datetime
import time
import pandas as pd
import psycopg2
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import re

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
Session = sessionmaker(bind=engine)
session = Session()
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
        # options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(options=options)
        self.actions = ActionChains(self.driver)

    # function to wait for an element to be visible on the page before performing an action
    def wait_for_element(self, by, value, wait=10):
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


game_data_detail = []
# driver setup
gs = GameScrap()
gs.configure_driver()
actions = gs.actions


def main():
    global game_data_detail
    game_data_detail = []
    home = None
    away = None
    away_city = None
    home_city = None
    game_date = None
    periods = ['Q1', 'Q2', 'Q3', 'Q4']

    default_url = 'https://www.nba.com/game/phx-vs-nyk-0022200550'

    gs.navigate_to_url(default_url)

    # close cookies
    try:
        gs.select_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]').click()
    except:
        pass

    time.sleep(20)

    try:
        dt = gs.select_element(By.XPATH, '//*[@id="story"]').find_elements(By.XPATH,
                                                                           './*[@class="GameStory_gsBy__JTuwp"]/p')
        mdt = dt[0].text
        mdt = mdt.split(",")
        mmdt = mdt[2].split(" ")
        mmmdt = mdt[1].split(" ")
        # print(mmmdt)
        dd = re.findall(r'\d+', mmmdt[2])
        game_date = str(mmmdt[1])+" "+str(dd[0])+", "+str(mmdt[1])
    except:
        game_date = ''
        print("Date not found")

    # gs.driver.close()

    # exit()

    for period in periods:
        url = str(default_url) + '/play-by-play?period=' + str(period)
        print(url)
        gs.navigate_to_url(url)
        gs.driver.refresh()

        # close cookies
        try:
            gs.select_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]').click()
        except:
            pass

        WebDriverWait(gs.driver, 10)
        time.sleep(20)
        # First, we need to get all the data from all available quarters
        gs.wait_for_element(By.XPATH, '//*[@id="playByPlayContainer"]')

        try:
            teams = gs.select_element(By.XPATH, '//*[@class="GamePlayByPlay_teams__Bdmzh"]').find_elements(By.XPATH,
                                                                                                           './*[@class="GamePlayByPlay_teamLogoWrapper__EHyDP"]')
            g = 0
            for team in teams:
                if g == 0:
                    home = team.text
                    print(home)
                else:
                    away = team.text
                    print(away)
                g = g + 1
        except:
            print("Cant capture teams")

        # gs.select_element(By.XPATH, '//*[@id="playByPlayContainer"]/section/div/div[1]/nav/button[1]').click()
        gs.wait_for_element(By.XPATH, '//*[@class="GamePlayByPlay_hasPlays__LgdnK"]')
        quarters = gs.select_element(By.XPATH, '//*[@class="GamePlayByPlay_hasPlays__LgdnK"]').find_elements(By.XPATH,
                                                                                                             './*[@class="GamePlayByPlayRow_article__asoO2"]')

        wait = WebDriverWait(gs.driver, 10)
        home_team = str(away)
        away_team = str(home)
        game_name = away_team + " at " + home_team

        for quarter in quarters:
            timeline_data = {}
            is_home_team = quarter.get_attribute('data-is-home-team')
            mytime = quarter.find_elements(By.CLASS_NAME, 'GamePlayByPlayRow_clockElement__LfzHV')
            description = quarter.find_elements(By.CLASS_NAME, 'GamePlayByPlayRow_desc__XLzrU')
            print(is_home_team, mytime[0].text, description[0].text)
            timeline_data['game_date'] = game_date
            timeline_data['game_id'] = 1
            timeline_data['game_name'] = game_name
            timeline_data['away_team'] = away_team
            timeline_data['home_team'] = home_team

            timeline_data['quarter'] = period
            if is_home_team == 'true':
                timeline_data['away_play_description'] = ''
                timeline_data['home_play_description'] = description[0].text

            else:
                timeline_data['away_play_description'] = description[0].text
                timeline_data['home_play_description'] = ''

            timeline_data['game_time '] = mytime[0].text

            data = pd.json_normalize(timeline_data)

            table_name = 'nba_solo_details'
            data.to_sql(table_name, engine, if_exists='append', index=False)


def work():
    main()
    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%d-%H-%M-%S")


if __name__ == '__main__':
    main()
    # scheduler = BlockingScheduler()
    #
    # # scrap every 30 seconds
    # scheduler.add_job(work, 'interval', seconds=60)
    # scheduler.start()
    # pass
