import json

class json_file:
    def set_json(data,url):
        with open(str(url),'w',encoding='utf-8')as f:
            json.dump(data,f,ensure_ascii=False)
            f.close()
    #读数据
    def get_json(url):
        with open(str(url),'r',encoding='utf-8')as f:
            data = json.load(f)
            f.close()
            return data