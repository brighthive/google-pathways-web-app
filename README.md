# Google Pathways Web App

## Why did we build this?
Google offers, in select US states, an extension of their search platform: [Google Pathways](https://jobs.google.com/pathways/), a free, online tool that maps out opportunities and “pathways” to new careers. A user can access Google pathways via Google Search in three simple steps: (1) the user visits google.com, (2) the user searches for “job training” + “some location,” and (3) the user sees topically organized programs data in an interactive panel.

Perhaps not surprisingly, Google finds programs data just like Google finds any data – by crawling the web. Google operates crawlers that visit billions of websites, pull data, and load that data into the massively comprehensive Google Search Index. For Pathways, the crawlers look for so-called “structured data" (a standardized, search-engine-friendly format for describing data, embedded in HTML, typically in JSON-LD format).

BrightHive's Google Pathways Web App serves a single purpose: to share programs data with Google Pathways.

## Features
The Google Pathways Web App has a few essential components that encourage Google to capture structured data for display in Pathways:

* A script tag with type "application/ld+json” that holds JSON-LD; the JSON-LD presents the requisite data for a single program.
* Links (i.e., `<a>` tags) at the bottom of each page that point to the “Next” and the “Previous” program; the links ensure that all pages on the app can be discovered.
* A dynamically generated `sitemap.xml`, which provides a human- and machine-readable list of all pages (and hence programs).
* A `robots.txt` file, which provides the location of the sitemap.xml and forbides crawlers (other than Google) to crawl the app.
* Logic to handle the `If-Modified-Since` HTTP header, which clearly directs Google to crawl the most recently updated programs.

Read [the white paper "Sharing Programs Data with Google Pathways"](https://docs.google.com/document/d/1c2wqYV1mDjGcbRVXu1ume0xZ-mBIBHJ-unIMEABnWQg/edit#) (by BrightHive engineer Regina Compton) for more information.

## How to develop

1. **Configure the Flask app**

The Google Pathways Web App configures the Flask app and database by ingesting environment variables. The `.env.development` assigns values to the env variables necessary for local development. Copy it, like so:

```cp
cp .env.development .env
```

2. **Build a local Docker image**
```bash
docker build -t brighthive/google_pathways_web_app:latest .
```

3. **Stand-up the Flask app and psql with `docker-compose`**
```bash
docker-compose up
```
4. **Add data**

Likely, you arrived at this repo, because you have Pathways-ready programs data: populate the database with (your own custom) scripts that directly connect with the `psql` database. 

Need some inspiration? BrightHive engineers can use the scripts in the `etl-goodwill` repo to populate the database or as resource for crafting an ETL pipeline.

## Tests
Run the tests like so:
```bash
pipenv run pytest
```

You also can run the tests with different options, depending on your needs:
```bash
# Print all logger output to terminal
pipenv run pytest --log-cli-level=INFO
```
```bash
# Do not stop the psql container after running tests
DO_NOT_KILL_DB=true pipenv run pytest
```

## Team

* Regina Compton (Software Engineer)
* John O'Sullivan (DevOps - Software Engineer)
