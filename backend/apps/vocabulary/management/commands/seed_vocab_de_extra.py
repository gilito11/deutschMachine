from django.core.management.base import BaseCommand
from core.models import Language
from vocabulary.models import Topic, VocabularyItem

# Tuple format per word:
# (word, translation_es, pos, gender, plural, ipa, example_sentence, example_translation, region, notes)
# Trailing fields can be omitted (defaults to '')

TOPICS_DATA = [
    {
        'lang': 'de', 'name': 'Beim Arzt', 'slug': 'de-beim-arzt',
        'category': 'daily_life', 'level': 'A2', 'icon': '[Arzt]', 'sort': 20,
        'description': 'Beim Arzt, in der Apotheke und mit der Krankenkasse.',
        'country_context': '',
        'words': [
            ('der Arzt', 'el medico', 'noun', 'der', 'die Aerzte', '', 'Ich muss zum Arzt gehen.', 'Tengo que ir al medico.', '', ''),
            ('die Aerztin', 'la medica', 'noun', 'die', 'die Aerztinnen', '', 'Meine Aerztin spricht Spanisch.', 'Mi medica habla espanol.', '', ''),
            ('der Termin', 'la cita', 'noun', 'der', 'die Termine', '', 'Ich moechte einen Termin vereinbaren.', 'Quisiera concertar una cita.', '', ''),
            ('die Apotheke', 'la farmacia', 'noun', 'die', 'die Apotheken', 'apo-TEE-kuh', 'Wo ist die naechste Apotheke?', 'Donde esta la farmacia mas cercana?', '', ''),
            ('das Rezept', 'la receta medica', 'noun', 'das', 'die Rezepte', '', 'Ich brauche ein Rezept.', 'Necesito una receta medica.', '', ''),
            ('die Krankenkasse', 'el seguro medico obligatorio', 'noun', 'die', 'die Krankenkassen', '', 'Die Krankenkasse ist in der Schweiz obligatorisch.', 'El seguro medico es obligatorio en Suiza.', 'CH', 'Mandatory health insurance in Switzerland; everyone must enroll within 3 months of arrival'),
            ('die Krankenversicherung', 'el seguro medico', 'noun', 'die', 'die Krankenversicherungen', '', 'Haben Sie eine Krankenversicherung?', 'Tiene seguro medico?', '', ''),
            ('die Kopfschmerzen', 'el dolor de cabeza', 'noun', 'die', '', 'KOPF-shmer-tsen', 'Ich habe starke Kopfschmerzen.', 'Tengo un fuerte dolor de cabeza.', '', 'Plural only'),
            ('das Fieber', 'la fiebre', 'noun', 'das', '', '', 'Ich habe Fieber, 38 Grad.', 'Tengo fiebre, 38 grados.', '', ''),
            ('der Husten', 'la tos', 'noun', 'der', '', '', 'Ich habe seit einer Woche Husten.', 'Tengo tos desde hace una semana.', '', ''),
            ('der Schmerz', 'el dolor', 'noun', 'der', 'die Schmerzen', '', 'Wo haben Sie Schmerzen?', 'Donde le duele?', '', ''),
            ('die Allergie', 'la alergia', 'noun', 'die', 'die Allergien', 'a-ler-GEE', 'Ich habe eine Allergie gegen Penicillin.', 'Soy alergico a la penicilina.', '', ''),
            ('die Tablette', 'la pastilla / el comprimido', 'noun', 'die', 'die Tabletten', '', 'Nehmen Sie zwei Tabletten pro Tag.', 'Tome dos pastillas al dia.', '', ''),
            ('der Notfall', 'la emergencia', 'noun', 'der', 'die Notfaelle', '', 'Das ist ein Notfall, rufen Sie 144!', 'Es una emergencia, llame al 144!', 'CH', 'Emergency number in Switzerland: 144'),
            ('krank', 'enfermo/a', 'adj', '', '', '', 'Ich bin krank und kann nicht arbeiten.', 'Estoy enfermo y no puedo trabajar.', '', ''),
            ('gesund', 'sano/a', 'adj', '', '', '', 'Ich moechte wieder gesund werden.', 'Quiero volver a estar sano.', '', ''),
            ('die Selbstbeteiligung', 'la franquicia / el copago', 'noun', 'die', '', '', 'Die Selbstbeteiligung betraegt 300 Franken pro Jahr.', 'La franquicia es de 300 francos al ano.', 'CH', 'The annual deductible (Franchise) in Swiss health insurance'),
            ('die Praxisgebuehr', 'la tasa de consulta', 'noun', 'die', '', '', 'Es gibt keine Praxisgebuehr mehr in der Schweiz.', 'Ya no hay tasa de consulta en Suiza.', 'CH', 'Abolished in Switzerland in 2024'),
        ]
    },
    {
        'lang': 'de', 'name': 'Bank und Geld', 'slug': 'de-bank-und-geld',
        'category': 'daily_life', 'level': 'A2', 'icon': '[Bank]', 'sort': 21,
        'description': 'Bankgeschaefte und Geldangelegenheiten in der Schweiz.',
        'country_context': 'CH',
        'words': [
            ('das Konto', 'la cuenta bancaria', 'noun', 'das', 'die Konten', '', 'Ich moechte ein Konto eroeffnen.', 'Quisiera abrir una cuenta bancaria.', '', ''),
            ('die Ueberweisung', 'la transferencia bancaria', 'noun', 'die', 'die Ueberweisungen', '', 'Ich mache eine Ueberweisung.', 'Hago una transferencia bancaria.', '', ''),
            ('der Geldautomat', 'el cajero automatico', 'noun', 'der', 'die Geldautomaten', '', 'Wo ist der naechste Geldautomat?', 'Donde esta el cajero automatico mas cercano?', '', ''),
            ('das Bargeld', 'el dinero en efectivo', 'noun', 'das', '', '', 'Haben Sie Bargeld dabei?', 'Lleva dinero en efectivo?', '', ''),
            ('der Franken', 'el franco (suizo)', 'noun', 'der', 'die Franken', 'FRAN-ken', 'Das kostet hundert Franken.', 'Eso cuesta cien francos.', 'CH', 'CHF - Swiss Franc, the currency of Switzerland'),
            ('der Wechselkurs', 'el tipo de cambio', 'noun', 'der', 'die Wechselkurse', '', 'Was ist der aktuelle Wechselkurs?', 'Cual es el tipo de cambio actual?', '', ''),
            ('die Kreditkarte', 'la tarjeta de credito', 'noun', 'die', 'die Kreditkarten', '', 'Kann ich mit Kreditkarte zahlen?', 'Puedo pagar con tarjeta de credito?', '', ''),
            ('die Debitkarte', 'la tarjeta de debito', 'noun', 'die', 'die Debitkarten', '', 'Ich bezahle mit Debitkarte.', 'Pago con tarjeta de debito.', '', ''),
            ('Twint', 'Twint (pago movil suizo)', 'noun', '', '', '', 'Kann ich mit Twint zahlen?', 'Puedo pagar con Twint?', 'CH', 'Swiss mobile payment app, widely used in Switzerland instead of cash'),
            ('die PostFinance', 'PostFinance (banco postal suizo)', 'noun', '', '', '', 'Ich habe ein Konto bei der PostFinance.', 'Tengo una cuenta en PostFinance.', 'CH', 'Swiss postal bank, popular with expats for easy account opening'),
            ('die Raiffeisen', 'Raiffeisen (banco cooperativo)', 'noun', '', '', '', 'Meine Bank ist die Raiffeisen.', 'Mi banco es Raiffeisen.', 'CH', 'Swiss cooperative bank, strong presence in smaller towns'),
            ('das Sparbuch', 'la libreta de ahorro', 'noun', 'das', 'die Sparbuechler', '', 'Ich habe ein Sparbuch bei der Bank.', 'Tengo una libreta de ahorro en el banco.', '', ''),
            ('der Kontoauszug', 'el extracto bancario', 'noun', 'der', 'die Kontoauszuege', '', 'Ich moechte einen Kontoauszug.', 'Quisiera un extracto bancario.', '', ''),
            ('die Gebuehr', 'la comision / la tasa', 'noun', 'die', 'die Gebuehren', '', 'Welche Gebuehren fallen an?', 'Que comisiones hay?', '', ''),
            ('ueberweisen', 'transferir (dinero)', 'verb', '', '', '', 'Ich ueberweise den Betrag heute.', 'Transfiero el importe hoy.', '', ''),
            ('abheben', 'retirar (dinero)', 'verb', '', '', '', 'Ich moechte 200 Franken abheben.', 'Quiero retirar 200 francos.', '', ''),
        ]
    },
    {
        'lang': 'de', 'name': 'Im Buero', 'slug': 'de-im-buero',
        'category': 'work', 'level': 'B1', 'icon': '[Buero]', 'sort': 30,
        'description': 'Wortschatz fuer den Arbeitsalltag im Buero.',
        'country_context': '',
        'words': [
            ('die Besprechung', 'la reunion', 'noun', 'die', 'die Besprechungen', '', 'Die Besprechung beginnt um 10 Uhr.', 'La reunion empieza a las 10.', '', ''),
            ('der Kollege', 'el colega / el companero', 'noun', 'der', 'die Kollegen', 'ko-LEE-guh', 'Mein Kollege hilft mir sehr.', 'Mi companero me ayuda mucho.', '', ''),
            ('die Kollegin', 'la colega / la companera', 'noun', 'die', 'die Kolleginnen', '', 'Meine Kollegin kommt aus Brasilien.', 'Mi companera es de Brasil.', '', ''),
            ('der Bericht', 'el informe', 'noun', 'der', 'die Berichte', '', 'Ich schreibe einen Bericht.', 'Estoy escribiendo un informe.', '', ''),
            ('die Deadline', 'la fecha limite', 'noun', 'die', 'die Deadlines', '', 'Die Deadline ist Freitag.', 'La fecha limite es el viernes.', '', ''),
            ('die Ueberstunden', 'las horas extra', 'noun', 'die', '', '', 'Ich muss heute Ueberstunden machen.', 'Tengo que hacer horas extra hoy.', '', 'Usually plural'),
            ('die Befoerderung', 'el ascenso', 'noun', 'die', 'die Befoerderungen', '', 'Ich hoffe auf eine Befoerderung.', 'Espero un ascenso.', '', ''),
            ('die Abteilung', 'el departamento', 'noun', 'die', 'die Abteilungen', '', 'In welcher Abteilung arbeiten Sie?', 'En que departamento trabaja?', '', ''),
            ('der Vorgesetzte', 'el jefe / el superior', 'noun', 'der', 'die Vorgesetzten', '', 'Mein Vorgesetzter ist sehr fair.', 'Mi jefe es muy justo.', '', ''),
            ('die Aufgabe', 'la tarea', 'noun', 'die', 'die Aufgaben', '', 'Ich habe viele Aufgaben heute.', 'Tengo muchas tareas hoy.', '', ''),
            ('das Homeoffice', 'el teletrabajo / trabajo desde casa', 'noun', 'das', '', '', 'Ich arbeite zwei Tage im Homeoffice.', 'Trabajo desde casa dos dias.', '', ''),
            ('der Feierabend', 'el fin de la jornada laboral', 'noun', 'der', '', '', 'Feierabend! Endlich!', 'Fin de la jornada! Por fin!', '', ''),
            ('die Pause', 'el descanso / la pausa', 'noun', 'die', 'die Pausen', '', 'Ich mache jetzt Pause.', 'Ahora hago una pausa.', '', ''),
            ('kuendigen', 'dimitir / renunciar', 'verb', '', '', '', 'Er hat gekuendigt.', 'Ha dimitido.', '', ''),
            ('einstellen', 'contratar', 'verb', '', '', '', 'Wir stellen neue Mitarbeiter ein.', 'Contratamos nuevos empleados.', '', ''),
            ('das Pensum', 'la carga de trabajo / jornada', 'noun', 'das', 'die Pensen', '', 'Ich arbeite ein 80%-Pensum.', 'Trabajo al 80% de jornada.', 'CH', 'Common in Swiss work culture to express part-time as a percentage'),
        ]
    },
    {
        'lang': 'de', 'name': 'Im Restaurant', 'slug': 'de-im-restaurant',
        'category': 'social', 'level': 'A1', 'icon': '[Restaurant]', 'sort': 13,
        'description': 'Essen gehen in der Schweiz - von der Bestellung bis zur Rechnung.',
        'country_context': '',
        'words': [
            ('die Speisekarte', 'la carta / el menu', 'noun', 'die', 'die Speisekarten', '', 'Kann ich die Speisekarte haben?', 'Puedo ver la carta?', '', ''),
            ('die Bestellung', 'el pedido', 'noun', 'die', 'die Bestellungen', '', 'Ich moechte meine Bestellung aufgeben.', 'Quisiera hacer mi pedido.', '', ''),
            ('bestellen', 'pedir', 'verb', '', '', '', 'Ich moechte bestellen.', 'Quisiera pedir.', '', ''),
            ('die Vorspeise', 'el entrante / la entrada', 'noun', 'die', 'die Vorspeisen', '', 'Als Vorspeise nehme ich die Suppe.', 'De entrante tomo la sopa.', '', ''),
            ('das Hauptgericht', 'el plato principal', 'noun', 'das', 'die Hauptgerichte', '', 'Als Hauptgericht haette ich gern das Steak.', 'De plato principal quisiera el filete.', '', ''),
            ('die Nachspeise', 'el postre', 'noun', 'die', 'die Nachspeisen', '', 'Als Nachspeise bitte einen Kaesekuchen.', 'De postre una tarta de queso por favor.', 'CH', 'Nachspeise is used in CH; Nachtisch or Dessert also common'),
            ('die Rechnung', 'la cuenta', 'noun', 'die', 'die Rechnungen', '', 'Die Rechnung bitte!', 'La cuenta por favor!', '', ''),
            ('das Trinkgeld', 'la propina', 'noun', 'das', '', '', 'Das Trinkgeld ist nicht obligatorisch.', 'La propina no es obligatoria.', '', 'In Switzerland tipping is optional, rounding up is common'),
            ('die Serviertochter', 'la camarera', 'noun', 'die', 'die Serviertoechter', '', 'Die Serviertochter bringt die Karte.', 'La camarera trae la carta.', 'CH', 'Swiss German term for waitress; Kellnerin used in Germany'),
            ('der Servicier', 'el camarero', 'noun', 'der', 'die Serviciers', '', 'Entschuldigung, Servicier!', 'Disculpe, camarero!', 'CH', 'Swiss term for waiter in formal restaurants'),
            ('das Nachtessen', 'la cena', 'noun', 'das', '', '', 'Gehen wir zum Nachtessen aus?', 'Salimos a cenar?', 'CH', 'Swiss German for dinner; Abendessen used in Germany'),
            ('das Mittagessen', 'la comida / el almuerzo', 'noun', 'das', '', '', 'Das Mittagessen ist um 12 Uhr.', 'La comida es a las 12.', '', ''),
            ('empfehlen', 'recomendar', 'verb', '', '', '', 'Was empfehlen Sie heute?', 'Que recomienda hoy?', '', ''),
            ('vegetarisch', 'vegetariano/a', 'adj', '', '', '', 'Haben Sie vegetarische Gerichte?', 'Tienen platos vegetarianos?', '', ''),
            ('der Tisch', 'la mesa', 'noun', 'der', 'die Tische', '', 'Einen Tisch fuer zwei, bitte.', 'Una mesa para dos, por favor.', '', ''),
            ('reservieren', 'reservar', 'verb', '', '', '', 'Ich moechte einen Tisch reservieren.', 'Quisiera reservar una mesa.', '', ''),
        ]
    },
    {
        'lang': 'de', 'name': 'Wetter und Jahreszeiten', 'slug': 'de-wetter-jahreszeiten',
        'category': 'daily_life', 'level': 'A1', 'icon': '[Wetter]', 'sort': 5,
        'description': 'Das Wetter und die vier Jahreszeiten in der Schweiz.',
        'country_context': '',
        'words': [
            ('sonnig', 'soleado/a', 'adj', '', '', '', 'Heute ist es sonnig und warm.', 'Hoy hace sol y calor.', '', ''),
            ('bewoelkt', 'nublado/a', 'adj', '', '', '', 'Es ist bewoelkt, kein Sonnenschein.', 'Esta nublado, sin sol.', '', ''),
            ('der Regen', 'la lluvia', 'noun', 'der', '', '', 'Es gibt viel Regen im Herbst.', 'Hay mucha lluvia en otono.', '', ''),
            ('regnen', 'llover', 'verb', '', '', '', 'Es regnet den ganzen Tag.', 'Llueve todo el dia.', '', ''),
            ('der Schnee', 'la nieve', 'noun', 'der', '', '', 'Im Winter gibt es viel Schnee in den Alpen.', 'En invierno hay mucha nieve en los Alpes.', '', ''),
            ('schneien', 'nevar', 'verb', '', '', '', 'Es schneit! Wunderschoen!', 'Esta nevando! Que bonito!', '', ''),
            ('die Temperatur', 'la temperatura', 'noun', 'die', 'die Temperaturen', '', 'Die Temperatur ist unter null.', 'La temperatura esta bajo cero.', '', ''),
            ('der Nebel', 'la niebla', 'noun', 'der', '', '', 'Im November gibt es viel Nebel in der Schweiz.', 'En noviembre hay mucha niebla en Suiza.', '', 'Switzerland is famous for its autumn fog in the Mittelland'),
            ('der Foehn', 'el foehn (viento calido de los Alpes)', 'noun', 'der', '', 'fern (like English)', 'Der Foehn bringt warmes Wetter aus dem Sueden.', 'El foehn trae tiempo calido del sur.', 'CH', 'Warm, dry Alpine wind from the south; can cause headaches'),
            ('die Bise', 'la bise (viento frio del norte)', 'noun', 'die', '', 'BEE-zuh', 'Die Bise macht es sehr kalt.', 'La bise hace mucho frio.', 'CH', 'Cold, dry north-easterly wind typical in Switzerland'),
            ('der Fruehling', 'la primavera', 'noun', 'der', '', '', 'Im Fruehling bluehen die Blumen.', 'En primavera florecen las flores.', '', ''),
            ('der Sommer', 'el verano', 'noun', 'der', '', '', 'Der Sommer in der Schweiz ist schoen.', 'El verano en Suiza es bonito.', '', ''),
            ('der Herbst', 'el otono', 'noun', 'der', '', '', 'Im Herbst faerben sich die Blaetter.', 'En otono cambian de color las hojas.', '', ''),
            ('der Winter', 'el invierno', 'noun', 'der', '', '', 'Im Winter kann es sehr kalt werden.', 'En invierno puede hacer mucho frio.', '', ''),
            ('das Gewitter', 'la tormenta', 'noun', 'das', 'die Gewitter', '', 'Es gibt ein Gewitter heute Abend.', 'Esta tarde hay tormenta.', '', ''),
            ('Wie ist das Wetter?', 'Como esta el tiempo?', 'phrase', '', '', '', 'Wie ist das Wetter morgen?', 'Como esta el tiempo manana?', '', ''),
        ]
    },
    {
        'lang': 'de', 'name': 'Haushalt und Wohnen', 'slug': 'de-haushalt-wohnen',
        'category': 'daily_life', 'level': 'A2', 'icon': '[Haushalt]', 'sort': 22,
        'description': 'Wortschatz fuer den Alltag zu Hause in der Schweiz.',
        'country_context': '',
        'words': [
            ('die Kueche', 'la cocina', 'noun', 'die', 'die Kuechen', '', 'Die Kueche ist gross und modern.', 'La cocina es grande y moderna.', '', ''),
            ('das Badezimmer', 'el cuarto de bano', 'noun', 'das', 'die Badezimmer', '', 'Das Badezimmer hat eine Badewanne.', 'El bano tiene banera.', '', ''),
            ('das Schlafzimmer', 'el dormitorio', 'noun', 'das', 'die Schlafzimmer', '', 'Das Schlafzimmer ist ruhig.', 'El dormitorio es tranquilo.', '', ''),
            ('das Wohnzimmer', 'el salon / la sala de estar', 'noun', 'das', 'die Wohnzimmer', '', 'Wir sitzen im Wohnzimmer.', 'Estamos sentados en el salon.', '', ''),
            ('die Moebl', 'los muebles', 'noun', 'die', '', '', 'Die Moebl sind neu gekauft.', 'Los muebles son recien comprados.', '', ''),
            ('der Vermieter', 'el casero / el propietario', 'noun', 'der', 'die Vermieter', '', 'Der Vermieter repariert die Heizung.', 'El casero repara la calefaccion.', '', ''),
            ('die Heizung', 'la calefaccion', 'noun', 'die', 'die Heizungen', '', 'Die Heizung funktioniert nicht.', 'La calefaccion no funciona.', '', ''),
            ('der Muell', 'la basura', 'noun', 'der', '', '', 'Wo kommt der Muell hin?', 'Donde va la basura?', '', ''),
            ('der Kehricht', 'la basura (suizo)', 'noun', 'der', '', 'KAY-risht', 'Den Kehricht rausbringen bitte.', 'Saca la basura por favor.', 'CH', 'Swiss German word for garbage/trash'),
            ('der Abfallsack', 'la bolsa de basura oficial', 'noun', 'der', 'die Abfallsaecke', '', 'In der Schweiz braucht man spezielle Abfallsaecke.', 'En Suiza se necesitan bolsas de basura oficiales.', 'CH', 'Mandatory paid garbage bags in most Swiss cantons; buying them funds waste disposal'),
            ('die Steckdose', 'el enchufe', 'noun', 'die', 'die Steckdosen', '', 'Wo ist die naechste Steckdose?', 'Donde esta el enchufe mas cercano?', '', ''),
            ('der Strom', 'la electricidad', 'noun', 'der', '', '', 'Der Strom ist ausgefallen.', 'Se ha ido la luz.', '', ''),
            ('die Waschmaschine', 'la lavadora', 'noun', 'die', 'die Waschmaschinen', '', 'Die Waschmaschine ist im Keller.', 'La lavadora esta en el sotano.', '', ''),
            ('der Keller', 'el sotano / el trastero', 'noun', 'der', 'die Keller', '', 'Jede Wohnung hat einen Keller.', 'Cada piso tiene un trastero.', '', ''),
            ('der Hausordnung', 'el reglamento de la casa', 'noun', 'der', '', '', 'Die Hausordnung gilt fuer alle Mieter.', 'El reglamento de la casa es para todos.', '', 'Rules of the building; important to follow in Switzerland'),
            ('aufraumen', 'ordenar / recoger', 'verb', '', '', '', 'Ich raeume heute das Zimmer auf.', 'Hoy ordeno la habitacion.', '', ''),
        ]
    },
    {
        'lang': 'de', 'name': 'Sport und Freizeit', 'slug': 'de-sport-freizeit',
        'category': 'daily_life', 'level': 'B1', 'icon': '[Sport]', 'sort': 31,
        'description': 'Sport treiben und Freizeit geniessen - typisch Schweiz.',
        'country_context': '',
        'words': [
            ('das Fitnessstudio', 'el gimnasio', 'noun', 'das', 'die Fitnessstudios', '', 'Ich gehe dreimal pro Woche ins Fitnessstudio.', 'Voy al gimnasio tres veces a la semana.', '', ''),
            ('wandern', 'hacer senderismo / senderear', 'verb', '', '', '', 'In der Schweiz wandert man viel.', 'En Suiza se hace mucho senderismo.', 'CH', 'Hiking is a national pastime; Switzerland has 65,000 km of marked trails'),
            ('die Wanderung', 'la caminata / la excursion', 'noun', 'die', 'die Wanderungen', '', 'Diese Wanderung dauert drei Stunden.', 'Esta excursion dura tres horas.', '', ''),
            ('das Schwimmbad', 'la piscina', 'noun', 'das', 'die Schwimmbaeder', '', 'Das Schwimmbad ist am Samstag geoeffnet.', 'La piscina esta abierta el sabado.', '', ''),
            ('das Velo', 'la bicicleta', 'noun', 'das', 'die Velos', '', 'Ich fahre mit dem Velo zur Arbeit.', 'Voy al trabajo en bicicleta.', 'CH', 'Swiss German for bicycle; Fahrrad used in Germany'),
            ('das Skifahren', 'el esqui', 'noun', 'das', '', '', 'Skifahren in den Alpen ist ein Erlebnis.', 'Esquiar en los Alpes es una experiencia.', '', ''),
            ('die Skipiste', 'la pista de esqui', 'noun', 'die', 'die Skipisten', '', 'Es gibt viele Skipisten in der Schweiz.', 'Hay muchas pistas de esqui en Suiza.', '', ''),
            ('die SAC-Huette', 'el refugio de montana (SAC)', 'noun', 'die', 'die SAC-Huetten', '', 'Wir uebernachten in einer SAC-Huette.', 'Pernoctamos en un refugio de montana.', 'CH', 'Mountain huts of the Swiss Alpine Club (SAC); bookable online'),
            ('der See', 'el lago', 'noun', 'der', 'die Seen', '', 'Wir schwimmen im See.', 'Nadamos en el lago.', '', 'Switzerland has many beautiful lakes for swimming'),
            ('das Freibad', 'la piscina al aire libre', 'noun', 'das', 'die Freibaeder', '', 'Im Sommer ist das Freibad sehr beliebt.', 'En verano la piscina al aire libre es muy popular.', '', ''),
            ('der Verein', 'el club / la asociacion', 'noun', 'der', 'die Vereine', '', 'Ich bin in einem Sportverein.', 'Estoy en un club deportivo.', '', 'Switzerland has a very strong club culture; joining a Verein is a great way to integrate'),
            ('klettern', 'escalar', 'verb', '', '', '', 'Wir gehen am Wochenende klettern.', 'El fin de semana vamos a escalar.', '', ''),
            ('das Hallenbad', 'la piscina cubierta', 'noun', 'das', 'die Hallenbaeder', '', 'Im Winter gehe ich ins Hallenbad.', 'En invierno voy a la piscina cubierta.', '', ''),
            ('der Spaziergang', 'el paseo', 'noun', 'der', 'die Spaziergaenge', '', 'Ein Spaziergang am Abend ist schoen.', 'Un paseo por la tarde es agradable.', '', ''),
            ('sich erholen', 'descansar / recuperarse', 'verb', '', '', '', 'Ich erhole mich am Wochenende.', 'Me recupero el fin de semana.', '', ''),
        ]
    },
    {
        'lang': 'de', 'name': 'Technik und Internet', 'slug': 'de-technik-internet',
        'category': 'work', 'level': 'A2', 'icon': '[Technik]', 'sort': 23,
        'description': 'Digitaler Alltag: Computer, Internet und Technik.',
        'country_context': '',
        'words': [
            ('das Passwort', 'la contrasena', 'noun', 'das', 'die Passwoerter', '', 'Das Passwort ist sicher.', 'La contrasena es segura.', '', ''),
            ('das WLAN', 'el wifi', 'noun', 'das', '', '', 'Was ist das WLAN-Passwort?', 'Cual es la contrasena del wifi?', '', ''),
            ('herunterladen', 'descargar', 'verb', '', '', '', 'Ich lade die App herunter.', 'Descargo la aplicacion.', '', ''),
            ('hochladen', 'subir / cargar', 'verb', '', '', '', 'Ich lade das Dokument hoch.', 'Subo el documento.', '', ''),
            ('aktualisieren', 'actualizar', 'verb', '', '', 'ak-tu-a-li-ZEE-ren', 'Ich muss das Betriebssystem aktualisieren.', 'Tengo que actualizar el sistema operativo.', '', ''),
            ('der Bildschirm', 'la pantalla', 'noun', 'der', 'die Bildschirme', '', 'Der Bildschirm ist zu dunkel.', 'La pantalla esta demasiado oscura.', '', ''),
            ('der Drucker', 'la impresora', 'noun', 'der', 'die Drucker', '', 'Der Drucker hat kein Papier mehr.', 'A la impresora se le ha acabado el papel.', '', ''),
            ('die Tastatur', 'el teclado', 'noun', 'die', 'die Tastaturen', '', 'Die Tastatur ist kaputt.', 'El teclado esta roto.', '', ''),
            ('die Maus', 'el raton (de ordenador)', 'noun', 'die', 'die Maeusen', '', 'Die Maus funktioniert nicht.', 'El raton no funciona.', '', ''),
            ('der Akku', 'la bateria', 'noun', 'der', 'die Akkus', '', 'Der Akku ist fast leer.', 'La bateria esta casi agotada.', '', ''),
            ('das Handy', 'el movil / el celular', 'noun', 'das', 'die Handys', '', 'Mein Handy ist kaputt.', 'Mi movil esta roto.', '', ''),
            ('die App', 'la aplicacion', 'noun', 'die', 'die Apps', '', 'Gibt es eine App fuer die SBB?', 'Hay una aplicacion para los SBB?', '', ''),
            ('die E-Mail', 'el correo electronico', 'noun', 'die', 'die E-Mails', '', 'Ich schicke Ihnen eine E-Mail.', 'Le envio un correo electronico.', '', ''),
            ('der Anhang', 'el archivo adjunto', 'noun', 'der', 'die Anhaenge', '', 'Bitte schicken Sie den Anhang.', 'Por favor envie el archivo adjunto.', '', ''),
            ('der Absturz', 'el cuelgue / el fallo', 'noun', 'der', 'die Absturzeuen', '', 'Der Computer ist abgestuerzt.', 'El ordenador se ha colgado.', '', ''),
            ('einschalten', 'encender', 'verb', '', '', '', 'Koennen Sie den Computer einschalten?', 'Puede encender el ordenador?', '', ''),
        ]
    },
    {
        'lang': 'de', 'name': 'Behoerden und Dokumente', 'slug': 'de-behoerden-dokumente',
        'category': 'culture', 'level': 'B1', 'icon': '[Behoerden]', 'sort': 40,
        'description': 'Buerokratie und wichtige Dokumente fuer das Leben in der Schweiz.',
        'country_context': 'CH',
        'words': [
            ('die Aufenthaltsbewilligung', 'el permiso de residencia', 'noun', 'die', 'die Aufenthaltsbewilligungen', 'owf-ENT-halts-buh-vil-ih-goong', 'Ich brauche eine Aufenthaltsbewilligung.', 'Necesito un permiso de residencia.', 'CH', 'Swiss residence permit; categories: B (annual), C (permanent), L (short-term)'),
            ('die Anmeldung', 'el empadronamiento / el registro', 'noun', 'die', 'die Anmeldungen', '', 'Die Anmeldung muss innerhalb von 14 Tagen erfolgen.', 'El empadronamiento debe hacerse en 14 dias.', 'CH', 'Mandatory registration at the local Einwohnerkontrolle within 14 days of arrival'),
            ('die Gemeinde', 'el municipio / el ayuntamiento', 'noun', 'die', 'die Gemeinden', '', 'Ich gehe zur Gemeinde fuer die Anmeldung.', 'Voy al ayuntamiento para empadronarme.', 'CH', ''),
            ('das Einwohneramt', 'la oficina del padron', 'noun', 'das', 'die Einwohneraemter', '', 'Das Einwohneramt ist am Montag geoeffnet.', 'La oficina del padron abre el lunes.', 'CH', ''),
            ('die Steuererklarung', 'la declaracion de impuestos', 'noun', 'die', 'die Steuererklarungen', '', 'Die Steuererklarung muss bis Ende Maerz eingereicht werden.', 'La declaracion de impuestos debe presentarse antes de fin de marzo.', 'CH', ''),
            ('die Quellensteuer', 'el impuesto en la fuente', 'noun', 'die', '', 'KVEL-en-shtoy-er', 'Als Auslaender zahle ich Quellensteuer.', 'Como extranjero pago el impuesto en la fuente.', 'CH', 'Tax withheld directly from salary for foreign residents without C permit'),
            ('die AHV', 'el seguro de vejez (AHV)', 'noun', 'die', '', '', 'Ich muss AHV-Beitraege zahlen.', 'Tengo que pagar las cotizaciones de la AHV.', 'CH', 'Alters- und Hinterlassenenversicherung; Swiss state pension system'),
            ('die AHV-Nummer', 'el numero de seguridad social suizo', 'noun', 'die', '', '', 'Meine AHV-Nummer steht auf der Karte.', 'Mi numero de la AHV esta en la tarjeta.', 'CH', '13-digit Swiss social security number'),
            ('der Ausweis B', 'el permiso B (residencia anual)', 'noun', 'der', '', '', 'Ich habe einen Ausweis B.', 'Tengo un permiso B.', 'CH', 'Annual residence permit; renewed yearly; most common for new arrivals'),
            ('der Ausweis C', 'el permiso C (residencia permanente)', 'noun', 'der', '', '', 'Nach fuenf Jahren kann man den Ausweis C beantragen.', 'Despues de cinco anos se puede solicitar el permiso C.', 'CH', 'Permanent residence permit; after 5 or 10 years depending on nationality'),
            ('der Ausweis L', 'el permiso L (corta duracion)', 'noun', 'der', '', '', 'Mein Ausweis L ist fuer ein Jahr gueltig.', 'Mi permiso L es valido por un ano.', 'CH', 'Short-term residence permit, up to 1 year'),
            ('das Formular', 'el formulario', 'noun', 'das', 'die Formulare', '', 'Bitte fuellen Sie das Formular aus.', 'Por favor rellene el formulario.', '', ''),
            ('unterschreiben', 'firmar', 'verb', '', '', '', 'Bitte hier unterschreiben.', 'Firme aqui por favor.', '', ''),
            ('der Reisepass', 'el pasaporte', 'noun', 'der', 'die Reisepaesse', '', 'Bitte zeigen Sie Ihren Reisepass.', 'Por favor muestre su pasaporte.', '', ''),
            ('beantragen', 'solicitar', 'verb', '', '', 'buh-AN-trah-gen', 'Ich moechte eine Bewilligung beantragen.', 'Quisiera solicitar un permiso.', '', ''),
            ('die Krankenversicherungspolice', 'la poliza del seguro medico', 'noun', 'die', '', '', 'Bitte zeigen Sie Ihre Krankenversicherungspolice.', 'Por favor muestre su poliza del seguro medico.', 'CH', ''),
        ]
    },
    {
        'lang': 'de', 'name': 'Meinungen und Diskussion', 'slug': 'de-meinungen-diskussion',
        'category': 'social', 'level': 'B1', 'icon': '[Meinung]', 'sort': 32,
        'description': 'Meinungen ausdruecken und diskutieren auf Deutsch.',
        'country_context': '',
        'words': [
            ('Ich glaube, dass...', 'Creo que...', 'phrase', '', '', '', 'Ich glaube, dass das eine gute Idee ist.', 'Creo que esa es una buena idea.', '', ''),
            ('meiner Meinung nach', 'en mi opinion', 'phrase', '', '', '', 'Meiner Meinung nach ist das falsch.', 'En mi opinion, eso esta mal.', '', ''),
            ('Ich bin einverstanden', 'Estoy de acuerdo', 'phrase', '', '', '', 'Ich bin einverstanden mit Ihrer Meinung.', 'Estoy de acuerdo con su opinion.', '', ''),
            ('Ich bin nicht einverstanden', 'No estoy de acuerdo', 'phrase', '', '', '', 'Tut mir leid, ich bin nicht einverstanden.', 'Lo siento, no estoy de acuerdo.', '', ''),
            ('eigentlich', 'en realidad / de hecho', 'adv', '', '', '', 'Eigentlich habe ich eine andere Meinung.', 'En realidad tengo otra opinion.', '', ''),
            ('trotzdem', 'sin embargo / de todas formas', 'adv', '', '', '', 'Es ist schwer, trotzdem versuche ich es.', 'Es dificil, pero de todas formas lo intento.', '', ''),
            ('einerseits... andererseits', 'por un lado... por otro lado', 'phrase', '', '', '', 'Einerseits ist es teuer, andererseits ist es gut.', 'Por un lado es caro, por otro lado es bueno.', '', ''),
            ('obwohl', 'aunque / a pesar de que', 'conj', '', '', '', 'Obwohl es regnet, gehe ich spazieren.', 'Aunque llueve, salgo a pasear.', '', ''),
            ('deswegen', 'por eso / por esa razon', 'adv', '', '', '', 'Es war teuer, deswegen habe ich es nicht gekauft.', 'Era caro, por eso no lo compre.', '', ''),
            ('dagegen', 'en contra (de ello)', 'adv', '', '', '', 'Ich bin dagegen.', 'Estoy en contra.', '', ''),
            ('dafuer', 'a favor (de ello)', 'adv', '', '', '', 'Ich bin dafuer.', 'Estoy a favor.', '', ''),
            ('Wie sehen Sie das?', 'Como lo ve usted? / Que opina?', 'phrase', '', '', '', 'Interessant! Wie sehen Sie das?', 'Interesante! Como lo ve usted?', '', ''),
            ('Ich stimme zu', 'Estoy de acuerdo / Lo acepto', 'phrase', '', '', '', 'Ja, ich stimme zu.', 'Si, estoy de acuerdo.', '', ''),
            ('Guter Punkt', 'Buen punto', 'phrase', '', '', '', 'Guter Punkt, daran habe ich nicht gedacht.', 'Buen punto, no lo habia pensado.', '', ''),
            ('um ehrlich zu sein', 'para ser honesto/a', 'phrase', '', '', '', 'Um ehrlich zu sein, ich weiss es nicht.', 'Para ser honesto, no lo se.', '', ''),
            ('Ich bin mir nicht sicher', 'No estoy seguro/a', 'phrase', '', '', '', 'Ich bin mir nicht sicher, ob das stimmt.', 'No estoy seguro de que eso sea correcto.', '', ''),
        ]
    },
]


class Command(BaseCommand):
    help = 'Seed expanded German vocabulary (A1-B1) for Spanish speakers in Switzerland'

    def handle(self, *args, **options):
        de, _ = Language.objects.update_or_create(code='de', defaults={'name': 'German'})
        self.stdout.write(self.style.SUCCESS('Language ready: German'))

        total_topics = 0
        total_words = 0

        for t in TOPICS_DATA:
            topic, created = Topic.objects.update_or_create(
                slug=t['slug'],
                defaults={
                    'language': de,
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
            self.stdout.write(f'  Topic {action}: {t["name"]} (DE {t["level"]})')
            total_topics += 1

            for w in t['words']:
                word       = w[0]
                trans      = w[1]
                pos        = w[2]
                gender     = w[3]
                plural     = w[4] if len(w) > 4 else ''
                ipa        = w[5] if len(w) > 5 else ''
                example    = w[6] if len(w) > 6 else ''
                ex_trans   = w[7] if len(w) > 7 else ''
                region     = w[8] if len(w) > 8 else ''
                notes      = w[9] if len(w) > 9 else ''

                VocabularyItem.objects.update_or_create(
                    language=de,
                    topic=topic,
                    word=word,
                    defaults={
                        'translation_es': trans,
                        'part_of_speech': pos,
                        'gender': gender,
                        'plural': plural,
                        'pronunciation_ipa': ipa,
                        'example_sentence': example,
                        'example_translation': ex_trans,
                        'difficulty_level': t['level'],
                        'region_variant': region,
                        'notes': notes,
                    }
                )
                total_words += 1

        self.stdout.write(self.style.SUCCESS(
            f'\nDone! {total_topics} topics, {total_words} vocabulary items seeded.'
        ))
