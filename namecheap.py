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
        answers = dns.resolver.query(url,'A')
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
    for dns_ip in dns_ipv4:
        if current_local_ipv4 in str(dns_ip):
            counter += 1
    if counter > 0:
        different = False
    return different

def send_update(host="",domain="",password="",namecheap_url = "", ipv4="",old_ipv4=[]):
    """
    Sends update to namecheap with new IP
    """
    if old_ipv4:
        print("A difference was found. Old IPs were  {} and the new found IP is {}. ".format(ipv4,str(old_ipv4)))
        try:
            request_params = {
                'host': host,
                'domain': domain,
                'password': password,
                'ip': ipv4,

            }
            response = requests.post(namecheap_url, request_params)
            if int(response.status_code) != 200:
                raise Exception("There was a problem with namecheap DDNS push: " + str(response))
            else:
                print("Namecheap was updated from {} to {} at .".format(ipv4,str(old_ipv4),str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"))))
        except:
            raise Exception("There was a problem with namecheap DDNS push: " + str(traceback.format_exc()))

def main():

    url = ""
    host = ""
    domain = "" 
    namecheap_url = "" 
    frequency = 5 #minutes
    print("Starting at " + str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")))
    while True:
        try:

            config = configparser.RawConfigParser()
            config.read('/opt/main.conf')
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
            if current_local_ipv4:
                if current_dns_ipv4:
                    if check_ip_versions(current_local_ipv4, current_dns_ipv4):
                        send_update(host, domain, password, namecheap_url, current_local_ipv4,current_dns_ipv4)
                else:
                    send_update(host, domain, password, namecheap_url, current_local_ipv4,current_dns_ipv4)
        except:
            print("There was an exception: " + str(traceback.format_exc()))
        time_to_sleep = int(frequency) * 60
        st = time_to_sleep - time.time() % time_to_sleep
        print("Sleeping for {} seconds".format(st))
        time.sleep(st)

if __name__ == '__main__':
    main()
    #get_dns_ip4("home.flowy.us")




    #testing
    # ip_list = ["173.20.144.128","8.8.8.8"]
    # check_ip_versions("173.20.144.138",ip_list)