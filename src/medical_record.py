import json
class medical_record_manager:
    def __init__(self,root):
        self.records=[]
        self.save_pt=root
    def load_record(self,data):
        self.records.append(data)
        if len(self.records)%100==0 and len(self.records)>100:
            self.save_file()

    def save_file(self):
        with open(self.save_pt, 'w', encoding='utf-8') as json_file:
            json.dump(self.records, json_file, ensure_ascii=False, indent=4)
    
