# bot, the

A bot intended to fix titles like "foo, the" by moving the "the" to the start ("the foo").

Currently searches for the following articles (with starting upper- and lowercase letter):
`The`, `Der`, `Die`, `Das`, `Le`, `La`, `El`, `Los`, `Las`, `Les`

"Home" repo: https://github.com/bsvka/CommaTheBot

## All types dump 2022-06-06 stats

| Total    | Found | %         |
| -------- | ----- | --------- |
| 72819552 | 25430 | 0.0349219 |

## install

1. Create a virtual env, copy the bot and cd into it

   `python -m venv venv; cp CommaTheBot.py requirements.txt; cd venv`

2. Activate it

   `source bin/activate`

3. Upgrade pip

   `pip install --upgrade pip`

4. Install requirements

   `pip install -r requirements.txt`

## uninstall

1. Deactivate the venv and cd out of it

   `deactivate; cd ..`

2. Remove it

   `rm -r venv`
