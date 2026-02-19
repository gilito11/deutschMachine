from django.core.management.base import BaseCommand
from core.models import Language
from vocabulary.models import Topic, VocabularyItem


TOPICS_DATA = [
    # ENGLISH A1
    {
        'lang': 'en', 'name': 'Greetings & Basics', 'slug': 'en-greetings-basics',
        'category': 'daily_life', 'level': 'A1', 'icon': '\U0001F44B', 'sort': 1,
        'description': 'Essential greetings and basic phrases for everyday interactions.',
        'words': [
            ('Hello', 'Hola', 'phrase', '', 'Hello, how are you?', 'Hola, como estas?'),
            ('Good morning', 'Buenos dias', 'phrase', '', 'Good morning, nice day today!', 'Buenos dias, buen dia hoy!'),
            ('Goodbye', 'Adios', 'phrase', '', 'Goodbye, see you tomorrow!', 'Adios, nos vemos manana!'),
            ('Please', 'Por favor', 'adv', '', 'Could you help me, please?', 'Podrias ayudarme, por favor?'),
            ('Thank you', 'Gracias', 'phrase', '', 'Thank you very much!', 'Muchas gracias!'),
            ("You're welcome", 'De nada', 'phrase', '', "You're welcome, no problem.", 'De nada, no hay problema.'),
            ('Excuse me', 'Disculpe', 'phrase', '', 'Excuse me, where is the station?', 'Disculpe, donde esta la estacion?'),
            ('Sorry', 'Lo siento', 'phrase', '', "I'm sorry, I didn't understand.", 'Lo siento, no entendi.'),
            ('Yes', 'Si', 'adv', '', 'Yes, I agree.', 'Si, estoy de acuerdo.'),
            ('No', 'No', 'adv', '', 'No, thank you.', 'No, gracias.'),
            ('How are you?', 'Como estas?', 'phrase', '', 'Hi! How are you today?', 'Hola! Como estas hoy?'),
            ('Nice to meet you', 'Encantado/a de conocerte', 'phrase', '', 'Nice to meet you, I am Eric.', 'Encantado de conocerte, soy Eric.'),
            ('My name is...', 'Me llamo...', 'phrase', '', 'My name is Eric, I am from Spain.', 'Me llamo Eric, soy de Espana.'),
            ('I dont understand', 'No entiendo', 'phrase', '', "I'm sorry, I don't understand.", 'Lo siento, no entiendo.'),
            ('Could you repeat that?', 'Podrias repetir eso?', 'phrase', '', 'Could you repeat that, please?', 'Podrias repetir eso, por favor?'),
            ('Do you speak English?', 'Hablas ingles?', 'phrase', '', 'Excuse me, do you speak English?', 'Disculpe, hablas ingles?'),
        ]
    },
    {
        'lang': 'en', 'name': 'At the Supermarket', 'slug': 'en-supermarket',
        'category': 'daily_life', 'level': 'A1', 'icon': '\U0001F6D2', 'sort': 2,
        'description': 'Vocabulary for grocery shopping at Migros, Coop, or Aldi.',
        'words': [
            ('bread', 'pan', 'noun', '', 'I need to buy some bread.', 'Necesito comprar pan.'),
            ('milk', 'leche', 'noun', '', 'Could I have a liter of milk?', 'Podria tener un litro de leche?'),
            ('water', 'agua', 'noun', '', 'A bottle of water, please.', 'Una botella de agua, por favor.'),
            ('fruit', 'fruta', 'noun', '', 'The fruit is very fresh here.', 'La fruta esta muy fresca aqui.'),
            ('vegetables', 'verduras', 'noun', '', 'I buy vegetables every week.', 'Compro verduras cada semana.'),
            ('cheese', 'queso', 'noun', '', 'Swiss cheese is delicious.', 'El queso suizo es delicioso.'),
            ('meat', 'carne', 'noun', '', 'How much is this meat?', 'Cuanto cuesta esta carne?'),
            ('eggs', 'huevos', 'noun', '', 'A dozen eggs, please.', 'Una docena de huevos, por favor.'),
            ('rice', 'arroz', 'noun', '', 'I need a bag of rice.', 'Necesito una bolsa de arroz.'),
            ('bag', 'bolsa', 'noun', '', 'Do you need a bag?', 'Necesitas una bolsa?'),
            ('receipt', 'recibo / ticket', 'noun', '', 'Could I have the receipt?', 'Podria darme el recibo?'),
            ('How much does this cost?', 'Cuanto cuesta esto?', 'phrase', '', 'How much does this cheese cost?', 'Cuanto cuesta este queso?'),
            ('cheap', 'barato', 'adj', '', 'This brand is cheaper.', 'Esta marca es mas barata.'),
            ('expensive', 'caro', 'adj', '', 'Switzerland is quite expensive.', 'Suiza es bastante cara.'),
            ('to pay', 'pagar', 'verb', '', 'Can I pay by card?', 'Puedo pagar con tarjeta?'),
        ]
    },
    {
        'lang': 'en', 'name': 'Public Transport', 'slug': 'en-public-transport',
        'category': 'travel', 'level': 'A1', 'icon': '\U0001F68A', 'sort': 3,
        'description': 'Getting around by train, tram, and bus in Switzerland.',
        'words': [
            ('train', 'tren', 'noun', '', 'The train to Zurich leaves at 9.', 'El tren a Zurich sale a las 9.'),
            ('bus', 'autobus', 'noun', '', 'Which bus goes to the center?', 'Que autobus va al centro?'),
            ('tram', 'tranvia', 'noun', '', 'Take tram number 4.', 'Coge el tranvia numero 4.'),
            ('station', 'estacion', 'noun', '', 'Where is the train station?', 'Donde esta la estacion de tren?'),
            ('ticket', 'billete', 'noun', '', 'One ticket to Bern, please.', 'Un billete a Berna, por favor.'),
            ('platform', 'anden', 'noun', '', 'The train departs from platform 3.', 'El tren sale del anden 3.'),
            ('stop', 'parada', 'noun', '', 'The next stop is Hauptbahnhof.', 'La siguiente parada es Hauptbahnhof.'),
            ('single ticket', 'billete de ida', 'noun', '', 'A single ticket to the airport.', 'Un billete de ida al aeropuerto.'),
            ('return ticket', 'billete de ida y vuelta', 'noun', '', 'A return ticket is cheaper.', 'Un billete de ida y vuelta es mas barato.'),
            ('timetable', 'horario', 'noun', '', 'Check the timetable on the app.', 'Mira el horario en la app.'),
            ('delay', 'retraso', 'noun', '', 'The train has a 5-minute delay.', 'El tren tiene un retraso de 5 minutos.'),
            ('to arrive', 'llegar', 'verb', '', 'What time does it arrive?', 'A que hora llega?'),
            ('to depart', 'salir', 'verb', '', 'The bus departs every 10 minutes.', 'El bus sale cada 10 minutos.'),
            ('to change', 'hacer transbordo', 'verb', '', 'You need to change at Bern.', 'Necesitas hacer transbordo en Berna.'),
            ('half-fare card', 'tarjeta medio billete', 'noun', '', 'A half-fare card saves you 50%.', 'La tarjeta medio billete te ahorra un 50%.'),
        ]
    },
    {
        'lang': 'en', 'name': 'Job Interview', 'slug': 'en-job-interview',
        'category': 'work', 'level': 'A2', 'icon': '\U0001F4BC', 'sort': 10,
        'description': 'Vocabulary and phrases for job interviews in English.',
        'words': [
            ('interview', 'entrevista', 'noun', '', 'I have a job interview tomorrow.', 'Tengo una entrevista de trabajo manana.'),
            ('resume / CV', 'curriculum', 'noun', '', 'Please send your CV by email.', 'Por favor envia tu curriculum por email.'),
            ('experience', 'experiencia', 'noun', '', 'I have 3 years of experience.', 'Tengo 3 anos de experiencia.'),
            ('skills', 'habilidades', 'noun', '', 'What are your main skills?', 'Cuales son tus principales habilidades?'),
            ('salary', 'salario', 'noun', '', 'What are your salary expectations?', 'Cuales son tus expectativas salariales?'),
            ('full-time', 'tiempo completo', 'adj', '', 'Is this a full-time position?', 'Es un puesto a tiempo completo?'),
            ('part-time', 'medio tiempo', 'adj', '', 'I am looking for part-time work.', 'Busco trabajo a medio tiempo.'),
            ('team', 'equipo', 'noun', '', 'I enjoy working in a team.', 'Disfruto trabajar en equipo.'),
            ('deadline', 'fecha limite', 'noun', '', 'I always meet my deadlines.', 'Siempre cumplo mis fechas limite.'),
            ('strength', 'fortaleza', 'noun', '', 'My biggest strength is problem-solving.', 'Mi mayor fortaleza es resolver problemas.'),
            ('weakness', 'debilidad', 'noun', '', 'What is your biggest weakness?', 'Cual es tu mayor debilidad?'),
            ('Tell me about yourself', 'Hablame de ti', 'phrase', '', 'Tell me about yourself and your background.', 'Hablame de ti y tu experiencia.'),
            ('Why do you want this job?', 'Por que quieres este trabajo?', 'phrase', '', '', ''),
            ('I am available from...', 'Estoy disponible desde...', 'phrase', '', 'I am available from March.', 'Estoy disponible desde marzo.'),
            ('to hire', 'contratar', 'verb', '', 'We will hire someone by next week.', 'Contrataremos a alguien la proxima semana.'),
            ('notice period', 'periodo de preaviso', 'noun', '', 'My notice period is one month.', 'Mi periodo de preaviso es un mes.'),
        ]
    },
    {
        'lang': 'en', 'name': 'Renting an Apartment', 'slug': 'en-renting-apartment',
        'category': 'daily_life', 'level': 'A2', 'icon': '\U0001F3E0', 'sort': 11,
        'description': 'Essential vocabulary for apartment hunting in Switzerland.',
        'words': [
            ('apartment', 'piso / apartamento', 'noun', '', 'I am looking for a 2-room apartment.', 'Busco un piso de 2 habitaciones.'),
            ('rent', 'alquiler', 'noun', '', 'The monthly rent is 1500 CHF.', 'El alquiler mensual es 1500 CHF.'),
            ('deposit', 'deposito / fianza', 'noun', '', 'The deposit is 3 months rent.', 'El deposito es 3 meses de alquiler.'),
            ('lease', 'contrato de alquiler', 'noun', '', 'The lease is for one year.', 'El contrato de alquiler es por un ano.'),
            ('landlord', 'propietario/a', 'noun', '', 'The landlord lives upstairs.', 'El propietario vive arriba.'),
            ('tenant', 'inquilino/a', 'noun', '', 'I am a new tenant.', 'Soy un inquilino nuevo.'),
            ('furnished', 'amueblado', 'adj', '', 'Is the apartment furnished?', 'El piso esta amueblado?'),
            ('unfurnished', 'sin amueblar', 'adj', '', 'Most Swiss apartments are unfurnished.', 'La mayoria de pisos suizos no estan amueblados.'),
            ('utilities', 'gastos / suministros', 'noun', '', 'Are utilities included in the rent?', 'Los gastos estan incluidos en el alquiler?'),
            ('kitchen', 'cocina', 'noun', '', 'The kitchen has a dishwasher.', 'La cocina tiene lavavajillas.'),
            ('bedroom', 'dormitorio', 'noun', '', 'The apartment has two bedrooms.', 'El piso tiene dos dormitorios.'),
            ('bathroom', 'bano', 'noun', '', 'There is a shared bathroom.', 'Hay un bano compartido.'),
            ('balcony', 'balcon', 'noun', '', 'The apartment has a nice balcony.', 'El piso tiene un bonito balcon.'),
            ('floor', 'planta / piso', 'noun', '', 'The apartment is on the third floor.', 'El piso esta en la tercera planta.'),
            ('to move in', 'mudarse', 'verb', '', 'I can move in next month.', 'Puedo mudarme el mes que viene.'),
            ('Nebenkosten', 'gastos adicionales', 'noun', '', 'Nebenkosten are extra monthly charges.', 'Los Nebenkosten son cargos mensuales extra.'),
        ]
    },
    {
        'lang': 'en', 'name': 'Making Friends', 'slug': 'en-making-friends',
        'category': 'social', 'level': 'A2', 'icon': '\U0001F91D', 'sort': 12,
        'description': 'Phrases for socializing and making friends in a new city.',
        'words': [
            ('Where are you from?', 'De donde eres?', 'phrase', '', 'Where are you from originally?', 'De donde eres originalmente?'),
            ('I just moved here', 'Acabo de mudarme aqui', 'phrase', '', 'I just moved here from Spain.', 'Acabo de mudarme aqui desde Espana.'),
            ("Let's grab a coffee", 'Vamos a tomar un cafe', 'phrase', '', "Let's grab a coffee after work.", 'Vamos a tomar un cafe despues del trabajo.'),
            ('hobby', 'aficion / hobby', 'noun', '', 'What are your hobbies?', 'Cuales son tus aficiones?'),
            ('weekend', 'fin de semana', 'noun', '', 'What are you doing this weekend?', 'Que haces este fin de semana?'),
            ('to hang out', 'quedar / pasar el rato', 'verb', '', "Do you want to hang out Saturday?", 'Quieres quedar el sabado?'),
            ('party', 'fiesta', 'noun', '', 'There is a party on Friday.', 'Hay una fiesta el viernes.'),
            ('bar', 'bar', 'noun', '', 'Do you know a good bar nearby?', 'Conoces un buen bar por aqui?'),
            ('restaurant', 'restaurante', 'noun', '', "Let's try that new restaurant.", 'Vamos a probar ese restaurante nuevo.'),
            ('hike', 'excursion / caminata', 'noun', '', 'Want to go for a hike on Sunday?', 'Quieres ir de excursion el domingo?'),
            ('to invite', 'invitar', 'verb', '', "I'd like to invite you for dinner.", 'Me gustaria invitarte a cenar.'),
            ('cheers!', 'salud!', 'phrase', '', 'Cheers! To new friends!', 'Salud! Por los nuevos amigos!'),
            ('fun', 'divertido', 'adj', '', 'That sounds like fun!', 'Eso suena divertido!'),
            ("What's your number?", 'Cual es tu numero?', 'phrase', '', "What's your number? I'll text you.", 'Cual es tu numero? Te escribo.'),
            ('See you later!', 'Nos vemos!', 'phrase', '', 'See you later, it was nice meeting you!', 'Nos vemos, fue un placer conocerte!'),
        ]
    },
    # GERMAN A1
    {
        'lang': 'de', 'name': 'Gruesse & Grundlagen', 'slug': 'de-gruesse-grundlagen',
        'category': 'daily_life', 'level': 'A1', 'icon': '\U0001F44B', 'sort': 1,
        'description': 'Grundlegende Begruessungen und Redewendungen. Swiss German variants included.',
        'country_context': '',
        'words': [
            ('Guten Tag', 'Buenos dias (formal)', 'phrase', '', 'Guten Tag, wie geht es Ihnen?', 'Buenos dias, como esta usted?'),
            ('Hallo', 'Hola', 'phrase', '', 'Hallo, wie gehts?', 'Hola, que tal?'),
            ('Grüezi', 'Buenos dias (suizo)', 'phrase', '', 'Grüezi mitenand!', 'Buenos dias a todos!', 'CH'),
            ('Tschüss', 'Adios (informal)', 'phrase', '', 'Tschüss, bis morgen!', 'Adios, hasta manana!'),
            ('Auf Wiedersehen', 'Hasta la vista (formal)', 'phrase', '', 'Auf Wiedersehen und danke!', 'Hasta la vista y gracias!'),
            ('Bitte', 'Por favor', 'adv', '', 'Ein Kaffee, bitte.', 'Un cafe, por favor.'),
            ('Danke', 'Gracias', 'adv', '', 'Danke schoen!', 'Muchas gracias!'),
            ('Merci vielmal', 'Muchas gracias (suizo)', 'phrase', '', 'Merci vielmal fuer Ihri Hilf!', 'Muchas gracias por su ayuda!', 'CH'),
            ('Entschuldigung', 'Disculpe / Perdon', 'phrase', '', 'Entschuldigung, wo ist die Toilette?', 'Disculpe, donde esta el bano?'),
            ('Ja', 'Si', 'adv', '', 'Ja, natuerlich!', 'Si, por supuesto!'),
            ('Nein', 'No', 'adv', '', 'Nein, danke.', 'No, gracias.'),
            ('Ich verstehe nicht', 'No entiendo', 'phrase', '', 'Entschuldigung, ich verstehe nicht.', 'Disculpe, no entiendo.'),
            ('Sprechen Sie Englisch?', 'Habla usted ingles?', 'phrase', '', 'Entschuldigung, sprechen Sie Englisch?', 'Disculpe, habla usted ingles?'),
            ('Ich heisse...', 'Me llamo...', 'phrase', '', 'Ich heisse Eric, ich komme aus Spanien.', 'Me llamo Eric, vengo de Espana.'),
            ('Wie heissen Sie?', 'Como se llama usted?', 'phrase', '', 'Guten Tag, wie heissen Sie?', 'Buenos dias, como se llama usted?'),
        ]
    },
    {
        'lang': 'de', 'name': 'Im Supermarkt', 'slug': 'de-im-supermarkt',
        'category': 'daily_life', 'level': 'A1', 'icon': '\U0001F6D2', 'sort': 2,
        'description': 'Einkaufen bei Migros, Coop, Aldi und Lidl.',
        'words': [
            ('das Brot', 'el pan', 'noun', 'das', 'Ich haette gern ein Brot, bitte.', 'Quisiera un pan, por favor.'),
            ('die Milch', 'la leche', 'noun', 'die', 'Ein Liter Milch, bitte.', 'Un litro de leche, por favor.'),
            ('das Wasser', 'el agua', 'noun', 'das', 'Eine Flasche Wasser, bitte.', 'Una botella de agua, por favor.'),
            ('das Obst', 'la fruta', 'noun', 'das', 'Das Obst ist sehr frisch.', 'La fruta esta muy fresca.'),
            ('das Gemuese', 'las verduras', 'noun', 'das', 'Ich kaufe viel Gemuese.', 'Compro muchas verduras.'),
            ('der Kaese', 'el queso', 'noun', 'der', 'Schweizer Kaese ist weltbekannt.', 'El queso suizo es mundialmente famoso.'),
            ('das Fleisch', 'la carne', 'noun', 'das', 'Wie viel kostet das Fleisch?', 'Cuanto cuesta la carne?'),
            ('die Eier', 'los huevos', 'noun', 'die', 'Sechs Eier, bitte.', 'Seis huevos, por favor.'),
            ('die Kasse', 'la caja', 'noun', 'die', 'Wo ist die Kasse?', 'Donde esta la caja?'),
            ('der Preis', 'el precio', 'noun', 'der', 'Was ist der Preis?', 'Cual es el precio?'),
            ('billig', 'barato', 'adj', '', 'Das ist sehr billig.', 'Eso es muy barato.'),
            ('teuer', 'caro', 'adj', '', 'Die Schweiz ist teuer.', 'Suiza es cara.'),
            ('die Tuete', 'la bolsa', 'noun', 'die', 'Brauchen Sie eine Tuete?', 'Necesita una bolsa?'),
            ('bezahlen', 'pagar', 'verb', '', 'Kann ich mit Karte bezahlen?', 'Puedo pagar con tarjeta?'),
            ('die Quittung', 'el recibo', 'noun', 'die', 'Kann ich die Quittung haben?', 'Puedo tener el recibo?'),
        ]
    },
    {
        'lang': 'de', 'name': 'Oeffentliche Verkehrsmittel', 'slug': 'de-oeffentliche-verkehrsmittel',
        'category': 'travel', 'level': 'A1', 'icon': '\U0001F68A', 'sort': 3,
        'description': 'Mit dem Zug, Tram und Bus unterwegs. SBB, ZVV, und mehr.',
        'words': [
            ('der Zug', 'el tren', 'noun', 'der', 'Der Zug nach Zuerich faehrt um 9 Uhr.', 'El tren a Zurich sale a las 9.'),
            ('der Bus', 'el autobus', 'noun', 'der', 'Welcher Bus faehrt ins Zentrum?', 'Que autobus va al centro?'),
            ('die Strassenbahn', 'el tranvia', 'noun', 'die', 'Nehmen Sie die Strassenbahn Nummer 4.', 'Coja el tranvia numero 4.'),
            ('s Tram', 'el tranvia (suizo)', 'noun', 'das', 'S Tram chunnt grad.', 'El tranvia viene ahora.', 'CH'),
            ('der Bahnhof', 'la estacion de tren', 'noun', 'der', 'Wo ist der Bahnhof?', 'Donde esta la estacion?'),
            ('die Fahrkarte', 'el billete', 'noun', 'die', 'Eine Fahrkarte nach Bern, bitte.', 'Un billete a Berna, por favor.'),
            ('s Billett', 'el billete (suizo)', 'noun', 'das', 'Es Billett bitte.', 'El billete, por favor.', 'CH'),
            ('das Gleis', 'el anden', 'noun', 'das', 'Der Zug faehrt von Gleis 3 ab.', 'El tren sale del anden 3.'),
            ('die Haltestelle', 'la parada', 'noun', 'die', 'Die naechste Haltestelle ist Paradeplatz.', 'La siguiente parada es Paradeplatz.'),
            ('umsteigen', 'hacer transbordo', 'verb', '', 'Sie muessen in Bern umsteigen.', 'Tiene que hacer transbordo en Berna.'),
            ('abfahren', 'salir / partir', 'verb', '', 'Wann faehrt der Zug ab?', 'Cuando sale el tren?'),
            ('ankommen', 'llegar', 'verb', '', 'Wann kommt der Zug an?', 'Cuando llega el tren?'),
            ('die Verspaetung', 'el retraso', 'noun', 'die', 'Der Zug hat 5 Minuten Verspaetung.', 'El tren tiene 5 minutos de retraso.'),
            ('das Halbtax', 'la tarjeta medio billete', 'noun', 'das', 'Mit dem Halbtax zahlen Sie die Haelfte.', 'Con el Halbtax paga la mitad.', 'CH'),
            ('hin und zurueck', 'ida y vuelta', 'phrase', '', 'Einmal Bern, hin und zurueck.', 'Una vez Berna, ida y vuelta.'),
        ]
    },
    {
        'lang': 'de', 'name': 'Vorstellungsgespraech', 'slug': 'de-vorstellungsgespraech',
        'category': 'work', 'level': 'A2', 'icon': '\U0001F4BC', 'sort': 10,
        'description': 'Wortschatz fuer das Vorstellungsgespraech auf Deutsch.',
        'words': [
            ('das Vorstellungsgespraech', 'la entrevista de trabajo', 'noun', 'das', 'Ich habe morgen ein Vorstellungsgespraech.', 'Tengo una entrevista de trabajo manana.'),
            ('der Lebenslauf', 'el curriculum', 'noun', 'der', 'Bitte senden Sie Ihren Lebenslauf.', 'Por favor envie su curriculum.'),
            ('die Erfahrung', 'la experiencia', 'noun', 'die', 'Ich habe 3 Jahre Erfahrung.', 'Tengo 3 anos de experiencia.'),
            ('das Gehalt', 'el salario', 'noun', 'das', 'Was sind Ihre Gehaltsvorstellungen?', 'Cuales son sus expectativas salariales?'),
            ('die Stelle', 'el puesto', 'noun', 'die', 'Ich bewerbe mich um diese Stelle.', 'Me postulo para este puesto.'),
            ('Vollzeit', 'tiempo completo', 'noun', '', 'Ist das eine Vollzeitstelle?', 'Es un puesto a tiempo completo?'),
            ('Teilzeit', 'medio tiempo', 'noun', '', 'Ich suche Teilzeitarbeit.', 'Busco trabajo a medio tiempo.'),
            ('die Staerke', 'la fortaleza', 'noun', 'die', 'Meine groesste Staerke ist Teamarbeit.', 'Mi mayor fortaleza es el trabajo en equipo.'),
            ('die Schwaeche', 'la debilidad', 'noun', 'die', 'Was ist Ihre groesste Schwaeche?', 'Cual es su mayor debilidad?'),
            ('sich bewerben', 'postularse', 'verb', '', 'Ich moechte mich bewerben.', 'Quiero postularme.'),
            ('die Kuendigungsfrist', 'el periodo de preaviso', 'noun', 'die', 'Meine Kuendigungsfrist betraegt einen Monat.', 'Mi periodo de preaviso es de un mes.'),
            ('Erzaehlen Sie von sich', 'Cuenteme sobre usted', 'phrase', '', 'Erzaehlen Sie uns etwas ueber sich.', 'Cuentenos algo sobre usted.'),
            ('ab sofort verfuegbar', 'disponible de inmediato', 'phrase', '', 'Ich bin ab sofort verfuegbar.', 'Estoy disponible de inmediato.'),
            ('die Arbeitsbewilligung', 'el permiso de trabajo', 'noun', 'die', 'Haben Sie eine Arbeitsbewilligung?', 'Tiene permiso de trabajo?', 'CH'),
            ('die Probezeit', 'el periodo de prueba', 'noun', 'die', 'Die Probezeit dauert drei Monate.', 'El periodo de prueba dura tres meses.'),
        ]
    },
    {
        'lang': 'de', 'name': 'Wohnungssuche', 'slug': 'de-wohnungssuche',
        'category': 'daily_life', 'level': 'A2', 'icon': '\U0001F3E0', 'sort': 11,
        'description': 'Wortschatz fuer die Wohnungssuche in der Schweiz / Deutschland.',
        'words': [
            ('die Wohnung', 'el piso / apartamento', 'noun', 'die', 'Ich suche eine 3-Zimmer-Wohnung.', 'Busco un piso de 3 habitaciones.'),
            ('die Miete', 'el alquiler', 'noun', 'die', 'Die Miete betraegt 1500 Franken.', 'El alquiler es de 1500 francos.'),
            ('die Kaution', 'la fianza', 'noun', 'die', 'Die Kaution ist drei Monatsmieten.', 'La fianza es de tres meses de alquiler.'),
            ('der Mietvertrag', 'el contrato de alquiler', 'noun', 'der', 'Bitte unterschreiben Sie den Mietvertrag.', 'Por favor firme el contrato de alquiler.'),
            ('der Vermieter', 'el propietario', 'noun', 'der', 'Der Vermieter wohnt im Erdgeschoss.', 'El propietario vive en la planta baja.'),
            ('der Mieter', 'el inquilino', 'noun', 'der', 'Ich bin ein neuer Mieter.', 'Soy un inquilino nuevo.'),
            ('die Nebenkosten', 'los gastos adicionales', 'noun', 'die', 'Sind die Nebenkosten inklusive?', 'Los gastos adicionales estan incluidos?'),
            ('die Kueche', 'la cocina', 'noun', 'die', 'Die Kueche hat einen Geschirrspueler.', 'La cocina tiene lavavajillas.'),
            ('das Schlafzimmer', 'el dormitorio', 'noun', 'das', 'Die Wohnung hat zwei Schlafzimmer.', 'El piso tiene dos dormitorios.'),
            ('das Badezimmer', 'el bano', 'noun', 'das', 'Das Badezimmer ist renoviert.', 'El bano esta renovado.'),
            ('der Balkon', 'el balcon', 'noun', 'der', 'Die Wohnung hat einen schoenen Balkon.', 'El piso tiene un bonito balcon.'),
            ('das Stockwerk', 'la planta', 'noun', 'das', 'Die Wohnung ist im dritten Stockwerk.', 'El piso esta en la tercera planta.'),
            ('einziehen', 'mudarse (entrar)', 'verb', '', 'Wann kann ich einziehen?', 'Cuando puedo mudarme?'),
            ('die Besichtigung', 'la visita (de piso)', 'noun', 'die', 'Kann ich eine Besichtigung vereinbaren?', 'Puedo concertar una visita?'),
            ('moebliert', 'amueblado', 'adj', '', 'Ist die Wohnung moebliert?', 'El piso esta amueblado?'),
        ]
    },
    {
        'lang': 'de', 'name': 'Freunde treffen', 'slug': 'de-freunde-treffen',
        'category': 'social', 'level': 'A2', 'icon': '\U0001F91D', 'sort': 12,
        'description': 'Sich verabreden, Smalltalk und neue Leute kennenlernen.',
        'words': [
            ('Woher kommst du?', 'De donde eres?', 'phrase', '', 'Woher kommst du urspruenglich?', 'De donde eres originalmente?'),
            ('Ich bin gerade hergezogen', 'Acabo de mudarme aqui', 'phrase', '', 'Ich bin gerade aus Spanien hergezogen.', 'Acabo de mudarme desde Espana.'),
            ('das Hobby', 'el hobby / la aficion', 'noun', 'das', 'Was sind deine Hobbys?', 'Cuales son tus hobbies?'),
            ('das Wochenende', 'el fin de semana', 'noun', 'das', 'Was machst du am Wochenende?', 'Que haces el fin de semana?'),
            ('sich treffen', 'quedar / encontrarse', 'verb', '', 'Wollen wir uns am Samstag treffen?', 'Quieres que quedemos el sabado?'),
            ('der Apero', 'el aperitivo', 'noun', 'der', 'Wir machen einen Apero am Freitag.', 'Hacemos un aperitivo el viernes.', 'CH'),
            ('das Bier', 'la cerveza', 'noun', 'das', 'Wollen wir ein Bier trinken?', 'Quieres tomar una cerveza?'),
            ('wandern', 'hacer senderismo', 'verb', '', 'Wollen wir am Sonntag wandern gehen?', 'Quieres ir de senderismo el domingo?'),
            ('Prost!', 'Salud!', 'phrase', '', 'Prost! Auf neue Freundschaften!', 'Salud! Por las nuevas amistades!'),
            ('Spass', 'diversion', 'noun', 'der', 'Das macht Spass!', 'Eso es divertido!'),
            ('einladen', 'invitar', 'verb', '', 'Ich moechte dich zum Essen einladen.', 'Me gustaria invitarte a comer.'),
            ('Bis spaeter!', 'Hasta luego!', 'phrase', '', 'Bis spaeter, es war schoen!', 'Hasta luego, fue genial!'),
            ('Wie ist deine Nummer?', 'Cual es tu numero?', 'phrase', '', 'Wie ist deine Nummer? Ich schreibe dir.', 'Cual es tu numero? Te escribo.'),
            ('Freut mich!', 'Encantado/a!', 'phrase', '', 'Freut mich, dich kennenzulernen!', 'Encantado de conocerte!'),
            ('gemütlich', 'acogedor / agradable', 'adj', '', 'Diese Bar ist sehr gemuetlich.', 'Este bar es muy acogedor.'),
        ]
    },
]


class Command(BaseCommand):
    help = 'Seed vocabulary data for English and German (A1-A2)'

    def handle(self, *args, **options):
        en, _ = Language.objects.update_or_create(code='en', defaults={'name': 'English'})
        de, _ = Language.objects.update_or_create(code='de', defaults={'name': 'German'})
        self.stdout.write(self.style.SUCCESS('Languages created: English, German'))

        langs = {'en': en, 'de': de}
        total_words = 0

        for t in TOPICS_DATA:
            lang = langs[t['lang']]
            topic, created = Topic.objects.update_or_create(
                slug=t['slug'],
                defaults={
                    'language': lang,
                    'name': t['name'],
                    'description': t.get('description', ''),
                    'difficulty_level': t['level'],
                    'category': t['category'],
                    'country_context': t.get('country_context', ''),
                    'sort_order': t['sort'],
                    'icon': t['icon'],
                    'is_active': True,
                }
            )
            action = 'CREATED' if created else 'updated'
            self.stdout.write(f'  Topic {action}: {t["name"]} ({t["lang"].upper()} {t["level"]})')

            for w in t['words']:
                word, trans, pos, gender = w[0], w[1], w[2], w[3]
                example = w[4] if len(w) > 4 else ''
                example_trans = w[5] if len(w) > 5 else ''
                region = w[6] if len(w) > 6 else ''

                VocabularyItem.objects.update_or_create(
                    language=lang,
                    topic=topic,
                    word=word,
                    defaults={
                        'translation_es': trans,
                        'part_of_speech': pos,
                        'gender': gender,
                        'example_sentence': example,
                        'example_translation': example_trans,
                        'difficulty_level': t['level'],
                        'region_variant': region,
                    }
                )
                total_words += 1

        self.stdout.write(self.style.SUCCESS(f'\nDone! {len(TOPICS_DATA)} topics, {total_words} vocabulary items.'))
