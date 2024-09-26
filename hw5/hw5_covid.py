import requests
import json
import datetime

# keys needed for analysis
key_pos_inc = 'positiveIncrease'
key_date = 'date'

# define a function to convert the month number to month name
def month_name_check(month):
    return datetime.datetime.strptime(month, '%m').strftime('%B')

# define a function to convert the date to a string
def date_str(date):
    date_obj = datetime.datetime.strptime(str(date), '%Y%m%d')
    return date_obj.strftime('%B %d, %Y')

# define a function to find the average number of new daily confirmed cases
def avg_new_cases(dct_full):

    # create a list of all positive cases
    pos_cases = [date[key_pos_inc] for date in dct_full]

    # calculate the average number of cases
    avg_cases = sum(pos_cases)/len(pos_cases)

    return avg_cases

# define a function to find the date with the highest new number of covid cases
def max_new_cases(dct_full):

    # create a list of all positive cases
    pos_cases = [date[key_pos_inc] for date in dct_full]

    # find the date with the highest number of cases
    for date in dct_full:
        if date[key_pos_inc] == max(pos_cases):
            break

    return date[key_pos_inc], date[key_date]

# define a function to find the most recent date with no new covid cases
def no_new_cases(dct_full):

    # loop through the data to find the most recent date with no new cases
    for date in dct_full:
        if date[key_pos_inc] == 0:
            fulldate = date[key_date]
            break
    return fulldate

# define a function to find the month with the highest and lowest new number of covid cases
def high_low_month(dct_full):
    
    # create a dictionary of the sum of positive cases for each month
    month_dict = {}

    # loop through dates to find the month with the highest and lowest number of cases
    for date in dct_full:

        # get the month and year from the date
        month = str(date[key_date])[:6]

        # add the number of cases to the month
        if month in month_dict:
            month_dict[month] += date[key_pos_inc]
        # add the month to the dictionary, add the number of cases to the month    
        else:
            month_dict[month] = date[key_pos_inc]

        # find the month with the max cases
        if month_dict[month] == max(month_dict.values()):
            max_month = month
        # find the month with the min cases
        if month_dict[month] == min(month_dict.values()):
            min_month = month     
    
    # convert the month number to month name
    max_month_name = month_name_check(max_month[4:6]) 
    min_month_name = month_name_check(min_month[4:6]) 

    # return month and year for min and max
    return max_month_name, max_month[:4], min_month_name, min_month[:4]

# define a function to save the state data to a json file
def save_data(name, dct_full):
    json.dump(dct_full, open(f'hw5\{name}.json', 'w'))


states_file_path = 'hw5\states.txt'   

# read the states from the file
states = [line.strip() for line in open(states_file_path).readlines()]    

# loop through the states
for state in states:
    print()

    # Get the state covid data from the API
    covid_url = 'https://api.covidtracking.com/v1/states/' + state + '/daily.json'
    request = requests.get(covid_url)

    # Convert the json data to a dictionary
    dct_full = json.loads(request.text)

    # Save the state data to a json file
    save_data(state, dct_full)


    # Average number of new daily confirmed cases:
    avg_cases = avg_new_cases(dct_full)
    print(f'The average number of new daily confirmed cases for {state.upper()} is {avg_cases}')


    # Date with the highest new number of covid cases:
    max_cases, max_date = max_new_cases(dct_full)
    print(f'The date with the highest number of new cases in {state.upper()} is {date_str(max_date)} with {max_cases} new cases.')


    # Most recent date with no new covid cases:         
    no_cases_date = no_new_cases(dct_full)
    print(f'The most recent date with no new cases in {state.upper()} is {date_str(no_cases_date)}.')


    # Month with the highest new number of covid cases: (sum the new number of cases for each day in a month)
    max_month_name, max_year, min_month_name, min_year = high_low_month(dct_full)
        
    print(f'The month with the highest number of new cases in {state.upper()} is {max_month_name} {max_year}.')
    print(f'The month with the lowest number of new cases in {state.upper()} is {min_month_name} {min_year}.')