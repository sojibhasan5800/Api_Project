from rest_framework import renderers
import json

class UserRender(renderers.JSONRenderer):
    charset='utf-8'
    def render(self,data,accepted_media_type=None, renderer_context=None):
        response=''
        if 'ErroDetail' in str(data):
            response = json.dumps({'errorsed':data})
        else:
            response = json.dumps(data)
        return response