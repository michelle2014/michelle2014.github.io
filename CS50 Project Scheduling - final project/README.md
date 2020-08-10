# CS50 Final Project 2019/Project Scheduling

Project Scheduling is a Python Flask-based website for dealing with project management and collaboration.

# Motivation

In the real programming world, project timing, communication and cooperation is much more complicated.
Project Scheduling is thus created in consideration of basic needs, including building user, project, team database, displaying project statistics and promoting communication by scheduling meetings and keeping minutes.

## Getting Started

The code was written in CS50 IDE.
The website connects to python Flask app and sqlite3 database.
Main functions of the website:
1 - register as a new user
2 - log in and create new projects
3 - display projects created by all users and those by logged-in user
4 - tracking status of existing projects by statistics
5 - create meetings to communicate, including time, date, location etc.
6 - record meeting minutes
7 - set up teams and team roles working on projects
8 - create new teams for new projects
Short video presentation on youtube:

### Usage

```
flask run
```

## Built With

* [Google Pie Chart](https://www.gstatic.com/charts/loader.js) - Google Pie Chart used
* [Bootstrap](https://maxcdn.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css) - Bootstrap CSS
* [jQuery](https://code.jquery.com/jquery-3.3.1.min.js) - jQuery
* [Font Awesome](//use.fontawesome.com/releases/v5.0.7/css/all.css) - Font Awesome

## Authors

* **Yuanyuan Jiang** - *Initial work* - [Michelle](https://github.com/michelle2014)

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc

CREATE A PROJECT
CREATE TABLE 'projects' ('No.' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 'id' INTEGER NOT NULL, 'name' TEXT NOT NULL, 'technology' TEXT NOT NULL, 'start' NUMERIC NOT NULL, 'due' NUMERIC NOT NULL, 'team' TEXT NOT NULL, 'status' TEXT NOT NULL);
CREATE TABLE 'meetings' ('No.' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 'id' INTEGER NOT NULL, 'title' TEXT NOT NULL, 'organizer' TEXT NOT NULL, 'date' NUMERIC NOT NULL, 'time' NUMERIC NOT NULL, 'location' TEXT NOT NULL, 'action' TEXT NOT NULL, 'status' TEXT NOT NULL);
CREATE TABLE 'teammates' ('No.' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 'id' INTEGER NOT NULL, 'team' TEXT NOT NULL, 'architecture' TEXT NOT NULL, 'frontend' TEXT NOT NULL, 'backend' TEXT NOT NULL, 'tester' TEXT NOT NULL, 'database' TEXT NOT NULL, 'devops' TEXT NOT NULL, 'mobile' TEXT NOT NULL);