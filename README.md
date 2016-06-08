# poloniex-holdings-tracker

ATTENTION: It is recommended that you change your poloniex API key used by this script to NOT have trading or withdrawal permissions. This way you can be a little less paranoid about the fact that the config file stores this info in plain-text.

---

This script tracks balances held by the user on poloniex, and optionally tracks additional funds held off of poloniex.

Each time the script is run, it reports the $USD value of each of the tracked coins. It also checks the current values from the last time it was run, and reports the % change. (The script is not aware of whether a % change is due to market changes or withdrawals/deposits/trades, so expect this value to swing wildly when depositing/withdrawing/trading). Finally, it tells you how much of your total value is held off of poloniex (I use this to know how much is truly "secured" in my cold wallets, and not susceptible to a poloniex exit scam). For each of these three columns, it also reports a total.

To setup the script for the first run, edit config.ini file to reflect your poloniex API key and secret. Also change the "coins:" line to reflect which coins you'd like to track (by default it tracks ETH and SC because I love ETH and SC). If you have coins held off of poloniex, the script can track them as well if you specify how much you hold elsewhere. See the comments near the "coins:" line for more info.

Donate (BTC): 12CJRstFmesNfGrPYqLXDUrNJzUyEgC1jC

I'll probably update this occasionally, but if I can get some donations for this, I'd make it a priority. Maybe add an optional encryption passphrase to unlock the API key and secret, or add in some rudimentary trading commands. Feel free to email me with requests at syriven@gmail.com.
