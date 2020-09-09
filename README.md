# Route sidewalk from map image

This is just a mini-project. I created it for finding a shortest sidewalk path from some point to 
another point (lat, long coordinate) and it can help you to count the number of cross-road that you need 
if you follow this path.

## Getting Started

### Setup environment

* **Python environment**

```shell script
$ pip install -r requirements.txt
```

* **Selenium docker**

```shell script
$ docker-compose up
```

### Running the code

```shell script
$ python -m route_sidewalk.scripts.route --lat1 18.31628 --lng1 99.39592 --lat2 18.3154363 --lng2 99.3968025
``` 

## TODO

* [ ] Add some result to README
* [ ] Support more color road
