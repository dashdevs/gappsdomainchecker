from __future__ import print_function
import httplib2
import os, json, sys
import time
from apiclient import discovery
from oauth2client import client
from oauth2client import service_account
from oauth2client import tools, client
from googleapiclient.errors import HttpError
from oauth2client.file import Storage
from google_credentials import create_directory_service
try:
    import argparse
    flags = tools.argparser.parse_args([])
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/admin-directory_v1-python-quickstart.json
#SCOPES = 'https://www.googleapis.com/auth/admin.directory.user'
#CLIENT_SECRET_FILE = 'clientsecret.json'
#APPLICATION_NAME = 'Directory API Python Quickstart'

customer_id="<YourGsuiteId>"

def domen_insert(domains=[]):
    domens=Domens()
    if type(domains)==list and len(domains)==0:
        domains_file=file("new_domains.txt")
        domains=domains_file.readlines()
        domains_file.close()
    elif type(domains)==str and len(domains)!=0:
        domainlist=[]
        domainlist.append(domains)
        domains=domainlist

    for domainName in domains:

        print(domainName.replace("\n", ""))
        domens.insert_domein(domainName.replace("\n", ""))
        #domens.delete_domain(domainName.replace("\n", ""))
        time.sleep(2)
    pass

class Domens():
    def __init__(self):
        self.service=create_directory_service()
        #self.get_domens()
    def get_domens(self):
        #try:
        results = self.service.domains().list(customer=customer_id).execute()

        #except HttpError as err:
        #    content=json.loads(err.content)
        #    print(content["error"]["message"])
        #    sys.exit(0)
        #else:
        for domain in results["domains"]:
            print(domain["domainName"])

    def insert_domein(self, domainName):
        try:
            self.service.domains().insert(customer=customer_id, body={"domainName":domainName}).execute()
        except HttpError as err:
            content = json.loads(err.content)
            print(content["error"]["message"])
            if content["error"]["message"]=="Domain already exists in some other Customer.":
                print("Domain '%s' already exists in some other Customer." % domainName)
                f=file("exists_domains.txt", "a")
                f.write("%s" %domainName)
                f.close()
            elif (content["error"]["message"]== "Not Found") or (content["error"]["message"]== "Bad Request"):
                print("Wrong customer ID")
                sys.exit(0)
            elif content["error"]["message"]=="Request rate higher than configured.":
                print(content["error"]["message"])
        else:
            self.delete_domain(domainName)
    def delete_domain(self, domainName):
        try:
            self.service.domains().delete(customer=customer_id, domainName=domainName).execute()
        except HttpError as err:
            content = json.loads(err.content)
            print(domainName, content["error"]["message"])
if __name__ == '__main__':
    #main()
    #test()
    domen_insert()
