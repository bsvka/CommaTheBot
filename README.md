# bot, the

A bot intended to fix titles like "foo, the" by moving the "the" to the start ("the foo").

Currently searches for the following articles (with starting upper- and lowercase letter):
`The`, `Der`, `Die`, `Das`, `Le`, `La`, `El`, `Los`, `Las`, `Les`

"Home" repo: https://github.com/bsvka/CommaTheBot

## All types dump 2022-06-06 stats

| Total    | Found | %         |
| -------- | ----- | --------- |
| 72819552 | 25430 | 0.0349219 |

## running it
You nedd `curl`, `zgrep` and `pv` installed on your system.

Start the `main.sh` file. It will set-up a venv, auto-install all dependencies into it, download the altest dump, pre-filter that and finally run the bot itself. All options you pass to `main.sh` will be passed to `CommaTheBot.py`. run `python CommaTheBot.py -h` to find out what options are available. You don't have to pass `--file|-f`.