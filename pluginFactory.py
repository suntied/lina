from pluginDefault import PluginDefault
from plugins.activity.plugin import PluginActivity
from plugins.alarm.plugin import PluginAlarm
from plugins.remote.plugin import PluginRemote

class PluginFactory:

    def getPlugin(subject, typeS):
        themeName= subject.split(".")[0]    
        if themeName == "alarm":
            return PluginAlarm(subject, typeS)
        elif themeName == "remote":
            return PluginRemote(subject, typeS)
        elif themeName == "activity":
            return PluginActivity(subject, typeS)
        return PluginDefault(subject, typeS)