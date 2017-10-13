'''
    Author: Venkata Varagani
    Description: The following script performs the following activites
    1. locate your chrome histroy database
    2. connect to the history database
    3. get the urls visited list and count
    4. order the data read from the databse
    5. Generate list of top n url
'''


import os
import sqlite3
import operator
from collections import OrderedDict
import matplotlib.pyplot as plt

# global variables
global_top_n_url_list = 5
global_query_statement = "SELECT urls.url, urls.visit_count FROM urls, visits WHERE urls.id = visits.url;"

# main
def main():
    getTopVisitedSiteDetails()

# helper function to get the domain names
def parse(url):
    try:
        parsed_url_components = url.split('//')
        sublevel_split = parsed_url_components[1].split('/', 1)
        domain = sublevel_split[0].replace("www.", "")
        return domain
    except IndexError:
        print "URL format error"

# get the list of sites, sort, print and plot them
def getTopVisitedSiteDetails():
    
    try:

        # locate database
        database_path = os.path.expanduser('~') + "/Library/Application Support/Google/Chrome/Default"
        history_database = os.path.join(database_path, 'history')
        print ("fetching fata from: " + history_database)

        # connect to database
        c = sqlite3.connect(history_database)
        cursor = c.cursor()
        cursor.execute(global_query_statement)
        resultset = cursor.fetchall()

        # extract data
        sites_count = {}
        for url, count in resultset:
            url = parse(url)
            
            if url in sites_count:
                sites_count[url] += 1
            else:
                sites_count[url] = 1

        # sorting list based on visits
        sites_count_sorted = OrderedDict(sorted(sites_count.items(), key=operator.itemgetter(1), reverse=True))

        # get top n sites
        counter = 0;
        top_n_sites = {}
        for key, value in sites_count_sorted.items():
            if counter < global_top_n_url_list:
                counter += 1
                top_n_sites[key] = value

        # sorting list based on visits
        top_n_sites_sorted = OrderedDict(sorted(top_n_sites.items(), key=operator.itemgetter(1), reverse=True))

        # print the list on the console
        for key, value in top_n_sites_sorted.items():
            print(key + "-" + str(value))


        plt.bar(range(len(top_n_sites_sorted)), top_n_sites_sorted.values())
        plt.xticks(rotation=20)
        plt.xticks(range(len(top_n_sites_sorted)), top_n_sites_sorted.keys())
        plt.show()

    except IndexError:
        print "Internal Error";


# main function 
main()