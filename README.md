# NBA Scrapper

NFL Scrapper is a website scraper. It scrap data from https://www.nba.com/

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install NFL Scrapper.

```bash
pip install requirements.txt
```

Install Postgres, Configure/Update db configuration in url.py, data.py
To-Do: I will add db config file later
```bash
conn_params = {
    "host": "localhost",
    "port": "5432",
    "database": "postgres",
    "user": "postgres",
    "password": "**********",
    "sslmode": "prefer",
    "connect_timeout": "10"
}
```

## Usage

# python solo.py
```python
Run solo.py
1. static url is hardcoded
2. visit static url
3. extract all the details like (game_date
game_id
game_name
away_team
home_team
quarter
away_play_description
home_play_description
game_time (pull game time from play_description))
4. Stores it in db
```

# python url.py
```python
First, run url.py
1. urls.py is responsible for extracting urls.
2. Overall urls.py will extract (gameid, home, away, year, week, url) from the site and store it in DB
```

# python data.py
```python
Second, run data.py
1. it will take information from stored file (DB/Table) which contains game urls and other information
2. visit every url
3. extract all the details like 
game_date
game_id
game_name
away_team
home_team
quarter
game_time
play_team
play_description
away_team_points
home_team_points
leading_team
leading_by_points
4. Stores it in db
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
