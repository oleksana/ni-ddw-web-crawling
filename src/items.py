import scrapy

class BookItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    category = scrapy.Field()
    upc = scrapy.Field()
    price_excl_tax = scrapy.Field()
    price_incl_tax = scrapy.Field()
    tax = scrapy.Field()
    availability = scrapy.Field()
    num_available = scrapy.Field()
    rating = scrapy.Field()
    review_count = scrapy.Field()
    image_url = scrapy.Field()