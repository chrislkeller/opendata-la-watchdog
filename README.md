### OpenData LA

Using code created by the [Los Angeles Times Data Desk](https://github.com/datadesk) and its [Checkbook LA Watchdog project](https://github.com/datadesk/checkbook-la-watchdog), this is a "periodically updated archive of data" published by the city of Los Angeles on its [open data portal](https://data.lacity.org/).

What it tracks
--------------

|Data set|Row count|Last download|   |   |
|:--------|--------:|:-----------|:--|:--|
|[2014 Registered Foreclosure Properties](https://data.lacity.org/A-Well-Run-City/2014-Registered-Foreclosure-Properties/fdwe-pgcu)|5600|2014-12-11 16:19:51.390125|[CSV](csv/2014 Registered Foreclosure Properties.csv)|[JSON](json/2014 Registered Foreclosure Properties.json)|


What changed in last download
-----------------------------

```bash
Nothing
```

What you can do
---------------

* Try it out and report bugs.
* Figure out ways to build notifications, visualizations or another application on top of the shifting data.
* Try forking it and making it go on a Socrata based data site in your city.
* Or just modify it to work off any old public data set.

Getting started
---------------

Create a virtual enviroment to work inside.

```bash
$ virtualenv --no-site-packages opendata-la-watchdog
```

Jump in and turn it on.

```bash
$ cd opendata-la-watchdog
$ . bin/activate
```

Clone the git repository from GitHub.

```bash
$ git clone git@github.com:SCPR/opendata-la-watchdog.git repo
```

Enter the project and install its dependencies.

```bash
$ cd repo
$ pip install -r requirements.txt
```

Run the script to get the latest files.

```bash
$ python watchdog.py
```