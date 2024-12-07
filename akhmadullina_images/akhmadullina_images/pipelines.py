from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import scrapy

class CustomImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        # Отправляем запросы на загрузку изображений
        if 'image_url' in item:
            yield scrapy.Request(item['image_url'])

    def item_completed(self, results, item, info):
        # Проверяем, были ли загружены изображения
        if not results:
            raise DropItem(f"Item contains no images: {item}")
        
        # Извлекаем информацию о загруженных изображениях
        item['image_paths'] = [x[1]['path'] for ok, x in results if ok]  # Сохраняем пути к изображениям
        return item
