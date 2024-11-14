import networkx as nx
import requests
import json


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
    return data


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


# find path weight
def find_path_weight(graph, tickers):

    # initialize variables
    max_path = []
    max_weight = 0
    min_path = []
    min_weight = 100 # set to 100 to ensure it is overwritten, will never be more than 100 (hopefully) (that would be crazy)

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
                    print(f'paths between {name1} and {name2}')
                    print()
                    
                    # iterate through paths
                    for path in paths:
                        # calculate path weight
                        total_weight = 1
                        for i in range(len(path)-1):
                            total_weight *= graph[path[i]][path[i+1]]['weight']
                        print(path, total_weight)

                        # find reverse path
                        reverse_path = path[::-1]
                        # calculate reverse path weight
                        reverse_weight = 1
                        for i in range(len(reverse_path)-1):
                            reverse_weight *= graph[reverse_path[i]][reverse_path[i+1]]['weight']
                        print(reverse_path, reverse_weight)

                        # calculate final weight
                        final_weight = total_weight*reverse_weight
                        print(final_weight)

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


# read in coin name and id data
tickers = [line.strip() for line in open('hw9/coin_ids.txt').readlines()]

# create graph
g = nx.DiGraph()

# get prices
prices = get_prices(tickers)

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



