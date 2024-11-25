# import module
from flask import Flask, render_template, request, session, redirect, flash, url_for
from flask_session import Session
import dao 

from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Corso

from PIL import Image

# create the application
app = Flask(__name__)
app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


PROFILE_IMG_HEIGHT = 300
POST_IMG_WIDTH = 300

@login_manager.user_loader
def load_user(user_mail):

    utente = dao.get_user_by_mail(user_mail)

    if utente is not None:
        user = User(mail=utente['mail'], password=utente['password'], 
                    nome=utente['nome'], cognome=utente['cognome'], docente=utente['docente'], 
                    immagine_profilo=utente['immagine_profilo'])
    else:
        user = None

    return user


# define the 'login' page

@app.route('/')
def login():
    if current_user.is_authenticated:
        
        return redirect('home')

    return render_template('login.html')

@app.route('/accedi', methods=['POST'])
def login_post():
    mail = request.form.get('mail')
    password = request.form.get('password')

    user = dao.get_user_by_mail(mail)

    if not user or not check_password_hash(user['password'], password):
        flash('Credenziali non valide, riprovare', 'danger')
        return redirect(url_for('login'))
    else: 
        new = User(mail=user['mail'], password=user['password'], 
                    nome=user['nome'], cognome=user['cognome'], docente=user['docente'], 
                    immagine_profilo=user['immagine_profilo'])                                                                 
        login_user(new, True)

        return redirect(url_for('home'))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login')) 


# define the 'signup' page

@app.route('/iscriviti')
def signup():
    return render_template('signup.html')

# define the 'add_user' method

@app.route('/iscriviti', methods=['POST'])
def signup_post():
    mail = request.form.get('mail')

    #controllo che l'utente non sia già registrato nel db
    user_in_db = dao.get_user_by_mail(mail)

    if(user_in_db) :
        flash('C\'è già un utente registrato con questa email', 'danger')
        return redirect(url_for('signup'))
    else :
        # controlli sul form 
        nome = request.form.get('nome')
        cognome = request.form.get('cognome')
        password = request.form.get('password')
        docente = request.form.get('inlineRadioOptions')

        if nome == '':
            app.logger.error('Il nome dell\'utente non può essere vuoto!')
            flash(
                'Utente non creato correttamente: il campo nome non può essere vuoto!', 'danger')
            return redirect(url_for('signup'))
        if cognome == '':
            app.logger.error('Il cognome dell\'utente non può essere vuoto!')
            flash(
                'Utente non creato correttamente: il campo cognome non può essere vuoto!', 'danger')
            return redirect(url_for('signup'))
        if password == '':
            app.logger.error('La password dell\'utente non può essere vuoto!')
            flash(
                'Utente non creato correttamente: il campo password non può essere vuoto!', 'danger')
            return redirect(url_for('signup'))       


        img_profilo = ''
        usr_image = request.files['immagine_profilo']
        if usr_image:
            img = Image.open(usr_image)

            width, height = img.size

            new_width = PROFILE_IMG_HEIGHT * width / height

            size = new_width, PROFILE_IMG_HEIGHT
            img.thumbnail(size, Image.ANTIALIAS)

            left = (new_width/2 - PROFILE_IMG_HEIGHT/2)
            top = 0
            right = (new_width/2 + PROFILE_IMG_HEIGHT/2)
            bottom = PROFILE_IMG_HEIGHT

            img = img.crop((left, top, right, bottom))

            ext = usr_image.filename.split('.')[1]

            img.save('static/' + mail.lower() + '.' + ext)

            img_profilo = mail.lower() + '.' + ext


        new_user = {
            "mail": mail, 
            "password": generate_password_hash(password, method='sha256'),
            "nome": nome, 
            "cognome": cognome,
            "docente": docente,
            "immagine_profilo": img_profilo
        }
        
        success = dao.add_user(new_user)

        if success:
            flash('Utente creato correttamente', 'success')
            return redirect(url_for('login'))
        else:
            flash('Errore nella creazione del utente: riprova!', 'danger')

    
    return redirect(url_for('signup'))






# define the 'home' page
@app.route('/home')
@login_required
def home():
    corsi = dao.get_corsi()
    if current_user.docente ==1:
        corsi_docente = dao.get_corsi_by_docente(current_user.mail)
        #lista oggetti corso 
        lista_ogg_corsi = list()
        for c in corsi_docente:
            #oggetto corso c
            ogg_corso = Corso(c[0], c[1], c[2], c[3],c[4], c[5], c[6])
            n_iscritti = dao.get_n_iscritti_by_corso(c[0]) 
            ogg_corso.n_iscritti = n_iscritti[0]
            lista_ogg_corsi.append(ogg_corso)
        return render_template('home.html', corsi=corsi, corsi_docente=lista_ogg_corsi, )
    
    return render_template('home.html', corsi=corsi)

@app.route('/course/new', methods=['POST'])
@login_required
def new_course(): 

    corso = request.form.to_dict()
    if corso['titolo'] == '':
        app.logger.error('Il titolo del corso non può essere vuoto!')
        flash(
            'Corso non creato correttamente: il titolo del corso non può essere vuoto!', 'danger')
        return redirect(url_for('home'))
    if corso['categoria'] == '':
        app.logger.error('Devi selezionare una categoria')
        flash(
            'Corso non creato correttamente: devi selezionare una categoria!', 'danger')
        return redirect(url_for('home'))   
    if corso['descrizione'] == '':
        app.logger.error('La descrizione del corso non può essere vuota!')
        flash(
            'Corso non creato correttamente: la descrizione del corso non può essere vuota!', 'danger')
        return redirect(url_for('home'))

    user_mail = current_user.mail
    corso['nome_docente'] = user_mail
    prerequisiti = ''
    course_image = request.files['immagine_corso']
    prerequisiti = corso['prerequisiti']
    if course_image:

        img = Image.open(course_image)

        width, height = img.size

        new_width = PROFILE_IMG_HEIGHT * width / height

        size = new_width, PROFILE_IMG_HEIGHT
        img.thumbnail(size, Image.ANTIALIAS)

        left = (new_width/2 - PROFILE_IMG_HEIGHT/2)
        top = 0
        right = (new_width/2 + PROFILE_IMG_HEIGHT/2)
        bottom = PROFILE_IMG_HEIGHT

        img = img.crop((left, top, right, bottom))

        ext = course_image.filename.split('.')[1]

        img.save('static/' + str(corso['titolo']) + '.' + ext)

        immagine_corso = str(corso['titolo']) + '.' + ext


        nuovo_corso = {
            "titolo": corso['titolo'],
            "descrizione": corso['descrizione'],
            "categoria": corso['categoria'],
            "immagine_corso": immagine_corso,
            "nome_docente": corso['nome_docente'],
            "prerequisiti": prerequisiti
        }
        success = dao.add_course(nuovo_corso)
        if success:
            flash('Corso creato correttamente', 'success')   
        else:
            flash('Errore nella creazione del corso', 'danger')   

    else:
        flash('L\'immagine non può essere vuota', 'warning')   

    return redirect(url_for('home'))

        
@app.route('/courses/<int:id>')
@login_required
def single_course(id):
    
    corso = dao.get_corso_by_id(id)
    #crea oggetto corso
    ogg_corso = Corso(corso[0],corso[1],corso[2],corso[3],corso[4],
                      corso[5],corso[6]) 
    
    n_iscritti = dao.get_n_iscritti_by_corso(id) 
    ogg_corso.n_iscritti = n_iscritti[0]
    user = dao.get_user_by_mail(ogg_corso.nome_docente)
    ogg_corso.creatore = user
    
    if(current_user.is_authenticated): 
        id_utente = current_user.mail
        # current_user is studente?
        if(current_user.docente == 0):
            # -> SI: chiedo al database se è presente nella tabella iscritti con il corso id_corso 
            iscritto = dao.is_iscritto(id_utente, id)    # è presente nel database?
            ogg_corso.frequenta_cu = False
            ogg_corso.materiale = False

            if(iscritto):      
                # -> SI: PULSANTE DISCISCRIVITI + PULSANTE AVVISI + PULSANTE MATERIALE
                ogg_corso.frequenta_cu = True
                ogg_corso.materiale = True

        # -> NO: PULSANTE ISCRIVITI        
        else: # -> NO: current_user is docente? 
             # -> DOCENTE_SI: PULSANTE AVVISI E MATERIALE
            ogg_corso.materiale = True

       

    return render_template('course.html', corso=ogg_corso )


@app.route('/courses/<int:id>/subscription', methods=['POST'])
@login_required
def subscription(id):
    id_utente = current_user.mail
    sub = request.form.get('selezione')
    if sub == 'true':
        dao.disiscriviti(id_utente, id)
    if sub == 'false':
        dao.iscrizione(id_utente, id)
    return redirect(url_for('single_course', id=id))


@app.route('/courses/<int:id>/materials', methods=['GET', 'POST'])
@login_required
def materials(id):

    corso = dao.get_corso_by_id(id)
    
    materiali = dao.get_all_materials_by_corso(id)
    

    return render_template('materials.html', materiali=materiali, corso=corso)

@app.route('/courses/<int:id>/materials/new', methods=['POST'])
@login_required
def new_material(id):

    materiale = request.form.to_dict()

    if materiale['titolo'] == '':
        app.logger.error('Il titolo del corso non può essere vuoto!')
        flash(
            'Materiale non caricato correttamente: il titolo del materiale non può essere vuoto!', 'danger')
        return redirect(url_for('materials', id=id))

    file_path = request.files['path']
    #print(file_path)
    if file_path :

        ext = file_path.filename.split('.')[1]
        file_path.save('static/' + 'materiale' + str(materiale['titolo']) + '.' + ext) 
        pdf = 'materiale' +str(materiale['titolo']) + '.' + ext

        nuovo_materiale = {
            'path' : pdf,
            'id_corso' : id,
            'titolo': materiale['titolo']
        }
        success = dao.add_materials(nuovo_materiale)
        if success:
            flash('Materiale caricato correttamente', 'success')   
        else:
            flash('Errore nel caricamento del materiale', 'danger')   

    else:
        flash('Il file non può essere vuoto', 'warning')   
    
    return redirect(url_for('materials', id=id))


@app.route('/courses/<int:id>/communications', methods=['GET', 'POST'])
@login_required
def avvisi(id):

    corso = dao.get_corso_by_id(id)
    creatore = dao.get_user_by_mail(corso['nome_docente'])
    avvisi = dao.get_all_avvisi_by_corso(id)

    return render_template('communications.html', avvisi=avvisi, corso=corso, creatore=creatore)

@app.route('/courses/<int:id>/communications/new', methods=['POST'])
@login_required
def new_avviso(id):

    corso = dao.get_corso_by_id(id)
    avviso = request.form.to_dict()
    
    id_utente = current_user.mail


    if avviso['testo'] == '':
        app.logger.error('Il testo non può essere vuoto!')
        flash(
            'Avviso non caricato correttamente: il testo dell\'avviso non può essere vuoto!', 'danger')
        return redirect(url_for('avviso', id=id))
    
    nuovo_avviso = {
        "testo" : avviso['testo'],
        "id_corso": id
    }

    success = dao.add_avviso(nuovo_avviso)
    if success:
        flash('Avviso pubblicato correttamente', 'success')   
    else:
        flash('Errore nella pubblicazione dell\' avviso', 'danger')   


    return redirect(url_for('avvisi', id=id))

@app.route('/communications/<int:id_avviso>', methods=['GET', 'POST'])
@login_required
def single_communication(id_avviso):

    avviso = dao.get_avviso_by_id(id_avviso)
    corso = dao.get_corso_by_id(avviso['id_corso'])
    creatore = dao.get_user_by_mail(corso['nome_docente'])
    comments = dao.get_comments(avviso['id_avviso'])

    return render_template('single_communication.html', avviso=avviso, corso=corso, creatore=creatore, comments=comments)
 
@app.route('/communications/<int:id_avviso>/comments/new',  methods=['POST'])
@login_required
def new_comment(id_avviso):
    comment = request.form.to_dict()
    if comment['testo_commento'] == '':
        app.logger.error('Il commento non può essere vuoto!')
        flash(
            'Commento non creato correttamente: il commento non può essere vuoto!', 'danger')
        return redirect(url_for('single_communication', id_avviso=id_avviso))

    mail = current_user.mail
    success = dao.add_comment(comment, mail)

    if success:
        flash('Commento creato correttamente', 'success')
    else:
        flash('Errore nella creazione del commento: riprova!', 'danger')

    return redirect(url_for('single_communication', id_avviso=id_avviso))

@app.route('/communications/<int:id_avviso>/comments/delete',  methods=['POST'])
@login_required
def delete_comment(id_avviso):

    comment = request.form.to_dict()
    id_commento = comment['id_commento']
    success = dao.delete_comment(id_commento)

    if success:
            flash('Commento eliminato con successo!', 'success')  
    else:
            flash('Errore nell\'eliminazione del commento', 'danger') 

    return redirect(url_for('single_communication', id_avviso=id_avviso))


@app.route('/communications/<int:id_avviso>/comments/update',  methods=['POST'])
@login_required
def update_comment(id_avviso):

    comment = request.form.to_dict()
    
    success = dao.update_comment(comment)
    
    if success:
            flash('Commento modificato!', 'success')  
    else:
            flash('Errore nell\'eliminazione del commento', 'danger')  

    return redirect(url_for('single_communication', id_avviso=id_avviso))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)