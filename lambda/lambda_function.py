import logging
import ask_sdk_core.utils as ask_utils
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.interfaces.audioplayer import PlayDirective, PlayBehavior, AudioItem, Stream

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

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
        instructions.append(f"Inhala durante {inhale_duration} segundos. Voy a contar: ")
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
        instructions.append("Inhala profundamente durante 4 segundos. Voy a contar: ")
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
        instructions.append("Inhala lentamente. Voy a contar: ")
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
        "<speak> Bienvenido al ejercicio de escaneo corporal. Cierra los ojos si te sientes cómodo. "
        "Relájate y lleva tu atención a cada parte de tu cuerpo. Comenzamos con tu cabeza y rostro, luego "
        "tu cuello y hombros, tus brazos y manos, tu pecho y abdomen, tu espalda, tus caderas y piernas, y finalmente tus pies. "
        "Respira profundamente y lleva tu atención a todo tu cuerpo. <break time='1s'/> ¡Bien hecho! Has completado el ejercicio. "
        "¿Te gustaría hacer otro ejercicio o regresar al menú principal? </speak>"
    )

# Atención Plena
def mindfulness_observation():
    return (
        "<speak> Bienvenido al ejercicio de atención plena. Observa tu entorno y piensa en tres cosas que puedes ver, "
        "tres cosas que puedes escuchar y tres cosas que puedes sentir. Reflexiona sobre tus respuestas. <break time='1s'/> "
        "¡Bien hecho! Has completado el ejercicio de atención plena. ¿Te gustaría hacer otro ejercicio o regresar al menú principal? </speak>"
    )

# Gratitud
def gratitude_exercise():
    return (
        "<speak> Bienvenido al ejercicio de gratitud. Reflexiona sobre tu día y piensa en tres cosas por las que te sientes agradecido. "
        "Dedica un momento a apreciar estas cosas. <break time='1s'/> ¡Bien hecho! Has completado el ejercicio de gratitud. "
        "¿Te gustaría hacer otro ejercicio o regresar al menú principal? </speak>"
    )

# Manejadores
class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speak_output = (
            "Bienvenido a Respira y Relájate. Puedes elegir entre: "
            "Ejercicios de respiración, "
            "Ejercicios Mindfulness, o "
            "Agregar recordatorio. "
            "¿Qué te gustaría hacer?"
        )
        reprompt = "Por favor, di qué te gustaría hacer: Ejercicios de respiración, Ejercicios Mindfulness, o Agregar recordatorios."

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
        
        return handler_input.response_builder.speak(speak_output).ask(reprompt).response

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
            speak_output = (            
                "Has seleccionado agregar recordatorios. "
                "Esta funcionalidad estará disponible próximamente. "
                "¿Te gustaría elegir otra opción?"
            )
            reprompt = "¿Te gustaría elegir otra opción?"
        
        else:
            speak_output = (
                "No entendí tu selección. Por favor, di qué te gustaría hacer: "
                "Ejercicios de respiración, "
                "Ejercicios Mindfulness, o "
                "Agregar recordatorios."
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
            "Agregar recordatorio. "
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
sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
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
