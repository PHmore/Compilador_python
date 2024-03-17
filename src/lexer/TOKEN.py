# Esta será uma classe que conterá o tipo e valor do token

class TOKEN:
    def __init__ (self, type, value):
        self.type = type
        self.value = value
        print(self.type,self.value)

    def TABELAR (self):
        print(self.type,self.value)