# Python-ddns
This is a simple script that keeps namecheap ddns up to date with v4 address. It will not hit namecheap servers unless there is a difference between its dig and the call out to ipinfo. Due to the nature of dns, if it does detect a difference it may (depending on your frequency) send the update more than once. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Best way to run this is via docker with instructions below. It does require a fleshed out config file including your namecheap ddns password which can be generated on the advanced DNS page of your domain. 
The config is layed out like 
```
[dynamic_dns]

host = 
domain = 
password = 
frequency = 15
namecheap_url = https://dynamicdns.park-your-domain.com/update?
```

Frequency is in minutes, I would advise to not go below 5 minutes or above the minutes in a day. 

## Deployment

Deployment I advise you go with docker otherwise you'll have to install a ton of dependencies. 

To run with docker run a variant of 
```
docker run -it -v `pwd`/example.conf:/opt/main.conf cajaks2/python-ddns
```
For detached 
```
docker run -td -v `pwd`/example.conf:/opt/main.conf cajaks2/python-ddns
```
Be sure to pass through your config file. 

## Multi-Platform Build
Assuming you're using Docker Desktop 2.5+ follow these instructions to use buildx for multiplatform builds
```
docker context create node-arm64
docker context create node-amd64

docker buildx create --use --name mybuild node-arm6
docker buildx create --use --append --name mybuild node-amd64
```
Once the contexts and builders are created you can than use buildx build
```
docker buildx build --platform linux/arm64/v8,linux/amd64 --push --tag cdower/python-ddns:latest .
```
## Authors

* **Cooper Jackson** 
* **Chris Dower**
## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

