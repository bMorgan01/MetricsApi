# MetricsAPI
Lightweight Flask API for Linux monitoring

## Overview
MetricsAPI is an extremely lightweight API built with Flask that I created to monitor my home server setup. Personally, I display these metrics on a Rainmeter dashboard, but you can choose to create anything you like.

### Features
- Lightweight
- Status webpage
- Per-core and packaged CPU metrics
  - Model name
  - Address sizes
  - Processor speed
  - User, system, idle, etc. load measures.
- Temperature data
  - CPU
  - Motherboard
  - ... and more (depends on your machine)
- Volume information
  - Space remaining
  - Read/written
  - Read/write per second
- IP addresses

### Future Work
- Network up/down

## Installation
### Dependencies
To run MetricsAPI you will need to install Flask.

MetricsAPI gets its data from shell commands. You will need to install the following with your package manager:
`sysstat`
`sensors`

### Try It!
I run the following command to start the API. Keep in mind that I only run this on my local network and the API is not open to the internet. As per Flask documention `--app run` is not intended for production. You should follow a Flask app deployment procedure (there are tons of them online) if you wish to open your API to the world wide web.

`flask --app main run --host=0.0.0.0`
