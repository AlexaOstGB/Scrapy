import scrapy
from akhmadullina_images.items import ImageItem

class ImagesSpider(scrapy.Spider):
    name = 'images_spider'
    allowed_domains = ['akhmadullinadreams.com']
    start_urls = ['https://akhmadullinadreams.com/catalog/odezhda/']  # Начальная страница для получения категорий

    def parse(self, response):
        # Извлекаем доступные категории
        categories = response.css('ul[data-for="66"] li a::attr(href)').getall()
        category_names = response.css('ul[data-for="66"] li a::text').getall()

        # Формируем словарь категорий
        category_dict = {name: href for name, href in zip(category_names, categories)}

        # Выводим доступные категории
        print("Доступные категории:")
        for index, name in enumerate(category_dict.keys(), start=1):
            print(f"{index}. {name}")

        # Запрос у пользователя ввода категории
        category_choice = input("Введите номер категории (например, 2 для 'Платья'): ")

        try:
            category_index = int(category_choice) - 1
            selected_category = list(category_dict.values())[category_index]
            self.start_urls = [response.urljoin(selected_category)]
            self.log(f"Выбрана категория: {selected_category}")
            yield scrapy.Request(url=self.start_urls[0], callback=self.parse_products)
        except (ValueError, IndexError):
            self.log("Некорректный ввод. Пожалуйста, попробуйте снова.")

    def parse_products(self, response):
        self.log('Parsing products page: {}'.format(response.url))
        
        # Извлекаем заголовок h1 для категории
        category_name = response.xpath('//div[@class="catalog__title"]/h1/text()').get()
        
        products = response.css('div.myslider__item')
        self.log('Found {} products'.format(len(products)))  
        
        for product in products:
            image_url = product.css('img.myslider__item__image2::attr(src)').get()
            if image_url:
                full_image_url = response.urljoin(image_url)
                self.log('Found image URL: {}'.format(full_image_url))
                
                item = ImageItem()
                item['image_url'] = full_image_url  # Сохраняем URL изображения
                
                # Получаем ссылку на детальную страницу продукта
                detail_page_url = product.css('a::attr(href)').get()
                if detail_page_url:
                    yield response.follow(detail_page_url, self.parse_product, meta={'item': item, 'category': category_name})

        next_page = response.css('a.next::attr(href)').get()
        if next_page is not None:
            self.log('Following next page: {}'.format(next_page))
            yield response.follow(next_page, self.parse_products)

    def parse_product(self, response):
        item = response.meta['item']
        category_name = response.meta['category']
        
        # Извлекаем артикул из элемента с классом pop-info__article
        article_info = response.xpath('//div[@class="pop-info__article"]/text()').get()
        
        # Если артикул найден, извлекаем только номер
        if article_info:
            article_number = article_info.split(': ')[1].strip() if ': ' in article_info else article_info.strip()
            item['image_name'] = article_number  # Используем артикул как название изображения
            self.log('Extracted article number: {}'.format(article_number))
        else:
            self.log('Article number not found for {}'.format(response.url))
        
        # Сохраняем категорию
        item['category'] = category_name
        
        # Извлекаем заголовок продукта, если это необходимо
        item['category1'] = response.xpath('//div[@class="pop-info__title"]/h1/text()').get()
        
        yield item
