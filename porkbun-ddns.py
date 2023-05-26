import json
import requests
import re
import sys


def get_domainIP(config, rootdomain, subdomain):
    try:
        endpoint = config["endpoint"] + "/dns/retrieveByNameType/" + rootdomain + "/A/" + subdomain
        response = json.loads(requests.post(endpoint, data = json.dumps(config)).text)
        return response["records"][0]["content"]
    except:
        domain = rootdomain if subdomain == "" else subdomain + "." + rootdomain
        print("Something went wrong while trying to retrieve the ip address of {}.".format(domain))
        try: print("Response:", response)
        except: print("No internet connection available.")
        sys.exit(1)


def get_myIP(config):
    try:
        endpoint = config["endpoint"] + "/ping/"
        response = json.loads(requests.post(endpoint, data = json.dumps(config)).text)
        return response["yourIp"]
    except:
        print("Something went wrong while trying to retrieve my ip address.")
        try: print("Response:", response)
        except: print("No internet connection available.")
        sys.exit(1)


def update_record(config, rootdomain, subdomain, myIP):
    try:
        config_copy = config.copy()
        config_copy.update({'content': myIP})
        endpoint = config["endpoint"] + "/dns/editByNameType/" + rootdomain + "/A/" + subdomain

        response = json.loads(requests.post(endpoint, data = json.dumps(config_copy)).text)
        if response["status"] != "SUCCESS":
            raise Exception
    except:
        domain = rootdomain if subdomain == "" else subdomain + "." + rootdomain
        print("Something went wrong while trying to update the ip address of {}.".format(domain))
        try: print("Response:", response)
        except: print("No internet connection available.")
        sys.exit(1)


def main():
    if len(sys.argv) < 3:
        print("usage: python porkbun-ddns.py /path/to/config.json example.com www")
        sys.exit(1)

    config = json.load(open(sys.argv[1]))

    rootdomain = sys.argv[2]
    subdomain  = sys.argv[3] if len(sys.argv) > 3 else ""

    myIP = get_myIP(config)
    domainIP = get_domainIP(config, rootdomain, subdomain)

    if myIP != domainIP:
        update_record(config, rootdomain, subdomain, myIP)


if __name__ == "__main__":
    main()
