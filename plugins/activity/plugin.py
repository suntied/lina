import time
import sys
import requests

from plugins.activity.ResponseActivity import ResponseActivity

sys.path.append('../../')
from pluginDefault import PluginDefault

class PluginActivity(PluginDefault):

    def response(self, sentence=""):
        themeName= self.subject.split(".")[1]
        r = requests.get('https://www.boredapi.com/api/activity')
        json = r.json()
        response = ResponseActivity(json['activity'],json['type'],json['participants'],json['price'],json['link'],json['accessibility'])
        if themeName == "whatActivity":
            #return r.json()
            return response.response()
        elif themeName == "whatActivityAlone":
            return response.response()
        elif themeName == "whatActivityTwo":
            return response.response()
        elif themeName == "whatActivityNumber":
            return response.response()



    