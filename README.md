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

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
