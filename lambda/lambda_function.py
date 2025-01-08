# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = ("Bienvenido a Respira y Relájate. Esta skill te ayudará a gestionar el estrés con ejercicios de respiración."
                        "Di 'comenzar un ejercicio de respiración' para iniciar.")

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class BreathingExerciseIntentHandler(AbstractRequestHandler):
    """Handler for Breathing Exercise Intent."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("BreathingExerciseIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = (
            "Vamos a comenzar un ejercicio de respiración. ¿Cuánto tiempo te gustaría practicar? "
            "Puedes decir, por ejemplo, 2 minutos o 5 minutos.")

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
        
class SetBreathingDurationIntentHandler(AbstractRequestHandler):
    """Handler to set the duration of the breathing exercise."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("SetBreathingDurationIntent")(handler_input)

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        duration = slots["duration"].value  # Duration slot captured from user input

        try:
            duration_minutes = int(duration)
            total_seconds = duration_minutes * 60

            speak_output = (f"Perfecto, practicaremos la respiración durante {duration_minutes} minutos. "
                            "Inhalemos durante 4 segundos, mantengamos la respiración durante 7 segundos, "
                            "y exhalemos durante 8 segundos. Comencemos.")

            # Loop to simulate breathing guidance
            for i in range(total_seconds // 19):  # Each cycle takes 19 seconds (4+7+8)
                speak_output += (
                    " Inhala... 1, 2, 3, 4. Mantén la respiración... 1, 2, 3, 4, 5, 6, 7. "
                    "Exhala... 1, 2, 3, 4, 5, 6, 7, 8.")

            speak_output += " ¡Bien hecho! Has completado el ejercicio. Espero que te sientas más relajado."

        except ValueError:
            speak_output = "Lo siento, no entendí la duración. Por favor di un número en minutos, como 2 o 5."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )        


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
sb.add_request_handler(SetBreathingDurationIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()