#########################
# GLOBAL VARIABLES USED #
#########################
ai_name = 'L.I.N.A'.lower()
EXIT_COMMANDS = ['bye', 'exit', 'quit', 'shut down', 'shutdown']

ownerDesignation = "Sir"
ownerPhoto = "1"

botChatTextBg = "#007cc7"
botChatText = "white"
userChatTextBg = "#4da8da"

chatBgColor = '#12232e'
background = '#203647'
AITaskStatusLblBG = '#203647'
KCS_IMG = 1  # 0 for light, 1 for dark
voice_id = 0  # 0 for female, 1 for male
ass_volume = 1  # max volume

####################################### IMPORTING MODULES ###########################################
""" System Modules """
try:
    import models
    import tools
    import tensorflow as tf
    import gc
    import numpy
    from pluginFactory import PluginFactory

    import os
    import speech_recognition as sr
    import pyttsx3
    import queue
    import sounddevice as sd
    import vosk
    import sys
    import json
    import models
    import tools
    import app
    import numpy
    import tensorflow as tf
    import gc

    from tkinter import *
    from tkinter import ttk
    from tkinter import messagebox
    from tkinter import colorchooser
    from PIL import Image, ImageTk
    from time import sleep
    from threading import Thread
except Exception as e:
    print(e)

if os.path.exists('userData') == False:
    os.mkdir('userData')

subjects, types, stopwords, dictionnary = tools.defaultValues()

############################################ SET UP VOICE ###########################################
q = queue.Queue()


class ObjectModel:
    def __init__(self):
        self.model = vosk.Model("model")
        self.spk_model = vosk.SpkModel("model-spk")

try:
    objectmodel = None
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[voice_id].id)  # male
    engine.setProperty('volume', ass_volume)

    subjects, types, stopwords, dictionnary = tools.defaultValues()
    device_info = sd.query_devices(None, 'input')
    # soundfile expects an int, sounddevice provides a float:
    default_samplerate = int(device_info['default_samplerate'])
    thrread = None
    UserField = None
except Exception as e:
    print(e)


def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))


def getSpeaker(vector):
    modelSpeaker = models.getModelSpeaker(["Joan", "Unknown"])
    modelSpeaker.load("data/modelSpeaker.tflearn")
    result = modelSpeaker.predict([vector])
    print(result)
    tf.keras.backend.clear_session()
    del modelSpeaker
    gc.collect()
    return numpy.argmax(result[0])


####################################### SET UP TEXT TO SPEECH #######################################
def speak(text, display=False, icon=False):
    AITaskStatusLbl['text'] = 'Speaking...'
    if icon: Label(chat_frame, image=botIcon, bg=chatBgColor).pack(anchor='w', pady=0)
    if display: attachTOframe(text, True)
    if "Selectionner le sujet qui se rapproche le plus du sujet demander" in text:
        return
    print('\n' + ai_name.upper() + ': ' + text)
    try:
        engine.say(text)
        engine.runAndWait()
    except:
        print("Try not to type more...")


####################################### SET UP SPEECH TO TEXT #######################################
def record(objectmodel,clearChat=True, iconDisplay=True):
    rec = vosk.KaldiRecognizer(objectmodel.model, default_samplerate)
    rec.SetSpkModel(objectmodel.spk_model)
    print('\nListening...')
    AITaskStatusLbl['text'] = 'Listening...'

    with sd.RawInputStream(samplerate=default_samplerate, blocksize=8000, device=None, dtype='int16',
                           channels=1, callback=callback):
        rec = vosk.KaldiRecognizer(objectmodel.model, default_samplerate)
        rec.SetSpkModel(objectmodel.spk_model)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                if "spk" in result:
                    speaker = getSpeaker(result["spk"])
                    if speaker == 0:
                        if clearChat:
                            clearChatScreen()
                        if iconDisplay: Label(chat_frame, image=userIcon, bg=chatBgColor).pack(anchor='e', pady=0)
                        attachTOframe(result["text"])
                        rSubject, rType, rValue = app.analyse(result["text"])
                        return {"text": result["text"], "subject": rSubject, "type": rType}


def voiceMedium(objectmodel):
    while True:
        recorder = record(objectmodel)
        main(recorder["text"], recorder["subject"], recorder["type"])


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


def keyboardInput(e):
    user_input = UserField.get().lower()
    if user_input != "":
        clearChatScreen()
        rSubject, rType, rValue = analyse(user_input)

        Label(chat_frame, image=userIcon, bg=chatBgColor).pack(anchor='e', pady=0)
        attachTOframe(user_input.capitalize())
        Thread(target=main, args=(user_input, rSubject, rType)).start()

        UserField.delete(0, END)


###################################### TASK/COMMAND HANDLER #########################################
def isContain(txt, lst):
    for word in lst:
        if word in txt:
            return True
    return False


def main(text, rSubject, rType):
    result = searchAnswer(text, subjects[numpy.argmax(rSubject)], types[numpy.argmax(rType)])
    speak(result, True, True)
    data = {
        'last':
            {
                'sentence': text,
            }
    }
    if "Dis lina" in text or "dis lina" in text:
        print("Dis lina talk")
    else :
        with open("historical.json", 'w') as writefile:
            json.dump(data, writefile)
    # webScrapping.googleSearch(text) #uncomment this if you want to show the result on web, means if nothing found


#####################
####### GUI #########
#####################

############ ATTACHING BOT/USER CHAT ON CHAT SCREEN ###########
def attachTOframe(text, bot=False):
    if bot:
        if "Selectionner le sujet qui se rapproche le plus du sujet demander" in text:
            print("*******************", text.split(':')[0])

            botchat = Label(chat_frame, text=text.split(':')[0], bg=botChatTextBg, fg=botChatText, justify=LEFT, wraplength=250,
                            font=('Montserrat', 12, 'bold'))
            listcombo = ttk.Combobox(chat_frame, values=text.split(':')[1].split(','))
            botchat.pack(anchor='w', ipadx=5, ipady=5, pady=5)
            listcombo.pack()
            listcombo.bind('<<ComboboxSelected>>', sendrequest(listcombo))

        else:
            botchat = Label(chat_frame, text=text, bg=botChatTextBg, fg=botChatText, justify=LEFT, wraplength=250,
                            font=('Montserrat', 12, 'bold'))
            botchat.pack(anchor='w', ipadx=5, ipady=5, pady=5)
    else:
        userchat = Label(chat_frame, text=text, bg=userChatTextBg, fg='white', justify=RIGHT, wraplength=250,
                         font=('Montserrat', 12, 'bold'))
        userchat.pack(anchor='e', ipadx=2, ipady=2, pady=5)


def clearChatScreen():
    for wid in chat_frame.winfo_children():
        wid.destroy()

def sendrequest(listcombo):
    while listcombo.get() == '':
        print("$$$$$$$$$$$$$$$")
    select = listcombo.get()
    print("------------------",select)
    global UserField
    UserField.delete(0,END)
    UserField.insert(0,"Dis lina" + listcombo.get())
    root.event_generate('<Return>')
### SWITCHING BETWEEN FRAMES ###
def raise_frame(frame):
    frame.tkraise()
    clearChatScreen()


######################## CHANGING CHAT BACKGROUND COLOR #########################


chatMode = 1


def changeChatMode():
    global chatMode
    if chatMode == 1:
        VoiceModeFrame.pack_forget()
        TextModeFrame.pack(fill=BOTH)
        UserField.focus()
        chatMode = 0
    else:
        TextModeFrame.pack_forget()
        VoiceModeFrame.pack(fill=BOTH)
        root.focus()
        chatMode = 1


#####################################  MAIN GUI ####################################################

#### SPLASH/LOADING SCREEN ####
def progressbar():
    s = ttk.Style()
    s.theme_use('clam')
    s.configure("white.Horizontal.TProgressbar", foreground='white', background='white')
    progress_bar = ttk.Progressbar(splash_root, style="white.Horizontal.TProgressbar", orient="horizontal",
                                   mode="determinate", length=303)
    progress_bar.pack()
    splash_root.update()
    progress_bar['value'] = 0
    splash_root.update()

    Thread(target=testThread).start()

    while objectmodel is None:
        progress_bar['value'] += 0.2
        # splash_percentage_label['text'] = str(progress_bar['value']) + ' %'
        splash_root.update()

        sleep(0.1)

def testThread():
    global objectmodel
    objectmodel = ObjectModel()

def destroySplash():
    splash_root.destroy()


if __name__ == '__main__':
    splash_root = Tk()
    splash_root.configure(bg='#3895d3')
    splash_root.overrideredirect(True)
    splash_label = Label(splash_root, text="Processing...", font=('montserrat', 15), bg='#3895d3', fg='white')
    splash_label.pack(pady=40)
    # splash_percentage_label = Label(splash_root, text="0 %", font=('montserrat',15),bg='#3895d3',fg='white')
    # splash_percentage_label.pack(pady=(0,10))

    w_width, w_height = 400, 200
    s_width, s_height = splash_root.winfo_screenwidth(), splash_root.winfo_screenheight()
    x, y = (s_width / 2) - (w_width / 2), (s_height / 2) - (w_height / 2)
    splash_root.geometry('%dx%d+%d+%d' % (w_width, w_height, x, y - 30))

    progressbar()
    splash_root.after(10, destroySplash)
    splash_root.mainloop()

    root = Tk()
    root.title('L.I.N.A')
    w_width, w_height = 400, 650
    s_width, s_height = root.winfo_screenwidth(), root.winfo_screenheight()
    x, y = (s_width / 2) - (w_width / 2), (s_height / 2) - (w_height / 2)
    root.geometry('%dx%d+%d+%d' % (w_width, w_height, x, y - 30))  # center location of the screen
    root.configure(bg=background)
    # root.resizable(width=False, height=False)
    root.pack_propagate(0)

    root1 = Frame(root, bg=chatBgColor)
    root2 = Frame(root, bg=background)
    root3 = Frame(root, bg=background)

    for f in (root1, root2, root3):
        f.grid(row=0, column=0, sticky='news')

    ################################
    ########  CHAT SCREEN  #########
    ################################

    # Chat Frame
    chat_frame = Frame(root1, width=380, height=551, bg=chatBgColor)
    chat_frame.pack(padx=10)
    chat_frame.pack_propagate(0)
    value = [""]
    bottomFrame1 = Frame(root1, bg='#dfdfdf', height=100)
    bottomFrame1.pack(fill=X, side=BOTTOM)
    VoiceModeFrame = Frame(bottomFrame1, bg='#dfdfdf')
    VoiceModeFrame.pack(fill=BOTH)
    TextModeFrame = Frame(bottomFrame1, bg='#dfdfdf')
    TextModeFrame.pack(fill=BOTH)

    # VoiceModeFrame.pack_forget()
    TextModeFrame.pack_forget()

    cblLightImg = PhotoImage(file='extrafiles/images/centralButton.png')
    cblDarkImg = PhotoImage(file='extrafiles/images/centralButton1.png')
    if KCS_IMG == 1:
        cblimage = cblDarkImg
    else:
        cblimage = cblLightImg
    cbl = Label(VoiceModeFrame, fg='white', image=cblimage, bg='#dfdfdf')
    cbl.pack(pady=17)
    AITaskStatusLbl = Label(VoiceModeFrame, text='    Offline', fg='white', bg=AITaskStatusLblBG,
                            font=('montserrat', 16))
    AITaskStatusLbl.place(x=140, y=32)

    # Keyboard Button
    kbphLight = PhotoImage(file="extrafiles/images/keyboard.png")
    kbphLight = kbphLight.subsample(2, 2)
    kbphDark = PhotoImage(file="extrafiles/images/keyboard1.png")
    kbphDark = kbphDark.subsample(2, 2)
    if KCS_IMG == 1:
        kbphimage = kbphDark
    else:
        kbphimage = kbphLight
    kbBtn = Button(VoiceModeFrame, image=kbphimage, height=30, width=30, bg='#dfdfdf', borderwidth=0,
                   activebackground="#dfdfdf", command=changeChatMode)
    kbBtn.place(x=25, y=30)

    # Mic
    micImg = PhotoImage(file="extrafiles/images/mic.png")
    micImg = micImg.subsample(2, 2)
    micBtn = Button(TextModeFrame, image=micImg, height=30, width=30, bg='#dfdfdf', borderwidth=0,
                    activebackground="#dfdfdf", command=changeChatMode)
    micBtn.place(relx=1.0, y=30, x=-20, anchor="ne")

    # Text Field
    TextFieldImg = PhotoImage(file='extrafiles/images/textField.png')
    UserFieldLBL = Label(TextModeFrame, fg='white', image=TextFieldImg, bg='#dfdfdf')
    UserFieldLBL.pack(pady=17, side=LEFT, padx=10)
    UserField = Entry(TextModeFrame, fg='white', bg='#203647', font=('Montserrat', 16), bd=6, width=22, relief=FLAT)
    UserField.place(x=20, y=30)
    UserField.insert(0, "Ask me anything...")
    UserField.bind('<Return>', keyboardInput)

    # User and Bot Icon
    userIcon = PhotoImage(file="extrafiles/images/avatars/ChatIcons/a" + str(ownerPhoto) + ".png")
    botIcon = PhotoImage(file="extrafiles/images/assistant2.png")
    botIcon = botIcon.subsample(2, 2)
    modelbis = objectmodel
    try:
        # pass
        Thread(target=voiceMedium,args=(modelbis,)).start()
    except:
        pass

    root.iconbitmap('extrafiles/images/assistant2.ico')
    raise_frame(root1)
    root.mainloop()
