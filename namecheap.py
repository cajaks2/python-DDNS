#!/usr/bin/env python
# encoding: utf-8

import configparser
import json
from io import StringIO
import dns.resolver
import traceback
import re
import time
import datetime
import requests
import ipaddr
import argparse

def get_local_ip4():
    """
    Gets the public ip address of the server v4 only 
    """
    public_ip = ""
    try:
        public_ip = ""
        ip_v4_url = "https://ipinfo.io"
        response = requests.get(ip_v4_url)
        if int(response.status_code) != 200:
            raise Exception("Failure to get IP: " + str(response.status_code))
        data = json.loads(response.text)
        public_ip = data['ip']
    except:
        print("There was an exception: " + str(traceback.format_exc()))
    return public_ip

def get_dns_ip4(url=""):
    """
    Gets the public dns ip address of the server v4 only, could be more than one
    """
    answers = []
    string_list_ips = []
    try:
        resolver = dns.resolver.Resolver(); 
        answers = dns.resolver.resolve(url,'A')
    except:
        print("There was an exception: " + str(traceback.format_exc()))
    for ip in answers:
        string_list_ips.append(str(ip))
    return string_list_ips

def check_ip_versions(current_local_ipv4="",dns_ipv4=[]):
    """
    Checks if the DNS ip and local ip are different, if so return true  
    """
    different = True
    counter = 0
    try:
        current_local_ipv4_check = ipaddr.IPAddress(current_local_ipv4)
    except:
        different = False #failed to get a valid IP
        print("Invalid IP {} for ip gotten from ipinfo.")
    for dns_ip in dns_ipv4:
        if current_local_ipv4 in str(dns_ip).strip():
            counter += 1
    if counter > 0:
        different = False
    return different

def send_update(host="",domain="",password="",namecheap_url = "", ipv4="",old_ipv4=[]):
    """
    Sends update to namecheap with new IP
    """
    if old_ipv4:
        print("A difference was found for domain {}.{}. Old IPs were {} and the new found IP is {}. ".format(host,domain,' '.join(old_ipv4),ipv4))
        request_params = {
            'host': host,
            'domain': domain,
            'password': password,
            'ip': ipv4,
        }
        response = requests.get(namecheap_url, request_params)
        if int(response.status_code) != 200 or "<ErrCount>0</ErrCount>" not in response.text:
            if "Domain name not found" in response.text:
                print("According to namecheap, the domain name was invalid. Wait an hour and if its still happening check your config.")
                print(response.text)
            else:
                raise Exception("There was a problem with namecheap DDNS push: " + response.text)
        else:
            print("Namecheap was updated from {} to {} at {} for domain {}.{}.".format(' '.join(old_ipv4),ipv4,str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")),host,domain))
            print("It may take some time to reflect in their servers.")
def main():

    url = ""
    host = ""
    domain = ""
    namecheap_url = ""
    frequency = 5 #minutes
    parser = argparse.ArgumentParser()
    parser.add_argument("--conf", help="Alertnate full path to source file for conf.", default="/opt/main.conf")
    print("Starting at " + str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")))
    args = parser.parse_args()
    while True:
        try:
            config = configparser.RawConfigParser()
            config.read(args.conf)
            #for each_section in conf.sections():
            host = config.get('dynamic_dns','host')
            domain = config.get('dynamic_dns','domain')
            password = config.get('dynamic_dns','password')
            namecheap_url = config.get('dynamic_dns','namecheap_url')
            frequency = config.get('dynamic_dns','frequency')
            if int(frequency) < 5:
                frequency = 5 
            url = "{}.{}".format(host,domain)
            if not host or not domain or not password or not namecheap_url:
                raise Exception("Fill in the configuration file fully.")
        except:
            raise Exception("Config load in failed. Make sure config is in /opt/main.conf. Error: " + str(traceback.format_exc()))
        try:
            current_dns_ipv4 = get_dns_ip4(url)
            current_local_ipv4 = get_local_ip4()
            change_occured = 0
            if current_local_ipv4:
                if current_dns_ipv4:
                    if check_ip_versions(current_local_ipv4, current_dns_ipv4):
                        change_occured += 1
                else:
                    change_occured += 1
            if change_occured > 0:
                send_update(host, domain, password, namecheap_url, current_local_ipv4,current_dns_ipv4)
        except:
            print("There was an exception: " + str(traceback.format_exc()))
        time_to_sleep = int(frequency) * 60
        st = time_to_sleep - time.time() % time_to_sleep
        print("Sleeping for {} seconds".format(st))
        time.sleep(st)

if __name__ == '__main__':
    main()



