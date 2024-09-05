from rest_framework import renderers
import json


class RenderUser(renderers.BaseRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ''
        if 'ErrorDetails' in str(data):
            response = json.dumps({
                'errors': data,
            })
        else:
            response = json.dumps(data)
        return response
