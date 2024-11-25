import sqlite3
import datetime

# funzione per aggiungere uno studente 

def add_user(user):
    conn = sqlite3.connect('db/gestione_corsi.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False 

    sql = 'INSERT into UTENTI(mail, password, nome, cognome, docente, immagine_profilo) VALUES(?,?,?,?,?,?)'

    try:
        cursor.execute(
            sql, (user['mail'], user['password'], user['nome'], user['cognome'], user['docente'], user['immagine_profilo']))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # if something goes wrong: rollback
        # conn.rollback()

    cursor.close()
    conn.close()

    return success

# funzione per prendere un user dal db avente una precisa mail

def get_user_by_mail(mail):
    conn = sqlite3.connect('db/gestione_corsi.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM UTENTI WHERE mail = ?'
    cursor.execute(sql, (mail,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user  

# funzione per aggiungere un corso nel database

def add_course(course):
    conn = sqlite3.connect('db/gestione_corsi.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False 

    # se ci sono i prerequisiti 
    if 'prerequisiti' in course:
        sql = 'INSERT into CORSI(titolo, descrizione, categoria, immagine_corso, nome_docente, prerequisiti) VALUES(?,?,?,?,?,?)'
        cursor.execute(sql, (course['titolo'], course['descrizione'], course['categoria'], course['immagine_corso'],
                            course['nome_docente'], course['prerequisiti']))
    else: 
        sql = 'INSERT into CORSI(titolo, descrizione, categoria, immagine_corso, nome_docente) VALUES(?,?,?,?,?)'
        cursor.execute(sql, (course['titolo'], course['descrizione'], course['categoria'], course['immagine_corso'],
                            course['nome_docente']))

    try:
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # if something goes wrong: rollback
        # conn.rollback()

    cursor.close()
    conn.close()

    return success

def get_corsi():
    conn = sqlite3.connect('db/gestione_corsi.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM CORSI ORDER BY CORSI.id_corso'
    cursor.execute(sql)
    courses = cursor.fetchall()

    cursor.close()
    conn.close()

    return courses

def get_corsi_by_docente(nome_docente):
    conn = sqlite3.connect('db/gestione_corsi.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM CORSI WHERE CORSI.nome_docente = ? GROUP BY CORSI.id_corso'
    cursor.execute(sql, (nome_docente,))
    courses = cursor.fetchall()

    cursor.close()
    conn.close()

    return courses

def get_corso_by_id(id):
    conn = sqlite3.connect('db/gestione_corsi.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM CORSI LEFT JOIN UTENTI ON CORSI.nome_docente = UTENTI.mail WHERE CORSI.id_corso = ? '
    cursor.execute(sql, (id,))
    course = cursor.fetchone()

    cursor.close()
    conn.close()
    
    
    return course

# metodi che gestiscono le iscrizioni ai corsi da parte degli studenti 

def disiscrivi_utente_da_iscrizioni(mail):
    conn = sqlite3.connect('db/gestione_corsi.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    success = False

    sql = 'DELETE FROM ISCRIZIONI WHERE id_utente= ?'
    cursor.execute(sql, (mail,))

    try:
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # if something goes wrong: rollback
        conn.rollback()
    cursor.close()
    conn.close()
    return success

def iscrizione(utente, corso):
    conn = sqlite3.connect('db/gestione_corsi.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    success = False


    sql = 'INSERT INTO ISCRIZIONI(id_utente, id_corso) VALUES(?,?)'
    cursor.execute(sql, (utente, corso,))
    try:
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # if something goes wrong: rollback
        conn.rollback()
    cursor.close()
    conn.close()
    return success

def disiscriviti(utente, corso):
    conn = sqlite3.connect('db/gestione_corsi.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    success = False


    sql = 'DELETE FROM ISCRIZIONI WHERE  id_utente = ? AND id_corso = ?'
    cursor.execute(sql, (utente, corso))
    try:
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # if something goes wrong: rollback
        conn.rollback()
    cursor.close()
    conn.close()
    return success

def get_n_iscritti_by_corso(id_corso):
    conn = sqlite3.connect('db/gestione_corsi.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT COUNT(*) as n_iscritti FROM ISCRIZIONI WHERE id_corso = ?'
    cursor.execute(sql, (id_corso,))
    n_iscritti = cursor.fetchone()

    cursor.close()
    conn.close()
    
    
    return n_iscritti

def is_iscritto(id_utente, id_corso):
    conn = sqlite3.connect('db/gestione_corsi.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM ISCRIZIONI WHERE ISCRIZIONI.id_utente =? AND ISCRIZIONI.id_corso = ? '
    cursor.execute(sql, (id_utente, id_corso))
    iscrizione = cursor.fetchone()
    cursor.close()
    conn.close()
    return iscrizione

# metodi per la gestione del materiale nel database

def add_materials(materiale):
    conn = sqlite3.connect('db/gestione_corsi.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    success = False


    sql = 'INSERT INTO MATERIALI(path, id_corso, titolo) VALUES(?,?,?)'
    cursor.execute(sql, (materiale['path'], materiale['id_corso'],
                         materiale['titolo']))
    try:
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # if something goes wrong: rollback
        conn.rollback()
    cursor.close()
    conn.close()
    return success

def get_all_materials_by_corso(id_corso):
    conn = sqlite3.connect('db/gestione_corsi.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql='SELECT * FROM MATERIALI WHERE MATERIALI.id_corso = ?'
    cursor.execute(sql, (id_corso,))
    materiali = cursor.fetchall()
    
    cursor.close()
    conn.close()

    return materiali

# operazioni per la gestione degli avvisi 

def get_all_avvisi_by_corso(id_corso):
    conn = sqlite3.connect('db/gestione_corsi.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM AVVISI WHERE AVVISI.id_corso = ?'
    cursor.execute(sql, (id_corso,))
    avvisi = cursor.fetchall()

    cursor.close()
    conn.close()

    return avvisi

def add_avviso(avviso):
    conn = sqlite3.connect('db/gestione_corsi.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    success = False

    x = datetime.datetime.now()


    sql = 'INSERT INTO AVVISI(data, testo, id_corso) VALUES(?,?,?)'
    cursor.execute(sql, (x.strftime("%Y-%m-%d"),
                          avviso['testo'], avviso['id_corso']))


    try:
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # if something goes wrong: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success

def get_avviso_by_id(id_avviso):
    conn = sqlite3.connect('db/gestione_corsi.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM AVVISI WHERE AVVISI.id_avviso = ?'
    cursor.execute(sql, (id_avviso,))
    avviso = cursor.fetchone()

    cursor.close()
    conn.close()

    return avviso

#operazioni sulla gestione dei commenti 

def add_comment(comment, mail):
    conn = sqlite3.connect('db/gestione_corsi.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    success = False

    
    x = datetime.datetime.now()

    sql = 'INSERT INTO COMMENTI(testo_commento, data_commento, id_avviso, mail_utente) VALUES(?,?,?,?)'
    cursor.execute(sql, (comment['testo_commento'],
                          x.strftime("%Y-%m-%d"), comment['id_avviso'], mail))
    try:
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # if something goes wrong: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success

def get_comments(id_avviso):
    conn = sqlite3.connect('db/gestione_corsi.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT COMMENTI.id_commento, COMMENTI.testo_commento, COMMENTI.data_commento, COMMENTI.id_avviso, UTENTI.mail, UTENTI.cognome, UTENTI.nome, UTENTI.immagine_profilo FROM COMMENTI LEFT JOIN UTENTI ON COMMENTI.mail_utente = UTENTI.mail WHERE COMMENTI.id_avviso = ?'
    cursor.execute(sql, (id_avviso,))
    comments = cursor.fetchall()    
    
    cursor.close()
    conn.close()

    return comments


def delete_comment(id_commento):
    conn = sqlite3.connect('db/gestione_corsi.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'DELETE FROM COMMENTI WHERE id_commento = ?'
    cursor.execute(sql, (id_commento,))

    try:
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # if something goes wrong: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success

def update_comment(comment):
    conn = sqlite3.connect('db/gestione_corsi.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    success = False

    x = datetime.datetime.now()

    sql = 'UPDATE COMMENTI SET testo_commento = ?, data_commento = ? WHERE id_commento = ?'
    cursor.execute(sql, (comment['testo_commento'],
                          x.strftime("%Y-%m-%d"), comment['id_commento']))

    try:
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # if something goes wrong: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success