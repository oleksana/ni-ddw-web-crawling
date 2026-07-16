vz# Web Crawler – Books to Scrape

## Overview
This project implements a web crawler and scraper for the website:

https://books.toscrape.com/

The crawler is implemented in **Python using Scrapy**.  
It collects structured information about books and stores the data in JSON format.  
The crawl process and results are logged using **MLflow**.

---

## Crawled resource

**Domain:** `books.toscrape.com`

This website is suitable for crawling experiments because:

- it contains many product pages
- it has clear listing and detail page structure
- each page includes title, description, and metadata
- it is designed for scraping practice

---

## Project Structure

/01
│
├── src/
│   ├── books_spider.py
│   ├── items.py
│   └── mlflow_log.py
│
├── results/
│   ├── books.json
│   └── crawl.log
│
└── index.adox

---

## Extracted data

For each book page the crawler extracts:

- URL
- title
- description
- category
- UPC
- price excluding tax
- price including tax
- tax
- availability
- number of available items
- rating
- number of reviews
- image URL

The extracted records are stored in: results/books.json


---

## Crawling configuration

The crawler uses the following settings:

- `ROBOTSTXT_OBEY = True`
- `DOWNLOAD_DELAY = 2`
- `CONCURRENT_REQUESTS_PER_DOMAIN = 2`
- `DEPTH_LIMIT = 4`
- custom user agent: `books-crawler-academic-project`

These settings ensure polite crawling and restrict the crawler to a single domain.

---

## Crawl strategy

1. Start from the homepage: https://books.toscrape.com/

2. Extract links to book pages from listing pages.

3. Follow pagination links.

4. Visit each book detail page and extract structured data.

---

## MLflow logging

The crawler results are logged using MLflow.

### Logged parameters
- source_domain
- crawler framework
- crawling configuration (delay, depth limit, user agent)

### Logged metrics
- number of extracted records
- number of categories

### Logged artifacts
- `books.json`
- `crawl.log`

---

## Results

### Crawl statistics

| Metric | Value |
|------|------|
| Pages crawled | 86 |
| Items extracted | 80 |
| Successful responses (200) | 85 |
| 404 responses | 1 |
| Maximum crawl depth | 4 |

### Runtime

| Parameter | Value |
|------|------|
| Start time | 20:05:17 UTC |
| Finish time | 20:08:39 UTC |
| Duration | ~201 seconds (~3 min 22 s) |

Average performance:

- **≈ 25 pages crawled per minute**
- **≈ 24 items extracted per minute**

### Output files

The crawler generated the following files:

- `results/books.json` – structured dataset containing extracted book information
- `results/crawl.log` – crawler execution log

---

## Future improvements

Possible extensions of this crawler include:

- converting ratings and prices to normalized numeric values
- improving error handling and retry logic
- expanding the crawler to collect the full catalog
