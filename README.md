Welcome to runner reader!
=========================

Installation
------------
Coming soon


Running
-------

pip install <dependencies> ## this will be automated later

PYTHONPATH=. python src/main.py --interactive --config_file <config path>


Configuration
-------------

The config file makes the app more configurable, such as saved runs, the yearly goal, etc.

An example can be found under "example_config"

TODO
----
* write to database instead of json file
** set up the database in configuration
** migrate all data over to the new database
** use the data in the database in the app
* gracefully handle multiple runs per day
* packaging
* more types of graphs
* option to save a "comment" along with a run (hot/cold, felt great, etc)
