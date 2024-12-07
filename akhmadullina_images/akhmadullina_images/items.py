# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AkhmadullinaImagesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

# akhmadullina_images/items.py

class ImageItem(scrapy.Item):
    image_url = scrapy.Field()  # URL изображения
    image_name = scrapy.Field()  # Название изображения
    category = scrapy.Field()
    image_name1 = scrapy.Field()  # Название изображения
    category1 = scrapy.Field()
    image_name2 = scrapy.Field()  # Название изображения
         # Категория изображения
#    image_path = scrapy.Field()   # Локальный путь к файлу после загрузки