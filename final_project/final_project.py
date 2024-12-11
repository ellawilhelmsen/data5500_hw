import networkx as nx
import requests
import json
import os
from datetime import datetime
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

# my os path
dir_path = os.path.dirname(__file__)

# authentication and connection details
api_key = 'PK3ZGRY8TTEYPFOTS4OA'
api_secret = '0oRuPAmEJ29kjsJyYdPODO4itAUrMqlYp7bCzbD3'
base_url = 'https://paper-api.alpaca.markets'

myclient = TradingClient(api_key, api_secret, paper=True)

data = myclient.get_account()


arbitrageList = []


# save data to txt file about exchange rates
def save_data(path, ids, names, prices):

    # get and format date
    today = datetime.now()
    formatted_date = today.strftime("%Y.%m.%d:%H.%M")

    # initialize list to store pair data
    pair_data = []

    # get reverse path
    rev_path = path[::-1]

    for point in range(len(path) - 1):  # Prevent index out of range
        # Get the currency pair and prices for forward path
        try:
            currency_from = path[point]
            currency_to = path[point + 1]

            # Get the price from the prices dictionary (id and names list are in the same order)
            price = prices[names[ids.index(path[point])]][currency_to]
            pair_data.append([currency_from, currency_to, price])
        except Exception as e:
            # error if issue with coin data
            print(f"Error processing pair {point}: {e}")
    
    for point in range(len(rev_path) - 1):  # Prevent index out of range
        # Get the currency pair and prices for reverse path
        try:
            currency_from = rev_path[point]
            currency_to = rev_path[point + 1]

            # Get the price from the prices dictionary (id and names list are in the same order)
            price = prices[names[ids.index(rev_path[point])]][currency_to]
            pair_data.append([currency_from, currency_to, price])
        except Exception as e:
            # error if issue with coin data
            print(f"Error processing pair {point}: {e}")

    # Save data to txt file
    directory = "final_project/data"
    try:
        # Write to CSV
        file_path = f'{directory}/currency_pair_{formatted_date}.txt'
        with open(file_path, 'w', newline='') as file:

            # Write headers
            file.write('Currency From,Currency To,Price\n')

            # Write data
            for pair in pair_data:
                file.write(f'{pair[0]},{pair[1]},{pair[2]}\n')

    except Exception as e:
        # my file is empty every time but error is not raised
        print(f"Error saving data to file: {e}")


# save results to json file after trade
def save_results(data_before, data_after, path):

    # create results dictionary
    results = {}
    results['path'] = path
    results['buying_power_before'] = float(data_before.buying_power)
    results['buying_power_after'] = float(data_after.buying_power)
    results['profit'] = float(data_after.buying_power) - float(data_before.buying_power)

    # dump to json
    json.dump(results, open(f'{dir_path}/results.json', 'w'))
    
    # print results to console
    print('Profit:', results['profit'])


# call api, get prices
def get_prices(tickers):
    ids = []
    names = []

    for item in tickers:
        # separate name and id
        name, id = item.split(',')
        ids.append(id)
        names.append(name)

    # create url
    url_names = ','.join(names)
    url_ids = ','.join(ids)
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={url_names}&vs_currencies={url_ids}'

    # get data
    request = requests.get(url)
    data = json.loads(request.text) 


    return data,ids,names


# add prices to graph
def graph_prices(tickers,data,graph):
    for coin in tickers:
        # seperate name and id  
        name, id = coin.split(',')

        # add edge to graph from coin to all other coins
        for line in data:
            if line == name:
                for item in data[line]:
                    if item != id:
                        graph.add_weighted_edges_from([(id, item, data[line][item])])


# function to submit paper trade(s)
def submit_trade(symbollist, qty):
    # submit trade

    # buy with usd
    for symbol in symbollist:
        order = MarketOrderRequest(
            symbol=(symbol.strip()+'USD').upper(),
            notional=qty,
            side=OrderSide.BUY,
            time_in_force=TimeInForce.GTC,
        )
        try:
            myclient.submit_order(order)
        except Exception as e:
            print(f'Error submitting buy trade for {symbol} {e}')

        # sell with usd, since it is a base currency for all coins used
        order = MarketOrderRequest(
            symbol=(symbol.strip()+'USD').upper(),
            notional=qty,
            side=OrderSide.SELL,
            time_in_force=TimeInForce.GTC,
        )
        try:
            myclient.submit_order(order)
        except:
            print(f'Error submitting sell trade for {symbol}')
    print('Trade(s) submitted')

    # submit trade


# find path weight
def find_path_weight(graph, tickers):

    # initialize variables
    max_path = []
    max_weight = 0
    min_path = []
    min_weight = 100 # set to 100 to ensure it is overwritten, will never be more than 100 (hopefully) (that would be crazy)
    weight_list = []

    # iterate through all pairs of coins
    for ticker1 in tickers:
        name1, id1 = ticker1.split(',')
        for ticker2 in tickers:
            name2, id2 = ticker2.split(',')
            if name1 != name2:
                try:

                    # find all paths between coins
                    paths = list(nx.all_simple_paths(graph, id1, id2))
                    print()
                    print()
                    print(f'finding paths between {name1} and {name2}...')
                    print()
                    
                    # iterate through paths
                    for path in paths:
                        # calculate path weight
                        total_weight = 1
                        for i in range(len(path)-1):
                            total_weight *= graph[path[i]][path[i+1]]['weight']
                        

                        # find reverse path
                        reverse_path = path[::-1]
                        # calculate reverse path weight
                        reverse_weight = 1
                        for i in range(len(reverse_path)-1):
                            reverse_weight *= graph[reverse_path[i]][reverse_path[i+1]]['weight']
                        

                        # calculate final weight
                        final_weight = total_weight*reverse_weight
                        
                        weight_list.append(final_weight)

                        # update max and min weights and paths
                        if final_weight > max_weight:
                            max_weight = final_weight
                            max_path = path
                            max_path_reverse = reverse_path
                        if final_weight < min_weight:
                            min_weight = final_weight
                            min_path = path
                            min_path_reverse = reverse_path
                        
                        
                except:
                    # if no path exists (error)
                    print(f'no path between {name1} and {name2}')

    return max_path, max_path_reverse, max_weight, min_path, min_path_reverse, min_weight

# Get the directory of the code file
current_dir = os.path.dirname(__file__)

# make the path to the coin data relative to current directory
# read in coin name and id data
tickers = [line.strip() for line in open(current_dir + '/coin_ids.txt').readlines()]

# create graph
g = nx.DiGraph()

# get prices
prices,ids,names = get_prices(tickers)

# add prices to graph
graph_prices(tickers, prices, g)

# find and print path weights
max_path, max_path_reverse, max_weight, min_path, min_path_reverse, min_weight = find_path_weight(g, tickers)


# print min and max results
print()
print()
print(f'Smallest Path Weight Factor: {min_weight}')
print(f'Smallest Path: {min_path} {min_path_reverse}')
print()
print(f'Largest Path Weight Factor: {max_weight}')
print(f'Largest Path: {max_path} {max_path_reverse}')


# submit trades
if max_weight > 1:

    save_data(max_path, ids, names, prices)

    submit_trade(max_path, 10000)
    print('Trade submitted for path:', max_path)

    save_results(data, myclient.get_account(), max_path)



else:
    print('No arbitrage opportunities found, no trades submitted')


