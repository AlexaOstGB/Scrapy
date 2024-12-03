# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class Jobparser1Pipeline:
    def __init__(self):
        self.file = open('out_data.json', 'w', encoding='utf-8')  # Открываем файл для записи

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"  # Преобразуем item в строку JSON
        self.file.write(line)  # Записываем строку в файл
        return item  # Возвращаем item для дальнейшей обработки

    def close_spider(self, spider):
        self.file.close()  # Закрываем файл при завершении паука


#class Jobparser1Pipeline:
#    def process_item(self, item, spider):
#        print()
#        return item
    

        # #item.get('salary')
        # #item['min_s'] = item.get('salary')[1]
        # #item['max_s'] = item.get('salary')[3]
        # # Сохранение данных в JSON файл
        # try:
        #     with open('out_data.json', 'w', encoding='utf-8') as json_file:
        #         json.dump(item, json_file, ensure_ascii=False, indent=4)
        #     print("Скрейпинг завершен, данные сохранены в books_data.json")
        # except Exception as e:
        #     print(f"Ошибка при сохранении файла: {e}")
