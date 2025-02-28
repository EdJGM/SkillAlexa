import logging
import os
import boto3
import datetime
from ask_sdk_dynamodb.adapter import DynamoDbAdapter
import ask_sdk_core.utils as ask_utils
from ask_sdk_core.skill_builder import CustomSkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.interfaces.audioplayer import PlayDirective, PlayBehavior, AudioItem, Stream
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# conexión a db
ddb_region = os.environ.get('DYNAMODB_PERSISTENCE_REGION')
ddb_table_name = os.environ.get('DYNAMODB_PERSISTENCE_TABLE_NAME')
ddb_resource = boto3.resource('dynamodb', region_name=ddb_region)
dynamodb_adapter = DynamoDbAdapter(table_name=ddb_table_name, create_table=False, dynamodb_resource=ddb_resource)
dynamodb = boto3.client('dynamodb', region_name='us-east-1')

# URLs de las músicas
MUSIC_URLS = [
    "https://www.dropbox.com/scl/fi/o0ucgmmpzv4zfoewnv1sn/718704__muyo5438__atmospheric-landscape-for-meditation-relaxation-and-yoga.mp3?rlkey=svedxtfoezpcg88qxxgixav2r&st=kkqvhxss&dl=1",
    "https://www.dropbox.com/scl/fi/r8hb5hwanjbcrdvp89y69/747599__viramiller__gentle-tracks-for-relaxing-and-enjoying-natures-beauty.mp3?rlkey=fitpmianlikjg4huwyddr8gn1&st=apo42s1g&dl=1",
    "https://www.dropbox.com/scl/fi/h5acxl6f8t6wwf9fvrovs/750212__nancy_sinclair__calm-atmosphere-with-fortepiano-and-birdsong-melodies.mp3?rlkey=xb7c4ih9symtoablyhccpxqxx&st=rdwrjqze&dl=1"
]

# Ejercicio mejorado de respiración básica
def breathing_exercise(cycles=5, inhale_duration=4, hold_duration=4, exhale_duration=4):
    instructions = []
    instructions.append("¡Bienvenido al ejercicio de respiración básica!")
    instructions.append(f"Haremos {cycles} ciclos. Sigue las instrucciones:")

    for cycle in range(1, cycles + 1):
        instructions.append(f"\nCiclo {cycle}/{cycles}:")
        instructions.append(f"Respira durante {inhale_duration} segundos. Voy a contar: ")
        instructions.extend([f"{i}..." for i in range(1, inhale_duration + 1)])
        instructions.append(f"<break time='1s'/> Sosten la respiración durante {hold_duration} segundos: ")
        instructions.extend([f"{i}..." for i in range(1, hold_duration + 1)])
        instructions.append(f"<break time='1s'/> Exhala suavemente durante {exhale_duration} segundos: ")
        instructions.extend([f"{i}..." for i in range(1, exhale_duration + 1)])
        instructions.append("<break time='1s'/>")

    instructions.append("\n¡Ejercicio completado! Espero que te sientas más relajado.")
    instructions.append("\n¿Te gustaría hacer otro ejercicio? Puedes elegir entre 'ejercicio basico', 'respiracion cuatro siete ocho' o 'ejercicio en caja'.")
    instructions.append("\nO ¿Te gustaría regresar al menú principal?")
    return " ".join(instructions)

# Ejercicio mejorado 4-7-8
def breathing_4_7_8(cycles=3):
    instructions = []
    instructions.append("Ejercicio de respiración 4-7-8 para relajarte:")

    for cycle in range(1, cycles + 1):
        instructions.append(f"\nCiclo {cycle}/{cycles}:")
        instructions.append("Respira profundamente durante 4 segundos. Voy a contar: ")
        instructions.extend([f"{i}..." for i in range(1, 5)])
        instructions.append("<break time='1s'/> Sosten la respiración durante 7 segundos: ")
        instructions.extend([f"{i}..." for i in range(1, 8)])
        instructions.append("<break time='1s'/> Exhala completamente durante 8 segundos: ")
        instructions.extend([f"{i}..." for i in range(1, 9)])
        instructions.append("<break time='1s'/>")

    instructions.append("\n¡Ejercicio completado! Este método ayuda a calmar la mente y el cuerpo.")
    instructions.append("\n¿Te gustaría hacer otro ejercicio? Puedes elegir entre 'ejercicio basico', 'respiracion cuatro siete ocho' o 'ejercicio en caja'.")
    instructions.append("\nO ¿Te gustaría regresar al menú principal?")
    return " ".join(instructions)

# Ejercicio mejorado de respiración en caja
def box_breathing(cycles=4, duration=4):
    instructions = []
    instructions.append("Ejercicio de respiración en caja (Box Breathing):")
    instructions.append(f"Duración de cada fase: {duration} segundos.")

    for cycle in range(1, cycles + 1):
        instructions.append(f"\nCiclo {cycle}/{cycles}:")
        instructions.append("Respira lentamente. Voy a contar: ")
        instructions.extend([f"{i}..." for i in range(1, duration + 1)])
        instructions.append(f"<break time='1s'/> Sosten la respiración durante {duration} segundos: ")
        instructions.extend([f"{i}..." for i in range(1, duration + 1)])
        instructions.append(f"<break time='1s'/> Exhala lentamente durante {duration} segundos: ")
        instructions.extend([f"{i}..." for i in range(1, duration + 1)])
        instructions.append(f"<break time='1s'/> Sosten nuevamente durante {duration} segundos: ")
        instructions.extend([f"{i}..." for i in range(1, duration + 1)])
        instructions.append("<break time='1s'/>")

    instructions.append("\n¡Ejercicio completado! Este método es excelente para centrarte.")
    instructions.append("\n¿Te gustaría hacer otro ejercicio? Puedes elegir entre 'ejercicio basico', 'respiracion cuatro siete ocho' o 'ejercicio en caja'.")
    instructions.append("\nO ¿Te gustaría regresar al menú principal?")
    return " ".join(instructions)

# Ejercicios de Mindfulness
# Escaneo Corporal
def body_scan_exercise():
    return (
        "<speak> Bienvenido al ejercicio de escaneo corporal. Vamos a tomarnos un momento para conectar con nuestro cuerpo y relajarnos profundamente. "
        "Cierra los ojos si te sientes cómodo y lleva tu atención a tu respiración. Inhala profundamente y exhala suavemente. "
        "<break time='4s'/> Comencemos. Lleva tu atención a tu cabeza y rostro. Nota cualquier sensación, tensión o relajación en esta área. "
        "<break time='6s'/> Ahora enfócate en tu cuello y hombros. Permíteles relajarse mientras respiras profundamente. "
        "<break time='6s'/> Continúa bajando tu atención a tus brazos y manos. Nota cómo se sienten. ¿Están relajados o tensos? "
        "<break time='6s'/> Lleva tu atención a tu pecho y abdomen. Observa el ritmo de tu respiración y cómo tu cuerpo se mueve con cada inhalación y exhalación. "
        "<break time='6s'/> Ahora siente tu espalda, desde la parte superior hasta la parte baja. Relaja cualquier tensión que puedas sentir. "
        "<break time='6s'/> Enfócate en tus caderas, piernas y pies. Nota cómo se sienten apoyados sobre el suelo o la superficie donde estás sentado. "
        "<break time='6s'/> Finalmente, lleva tu atención a todo tu cuerpo. Siente cómo cada parte está conectada. Respira profundamente y disfruta de este momento de calma. "
        "<break time='6s'/> ¡Bien hecho! Has completado el ejercicio de escaneo corporal. "
        "¿Te gustaría hacer otro ejercicio o regresar al menú principal? </speak>"
    )


# Atención Plena
def mindfulness_observation():
    return (
        "<speak> Bienvenido al ejercicio de atención plena. Vamos a tomarnos un momento para observar nuestro entorno y conectar con el presente. "
        "<break time='1s'/> Primero, mira a tu alrededor. Nota tres cosas que puedes ver. Pueden ser objetos, colores o detalles que antes no habías notado. "
        "<break time='6s'/> Ahora, cierra los ojos si te sientes cómodo y presta atención a los sonidos a tu alrededor. "
        "Identifica tres sonidos diferentes. Tal vez puedas escuchar el sonido de tu respiración, el viento, o incluso algún ruido distante. "
        "<break time='8s'/> Por último, enfócate en lo que puedes sentir en tu cuerpo. Nota tres sensaciones físicas. "
        "Podría ser la temperatura del aire en tu piel, la sensación de la ropa en tu cuerpo, o cómo tus pies tocan el suelo. "
        "<break time='8s'/> Respira profundamente y toma un momento para apreciar esta conexión con el presente. "
        "<break time='5s'/> ¡Bien hecho! Has completado este ejercicio de atención plena. "
        "¿Te gustaría hacer otro ejercicio o regresar al menú principal? </speak>"
    )

# Gratitud
def gratitude_exercise():
    return (
        "<speak> Bienvenido al ejercicio de gratitud. Vamos a reflexionar sobre tres cosas por las que te sientas agradecido el día de hoy. "
        "<break time='1s'/> Primero, piensa en algo que haya sucedido hoy que te hizo sonreír o sentir bien. "
        "<break time='5s'/> Ahora, reflexiona sobre una persona en tu vida a quien aprecias. "
        "<break time='5s'/> Por último, piensa en algo simple pero importante, como un lugar que disfrutes, una comida que te guste, o incluso un momento de tranquilidad. "
        "<break time='5s'/> Tómate un momento para sentirte agradecido por estas tres cosas. "
        "<break time='10s'/> La gratitud nos ayuda a enfocarnos en lo positivo y mejora nuestro bienestar emocional. "
        "<break time='1s'/> ¡Bien hecho! Has completado este ejercicio de gratitud. "
        "¿Te gustaría hacer otro ejercicio o regresar al menú principal? </speak>"
    )

# Manejadores
# Manejador para la bienvenida y selección del test
class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speak_output = "Bienvenido a Respira y Relájate. Puedes elegir entre el test de estrés o el test de bienestar emocional. O si ya hiciste algún test puedes pasar directamente a los ejercicios diciendo 'menu principal'. ¿Cuál prefieres?"
        
        # Inicia la música desde la primera pista
        handler_input.response_builder.add_directive(
            PlayDirective(
                play_behavior=PlayBehavior.REPLACE_ALL,
                audio_item=AudioItem(
                    stream=Stream(
                        token="music_1",
                        url=MUSIC_URLS[0],
                        offset_in_milliseconds=0,
                        expected_previous_token=None
                    )
                )
            )
        )
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# Manejador para las preguntas
class SelectTestIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("SelectTestIntent")(handler_input)

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        test_type = slots["testType"].value.lower() if slots and slots.get("testType") and slots["testType"].value else None

        # Obtener el attributes manager y los atributos persistentes
        attributes_manager = handler_input.attributes_manager
        # Inicializar los atributos persistentes si no existen
        persistent_attributes = attributes_manager.persistent_attributes
        if not persistent_attributes:
            persistent_attributes = {}

        if test_type == "estrés" or test_type == "estres":
            persistent_attributes["current_test"] = "stress"
            persistent_attributes["stress_questions"] = [
                "¿Te sientes abrumado(a) por tus responsabilidades?",
                "¿Tienes dificultad para dormir por preocupaciones?",
                "¿Te sientes irritable o frustrado(a) con frecuencia?",
                "¿Sientes que no tienes tiempo suficiente para ti mismo(a)?",
                "¿Te resulta difícil concentrarte en tus tareas diarias?",
                "¿Te preocupa tu salud física o mental?",
                "¿Sientes que tu vida está fuera de control?",
                "¿Te sientes solo(a) o aislado(a) en tus problemas?",
                "¿Te cuesta disfrutar de las cosas que antes te hacían feliz?",
                "¿Experimentas síntomas físicos como dolores de cabeza o tensión muscular?"
            ]
            persistent_attributes["stress_answers"] = []
            persistent_attributes["current_question_index"] = 0

        elif test_type == "bienestar emocional":
            persistent_attributes["current_test"] = "wellbeing"
            persistent_attributes["wellbeing_questions"] = [
                "¿Te sientes feliz en tu vida cotidiana?",
                "¿Tienes relaciones satisfactorias con amigos y familiares?",
                "¿Te sientes motivado(a) para alcanzar tus metas?",
                "¿Eres capaz de manejar los desafíos que enfrentas?",
                "¿Sientes que tienes un propósito en la vida?",
                "¿Te sientes agradecido(a) por lo que tienes?",
                "¿Te tomas tiempo para ti mismo(a) regularmente?",
                "¿Disfrutas de actividades que te hacen sentir bien?",
                "¿Sientes que puedes expresar tus emociones de manera saludable?",
                "¿Te sientes optimista sobre el futuro?"
            ]
            persistent_attributes["wellbeing_answers"] = []
            persistent_attributes["current_question_index"] = 0

        else:
            speak_output = "No entendí el tipo de test que quieres hacer. Por favor elige entre 'estrés' o 'bienestar emocional'."
            return (
                handler_input.response_builder
                    .speak(speak_output)
                    .ask(speak_output)
                    .response
            )

        # Guardar los atributos actualizados
        attributes_manager.persistent_attributes = persistent_attributes
        attributes_manager.save_persistent_attributes()

        # Obtener la primera pregunta
        current_test = persistent_attributes["current_test"]
        first_question = persistent_attributes[f"{current_test}_questions"][0]

        speak_output = f"Has elegido el test de {test_type}. {first_question}"
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(first_question)
                .response
        )

# Manejador para respuestas
class YesIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.YesIntent")(handler_input)

    def handle(self, handler_input):
        return AnswerProcessor.handle_test_response(handler_input, "si")


class NoIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.NoIntent")(handler_input)

    def handle(self, handler_input):
        return AnswerProcessor.handle_test_response(handler_input, "no")

class AnswerProcessor:
    @staticmethod
    def handle_test_response(handler_input, user_response):
        try:
            attributes_manager = handler_input.attributes_manager
            persistent_attributes = attributes_manager.persistent_attributes
            
            if not persistent_attributes or "current_test" not in persistent_attributes:
                speak_output = "Lo siento, necesitas elegir primero un test. ¿Te gustaría hacer el test de estrés o el de bienestar emocional?"
                return handler_input.response_builder.speak(speak_output).ask(speak_output).response
                
            current_test = persistent_attributes["current_test"]
            current_index = int(persistent_attributes.get("current_question_index", 0))
            answers_key = f"{current_test}_answers"
            questions_key = f"{current_test}_questions"

            if answers_key not in persistent_attributes:
                persistent_attributes[answers_key] = []
            persistent_attributes[answers_key].append(user_response)
            persistent_attributes["current_question_index"] = current_index + 1

            attributes_manager.persistent_attributes = persistent_attributes
            attributes_manager.save_persistent_attributes()

            if current_index + 1 < len(persistent_attributes[questions_key]):
                next_question = persistent_attributes[questions_key][current_index + 1]
                return handler_input.response_builder.speak(next_question).ask(next_question).response

            # Analizar resultados
            yes_count = persistent_attributes[answers_key].count("si")
            timestamp = datetime.datetime.utcnow().isoformat() + "Z"  # Timestamp en formato ISO8601
            if current_test == "stress":
                if yes_count <= 3:
                    speak_output = "Tienes un bajo nivel de estrés. Te recomiendo realizar ejercicios de respiración básica."
                elif yes_count <= 6:
                    speak_output = "Tienes un nivel moderado de estrés. Puedes intentar el ejercicio de respiración 4-7-8."
                else:
                    speak_output = "Tienes un alto nivel de estrés. Te sugiero hacer el ejercicio de respiración en caja."
            else:
                if yes_count <= 3:
                    speak_output = "Tienes un bajo bienestar emocional. Considera realizar ejercicios de gratitud."
                elif yes_count <= 6:
                    speak_output = "Tienes un bienestar emocional moderado. Puedes intentar ejercicios de atención plena."
                else:
                    speak_output = "Tienes un alto bienestar emocional. Sigue manteniendo tus hábitos saludables."

            # **Actualizar test_history sin sobrescribir los datos anteriores**
            if "test_history" not in persistent_attributes:
                persistent_attributes["test_history"] = []

            # Agregar nuevo resultado a la lista de test_history
            persistent_attributes["test_history"].append({
                "test_type": current_test,
                "score": yes_count,
                "timestamp": timestamp
            })

            # Guardar en DynamoDB
            attributes_manager.persistent_attributes = persistent_attributes
            attributes_manager.save_persistent_attributes()

            return handler_input.response_builder.speak(speak_output + ". Ingresa al menú principal para realizar lo sugerido.").ask("Di 'menú principal' para continuar.").response

        except Exception as e:
            logger.error(f"Error en handle_test_response: {str(e)}", exc_info=True)
            return handler_input.response_builder.speak("Lo siento, ha ocurrido un error. Intenta nuevamente.").response
    


class AudioPlaybackFinishedHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("AudioPlayer.PlaybackFinished")(handler_input)

    def handle(self, handler_input):
        # Obtiene el token actual y calcula el siguiente
        current_token = handler_input.request_envelope.context.audio_player.token
        next_index = (int(current_token.split("_")[1]) % len(MUSIC_URLS)) + 1
        next_token = f"music_{next_index}"
        next_url = MUSIC_URLS[next_index - 1]

        # Reproduce la siguiente música
        handler_input.response_builder.add_directive(
            PlayDirective(
                play_behavior=PlayBehavior.REPLACE_ALL,
                audio_item=AudioItem(
                    stream=Stream(
                        token=next_token,
                        url=next_url,
                        offset_in_milliseconds=0,
                        expected_previous_token=current_token
                    )
                )
            )
        )
        return handler_input.response_builder.response

# Manejador de selección de menú
class MenuSelectionHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("MenuSelectionIntent")(handler_input)

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        option = slots["option"].value if slots.get("option") and slots["option"].value else ""
        
        # Normalizar la entrada a minúsculas y sin acentos
        option = option.lower().replace('ó', 'o').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ú', 'u')
        
        if "respiracion" in option or "respiratorio" in option or "respirar" in option:
            speak_output = (
                "Has seleccionado ejercicios de respiración. "
                "Puedes elegir entre: ejercicio básico, "
                "respiración cuatro siete ocho, o "
                "respiración en caja. "
                "¿Cuál te gustaría hacer?"
            )
            reprompt = "¿Qué ejercicio te gustaría hacer?"
        
        elif "mindfulness" in option or "meditacion" in option:
            speak_output = (
                "Has seleccionado ejercicios de mindfulness. "
                "Puedes elegir entre: escaneo Corporal, " 
                "atención plena, o " 
                "gratitud. "
                "¿Qué ejercicio te gustaría hacer?"
            )
            reprompt = "¿Te gustaría elegir otra opción?"
        
        elif "recordatorio" in option or "recordatorios":
            # Redirige al sistema nativo de recordatorios
            return handler_input.response_builder.add_directive({
                "type": "Dialog.DelegateRequest",
                "target": "AMAZON.Reminders",
                "period": None,
                "updatedIntent": {
                    "name": "AMAZON.Reminders",
                    "confirmationStatus": "NONE"
                }
            }).response
        
        else:
            speak_output = (
                "No entendí tu selección. Por favor, di qué te gustaría hacer: "
                "Ejercicios de respiración, "
                "Ejercicios Mindfulness, o "
                "Recordatorios."
            )
            reprompt = "¿Qué te gustaría hacer?"

        return handler_input.response_builder.speak(speak_output).ask(reprompt).response

# Manejador para regresar al menú principal
class ReturnToMenuHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("ReturnToMenuIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = (
            "De acuerdo. Puedes elegir entre: "
            "Ejercicios de respiración, "
            "Ejercicios Mindfulness, o "
            "Recordatorios. "
            "¿Qué te gustaría hacer?"
        )
        reprompt = "¿Qué te gustaría hacer?"
        return handler_input.response_builder.speak(speak_output).ask(reprompt).response

# Adaptar para cada ejercicio
class BreathingExerciseIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("BreathingExerciseIntent")(handler_input)

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        cycles = int(slots["cycles"].value) if slots.get("cycles") and slots["cycles"].value else 5
        inhale_duration = int(slots["inhale_duration"].value) if slots.get("inhale_duration") and slots["inhale_duration"].value else 4
        hold_duration = int(slots["hold_duration"].value) if slots.get("hold_duration") and slots["hold_duration"].value else 4
        exhale_duration = int(slots["exhale_duration"].value) if slots.get("exhale_duration") and slots["exhale_duration"].value else 4

        instructions = breathing_exercise(cycles, inhale_duration, hold_duration, exhale_duration)
        reprompt = "¿Te gustaría hacer otro ejercicio? Puedes elegir entre 'ejercicio basico', 'respiracion cuatro siete ocho' o 'ejercicio en caja'. O puedes decir 'regresar al menú principal'."
        
        return handler_input.response_builder.speak(instructions).ask(reprompt).response

class BreathingIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("BreathingIntent")(handler_input)

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        cycles = int(slots["cycles"].value) if slots.get("cycles") and slots["cycles"].value else 3

        instructions = breathing_4_7_8(cycles)
        reprompt = "¿Te gustaría hacer otro ejercicio? Puedes elegir entre 'ejercicio basico', 'respiracion cuatro siete ocho' o 'ejercicio en caja'. O puedes decir 'regresar al menú principal'."
        
        return handler_input.response_builder.speak(instructions).ask(reprompt).response

class BoxBreathingIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("BoxBreathingIntent")(handler_input)

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        cycles = int(slots["cycles"].value) if slots.get("cycles") and slots["cycles"].value else 4
        duration = int(slots["duration"].value) if slots.get("duration") and slots["duration"].value else 4

        instructions = box_breathing(cycles, duration)
        reprompt = "¿Te gustaría hacer otro ejercicio? Puedes elegir entre 'ejercicio basico', 'respiracion cuatro siete ocho' o 'ejercicio en caja'. O puedes decir 'regresar al menú principal'."
        
        return handler_input.response_builder.speak(instructions).ask(reprompt).response

class BreathingExercisesIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("BreathingExercisesIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = (
            "¡Claro! Puedes elegir entre los siguientes ejercicios de respiración: "
            "'básico', 'cuatro siete ocho' o 'respiración en caja'. "
            "¿Cuál te gustaría hacer?"
        )
        return handler_input.response_builder.speak(speak_output).ask(speak_output).response

# Menu mindfulness
class MindfulnessMenuHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("MindfulnessMenuIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = (
            "Has seleccionado ejercicios de mindfulness. Puedes elegir entre: "
            "Escaneo Corporal, Atención Plena, o Gratitud. ¿Qué ejercicio te gustaría hacer?"
        )
        return handler_input.response_builder.speak(speak_output).ask(speak_output).response

# Ejercicio Escaneo Corporal
class BodyScanIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("BodyScanIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = body_scan_exercise()
        return handler_input.response_builder.speak(speak_output).ask("¿Te gustaría hacer otro ejercicio?").response

# Ejercicio Atencion Plena
class MindfulnessObservationIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("MindfulnessObservationIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = mindfulness_observation()
        return handler_input.response_builder.speak(speak_output).ask("¿Te gustaría hacer otro ejercicio?").response

# Ejercicio Gratitud
class GratitudeIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("GratitudeIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = gratitude_exercise()
        return handler_input.response_builder.speak(speak_output).ask("¿Te gustaría hacer otro ejercicio?").response

class FallbackIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = (
            "Lo siento, no entendí eso. Puedes intentar decir: 'respiración básica', "
            "'cuatro siete ocho' o 'respiración en caja'."
        )
        return handler_input.response_builder.speak(speak_output).ask(speak_output).response

class CancelAndStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        speak_output = "¡Hasta luego! Gracias por usar el asistente de respiración."
        return handler_input.response_builder.speak(speak_output).response

class CatchAllExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        logger.error(exception, exc_info=True)
        speak_output = "Lo siento, ha ocurrido un error. Por favor, intenta nuevamente."
        return handler_input.response_builder.speak(speak_output).response

# Configuración del Skill Builder
sb = CustomSkillBuilder(persistence_adapter = dynamodb_adapter)

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(SelectTestIntentHandler())
sb.add_request_handler(YesIntentHandler())
sb.add_request_handler(NoIntentHandler())
sb.add_request_handler(AudioPlaybackFinishedHandler())
sb.add_request_handler(BreathingExerciseIntentHandler())
sb.add_request_handler(BreathingIntentHandler())
sb.add_request_handler(BoxBreathingIntentHandler())
sb.add_request_handler(MenuSelectionHandler())
sb.add_request_handler(ReturnToMenuHandler())
sb.add_request_handler(BreathingExercisesIntentHandler())
sb.add_request_handler(MindfulnessMenuHandler())
sb.add_request_handler(BodyScanIntentHandler())
sb.add_request_handler(MindfulnessObservationIntentHandler())
sb.add_request_handler(GratitudeIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(CancelAndStopIntentHandler())
sb.add_exception_handler(CatchAllExceptionHandler())


lambda_handler = sb.lambda_handler()