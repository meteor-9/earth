from django.http.response import JsonResponse
import json, datetime


class NbJSONEncoder(json.JSONEncoder):
    '''解析json里面日期格式'''

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


def NbResponse(error_code=0, msg="操作成功", **kwargs):
    '''自定义返回数据'''
    data = {'code': error_code, 'msg': msg}
    data.update(kwargs)
    return JsonResponse(data, json_dumps_params={"ensure_ascii": False}, encoder=NbJSONEncoder)
