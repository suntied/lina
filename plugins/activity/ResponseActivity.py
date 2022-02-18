from googletrans import Translator


class ResponseActivity:
    def __init__(self, activity, type, participants, price, link, accessibility):
        self.activity = activity
        self.type = type
        self.participants = participants
        self.price = price
        self.link = link
        self.accessibility = accessibility

    def response(self):
        translator = Translator()
        result = translator.translate(self.activity, dest='fr')
        print("prix : ",self.price,"participants : ", self.participants,"link",self.link)
        return result.text + \
               self.getPriceResponse() + \
               self.getParticipantsResponse() + \
               self.getLinkResponse()

    def getPriceResponse(self):
        if self.price == 0:
            return " en plus c'est gratuit !"
        if 0.01 <= self.price <= 0.3:
            return " en plus ce n'est pas très cher."
        if 0.31 <= self.price <= 0.6:
            return ". Le prix de l'activité est raisonnable."
        if 0.61 <= self.price <= 1:
            return ". Il faut avoir les moyens, l'activité est cher !"
        return ""

    def getParticipantsResponse(self):
        if self.participants == 1:
            return " Vous n'avez besoin de personne"
        if self.participants <= 2:
            return " C'est une activité pour " + str(self.participants) + " personnes."
        return ""

    def getLinkResponse(self):
        if self.link is not None and self.link != '':
            return " Je peux vous proposer ce lien pour plus d'information : " + str(self.link)
        return ""
