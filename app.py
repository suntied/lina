import models
import tools
import tensorflow as tf
import gc
import numpy
import json

from pluginFactory import PluginFactory


def analyse(sentence):
    subjects, types, stopwords, dictionnary = tools.defaultValues()
    modelSubjects = models.getModelSubjects(dictionnary, subjects)
    modelSubjects.load("data/modelSubjects.tflearn")
    resultS = modelSubjects.predict([tools.bagOfWords(sentence, dictionnary, stopwords)])
    tf.keras.backend.clear_session()
    del modelSubjects
    gc.collect()

    modelTypes = models.getModelTypes(dictionnary, types)
    modelTypes.load("data/modelTypes.tflearn")
    resultT = modelTypes.predict([tools.bagOfWords(sentence, dictionnary, stopwords)])
    tf.keras.backend.clear_session()
    del modelTypes
    gc.collect()

    modelValues = models.getModelValues(dictionnary)
    modelValues.load("data/modelValues.tflearn")
    resultV = modelValues.predict([tools.bagOfWords(sentence, dictionnary, stopwords)])
    tf.keras.backend.clear_session()
    del modelValues
    gc.collect()
    return resultS[0], resultT[0], resultV[0][0]


def searchAnswer(sentence, subject, typeS):
    plugin = PluginFactory.getPlugin(subject, typeS)
    return plugin.response(sentence)


if __name__ == '__main__':
    subjects, types, stopwords, dictionnary = tools.defaultValues()
    while True:
        print("Tape your sentence:")
        test = input()
        rSubject, rType, rValue = analyse(test)
        data = {
            '25-02-2022-12-16': [
                {
                    'type': 'Question',
                    'sentence': 'Hello',
                },
                {
                    'type': 'Answer',
                    'sentence': 'TG'
                }],
            '25-02-2022-12-15': [
                {
                    'type': 'Question',
                    'sentence': 'Hello',
                },
                {
                    'type': 'Answer',
                    'sentence': 'TG'
                }]
        }
        with open('historical.json', 'w') as outfile:
            outfile.write(json.dumps(data))
        if test == "Dis lina correction":
            with open('historical.json') as json_file:
                data = json.load(json_file)
            values_view = data.values()
            value_iterator = iter(values_view)
            first_value = next(value_iterator)
            print("La question était : " + first_value[0]["sentence"])
            print("Selectionner le sujet qui se rapproche le plus du sujet demander : ", subjects)
        result = searchAnswer(test, subjects[numpy.argmax(rSubject)], types[numpy.argmax(rType)])

