import scrapy
from scrapy.http import HtmlResponse
from jobparser1.items import Jobparser1Item
import re  # Импортируем модуль для работы с регулярными выражениями

class Hhru1Spider(scrapy.Spider):
    name = "hhru1"
    allowed_domains = ["hh.ru"]
    start_urls = ["https://hh.ru/search/vacancy?text=Python&from=suggest_post&area=1&hhtmFrom=main&hhtmFromLabel=vacancy_search_line"]

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//a[@data-qa='serp-item__title']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vac_parce)

    def vac_parce(self, responce: HtmlResponse):
        name = responce.xpath("//h1/text()").get()
        
        # Извлекаем строку зарплаты
        salary_text = responce.xpath("//div[@data-qa='vacancy-salary']//text()").getall()
        salary_text = ''.join(salary_text).strip()  # Объединяем список строк в одну строку и убираем пробелы

        # Используем регулярное выражение для разбивки строки на элементы
        salary_pattern = r"от\s*(\d[\d\s]*)\s*до\s*(\d[\d\s]*)\s*([₽$€])\s*(.*)"
        match = re.search(salary_pattern, salary_text)

        if match:
            salary_from = match.group(1).replace(" ", "")  # Убираем пробелы
            salary_to = match.group(2).replace(" ", "")
            currency = match.group(3)
            salary_type = match.group(4)

            salary = {
                "from": salary_from,
                "to": salary_to,
                "currency": currency,
                "type": salary_type
            }
        else:
            salary = {"from": None, "to": None, "currency": None, "type": None}  # Если не удалось распарсить

        url = responce.url
        yield Jobparser1Item(name=name, salary=salary, url=url)
