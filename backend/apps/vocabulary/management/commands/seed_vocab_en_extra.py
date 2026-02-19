from django.core.management.base import BaseCommand
from core.models import Language
from vocabulary.models import Topic, VocabularyItem


# Format: (word, translation_es, part_of_speech, ipa, example_sentence, example_translation, notes)
# ipa and notes can be empty string ''

TOPICS_DATA = [
    {
        'lang': 'en', 'name': "At the Doctor's Office", 'slug': 'en-doctors-office',
        'category': 'daily_life', 'level': 'A2', 'sort': 10, 'country_context': '',
        'description': 'Medical vocabulary for doctor visits, symptoms, and pharmacies.',
        'words': [
            ('headache', 'dolor de cabeza', 'noun', 'ˈhɛdeɪk', 'I have a headache since this morning.', 'Tengo dolor de cabeza desde esta manana.', ''),
            ('fever', 'fiebre', 'noun', 'ˈfiːvər', 'The child has a fever of 39 degrees.', 'El nino tiene fiebre de 39 grados.', ''),
            ('prescription', 'receta medica', 'noun', 'prɪˈskrɪpʃən', 'The doctor gave me a prescription.', 'El medico me dio una receta.', ''),
            ('appointment', 'cita medica', 'noun', 'əˈpɔɪntmənt', 'I have a doctor appointment on Friday.', 'Tengo cita medica el viernes.', ''),
            ('pharmacy', 'farmacia', 'noun', 'ˈfɑːrməsi', 'Is there a pharmacy near here?', 'Hay una farmacia cerca de aqui?', 'In CH: Apotheke in German areas'),
            ('blood pressure', 'presion arterial', 'phrase', '', 'My blood pressure is a bit high.', 'Mi presion arterial esta un poco alta.', ''),
            ('insurance card', 'tarjeta del seguro medico', 'phrase', '', 'Please show your insurance card.', 'Por favor muestre su tarjeta del seguro.', 'In CH called Krankenkassenkarte'),
            ('sore throat', 'dolor de garganta', 'phrase', '', 'I have a sore throat and cough.', 'Tengo dolor de garganta y tos.', ''),
            ('cough', 'tos', 'noun', 'kɒf', 'I have had a cough for a week.', 'Llevo una semana con tos.', ''),
            ('allergy', 'alergia', 'noun', 'ˈælərdʒi', 'I have an allergy to penicillin.', 'Tengo alergia a la penicilina.', ''),
            ('to hurt', 'doler', 'verb', 'hɜːrt', 'My back hurts a lot.', 'Me duele mucho la espalda.', ''),
            ('waiting room', 'sala de espera', 'phrase', '', 'Please wait in the waiting room.', 'Por favor espere en la sala de espera.', ''),
            ('specialist', 'especialista', 'noun', 'ˌspɛʃəˈlɪst', 'I need a referral to a specialist.', 'Necesito una derivacion a un especialista.', ''),
            ('blood test', 'analisis de sangre', 'phrase', '', 'The doctor ordered a blood test.', 'El medico pidio un analisis de sangre.', ''),
            ('painkiller', 'analgesico / calmante', 'noun', 'ˈpeɪnkɪlər', 'Take two painkillers every 8 hours.', 'Tome dos analgesicos cada 8 horas.', ''),
            ('nausea', 'nauseas', 'noun', 'ˈnɔːziə', 'I feel nausea and dizziness.', 'Siento nauseas y mareos.', ''),
            ('emergency', 'urgencias', 'noun', 'ɪˈmɜːrdʒənsi', 'Go to the emergency room immediately.', 'Vaya a urgencias inmediatamente.', 'In CH: dial 144 for ambulance'),
            ('symptom', 'sintoma', 'noun', 'ˈsɪmptəm', 'What are your symptoms?', 'Cuales son sus sintomas?', ''),
        ]
    },
    {
        'lang': 'en', 'name': 'Banking & Money', 'slug': 'en-banking-money',
        'category': 'daily_life', 'level': 'A2', 'sort': 11, 'country_context': '',
        'description': 'Opening accounts, transfers, ATMs, and financial vocabulary.',
        'words': [
            ('bank account', 'cuenta bancaria', 'phrase', '', 'I need to open a bank account.', 'Necesito abrir una cuenta bancaria.', 'In CH: UBS, ZKB, PostFinance are common'),
            ('transfer', 'transferencia', 'noun', 'ˈtrænsfɜːr', 'I made a bank transfer yesterday.', 'Hice una transferencia bancaria ayer.', ''),
            ('exchange rate', 'tipo de cambio', 'phrase', '', 'What is the exchange rate today?', 'Cual es el tipo de cambio hoy?', 'CHF (Swiss franc) vs EUR'),
            ('credit card', 'tarjeta de credito', 'phrase', '', 'Can I pay by credit card?', 'Puedo pagar con tarjeta de credito?', ''),
            ('withdrawal', 'retiro / extraccion', 'noun', 'wɪðˈdrɔːəl', 'I need to make a withdrawal at the ATM.', 'Necesito hacer un retiro en el cajero.', ''),
            ('savings', 'ahorros', 'noun', 'ˈseɪvɪŋz', 'I keep my savings in a separate account.', 'Guardo mis ahorros en una cuenta separada.', ''),
            ('mortgage', 'hipoteca', 'noun', 'ˈmɔːrɡɪdʒ', 'We applied for a mortgage last month.', 'Solicitamos una hipoteca el mes pasado.', ''),
            ('ATM', 'cajero automatico', 'noun', '', 'Is there an ATM nearby?', 'Hay un cajero automatico cerca?', 'In CH often called Bancomat'),
            ('deposit', 'deposito', 'noun', 'dɪˈpɒzɪt', 'I made a deposit of 500 francs.', 'Hice un deposito de 500 francos.', ''),
            ('invoice', 'factura', 'noun', 'ˈɪnvɔɪs', 'Please send me the invoice by email.', 'Por favor enviame la factura por correo.', ''),
            ('standing order', 'orden permanente / domiciliacion', 'phrase', '', 'The rent is paid by standing order.', 'El alquiler se paga por domiciliacion.', 'Very common in CH for recurring payments'),
            ('balance', 'saldo / balance', 'noun', 'ˈbæləns', 'What is the balance in my account?', 'Cual es el saldo en mi cuenta?', ''),
            ('fee', 'comision / tarifa', 'noun', 'fiː', 'There is a monthly fee for the account.', 'Hay una comision mensual por la cuenta.', ''),
            ('loan', 'prestamo', 'noun', 'loʊn', 'I took a loan to buy furniture.', 'Pedi un prestamo para comprar muebles.', ''),
            ('cash', 'dinero en efectivo', 'noun', 'kæʃ', 'Do you accept cash?', 'Aceptan efectivo?', 'In CH cash is still widely used'),
            ('direct debit', 'debito directo / domiciliacion', 'phrase', '', 'Set up a direct debit for utilities.', 'Configura un debito directo para los suministros.', ''),
            ('IBAN', 'IBAN (numero de cuenta internacional)', 'noun', '', 'Please provide your IBAN for the transfer.', 'Por favor proporcioname tu IBAN para la transferencia.', 'Required for all bank transfers in CH/EU'),
        ]
    },
    {
        'lang': 'en', 'name': 'At the Office', 'slug': 'en-at-the-office',
        'category': 'work', 'level': 'B1', 'sort': 12, 'country_context': '',
        'description': 'Workplace vocabulary: meetings, emails, and professional interactions.',
        'words': [
            ('deadline', 'plazo limite / fecha de entrega', 'noun', 'ˈdɛdlaɪn', 'The deadline is this Friday at noon.', 'El plazo limite es este viernes al mediodia.', ''),
            ('meeting', 'reunion', 'noun', 'ˈmiːtɪŋ', 'We have a team meeting every Monday.', 'Tenemos una reunion de equipo cada lunes.', ''),
            ('colleague', 'colega / companero de trabajo', 'noun', 'ˈkɒliːɡ', 'My colleague helped me with the report.', 'Mi colega me ayudo con el informe.', ''),
            ('report', 'informe', 'noun', 'rɪˈpɔːrt', 'Could you send me the report?', 'Podrias enviarme el informe?', ''),
            ('schedule', 'horario / agenda', 'noun', 'ˈʃɛdjuːl', 'Let me check my schedule for next week.', 'Dejame revisar mi agenda para la semana que viene.', ''),
            ('overtime', 'horas extra', 'noun', 'ˈoʊvərtaɪm', 'I worked overtime yesterday to finish.', 'Trabaje horas extra ayer para terminar.', ''),
            ('promotion', 'ascenso / promocion', 'noun', 'prəˈmoʊʃən', 'She got a promotion after two years.', 'Ella consiguio un ascenso despues de dos anos.', ''),
            ('feedback', 'retroalimentacion / comentarios', 'noun', 'ˈfiːdbæk', 'Can I get some feedback on my work?', 'Puedo recibir comentarios sobre mi trabajo?', ''),
            ('to attend', 'asistir', 'verb', 'əˈtɛnd', 'I cannot attend the meeting tomorrow.', 'No puedo asistir a la reunion manana.', ''),
            ('remote work', 'trabajo remoto / teletrabajo', 'phrase', '', 'I work remote two days a week.', 'Trabajo en remoto dos dias a la semana.', 'Very common in CH tech companies'),
            ('presentation', 'presentacion', 'noun', 'ˌprɛzənˈteɪʃən', 'I have a presentation for the client.', 'Tengo una presentacion para el cliente.', ''),
            ('invoice', 'factura', 'noun', 'ˈɪnvɔɪs', 'Please approve this invoice.', 'Por favor aprueba esta factura.', ''),
            ('spreadsheet', 'hoja de calculo', 'noun', '', 'Update the spreadsheet with the new data.', 'Actualiza la hoja de calculo con los nuevos datos.', ''),
            ('to delegate', 'delegar', 'verb', 'ˈdɛlɪɡeɪt', 'The manager delegated the task to me.', 'El jefe delego la tarea en mi.', ''),
            ('probation period', 'periodo de prueba', 'phrase', '', 'My probation period ends next month.', 'Mi periodo de prueba termina el mes que viene.', 'In CH usually 1-3 months'),
            ('payslip', 'nomina / recibo de sueldo', 'noun', 'ˈpeɪslɪp', 'I need my payslip for the apartment application.', 'Necesito mi nomina para la solicitud del piso.', ''),
            ('pension fund', 'fondo de pension / jubilacion', 'phrase', '', 'The company contributes to your pension fund.', 'La empresa contribuye a tu fondo de pension.', 'In CH: Pillar 2 (BVG/LPP) is mandatory'),
        ]
    },
    {
        'lang': 'en', 'name': 'Eating Out', 'slug': 'en-eating-out',
        'category': 'social', 'level': 'A1', 'sort': 13, 'country_context': '',
        'description': 'Restaurants, ordering food, dietary needs, and dining etiquette.',
        'words': [
            ('menu', 'carta / menu', 'noun', 'ˈmɛnjuː', 'Could we see the menu, please?', 'Podriamos ver la carta, por favor?', ''),
            ('bill', 'cuenta', 'noun', 'bɪl', 'Could we have the bill, please?', 'Nos podria traer la cuenta, por favor?', ''),
            ('tip', 'propina', 'noun', 'tɪp', 'Is the tip included in the bill?', 'Esta incluida la propina en la cuenta?', 'In CH tipping is optional, round up is common'),
            ('reservation', 'reserva', 'noun', 'ˌrɛzərˈveɪʃən', 'I have a reservation for two at 8pm.', 'Tengo una reserva para dos a las 8.', ''),
            ('appetizer', 'entrante / aperitivo', 'noun', 'ˈæpɪtaɪzər', 'What would you like as an appetizer?', 'Que le gustaria como entrante?', ''),
            ('main course', 'plato principal', 'phrase', '', 'For the main course I will have the fish.', 'De plato principal tomare el pescado.', ''),
            ('dessert', 'postre', 'noun', 'dɪˈzɜːrt', 'Would you like to see the dessert menu?', 'Gustaria ver la carta de postres?', ''),
            ('vegetarian', 'vegetariano/a', 'adj', 'ˌvɛdʒɪˈtɛəriən', 'Do you have vegetarian options?', 'Tienen opciones vegetarianas?', ''),
            ('allergic', 'alergico/a', 'adj', 'əˈlɜːrdʒɪk', 'I am allergic to nuts.', 'Soy alergico a los frutos secos.', ''),
            ('waiter', 'camarero / mesero', 'noun', 'ˈweɪtər', 'Excuse me, waiter! Can we order?', 'Disculpe, camarero! Podemos pedir?', ''),
            ('to order', 'pedir / ordenar', 'verb', 'ˈɔːrdər', 'Are you ready to order?', 'Estan listos para pedir?', ''),
            ('portion', 'porcion / racion', 'noun', 'ˈpɔːrʃən', 'The portions here are very generous.', 'Las raciones aqui son muy generosas.', ''),
            ('tap water', 'agua del grifo', 'phrase', '', 'Can I get some tap water?', 'Me puede traer agua del grifo?', 'In CH tap water is excellent quality'),
            ('daily special', 'menu del dia / plato del dia', 'phrase', '', 'What is the daily special today?', 'Cual es el plato del dia hoy?', ''),
            ('to split the bill', 'pagar por separado / dividir la cuenta', 'phrase', '', 'Can we split the bill?', 'Podemos pagar por separado?', ''),
            ('gluten-free', 'sin gluten', 'adj', '', 'Do you have any gluten-free dishes?', 'Tienen platos sin gluten?', ''),
        ]
    },
    {
        'lang': 'en', 'name': 'Weather & Seasons', 'slug': 'en-weather-seasons',
        'category': 'daily_life', 'level': 'A1', 'sort': 14, 'country_context': 'CH',
        'description': 'Swiss weather vocabulary: seasons, forecasts, and the famous fog.',
        'words': [
            ('sunny', 'soleado', 'adj', 'ˈsʌni', 'It is sunny and warm today.', 'Hoy esta soleado y caluroso.', ''),
            ('cloudy', 'nublado', 'adj', 'ˈklaʊdi', 'It will be cloudy in the afternoon.', 'Por la tarde estara nublado.', ''),
            ('rain', 'lluvia', 'noun', 'reɪn', 'I forgot my umbrella and it started to rain.', 'Olvide el paraguas y empezo a llover.', ''),
            ('snow', 'nieve', 'noun', 'snoʊ', 'There is a lot of snow in the Alps.', 'Hay mucha nieve en los Alpes.', ''),
            ('temperature', 'temperatura', 'noun', 'ˈtɛmprɪtʃər', 'The temperature drops below zero at night.', 'La temperatura baja de cero por la noche.', ''),
            ('forecast', 'pronostico del tiempo', 'noun', 'ˈfɔːrkæst', 'Have you checked the weather forecast?', 'Has comprobado el pronostico del tiempo?', ''),
            ('warm', 'calido / caluroso', 'adj', 'wɔːrm', 'It is warm enough to eat outside.', 'Hace suficiente calor para comer fuera.', ''),
            ('cold', 'frio', 'adj', 'koʊld', 'It is very cold this morning.', 'Hace mucho frio esta manana.', ''),
            ('foggy', 'con niebla / neblinoso', 'adj', 'ˈfɒɡi', 'It is very foggy on the plateau today.', 'Hoy hay mucha niebla en el altiplano.', 'Nebel/fog on the Mittelland plateau Nov-Feb is very common in CH'),
            ('thunderstorm', 'tormenta electrica', 'noun', 'ˈθʌndərstɔːrm', 'There will be thunderstorms this evening.', 'Esta tarde habra tormentas electricas.', 'CH has frequent summer storms'),
            ('hail', 'granizo', 'noun', 'heɪl', 'The hail damaged the car roof.', 'El granizo danio el techo del coche.', ''),
            ('wind', 'viento', 'noun', 'wɪnd', 'There is a strong wind from the north.', 'Hay un fuerte viento del norte.', 'Fohn wind is a famous warm wind in CH'),
            ('umbrella', 'paraguas', 'noun', 'ʌmˈbrɛlə', 'Always carry an umbrella in autumn.', 'Lleva siempre el paraguas en otono.', ''),
            ('season', 'estacion del ano', 'noun', 'ˈsiːzən', 'Autumn is my favourite season in Switzerland.', 'El otono es mi estacion favorita en Suiza.', ''),
            ('degree', 'grado', 'noun', 'dɪˈɡriː', 'It is minus five degrees outside.', 'Afuera hace cinco grados bajo cero.', 'CH uses Celsius'),
            ('humidity', 'humedad', 'noun', 'hjuːˈmɪdɪti', 'The humidity is high today.', 'La humedad es alta hoy.', ''),
            ('ice', 'hielo', 'noun', 'aɪs', 'Be careful, there is ice on the road.', 'Ten cuidado, hay hielo en la carretera.', ''),
        ]
    },
    {
        'lang': 'en', 'name': 'Housing & Home', 'slug': 'en-housing-home',
        'category': 'daily_life', 'level': 'A2', 'sort': 15, 'country_context': '',
        'description': 'Furniture, rooms, household chores, and renting vocabulary.',
        'words': [
            ('kitchen', 'cocina', 'noun', 'ˈkɪtʃɪn', 'The kitchen is fully equipped.', 'La cocina esta totalmente equipada.', ''),
            ('bathroom', 'bano', 'noun', 'ˈbæθruːm', 'The apartment has two bathrooms.', 'El apartamento tiene dos banos.', ''),
            ('bedroom', 'dormitorio / habitacion', 'noun', 'ˈbɛdruːm', 'My bedroom faces the garden.', 'Mi dormitorio da al jardin.', ''),
            ('furniture', 'muebles', 'noun', 'ˈfɜːrnɪtʃər', 'The apartment comes with furniture.', 'El apartamento viene amueblado.', ''),
            ('landlord', 'propietario / casero', 'noun', 'ˈlændlɔːrd', 'The landlord lives on the ground floor.', 'El propietario vive en la planta baja.', ''),
            ('tenant', 'inquilino', 'noun', 'ˈtɛnənt', 'As a tenant you must keep the place clean.', 'Como inquilino debes mantener el lugar limpio.', ''),
            ('heating', 'calefaccion', 'noun', 'ˈhiːtɪŋ', 'Is the heating included in the rent?', 'Esta la calefaccion incluida en el alquiler?', 'In CH heating costs (Nebenkosten) often added separately'),
            ('garbage', 'basura', 'noun', 'ˈɡɑːrbɪdʒ', 'Put the garbage in the correct bin.', 'Pon la basura en el contenedor correcto.', ''),
            ('recycling', 'reciclaje', 'noun', 'riːˈsaɪklɪŋ', 'Recycling rules are very strict here.', 'Las normas de reciclaje son muy estrictas aqui.', 'In CH glass/paper/PET must be sorted and taken to collection points'),
            ('deposit', 'deposito / fianza', 'noun', 'dɪˈpɒzɪt', 'The deposit is three months rent.', 'La fianza equivale a tres meses de alquiler.', 'In CH rental deposit (Mietkaution) is max 3 months rent'),
            ('utility bills', 'facturas de suministros', 'phrase', '', 'Utility bills are not included in the rent.', 'Las facturas de suministros no estan incluidas en el alquiler.', ''),
            ('lease', 'contrato de arrendamiento', 'noun', 'liːs', 'Please read the lease carefully.', 'Por favor lee el contrato de arrendamiento con cuidado.', ''),
            ('notice period', 'periodo de preaviso', 'phrase', '', 'The notice period is three months.', 'El periodo de preaviso es de tres meses.', 'In CH typically 3 months before end of quarter'),
            ('cellar', 'sotano / bodega', 'noun', 'ˈsɛlər', 'Each apartment has a cellar for storage.', 'Cada apartamento tiene un sotano para guardar cosas.', 'Common in Swiss apartment buildings (Keller)'),
            ('laundry room', 'lavanderia comun', 'phrase', '', 'The laundry room is in the basement.', 'La lavanderia comun esta en el sotano.', 'In CH shared laundry rooms with booking schedules are standard'),
            ('neighbor', 'vecino', 'noun', 'ˈneɪbər', 'I introduced myself to my neighbors.', 'Me presente a mis vecinos.', 'In CH quiet hours (Ruhezeit) are important to respect'),
        ]
    },
    {
        'lang': 'en', 'name': 'Health & Fitness', 'slug': 'en-health-fitness',
        'category': 'daily_life', 'level': 'B1', 'sort': 16, 'country_context': '',
        'description': 'Gym, sports, outdoor activities, and general wellbeing vocabulary.',
        'words': [
            ('gym membership', 'membresia / abono al gimnasio', 'phrase', '', 'I signed up for a gym membership.', 'Me apunte a un abono del gimnasio.', 'Fitness First, Migros Fitness common in CH'),
            ('workout', 'entrenamiento', 'noun', 'ˈwɜːrkaʊt', 'I do a 30-minute workout every morning.', 'Hago 30 minutos de entrenamiento cada manana.', ''),
            ('swimming pool', 'piscina', 'phrase', '', 'The outdoor swimming pool opens in June.', 'La piscina al aire libre abre en junio.', 'CH has many public Freibad pools'),
            ('hiking', 'senderismo / excursionismo', 'noun', 'ˈhaɪkɪŋ', 'Hiking in the Alps is amazing.', 'Hacer senderismo en los Alpes es increible.', 'CH has 65,000 km of marked hiking trails'),
            ('yoga', 'yoga', 'noun', '', 'She attends a yoga class twice a week.', 'Ella asiste a una clase de yoga dos veces por semana.', ''),
            ('injury', 'lesion', 'noun', 'ˈɪndʒəri', 'I had a knee injury from running.', 'Tuve una lesion en la rodilla por correr.', ''),
            ('diet', 'dieta / alimentacion', 'noun', 'ˈdaɪɪt', 'I am trying to eat a balanced diet.', 'Estoy intentando seguir una dieta equilibrada.', ''),
            ('stretch', 'estirar / estiramiento', 'verb', 'strɛtʃ', 'Always stretch before and after exercise.', 'Estira siempre antes y despues de ejercicio.', ''),
            ('to burn calories', 'quemar calorias', 'phrase', '', 'Cycling burns a lot of calories.', 'Andar en bicicleta quema muchas calorias.', ''),
            ('wellness', 'bienestar', 'noun', 'ˈwɛlnɪs', 'Switzerland has great wellness options.', 'Suiza tiene excelentes opciones de bienestar.', ''),
            ('physiotherapy', 'fisioterapia', 'noun', 'ˌfɪzioʊˈθɛrəpi', 'I go to physiotherapy for my back.', 'Voy a fisioterapia por mi espalda.', ''),
            ('sports club', 'club deportivo', 'phrase', '', 'I joined the local sports club.', 'Me uni al club deportivo local.', 'Verein (association/club) culture is strong in CH'),
            ('sleep', 'dormir / sueno', 'noun', 'sliːp', 'Good sleep is essential for recovery.', 'El sueno es esencial para la recuperacion.', ''),
            ('hydration', 'hidratacion', 'noun', 'ˌhaɪˈdreɪʃən', 'Stay hydrated during outdoor activities.', 'Mantente hidratado durante actividades al aire libre.', ''),
            ('pulse', 'pulso', 'noun', 'pʌls', 'My resting pulse is 60 beats per minute.', 'Mi pulso en reposo es 60 latidos por minuto.', ''),
            ('trail', 'sendero', 'noun', 'treɪl', 'This trail leads to the summit.', 'Este sendero lleva a la cima.', 'CH trails are colour-coded: yellow=easy, white-red=mountain'),
        ]
    },
    {
        'lang': 'en', 'name': 'Technology & Internet', 'slug': 'en-technology-internet',
        'category': 'work', 'level': 'A2', 'sort': 17, 'country_context': '',
        'description': 'Digital life: devices, internet, and everyday tech vocabulary.',
        'words': [
            ('password', 'contrasena', 'noun', 'ˈpæswɜːrd', 'My password must have 8 characters.', 'Mi contrasena debe tener 8 caracteres.', ''),
            ('wifi', 'wifi / red inalambrica', 'noun', 'ˈwaɪfaɪ', 'What is the wifi password here?', 'Cual es la contrasena del wifi aqui?', ''),
            ('download', 'descargar / descarga', 'verb', 'ˈdaʊnloʊd', 'I need to download this document.', 'Necesito descargar este documento.', ''),
            ('update', 'actualizar / actualizacion', 'verb', 'ˈʌpdeɪt', 'Please update your software regularly.', 'Por favor actualiza tu software regularmente.', ''),
            ('app', 'aplicacion / app', 'noun', 'æp', 'There is an app for the public transport.', 'Hay una app para el transporte publico.', 'SBB app is essential in CH'),
            ('website', 'sitio web / pagina web', 'noun', '', 'Check the company website for details.', 'Consulta la pagina web de la empresa para mas detalles.', ''),
            ('email', 'correo electronico', 'noun', 'ˈiːmeɪl', 'I will send you the details by email.', 'Te enviare los detalles por correo electronico.', ''),
            ('printer', 'impresora', 'noun', 'ˈprɪntər', 'The printer is out of paper.', 'La impresora no tiene papel.', ''),
            ('screen', 'pantalla', 'noun', 'skriːn', 'The screen resolution is excellent.', 'La resolucion de la pantalla es excelente.', ''),
            ('laptop', 'portatil / laptop', 'noun', 'ˈlæptɒp', 'I work with my laptop from home.', 'Trabajo con mi portatil desde casa.', ''),
            ('charger', 'cargador', 'noun', 'ˈtʃɑːrdʒər', 'Have you seen my phone charger?', 'Has visto mi cargador del movil?', ''),
            ('cloud storage', 'almacenamiento en la nube', 'phrase', '', 'I back up my files to cloud storage.', 'Guardo mis archivos en la nube.', ''),
            ('video call', 'videollamada', 'phrase', '', 'We have a video call with the team at 10.', 'Tenemos videollamada con el equipo a las 10.', ''),
            ('to reboot', 'reiniciar', 'verb', 'riːˈbuːt', 'Try rebooting your computer first.', 'Intenta reiniciar el ordenador primero.', ''),
            ('data plan', 'plan de datos / tarifa de datos', 'phrase', '', 'My data plan includes 10 GB per month.', 'Mi plan de datos incluye 10 GB al mes.', 'Mobile data in CH is expensive; Sunrise/Swisscom are main providers'),
            ('browser', 'navegador', 'noun', 'ˈbraʊzər', 'Which browser do you use?', 'Que navegador usas?', ''),
        ]
    },
    {
        'lang': 'en', 'name': 'Bureaucracy & Permits', 'slug': 'en-bureaucracy-permits',
        'category': 'culture', 'level': 'B1', 'sort': 18, 'country_context': 'CH',
        'description': 'Essential Swiss bureaucracy: permits, registration, taxes, and insurance.',
        'words': [
            ('residence permit', 'permiso de residencia', 'phrase', '', 'I need to renew my residence permit.', 'Necesito renovar mi permiso de residencia.', 'In CH: L (short), B (annual), C (permanent) permits for EU citizens'),
            ('registration', 'empadronamiento / registro', 'noun', 'ˌrɛdʒɪˈstreɪʃən', 'You must complete registration within 14 days.', 'Debes completar el empadronamiento en 14 dias.', 'Anmeldung at your local Einwohnerkontrolle is mandatory within 14 days of arrival'),
            ('Anmeldung', 'empadronamiento / registro municipal', 'noun', '', 'Did you do your Anmeldung already?', 'Ya hiciste tu Anmeldung?', 'German word used in CH even in English speech; required at local Gemeinde/Einwohnerkontrolle'),
            ('tax return', 'declaracion de la renta / impuestos', 'phrase', '', 'The tax return deadline is March 31st.', 'La fecha limite de la declaracion de la renta es el 31 de marzo.', 'In CH: Steuererklarung; some cantons extend deadline on request'),
            ('social security', 'seguridad social', 'phrase', '', 'I pay social security contributions every month.', 'Pago contribuciones de seguridad social cada mes.', 'In CH: AHV/AVS contributions are deducted from salary'),
            ('health insurance', 'seguro medico obligatorio', 'phrase', '', 'Health insurance is mandatory in Switzerland.', 'El seguro medico es obligatorio en Suiza.', 'Krankenkasse must be arranged within 3 months of arrival; Swisscare, Comparis to compare'),
            ('deductible', 'franquicia / deducible', 'noun', 'dɪˈdʌktɪbəl', 'I chose a higher deductible to lower my premium.', 'Elegi una franquicia mas alta para reducir la prima.', 'In CH called Franchise; ranges from CHF 300 to 2500'),
            ('premium', 'prima (del seguro)', 'noun', 'ˈpriːmiəm', 'Health insurance premiums vary by canton.', 'Las primas del seguro medico varian segun el canton.', 'Praemie in German; one of the biggest monthly expenses in CH'),
            ('municipality', 'municipio / ayuntamiento', 'noun', 'mjuːˌnɪsɪˈpælɪti', 'Contact your municipality for the form.', 'Contacta tu municipio para el formulario.', 'Gemeinde in German; most permits handled locally in CH'),
            ('work permit', 'permiso de trabajo', 'phrase', '', 'Do you need a work permit here?', 'Necesitas permiso de trabajo aqui?', 'EU citizens: auto-permitted via B permit; non-EU: more complex process'),
            ('notarized document', 'documento notariado', 'phrase', '', 'I need a notarized document for this.', 'Necesito un documento notariado para esto.', ''),
            ('civil status', 'estado civil', 'phrase', '', 'Please state your civil status on the form.', 'Por favor indica tu estado civil en el formulario.', ''),
            ('certificate', 'certificado', 'noun', 'sərˈtɪfɪkɪt', 'I need a certificate of residence.', 'Necesito un certificado de residencia.', 'Wohnsitzbestatigung or Heimatausweis in CH'),
            ('deadline', 'plazo / fecha limite', 'noun', 'ˈdɛdlaɪn', 'Do not miss the registration deadline.', 'No te pierdas el plazo de registro.', ''),
            ('stamp', 'sello', 'noun', 'stæmp', 'The form must have an official stamp.', 'El formulario debe tener un sello oficial.', ''),
            ('to fill in a form', 'rellenar un formulario', 'phrase', '', 'Please fill in this form in block letters.', 'Por favor rellena este formulario en letras de imprenta.', ''),
            ('fine', 'multa', 'noun', 'faɪn', 'There is a fine for late registration.', 'Hay una multa por registro tardio.', 'In CH fines for missed deadlines are enforced'),
        ]
    },
    {
        'lang': 'en', 'name': 'Small Talk & Opinions', 'slug': 'en-small-talk-opinions',
        'category': 'social', 'level': 'B1', 'sort': 19, 'country_context': '',
        'description': 'Expressing opinions, agreeing, disagreeing, and keeping conversation going.',
        'words': [
            ('I think', 'creo que / pienso que', 'phrase', '', 'I think this is a great idea.', 'Creo que esta es una gran idea.', ''),
            ('I agree', 'estoy de acuerdo', 'phrase', '', 'I completely agree with you.', 'Estoy completamente de acuerdo contigo.', ''),
            ('in my opinion', 'en mi opinion', 'phrase', '', 'In my opinion, public transport is excellent here.', 'En mi opinion, el transporte publico es excelente aqui.', ''),
            ('actually', 'en realidad / de hecho', 'adv', 'ˈæktʃuəli', 'Actually, I prefer working in the morning.', 'En realidad, prefiero trabajar por la manana.', ''),
            ('however', 'sin embargo / no obstante', 'conj', 'haʊˈɛvər', 'The rent is expensive, however the city is great.', 'El alquiler es caro, sin embargo la ciudad es genial.', ''),
            ('although', 'aunque / a pesar de que', 'conj', 'ɔːlˈðoʊ', 'Although it rains a lot, I love it here.', 'Aunque llueve mucho, me encanta estar aqui.', ''),
            ('it depends', 'depende', 'phrase', '', 'It depends on the situation.', 'Depende de la situacion.', ''),
            ('I disagree', 'no estoy de acuerdo', 'phrase', '', 'I disagree with that point.', 'No estoy de acuerdo con ese punto.', ''),
            ('to be honest', 'para ser honesto', 'phrase', '', 'To be honest, I was a bit nervous.', 'Para ser honesto, estaba un poco nervioso.', ''),
            ('as far as I know', 'que yo sepa / hasta donde se', 'phrase', '', 'As far as I know, the office is closed today.', 'Que yo sepa, la oficina esta cerrada hoy.', ''),
            ('on the other hand', 'por otro lado', 'phrase', '', 'The winters are harsh. On the other hand, skiing is amazing.', 'Los inviernos son duros. Por otro lado, el esqui es increible.', ''),
            ('more or less', 'mas o menos', 'phrase', '', 'I understand more or less what you said.', 'Entiendo mas o menos lo que dijiste.', ''),
            ('presumably', 'presumiblemente / supongo que', 'adv', 'prɪˈzjuːməbli', 'Presumably the meeting starts at 9.', 'Supongo que la reunion empieza a las 9.', ''),
            ('I am not sure', 'no estoy seguro/a', 'phrase', '', 'I am not sure about that, let me check.', 'No estoy seguro sobre eso, dejame comprobarlo.', ''),
            ('it seems like', 'parece que', 'phrase', '', 'It seems like the train is delayed.', 'Parece que el tren tiene retraso.', ''),
            ('by the way', 'por cierto', 'phrase', '', 'By the way, did you hear about the new policy?', 'Por cierto, has oido hablar de la nueva politica?', ''),
            ('I would say', 'yo diria que', 'phrase', '', 'I would say the quality of life here is very high.', 'Yo diria que la calidad de vida aqui es muy alta.', ''),
        ]
    },
]


class Command(BaseCommand):
    help = 'Seed extra English vocabulary topics (10 new topics, ~170 words)'

    def handle(self, *args, **options):
        try:
            lang = Language.objects.get(code='en')
        except Language.DoesNotExist:
            self.stdout.write(self.style.ERROR('Language "en" not found. Run seed_content first.'))
            return

        total_topics = 0
        total_words = 0

        for topic_data in TOPICS_DATA:
            topic, created = Topic.objects.update_or_create(
                slug=topic_data['slug'],
                defaults={
                    'language': lang,
                    'name': topic_data['name'],
                    'description': topic_data['description'],
                    'difficulty_level': topic_data['level'],
                    'category': topic_data['category'],
                    'country_context': topic_data.get('country_context', ''),
                    'sort_order': topic_data['sort'],
                    'is_active': True,
                }
            )
            action = 'Created' if created else 'Updated'
            self.stdout.write(f'  {action} topic: {topic_data["name"]}')
            total_topics += 1

            for word_tuple in topic_data['words']:
                word, trans, pos, ipa, example, example_trans, notes = word_tuple
                _, w_created = VocabularyItem.objects.update_or_create(
                    language=lang,
                    topic=topic,
                    word=word,
                    defaults={
                        'translation_es': trans,
                        'part_of_speech': pos,
                        'pronunciation_ipa': ipa,
                        'example_sentence': example,
                        'example_translation': example_trans,
                        'difficulty_level': topic_data['level'],
                        'region_variant': topic_data.get('country_context', ''),
                        'notes': notes,
                    }
                )
                total_words += 1

        self.stdout.write(self.style.SUCCESS(
            f'Done. {total_topics} topics and {total_words} vocabulary items seeded.'
        ))
