import json
from datetime import datetime

class JsonPipeline:
    def open_spider(self, spider):
        # Créer un fichier avec la date et l'heure
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.filename = f"data/raw_mangs_{timestamp}.json"
        self.file = open(self.filename, "w", encoding='utf-8')
        print(f"Sauvegarde dans : {self.filename}")
    
    def close_spider(self, spider):
        self.file.close()
        print(f"Fichier sauvegardé : {self.filename}")
    
    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item