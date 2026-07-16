import re
import scrapy
from urllib.parse import urljoin
from items import BookItem


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    # Spider configuration
    custom_settings = {
        "ROBOTSTXT_OBEY": True,
        "DOWNLOAD_DELAY": 2,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
        "DEPTH_LIMIT": 4,
        "USER_AGENT": "books-crawler-academic-project",
        "FEEDS": {
            "../results/books.json": {
                "format": "json",
                "encoding": "utf8",
                "indent": 2,
                "overwrite": True,
            }
        },
        "LOG_FILE": "../results/crawl.log",
        "LOG_LEVEL": "INFO",
    }

    def parse(self, response):
        # Extract links to book detail pages
        book_links = response.css("article.product_pod h3 a::attr(href)").getall()

        for link in book_links:
            yield response.follow(link, callback=self.parse_book)

        # Follow pagination
        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_book(self, response):

        # Helper to extract values from product info table
        def extract_table_value(label):
            xpath = f'//th[text()="{label}"]/following-sibling::td/text()'
            return response.xpath(xpath).get()

        # Extract availability and number in stock
        availability_text = extract_table_value("Availability") or ""
        stock_match = re.search(r"(\d+)", availability_text)
        num_available = int(stock_match.group(1)) if stock_match else None

        description = response.css("#product_description ~ p::text").get()

        # Extract rating
        rating_classes = response.css("p.star-rating::attr(class)").get("")
        rating = rating_classes.replace("star-rating", "").strip()

        # Build absolute image URL
        image_rel = response.css("div.item.active img::attr(src)").get()
        image_url = urljoin(response.url, image_rel) if image_rel else None

        # Extract category from breadcrumbs
        breadcrumbs = response.css("ul.breadcrumb li a::text").getall()
        category = breadcrumbs[-1].strip() if breadcrumbs else None

        item = BookItem()
        item["url"] = response.url
        item["title"] = response.css("div.product_main h1::text").get()
        item["description"] = description.strip() if description else None
        item["category"] = category
        item["upc"] = extract_table_value("UPC")
        item["price_excl_tax"] = extract_table_value("Price (excl. tax)")
        item["price_incl_tax"] = extract_table_value("Price (incl. tax)")
        item["tax"] = extract_table_value("Tax")
        item["availability"] = availability_text.strip()
        item["num_available"] = num_available
        item["rating"] = rating
        item["review_count"] = extract_table_value("Number of reviews")
        item["image_url"] = image_url

        yield item