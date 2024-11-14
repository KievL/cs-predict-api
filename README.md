 # CS Matches predict API
---
This project is an API built with Django to predict the winners of professional Counter-Strike matches.
Using data collected using my other project [hltv-data-miner](https://github.com/KievL/hltv-data-miner), I developed an XGBoost model that predicts match results based on team statistics and performance indicators.The model was built without fine tuning and has an accuracy of 74%.

It can be used with the [Angular Client](https://github.com/KievL/cs-predict-client).

## Endpoint

POST to `/api`
The body should contain de key "html" with the match page html from HLTV as value.

The response has the following format:
`{'winner': int (0:team1 / 1:team2), 'team1': str,'team2': str,'team1_logo': str (URL), 'team2_logo': str (URL)}`
