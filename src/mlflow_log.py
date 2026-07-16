import json
from pathlib import Path

import mlflow
from scrapy.crawler import CrawlerProcess

from books_spider import BooksSpider


# Output paths
RESULTS_DIR = Path("../results")
DATA_PATH = RESULTS_DIR / "books.json"
LOG_PATH = RESULTS_DIR / "crawl.log"


def run_crawl():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # Start Scrapy crawler
    process = CrawlerProcess(settings={})
    process.crawl(BooksSpider)
    process.start()


def load_data():
    # Load crawler output
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Missing output file: {DATA_PATH}")

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data


def log_to_mlflow(data):
    num_records = len(data)
    num_categories = len({x.get("category") for x in data if x.get("category")})

    mlflow.set_experiment("books_to_scrape_crawl")

    with mlflow.start_run():
        # Log crawler parameters
        mlflow.log_param("source_domain", "books.toscrape.com")
        mlflow.log_param("framework", "Scrapy")

        # Log simple metrics
        mlflow.log_metric("num_records", num_records)
        mlflow.log_metric("num_categories", num_categories)

        # Log output files
        mlflow.log_artifact(str(DATA_PATH))
        if LOG_PATH.exists():
            mlflow.log_artifact(str(LOG_PATH))


if __name__ == "__main__":
    run_crawl()
    data = load_data()
    log_to_mlflow(data)
    print("Crawl finished and results logged to MLflow.")