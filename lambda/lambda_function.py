import logging
import ask_sdk_core.utils as ask_utils
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response

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
    return " ".join(instructions)

# Manejadores
class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speak_output = (
            "¡Bienvenido a tu asistente de respiración! "
            "Puedes decir: 'iniciar ejercicio básico', 'respiración cuatro siete ocho' o 'ejercicio en caja'."
        )
        reprompt = "¿Qué tipo de ejercicio te gustaría hacer?"
        return handler_input.response_builder.speak(speak_output).ask(reprompt).response

# Adaptar para cada ejercicio
class BreathingExerciseIntentHandler(AbstractRequestHandler):
    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        cycles = int(slots["cycles"].value) if slots.get("cycles") and slots["cycles"].value else 5
        inhale_duration = int(slots["inhale_duration"].value) if slots.get("inhale_duration") and slots["inhale_duration"].value else 4
        hold_duration = int(slots["hold_duration"].value) if slots.get("hold_duration") and slots["hold_duration"].value else 4
        exhale_duration = int(slots["exhale_duration"].value) if slots.get("exhale_duration") and slots["exhale_duration"].value else 4

        instructions = breathing_exercise(cycles, inhale_duration, hold_duration, exhale_duration)
        reprompt = "¿Te gustaría hacer otro ejercicio? Puedes elegir entre 'ejercicio basico', 'respiracion cuatro siete ocho' o 'ejercicio en caja'."
        
        return handler_input.response_builder.speak(instructions).ask(reprompt).response

class BreathingIntentHandler(AbstractRequestHandler):
    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        cycles = int(slots["cycles"].value) if slots.get("cycles") and slots["cycles"].value else 3

        instructions = breathing_4_7_8(cycles)
        reprompt = "¿Te gustaría hacer otro ejercicio? Puedes elegir entre 'ejercicio basico', 'respiracion cuatro siete ocho' o 'ejercicio en caja'."
        
        return handler_input.response_builder.speak(instructions).ask(reprompt).response

class BoxBreathingIntentHandler(AbstractRequestHandler):
    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        cycles = int(slots["cycles"].value) if slots.get("cycles") and slots["cycles"].value else 4
        duration = int(slots["duration"].value) if slots.get("duration") and slots["duration"].value else 4

        instructions = box_breathing(cycles, duration)
        reprompt = "¿Te gustaría hacer otro ejercicio? Puedes elegir entre 'ejercicio basico', 'respiracion cuatro siete ocho' o 'ejercicio en caja'."
        
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
sb.add_request_handler(BreathingExerciseIntentHandler())
sb.add_request_handler(BreathingIntentHandler())
sb.add_request_handler(BoxBreathingIntentHandler())
sb.add_request_handler(BreathingExercisesIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(CancelAndStopIntentHandler())
sb.add_exception_handler(CatchAllExceptionHandler())


lambda_handler = sb.lambda_handler()
