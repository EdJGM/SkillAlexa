# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils
import time

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# Función del Ejercicio 1
def breathing_exercise(cycles=5, inhale_duration=4, hold_duration=4, exhale_duration=4):
    instructions = []
    instructions.append("\u00a1Bienvenido al ejercicio de respiraci\u00f3n!")
    instructions.append(f"Haremos {cycles} ciclos de respiraci\u00f3n. Sigue las instrucciones:")
    
    for cycle in range(1, cycles + 1):
        instructions.append(f"\nCiclo {cycle}/{cycles}")
        instructions.append("Inhala... 🌬️")
        time.sleep(inhale_duration)
        
        instructions.append("Sost\u00e9n la respiraci\u00f3n... 🤐")
        time.sleep(hold_duration)
        
        instructions.append("Exhala... 🧘")
        time.sleep(exhale_duration)
    
    instructions.append("\n\u00a1Ejercicio completado! Espero que te sientas m\u00e1s relajado. 😊")
    return " ".join(instructions)

# Función del Ejercicio 2
def breathing_4_7_8(cycles=3):
    instructions = []
    instructions.append("Ejercicio de respiraci\u00f3n 4-7-8 para relajarte:")
    
    for cycle in range(1, cycles + 1):
        instructions.append(f"\nCiclo {cycle}/{cycles}")
        instructions.append("Inhala profundamente durante 4 segundos... 🌬️")
        time.sleep(4)
        
        instructions.append("Sost\u00e9n la respiraci\u00f3n durante 7 segundos... 🤐")
        time.sleep(7)
        
        instructions.append("Exhala completamente durante 8 segundos... 🧘")
        time.sleep(8)
    
    instructions.append("\n\u00a1Ejercicio completado! Este m\u00e9todo ayuda a calmar la mente y el cuerpo. 😊")
    return " ".join(instructions)

# Función del Ejercicio 3
def box_breathing(cycles=4, duration=4):
    instructions = []
    instructions.append("Ejercicio de respiraci\u00f3n en caja (Box Breathing):")
    instructions.append(f"Duraci\u00f3n de cada fase: {duration} segundos.")
    
    for cycle in range(1, cycles + 1):
        instructions.append(f"\nCiclo {cycle}/{cycles}")
        instructions.append("Inhala lentamente durante 4 segundos... 🌬️")
        time.sleep(duration)
        
        instructions.append("Sost\u00e9n la respiraci\u00f3n durante 4 segundos... 🤐")
        time.sleep(duration)
        
        instructions.append("Exhala lentamente durante 4 segundos... 🧘")
        time.sleep(duration)
        
        instructions.append("Sost\u00e9n nuevamente durante 4 segundos... 🤐")
        time.sleep(duration)
    
    instructions.append("\n\u00a1Ejercicio completado! Este m\u00e9todo es excelente para centrarte. 🧘\u200d♀️")
    return " ".join(instructions)

# Handlers
class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "\u00a1Bienvenido a la skill de gesti\u00f3n del estr\u00e9s! Puedes decir: 'Iniciar ejercicio de respiraci\u00f3n', 'Hacer respiraci\u00f3n 4-7-8' o 'Realizar respiraci\u00f3n en caja'."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class BreathingExerciseIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return handler_input.request_envelope.request.type == "IntentRequest" and handler_input.request_envelope.request.intent.name == "BreathingExerciseIntent"

    def handle(self, handler_input):
        # Leer los slots
        slots = handler_input.request_envelope.request.intent.slots
        cycles = int(slots["cycles"].value) if "cycles" in slots and slots["cycles"].value else 5
        inhale_duration = int(slots["inhale_duration"].value) if "inhale_duration" in slots and slots["inhale_duration"].value else 4
        hold_duration = int(slots["hold_duration"].value) if "hold_duration" in slots and slots["hold_duration"].value else 4
        exhale_duration = int(slots["exhale_duration"].value) if "exhale_duration" in slots and slots["exhale_duration"].value else 4

        # Ejecutar el ejercicio con los valores del usuario
        instructions = breathing_exercise(cycles, inhale_duration, hold_duration, exhale_duration)
        return handler_input.response_builder.speak(instructions).response


class BreathingIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return handler_input.request_envelope.request.type == "IntentRequest" and handler_input.request_envelope.request.intent.name == "Breathing478Intent"

    def handle(self, handler_input):
        # Leer los slots
        slots = handler_input.request_envelope.request.intent.slots
        cycles = int(slots["cycles"].value) if "cycles" in slots and slots["cycles"].value else 3

        # Ejecutar el ejercicio con los valores del usuario
        instructions = breathing_4_7_8(cycles)
        return handler_input.response_builder.speak(instructions).response


class BoxBreathingIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return handler_input.request_envelope.request.type == "IntentRequest" and handler_input.request_envelope.request.intent.name == "BoxBreathingIntent"

    def handle(self, handler_input):
        # Leer los slots
        slots = handler_input.request_envelope.request.intent.slots
        cycles = int(slots["cycles"].value) if "cycles" in slots and slots["cycles"].value else 4
        duration = int(slots["duration"].value) if "duration" in slots and slots["duration"].value else 4

        # Ejecutar el ejercicio con los valores del usuario
        instructions = box_breathing(cycles, duration)
        return handler_input.response_builder.speak(instructions).response



class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = (
            "Puedes decir 'comenzar un ejercicio de respiración' para iniciar. "
            "Luego, elige la duración del ejercicio en minutos. ¿En qué más puedo ayudarte?")

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "¡Adiós! Espero haberte ayudado a relajarte."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = (
            "Lo siento, no entendí eso. Por favor intenta decir 'comenzar un ejercicio de respiración'.")

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Lo siento, hubo un problema. Por favor, inténtalo de nuevo."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(BreathingExerciseIntentHandler())
sb.add_request_handler(BreathingIntentHandler())
sb.add_request_handler(BoxBreathingIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()