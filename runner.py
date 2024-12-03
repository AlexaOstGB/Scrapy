#import sys
#import os

# Добавьте родительскую директорию в путь Python
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scrapy.crawler import CrawlerProcess
from scrapy.utils.reactor import install_reactor
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from jobparser1.spiders.hhru1 import Hhru1Spider

if __name__ == '__main__':
    configure_logging()
    install_reactor('twisted.internet.asyncioreactor.AsyncioSelectorReactor')
    process = CrawlerProcess(get_project_settings())
    process.crawl(Hhru1Spider) #в скобках указываем класс, который импортируем
    process.start() #создали объекты классов