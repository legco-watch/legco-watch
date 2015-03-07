# LegCo Watch

This project is no longer in active development.  Feel free to use its components for your own projects.

# Overview

LegCo Watch is a parliamentary monitoring website in the same vein as [openparliament.ca](http://openparliament.ca),
[GovTrack.us](http://govtrack.us), and [TheyWorkForYou](http://theyworkforyou.com).

One of the first challenges is that we need to parse much of the data that is stored on the LegCo's
[official website](http://legco.gov.hk).  Some of it is accessible as XML or in an API, but the majority
is in HTML or PDF.  The majority of the current code focuses on the parsing, with some basic display
of the parsed data.

# Technology stack

We use Django for our backend and various Python packages to conduct our scraping.  The
[Pombola](https://github.com/mysociety/pombola/) and [Poplus](http://poplus.org/) projects have been very
helpful as a guide for how to implement some of our components in Django.

# Development Environment

There are some Dockerfiles that build a set of docker containers with all of the required services.  You can run
`docker/build.sh` to build all of the necessary containers.  Here's a brief description of what each container does:

 - Data only containers
   - appdata
   - dbdata
   - logdata
 - base - base container with common apt-get libraries
 - dbserver - Postgres server
 - rabbitmq - RabbitMQ server
 - appserver - Django application server
   - dev - Dev container that you can SSH into
 - worker - Celery worker
 - scrapydserver - Scrapyd, but don't think you need this anymore
 
[Fig](www.fig.sh) is a tool for configuring docker containers and quickly launching them.  
`fig.yml` is the Fig configuration file, and defines how the containers should be set up so that they talk to each other.

Once you've built your containers, `fig up dev` should launch the dev environment.  You can ssh in with user `root`
and password `foo`.

If you don't want to use docker, you can just get the apt-get dependencies and pip packages from within the requirements
files and Dockerfiles in each of the containers.  The pip requirements are also in `./requirements` but these may be out
of date.  Then install all of the packages, make sure Postgres is running, and sync / migrate the Django db.  You
only need rabbitmq if you intend to use Celery to run tasks.

Vagrant and Ansible are not longer used.

# Folder structure

## Scraping

All of the Scrapy scrapers are stored in `app/raw/scraper`.  The scrapers were intended to kick off their jobs with
Celery tasks.  The status of these jobs are stored in the Django db.  You can find the logic in `app/raw/tasks.py`.

You can also run the scrapers with Celery, in which case they're just normal Scrapy scrapers.  The scrapers' JSON
outputs should be saved, and some scrapers will download additional files (e.g. the Hansard scraper).

## Parsing

Once data has been downloaded, they are processed by the classes in `app/processors`.  There is also a Celery task
that kicks off processing: `raw.tasks.process_scrape`.  You can run the processing manually, but be careful
with the paths in the JSON results and the downloaded files -- you may need to fiddle with the processors so that
they find the right files.

The processors will take the Raw objects and stick them into cleaned up parsed models.

In addition to the processors, there is a parser for Agenda documents that creates an `Agenda` class that can be
used to extract data out of the Docs.  This is in `app/raw/docs/agenda.py`.  It's far from perfect, but it'll get you
most of the data.

There is a bit of useful code in `app/raw/names.py` that helps disambiguate member names.  In different parts of the LegCo
documents, members can be referred to by their Chinese name, their English, name, with or without their title, or any
number of variants.  This code tries to build some utility classes that lets you match two people even if their names
appear a bit differently.  It's pretty naive, but it covers a lot of the cases in the LegCo docs.

There is also the ability to override the results of a parse with user inputs.  This model is in `raw.models.parsed.Override`.

## Viewing the results

There is a basic front end that allows you to view the raw and parsed results of scrapes.  Start the Django development
server, and you should be able to see an index page that lists some of the models and their data.
