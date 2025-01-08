import logging
import ask_sdk_core.utils as ask_utils
import asyncio

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

async def breathing_exercise(cycles=5, inhale_duration=4, hold_duration=4, exhale_duration=4):
    instructions = []
    instructions.append("¡Bienvenido al ejercicio de respiración!")
    instructions.append(f"Haremos {cycles} ciclos de respiración. Sigue las instrucciones:")
    
    for cycle in range(1, cycles + 1):
        instructions.append(f"\nCiclo {cycle}/{cycles}")
        instructions.append("Inhala...")
        await asyncio.sleep(inhale_duration)
        
        instructions.append("Sostén la respiración...")
        await asyncio.sleep(hold_duration)
        
        instructions.append("Exhala...")
        await asyncio.sleep(exhale_duration)
    
    instructions.append("\n¡Ejercicio completado! Espero que te sientas más relajado.")
    return " ".join(instructions)

async def breathing_4_7_8(cycles=3):
    instructions = []
    instructions.append("Ejercicio de respiración 4-7-8 para relajarte:")
    
    for cycle in range(1, cycles + 1):
        instructions.append(f"\nCiclo {cycle}/{cycles}")
        instructions.append("Inhala profundamente durante 4 segundos...")
        await asyncio.sleep(4)
        
        instructions.append("Sostén la respiración durante 7 segundos...")
        await asyncio.sleep(7)
        
        instructions.append("Exhala completamente durante 8 segundos...")
        await asyncio.sleep(8)
    
    instructions.append("\n¡Ejercicio completado! Este método ayuda a calmar la mente y el cuerpo.")
    return " ".join(instructions)

async def box_breathing(cycles=4, duration=4):
    instructions = []
    instructions.append("Ejercicio de respiración en caja (Box Breathing):")
    instructions.append(f"Duración de cada fase: {duration} segundos.")
    
    for cycle in range(1, cycles + 1):
        instructions.append(f"\nCiclo {cycle}/{cycles}")
        instructions.append("Inhala lentamente...")
        await asyncio.sleep(duration)
        
        instructions.append("Sostén la respiración...")
        await asyncio.sleep(duration)
        
        instructions.append("Exhala lentamente...")
        await asyncio.sleep(duration)
        
        instructions.append("Sostén nuevamente...")
        await asyncio.sleep(duration)
    
    instructions.append("\n¡Ejercicio completado! Este método es excelente para centrarte.")
    return " ".join(instructions)

class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speak_output = "¡Bienvenido a tu asistente de respiración! Puedes decir: 'Iniciar ejercicio de respiración', 'Hacer respiración 4-7-8' o 'Realizar respiración en caja'."
        reprompt = "¿Qué tipo de ejercicio te gustaría hacer?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt)
                .response
        )

class BreathingExerciseIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("BreathingExerciseIntent")(handler_input)

    async def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        try:
            cycles = int(slots["cycles"].value) if slots.get("cycles") and slots["cycles"].value else 5
            inhale_duration = int(slots["inhale_duration"].value) if slots.get("inhale_duration") and slots["inhale_duration"].value else 4
            hold_duration = int(slots["hold_duration"].value) if slots.get("hold_duration") and slots["hold_duration"].value else 4
            exhale_duration = int(slots["exhale_duration"].value) if slots.get("exhale_duration") and slots["exhale_duration"].value else 4
        except (ValueError, TypeError):
            speak_output = "Lo siento, no entendí los valores proporcionados. Usaré los valores predeterminados."
            cycles, inhale_duration, hold_duration, exhale_duration = 5, 4, 4, 4

        instructions = await breathing_exercise(cycles, inhale_duration, hold_duration, exhale_duration)
        return handler_input.response_builder.speak(instructions).response

class BreathingIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("BreathingIntent")(handler_input)

    async def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        try:
            cycles = int(slots["cycles"].value) if slots.get("cycles") and slots["cycles"].value else 3
        except (ValueError, TypeError):
            cycles = 3

        instructions = await breathing_4_7_8(cycles)
        return handler_input.response_builder.speak(instructions).response

class BoxBreathingIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("BoxBreathingIntent")(handler_input)

    async def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        try:
            cycles = int(slots["cycles"].value) if slots.get("cycles") and slots["cycles"].value else 4
            duration = int(slots["duration"].value) if slots.get("duration") and slots["duration"].value else 4
        except (ValueError, TypeError):
            cycles, duration = 4, 4

        instructions = await box_breathing(cycles, duration)
        return handler_input.response_builder.speak(instructions).response

class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = (
            "Puedes elegir entre tres tipos de ejercicios de respiración: "
            "básico, 4-7-8, o respiración en caja. "
            "Por ejemplo, di 'hacer respiración básica' o 'iniciar respiración en caja'. "
            "¿Cuál te gustaría intentar?"
        )

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class CancelOrStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        speak_output = "¡Gracias por practicar respiración conmigo! ¡Hasta pronto!"
        return handler_input.response_builder.speak(speak_output).response

class FallbackIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = (
            "Lo siento, no entendí eso. Puedes decir 'ayuda' para conocer "
            "las opciones disponibles."
        )
        reprompt = "¿Qué tipo de ejercicio de respiración te gustaría hacer?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt)
                .response
        )

class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        return handler_input.response_builder.response

class CatchAllExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        logger.error(exception, exc_info=True)
        speak_output = "Lo siento, hubo un problema. Por favor, inténtalo de nuevo."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(BreathingExerciseIntentHandler())
sb.add_request_handler(BreathingIntentHandler())
sb.add_request_handler(BoxBreathingIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()