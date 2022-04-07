# pylogparser

Python command line tool to parses the included sample.log and presents the following info:

- What are the number of requests served by day?
- What are the 3 most frequent User Agents by day?
- What is the ratio of GET's to POST's by OS by day?

## Code
The code is divided into two parts:
1. Python Class/Module
2. CLI tool

## Dependencies
This CLI is developed in Python version 3.7 and should work with any Python version 3.x (though it is not tested with any other versions) and it depends on the following python modules:
1. numpy
2. pandas
3. python-dateutil
4. pytz
5. six

## How it work?
When executed it read the log file and load it in a data frame removing any invalid fields. Based on the selected task(s) it print out the report.

## Howto setup?
The runtime environment can also run on Python virtual environment. Please follow the steps to setup the environment:
```
$ git clone https://github.com/santosh0705/pylogparser.git
$ cd pylogparser
$ python3 -m venv py3env
$ source py3env/bin/activate
$ pip install -r requirements.txt
```

## Howto run?
To get the help run `python3 report.py -h`. It will print all the accepted parameters:
```
usage: report.py [-h] -f LOGFILE [-r] [-u] [-m]

Parse log file and get report(s)

optional arguments:
  -h, --help  show this help message and exit
  -f LOGFILE  Path to the log file, eg: sample.log
  -r          Report type: Number of requests served by day
  -u          Report type: Three most frequent user-agent by day
  -m          Report type: Ratio of GETs to POSTs by OS by day
```

To get the number of requests served by day run:

`$ python3 report.py -f sample.log -r`

Multiple reports can combined in a single command:

`$ python3 report.py -f sample.log -rum`

## Pending tasks
* Write unit tests.
