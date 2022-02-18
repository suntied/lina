import time
import sys
import requests

from plugins.activity.ResponseActivity import ResponseActivity

sys.path.append('../../')
from pluginDefault import PluginDefault

class PluginActivity(PluginDefault):

    def response(self, sentence=""):
        global r
        themeName= self.subject.split(".")[1]
        if themeName == "whatActivity":
            #return r.json()
            r = requests.get('https://www.boredapi.com/api/activity')
        elif themeName == "whatActivityAlone":
            r = requests.get('https://www.boredapi.com/api/activity?participants=1')
        elif themeName == "whatActivityTwo":
            r = requests.get('https://www.boredapi.com/api/activity?participants=2')
        elif themeName == "whatActivityNumber":
            r = requests.get('https://www.boredapi.com/api/activity')
        json = r.json()
        response = ResponseActivity(json['activity'],json['type'],json['participants'],json['price'],json['link'],json['accessibility'])
        return response.response()



    