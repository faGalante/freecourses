from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, mail, password, nome, cognome, docente, immagine_profilo):
        self.mail = mail 
        self.password = password
        self.nome = nome
        self.cognome = cognome
        self.docente = docente
        self.immagine_profilo = immagine_profilo
        self.iscrizioni = []

    def get_id(self):
        return self.mail 
    
class Corso():
    def __init__(self, id_corso, titolo, descrizione, categoria, immagine_corso,
                  nome_docente, prerequisiti):
        self.id_corso = id_corso 
        self.titolo = titolo
        self.descrizione = descrizione
        self.categoria = categoria
        self.immagine_corso = immagine_corso
        self.nome_docente = nome_docente 
        self.prerequisiti = prerequisiti 
        self.n_iscritti = 0
        self.frequentanti = []
        self.creatore = ''
        self.frequenta_cu = False
        self.materiale = False
        
        
        
    def get_id(self):
        return self.mail

