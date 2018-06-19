# Python-ddns
This is a simple script that keeps namecheap ddns up to date with v4 address. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Best way to run this is via docker with instructions below. It does require a fleshed out config file including your namecheap ddns password which can be generated on the advanced DNS page of your domain. 
The config is layed out like 
[dynamic_dns]

host = 

domain = 

password = 

frequency = 15

namecheap_url = https://dynamicdns.park-your-domain.com/update?


Frequency is in minutes, I would advise to not go below 5 minutes or above the minutes in a day. 

## Deployment

Deployment I advise you go with docker otherwise you'll have to install a ton of dependencies. 

To run with docker run a variant of 
```
docker run -it -v `pwd`/personal.conf:/opt/main.conf cajaks2/python-ddns
```
For detached 
```
docker run -td -v `pwd`/flowy.conf:/opt/main.conf cajaks2/python-ddns
```
Be sure to pass through your config file. 


## Authors

* **Cooper Jackson** 
## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

