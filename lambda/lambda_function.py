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
        return handler_input.response_builder.speak(speak_output).ask(reprompt).response

class PlayBackgroundMusicHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("PlayBackgroundMusicIntent")(handler_input)

    def handle(self, handler_input):
        audio_url = "https://www.dropbox.com/scl/fi/o0ucgmmpzv4zfoewnv1sn/718704__muyo5438__atmospheric-landscape-for-meditation-relaxation-and-yoga.mp3?rlkey=svedxtfoezpcg88qxxgixav2r&st=2leafyic&dl=1"
        handler_input.response_builder.add_directive(
            PlayDirective(
                play_behavior=PlayBehavior.REPLACE_ALL,
                audio_item=AudioItem(
                    stream=Stream(
                        token="background_music",
                        url=audio_url,
                        offset_in_milliseconds=0
                    )
                )
            )
        ).set_should_end_session(False)
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
                "Has seleccionado ejercicios Mindfulness. "
                "Esta funcionalidad estará disponible próximamente. "
                "¿Te gustaría elegir otra opción?"
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
        
        handler_input.response_builder.add_directive(
            PlayDirective(
                play_behavior=PlayBehavior.REPLACE_ALL,
                audio_item=AudioItem(
                    stream=Stream(
                        token="background_music",
                        url="https://www.dropbox.com/scl/fi/o0ucgmmpzv4zfoewnv1sn/718704__muyo5438__atmospheric-landscape-for-meditation-relaxation-and-yoga.mp3?rlkey=svedxtfoezpcg88qxxgixav2r&st=2leafyic&dl=1",
                        offset_in_milliseconds=0
                    )
                )
            )
        ).speak(instructions).ask(reprompt)
        
        return handler_input.response_builder.response

class BreathingIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("BreathingIntent")(handler_input)

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        cycles = int(slots["cycles"].value) if slots.get("cycles") and slots["cycles"].value else 3

        instructions = breathing_4_7_8(cycles)
        reprompt = "¿Te gustaría hacer otro ejercicio? Puedes elegir entre 'ejercicio basico', 'respiracion cuatro siete ocho' o 'ejercicio en caja'. O puedes decir 'regresar al menú principal'."
        
        handler_input.response_builder.add_directive(
            PlayDirective(
                play_behavior=PlayBehavior.REPLACE_ALL,
                audio_item=AudioItem(
                    stream=Stream(
                        token="background_music",
                        url="https://www.dropbox.com/scl/fi/o0ucgmmpzv4zfoewnv1sn/718704__muyo5438__atmospheric-landscape-for-meditation-relaxation-and-yoga.mp3?rlkey=svedxtfoezpcg88qxxgixav2r&st=2leafyic&dl=1",
                        offset_in_milliseconds=0
                    )
                )
            )
        ).speak(instructions).ask(reprompt)
        
        return handler_input.response_builder.response

class BoxBreathingIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("BoxBreathingIntent")(handler_input)

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        cycles = int(slots["cycles"].value) if slots.get("cycles") and slots["cycles"].value else 4
        duration = int(slots["duration"].value) if slots.get("duration") and slots["duration"].value else 4

        instructions = box_breathing(cycles, duration)
        reprompt = "¿Te gustaría hacer otro ejercicio? Puedes elegir entre 'ejercicio basico', 'respiracion cuatro siete ocho' o 'ejercicio en caja'. O puedes decir 'regresar al menú principal'."
        
        handler_input.response_builder.add_directive(
            PlayDirective(
                play_behavior=PlayBehavior.REPLACE_ALL,
                audio_item=AudioItem(
                    stream=Stream(
                        token="background_music",
                        url="https://www.dropbox.com/scl/fi/o0ucgmmpzv4zfoewnv1sn/718704__muyo5438__atmospheric-landscape-for-meditation-relaxation-and-yoga.mp3?rlkey=svedxtfoezpcg88qxxgixav2r&st=2leafyic&dl=1",
                        offset_in_milliseconds=0
                    )
                )
            )
        ).speak(instructions).ask(reprompt)
        
        return handler_input.response_builder.response

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
sb.add_request_handler(PlayBackgroundMusicHandler())
sb.add_request_handler(BreathingExerciseIntentHandler())
sb.add_request_handler(BreathingIntentHandler())
sb.add_request_handler(BoxBreathingIntentHandler())
sb.add_request_handler(MenuSelectionHandler())
sb.add_request_handler(ReturnToMenuHandler())
sb.add_request_handler(BreathingExercisesIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(CancelAndStopIntentHandler())
sb.add_exception_handler(CatchAllExceptionHandler())


lambda_handler = sb.lambda_handler()
