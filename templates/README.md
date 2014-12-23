### OpenData LA

Using code created by the [Los Angeles Times Data Desk](https://github.com/datadesk) and its [Checkbook LA Watchdog project](https://github.com/datadesk/checkbook-la-watchdog), this is a "periodically updated archive of data" published by the city of Los Angeles on its [open data portal](https://data.lacity.org/).

What it tracks
--------------

If a given csv file and its corresponding json file is below 10,000 rows, the file will be linked to a location in this repo. Otherwise it will be designated ```n/a```.

I'm storing files larger than 10,000 rows locally, but at my knowledge level they are too large for GitHub, and too large to handle efficiently in a local repository.

|Data set|Row count|Last download|   |   |
|:--------|--------:|:-----------|:--|:--|
{% for obj in file_list %}|[{{ obj.name }}]({{ obj.url }})|{{ obj.row_count }}|{{ obj.last_updated }}|{% if obj.repo_status %}[CSV](csv/{{ obj.csv_name }})|[JSON](json/{{ obj.json_name }}){% else %}n/a|n/a{% endif %}|
{% endfor %}

What changed in last download
-----------------------------

```bash
{% if diff %}{{ diff }}{% else %}Nothing{% endif %}
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