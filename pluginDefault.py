import json
import os
import re
import shutil

import models2
import tools
import random


class PluginDefault:

    def __init__(self, subject, typeS):
        self.intents = tools.getAllIntents("plugins")
        self.intents += tools.getAllIntents("training_data")
        self.subject = subject
        self.typeS = typeS

    def intentsBySubject(self, name):
        intents = []
        for i in range(len(self.intents)):
            if self.intents[i]["subject"].split(".")[0] == name:
                intents.append(self.intents[i])
        return intents

    def searchSentence(self, sentence, subject, intents):
        subjects, types, stopwords, dictionnary = tools.defaultValues()
        best = -1
        bestIndex = -1
        for i in range(len(intents)):
            if intents[i]["subject"] == subject:
                for j in range(len(intents[i]["sentences"])):
                    tmp = tools.similitude(sentence, intents[i]["sentences"][j], dictionnary, stopwords)
                    if best < tmp:
                        best = tmp
                        bestIndex = j
                if len(intents[i]["sentences"]) > bestIndex + 1:
                    return intents[i]["sentences"][bestIndex] + "\n" + intents[i]["sentences"][bestIndex + 1]
                elif bestIndex - 1 > 0:
                    return intents[i]["sentences"][bestIndex - 1] + "\n" + intents[i]["sentences"][bestIndex]
                else:
                    return intents[i]["sentences"][bestIndex]
        return "Pas mal la punchline"

    def getAllSubjects(self):
        subjects, types, stopwords, dictionnary = tools.defaultValues()
        return subjects

    def response(self, sentence=""):
        # HUMOR
        if self.subject == "humor.joke":
            intents = self.intentsBySubject("humor")
            joke = intents[random.randrange(len(intents))]
            if (joke["subject"] == "humor.joke"):
                return "Toi " + joke["sentences"][0]
            return joke["sentences"][0]

        # Correction str(self.getAllSubjects()
        if self.subject == "configuration.reload":
            src = r"D:\Project\lina\plugins\activity\intentsTemp.json"
            dest = r"D:\Project\lina\plugins\activity\intents.json"
            shutil.copy2(src, dest)
            models2.getModel()
            return "Redemarrage effectué"
        if self.subject == "configuration.subject":
            historicalSentence = ""
            with open("historical.json", 'r') as openfile:
                json_object = json.load(openfile)
                historicalSentence = json_object["last"]["sentence"]
            route = 'plugins/activity/intentsTemp.json'
            if sentence == "Dis lina activité" or sentence == "dis lina activité":
                with open(route, 'r') as jsonfile:
                    # Reading from json file
                    #a = openfile.read()
                    json_object1 = json.load(jsonfile)
                    json_object1[0]["sentences"].append(historicalSentence)
                    openfile.close()
                    jsonfile.close()
                with open("plugins/activity/intentsTemp.json", 'w') as writefile:
                    json.dump(json_object1,writefile,ensure_ascii=False, indent=1)
                    print("WRITEDDDDDDDDDDDDDDDDDDDDDDDDDDDDD")
                    #li = str(sentenceToWrite).rsplit("'", 2)
                    #sentenceToWriteText = "\"".join(li)
                    #sentenceToWriteText.replace("\"","")
                    #replaced = re.sub(r'\"sentences\":(.+?)],', "\"sentences\": "+sentenceToWriteText+",", a, 1)

                    #writefile.write(replaced)
                    writefile.close()
            if sentence == "Dis lina activité à deux" or sentence == "dis lina activité à deux":
                with open(route, 'r') as jsonfile:
                    # Reading from json file
                    #a = openfile.read()
                    json_object1 = json.load(jsonfile)
                    json_object1[2]["sentences"].append(historicalSentence)
                    openfile.close()
                    jsonfile.close()
                with open("plugins/activity/intentsTemp.json", 'w') as writefile:
                    json.dump(json_object1,writefile,ensure_ascii=False, indent=1)
                    print("WRITEDDDDDDDDDDDDDDDDDDDDDDDDDDDDD")
                    #li = str(sentenceToWrite).rsplit("'", 2)
                    #sentenceToWriteText = "\"".join(li)
                    #sentenceToWriteText.replace("\"","")
                    #replaced = re.sub(r'\"sentences\":(.+?)],', "\"sentences\": "+sentenceToWriteText+",", a, 1)

                    #writefile.write(replaced)
                    writefile.close()

            return "Modification effectuée veuillez redémarrez l'application"
        if self.subject == "configuration.correction":
            intents = self.intentsBySubject("configuration")
            return intents[0]["responses"][
                       0] + " : " + "meilleur film, bon film, bon mauvais film, activité, activité tout seul, " \
                                    "activité à deux, activité indéfini, alarme à quelle heure, alarme à quelle heure " \
                                    ", configuration d'alarme, son à distance activé, son à distance désactivé, " \
                                    "son à distance muet, tâches aujourd'hui, ajouter une tâche "

        # DEFAULT
        for i in range(len(self.intents)):
            if self.intents[i]["subject"] == self.subject and self.intents[i]["type"] == self.typeS:
                return self.intents[i]["responses"][random.randrange(len(self.intents[i]["responses"]))]
        return "Je n'ai pas de réponse"
