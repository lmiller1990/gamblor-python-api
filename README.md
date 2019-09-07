A simple API built using python, peewee and flask.

## Development

You can run locally by installing the dependencies or using docker. You will need the lcs database (need to contact me for a dump).

### Locally

You can run it locally. Install using `pip install -r requirements.txt`. Make sure you are using python3/pip3. Then start the app with `POSTGRES_DB=web_development POSTGRES_HOST=localhost POSTGRES_USER=lachlan FLASK_ENV=development python run.py`. You need to put your own postgres user in.

### Docker

Build the container using `docker build -t gamblor-python-api:latest .`. Then run it using `docker run -v ${PWD}:/app -p 5000:5000 --rm -e POSTGRES_DB=web_development -e POSTGRES_HOST=docker.for.mac.host.internal -e POSTGRES_USER=lachlan -e FLASK_ENV=development gamblor-python-api:latest`

### docker-compose

Production uses nginx to handle the HTTP requests, before handing off to flask. The frontend and nginx configuration is found in [this repo](https://github.com/lmiller1990/gamblor-frontend). Build the nginx image: `docker build -t g-nginx nginx`. Fill out `.env` and run with `docker-compose up -d g-nginx`. As above, you will need the database (ask me for that).

## Endpoints

### GET /leagues

```
  Return a list of all active leagues

  Parameters:
      None

  Example:
      curl /leagues

  Example response:
      [
         {
            "active" : true,
            "id" : 2,
            "name" : "NA LCS 2019"
         }
      ]
```

### GET /previous_game_results


```
Return a list of results of previous games for a team

Parameters:
    team_id: team_id to return game results for
    n: number of previous games

Example:
    curl /previous_game_results?team_id=1&n=10

Example response:
    [
       {
          "fb" : false,
          "fbaron" : false,
          "fd" : true,
          "ft" : false,
          "date": '2019-10-01 12:00:00',
          "team_id": 1,
          "opponent_id": 2,
          "game_id" : 809,
          "win" : false
       }
    ]
```

### GET /recommendations

```
Return a list of recommendations for upcoming games, including EV, success rate, etc.

Parameters:
    past_n_games (int): number of games to consider in EV calculation
    game_ids (int[]): games to retreive recommendations for

Example:
    curl /recommendations?past_n_games=20

Example response:
    [
        {
          "blue_ev" : 0.605,
          "blue_odds" : 2.2,
          "blue_side_team_id" : 119,
          "blue_success" : 0.4,
          "game_id": 1,
          "market" : "fd",
          "red_ev" : 1.16725,
          "red_odds" : 1.61,
          "red_side_team_id" : 4,
          "red_success" : 0.85
       }
   ]
```

### GET /Schedule

```
Return upcoming games for a given league

Parameters:
    leaguee: league id to fetch schedule for

Example:
    curl /schedule?league=2

Example response:
    {
        "games": [
            {
                "blue_side_team_fb_odds" : 2.1,
                "blue_side_team_fbaron_odds" : 2.62,
                "blue_side_team_fd_odds" : 2.2,
                "blue_side_team_ft_odds" : 2.25,
                "blue_side_team_id" : 119,
                "date" : "2019-08-22 00:00:00",
                "id" : 1077,
                "league_id" : 2,
                "loser_id" : null,
                "red_side_team_fb_odds" : 1.66,
                "red_side_team_fbaron_odds" : 1.44,
                "red_side_team_fd_odds" : 1.61,
                "red_side_team_ft_odds" : 1.57,
                "red_side_team_id" : 4,
                "split_id" : 4,
                "winner_id" : null
            }
        ],
        "league_id" 2
    }
```

### GET /splits

```
Return a list of all active splits

Parameters:
    None

Example:
    curl /splits

Example response:
    [
       {
          "created_at" : "2019-04-30 08:24:08",
          "id" : 12,
          "league_id" : 10,
          "name" : "All Games"
       }
    ]
```

### GET /teams

```
Return a list of all teams

Parameters:
    None

Example:
    curl /teams

Example response:
    [
      {
        "id" : 116,
        "name" : "Golden Guardians",
        "short_name" : 'ggs'
      }
    ]
```

### Useful Snippets

import code; code.interact(local=dict(globals(), **locals()))
