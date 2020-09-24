import requests
import os
from urllib3.exceptions import InsecureRequestWarning
import string 
import sys

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)



fuzz_list = [line.rstrip('\n') for line in open(sys.argv[2])]



def fuzzy_wuzzy(paths_in,main_url):
    discovered_tables = []
    for paths in paths_in:
        url = "https://"+main_url+"/graphql?query=query{"+paths+"}"
        print("Testing Endpoint {}".format(paths))
        try:
           response = requests.get(url,timeout=3,verify=False,headers={'h1': 'h1-token'})
           print(response.text)
           start_string = "Did you mean"
           end_string = "?"
           extracted_table = (response.text.split(start_string))[1].split(end_string)[0]
           extracted_table = extracted_table.replace("\"","")
           extracted_table = extracted_table.replace("\\", "")
           if extracted_table:
              print("Extracted Table Name: "+str(extracted_table))
              discovered_tables.append(extracted_table)
              
          
        except Exception as ex1:
           print(ex1)
           pass
    return discovered_tables
    
    
    
           
def main():
    print("Testing GraphQl Endpoints for Fuzz keywords")
    try:
        main_url = sys.argv[1]
        discovered_tables = fuzzy_wuzzy(fuzz_list,main_url)
        if discovered_tables:
           outputfile = open("foundtables.txt","a")
           for tables in discovered_tables:
               outputfile.write(str(tables))
           outputfile.close()
           
    except  Exception as ex:
       print(ex)
       pass
       
main()
