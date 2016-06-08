import poloniex_api_python_wrapper_version_2
from pprint import pprint
import pickle, ConfigParser

def get_pchange_str(last_value, current_value, format_str):
    diff = current_value - last_value
    if last_value != 0:
        p_change = (diff/last_value)*100
        if (p_change >= 0):
            return "+"+format_str.format(p_change)+"%"
        else:
            return format_str.format(p_change)+"%"
    else:
        return "N/A"


config = ConfigParser.ConfigParser()
config.read("config.ini")

key = config.get('general', 'key')
secret = config.get('general', 'secret')

p = poloniex_api_python_wrapper_version_2.poloniex(key, secret)

def main():
    coins_str = config.get('general','coins')
    coin_strs = coins_str.split(',')
    coins = []
    for coin_str in coin_strs:
        coins.append(coin_str.split(':'))

    print "loading last values"
    try:
        last_values = pickle.load(open("last_values.p", 'rb'))
    except IOError:
        "no last_values.p file found; creating one"
        last_values = {'total':0}

    for coin in coins:
        if coin[0] not in last_values:
            last_values[coin[0]] = 0

    print "fetching info"
    ticker = p.returnTicker()
    balances = p.returnBalances()
    print

    btc_price = float(ticker['USDT_BTC']['last'])
    print "btc price: $" + str(int(btc_price))
    print

    current_values = {}
    total = 0
    external_total = 0
    
    table = []#table to populate, then print later with .format()
    table.append(['coin','usd value','% change','non-polo usd value'])
    table.append([' ',' ',' ',' '])
    
    for coin in coins:
        #if an external balance is specified, 
        if len(coin) == 2:
            coin_label = coin[0]
            external_balance = float(coin[1])
        else:
            [coin_label, external_balance] = [coin[0], 0]

        if coin_label != "BTC":
            btc_value = float(ticker['BTC_' + coin_label]['last'])
        else:
            btc_value = 1

        balance = float(balances[coin_label]) + external_balance
            
        usd_value = btc_value*btc_price*balance
        external_usd_value = btc_value*btc_price*external_balance
        current_values[coin_label] = usd_value

        #format and add to table
        format_str = config.get('general','format-str')

        pchange_str = get_pchange_str(last_values[coin_label], usd_value, format_str)
        
        table.append([coin_label, "$"+str(int(usd_value)), pchange_str, "$"+str(int(external_usd_value))])
        #print coin_label + ":\t$" + str(int(usd_value)) + "\t(" + change_str + ")"

        total += usd_value
        external_total += external_usd_value



    current_values['total'] = total

    pchange_str = get_pchange_str(last_values['total'], current_values['total'], format_str)
    
    table.append([' ',' ',' ',' '])
    table.append(['total', "$"+str(int(total)), pchange_str, "$"+str(int(external_total))])
    #print 'total:\t$'+str(int(total)) + "\t(" + change_str + ")"

    #print table    
    for row in table:
        print ("{: >5} |{: >10} |{: >10} |{: >10}".format(*row))

    print "Writing new values to file."
    pickle.dump(current_values, open("last_values.p", 'wb'))
    
    print "New values written. Press enter to quit."
    raw_input()
    

main()
