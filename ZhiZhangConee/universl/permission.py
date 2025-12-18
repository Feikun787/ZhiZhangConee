from plugins.ZhiZhangConee.universl.io_json import json_file

class Permission:
    #权限判断 主人0   管理员1   普通用户2
    def quanxian(id):
        data = json_file.get_json('plugins/ZhiZhangConee/data/ZhiZhangCon_quanxian.json')
        i = None
        for i in data['zr_qq']:
            print(i,id)
            if str(id) == str(i):
                return 0
        for i in data['gly_qq']:
            if str(id) == str(i):
                return 1
        else:
            return 2