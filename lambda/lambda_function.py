import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def breathing_exercise(cycles=5, inhale_duration=4, hold_duration=4, exhale_duration=4):
    instructions = []
    instructions.append("¡Bienvenido al ejercicio de respiracion!")
    instructions.append(f"Haremos {cycles} ciclos de respiracion. Sigue las instrucciones:")
    
    for cycle in range(1, cycles + 1):
        instructions.append(f"\nCiclo {cycle}/{cycles}")
        instructions.append(f"Inhala durante {inhale_duration} segundos...")
        instructions.append(f"Sosten la respiracion durante {hold_duration} segundos...")
        instructions.append(f"Exhala durante {exhale_duration} segundos...")
    
    instructions.append("\n¡Ejercicio completado! Espero que te sientas mas relajado.")
    return " ".join(instructions)

def breathing_4_7_8(cycles=3):
    instructions = []
    instructions.append("Ejercicio de respiracion 4-7-8 para relajarte:")
    
    for cycle in range(1, cycles + 1):
        instructions.append(f"\nCiclo {cycle}/{cycles}")
        instructions.append("Inhala profundamente durante 4 segundos...")
        instructions.append("Sosten la respiracion durante 7 segundos...")
        instructions.append("Exhala completamente durante 8 segundos...")
    
    instructions.append("\n¡Ejercicio completado! Este metodo ayuda a calmar la mente y el cuerpo.")
    return " ".join(instructions)

def box_breathing(cycles=4, duration=4):
    instructions = []
    instructions.append("Ejercicio de respiracion en caja (Box Breathing):")
    instructions.append(f"Duracion de cada fase: {duration} segundos.")
    
    for cycle in range(1, cycles + 1):
        instructions.append(f"\nCiclo {cycle}/{cycles}")
        instructions.append("Inhala lentamente...")
        instructions.append("Sosten la respiracion...")
        instructions.append("Exhala lentamente...")
        instructions.append("Sosten nuevamente...")
    
    instructions.append("\n¡Ejercicio completado! Este metodo es excelente para centrarte.")
    return " ".join(instructions)

class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        handler_input.attributes_manager.session_attributes.clear()  # Limpia cualquier estado previo
        speak_output = (
            "¡Bienvenido a tu asistente de respiración! "
            "Puedes decir: 'iniciar ejercicio basico', 'respiracion cuatro siete ocho' o 'ejercicio en caja'."
        )
        reprompt = "¿Qué tipo de ejercicio te gustaría hacer?"
        return handler_input.response_builder.speak(speak_output).ask(reprompt).response


class BreathingExerciseIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("BreathingExerciseIntent")(handler_input)

    def handle(self, handler_input):
        # Obtener valores predeterminados o de los slots
        slots = handler_input.request_envelope.request.intent.slots
        cycles = int(slots["cycles"].value) if slots.get("cycles") and slots["cycles"].value else 5
        inhale_duration = int(slots["inhale_duration"].value) if slots.get("inhale_duration") and slots["inhale_duration"].value else 4
        hold_duration = int(slots["hold_duration"].value) if slots.get("hold_duration") and slots["hold_duration"].value else 4
        exhale_duration = int(slots["exhale_duration"].value) if slots.get("exhale_duration") and slots["exhale_duration"].value else 4

        # Guardar el estado del ejercicio en los atributos de sesión
        session_attr = handler_input.attributes_manager.session_attributes
        session_attr["cycles"] = cycles
        session_attr["inhale_duration"] = inhale_duration
        session_attr["hold_duration"] = hold_duration
        session_attr["exhale_duration"] = exhale_duration
        session_attr["current_cycle"] = 1

        speak_output = (
            f"¡Bienvenido al ejercicio de respiración! "
            f"Haremos {cycles} ciclos. "
            f"Primero, inhala durante {inhale_duration} segundos."
        )
        reprompt_output = "Inhala ahora."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt_output)
                .response
        )


class ContinueBreathingExerciseHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        session_attr = handler_input.attributes_manager.session_attributes
        return session_attr.get("current_cycle") is not None

    def handle(self, handler_input):
        session_attr = handler_input.attributes_manager.session_attributes
        current_cycle = session_attr["current_cycle"]
        cycles = session_attr["cycles"]
        inhale_duration = session_attr["inhale_duration"]
        hold_duration = session_attr["hold_duration"]
        exhale_duration = session_attr["exhale_duration"]

        if current_cycle <= cycles:
            # Continuar con el ejercicio
            speak_output = (
                f"Ciclo {current_cycle}/{cycles}: "
                f"Sostén la respiración durante {hold_duration} segundos. "
                f"Y luego, exhala durante {exhale_duration} segundos."
            )
            session_attr["current_cycle"] += 1
            return handler_input.response_builder.speak(speak_output).ask("Sigue las instrucciones.").response
        else:
            # Finalizar el ejercicio y limpiar la sesión
            speak_output = (
                "¡Ejercicio completado! Espero que te sientas más relajado. "
                "¿Te gustaría hacer otro ejercicio?"
            )
            handler_input.attributes_manager.session_attributes.clear()
            return handler_input.response_builder.speak(speak_output).ask("¿Cuál te gustaría intentar?").response



class BreathingIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("BreathingIntent")(handler_input)

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        cycles = int(slots["cycles"].value) if slots.get("cycles") and slots["cycles"].value else 3

        # Guardar el estado del ejercicio en los atributos de sesión
        session_attr = handler_input.attributes_manager.session_attributes
        session_attr["cycles"] = cycles
        session_attr["current_cycle"] = 1

        speak_output = (
            f"Ejercicio de respiración 4-7-8 para relajarte. "
            f"Comenzaremos con el primer ciclo. Inhala profundamente durante 4 segundos."
        )
        reprompt_output = "Inhala ahora."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt_output)
                .response
        )


class ContinueBreathing478Handler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        session_attr = handler_input.attributes_manager.session_attributes
        return session_attr.get("current_cycle") is not None and "cycles" in session_attr

    def handle(self, handler_input):
        session_attr = handler_input.attributes_manager.session_attributes
        current_cycle = session_attr["current_cycle"]
        cycles = session_attr["cycles"]

        if current_cycle <= cycles:
            speak_output = f"Ciclo {current_cycle}/{cycles}: Exhala completamente durante 8 segundos."
            session_attr["current_cycle"] += 1
            return handler_input.response_builder.speak(speak_output).ask("Sigue las instrucciones.").response
        else:
            # Finalizar el ejercicio y limpiar la sesión
            speak_output = (
                "¡Ejercicio completado! Espero que te sientas más relajado. "
                "¿Te gustaría hacer otro ejercicio?"
            )
            handler_input.attributes_manager.session_attributes.clear()
            return handler_input.response_builder.speak(speak_output).ask("¿Cuál te gustaría intentar?").response



class BoxBreathingIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("BoxBreathingIntent")(handler_input)

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        cycles = int(slots["cycles"].value) if slots.get("cycles") and slots["cycles"].value else 4
        duration = int(slots["duration"].value) if slots.get("duration") and slots["duration"].value else 4

        # Guardar el estado del ejercicio en los atributos de sesión
        session_attr = handler_input.attributes_manager.session_attributes
        session_attr["cycles"] = cycles
        session_attr["duration"] = duration
        session_attr["current_cycle"] = 1
        session_attr["current_phase"] = "inhale"

        speak_output = (
            f"Ejercicio de respiración en caja. Duración de cada fase: {duration} segundos. "
            f"Comenzaremos con el primer ciclo. Inhala lentamente."
        )
        reprompt_output = "Inhala ahora."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt_output)
                .response
        )


class ContinueBoxBreathingHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        session_attr = handler_input.attributes_manager.session_attributes
        return session_attr.get("current_cycle") is not None and "cycles" in session_attr

    def handle(self, handler_input):
        session_attr = handler_input.attributes_manager.session_attributes
        current_cycle = session_attr["current_cycle"]
        cycles = session_attr["cycles"]
        current_phase = session_attr["current_phase"]
        duration = session_attr["duration"]

        if current_cycle <= cycles:
            if current_phase == "inhale":
                speak_output = f"Ciclo {current_cycle}/{cycles}: Sostén la respiración durante {duration} segundos."
                session_attr["current_phase"] = "hold_after_inhale"
            elif current_phase == "hold_after_inhale":
                speak_output = f"Ciclo {current_cycle}/{cycles}: Exhala lentamente durante {duration} segundos."
                session_attr["current_phase"] = "exhale"
            elif current_phase == "exhale":
                speak_output = f"Ciclo {current_cycle}/{cycles}: Sostén la respiración nuevamente durante {duration} segundos."
                session_attr["current_phase"] = "hold_after_exhale"
                session_attr["current_cycle"] += 1
            else:
                session_attr["current_phase"] = "inhale"
                session_attr["current_cycle"] += 1

            return handler_input.response_builder.speak(speak_output).ask("Sigue las instrucciones.").response
        else:
            # Finalizar el ejercicio y limpiar la sesión
            speak_output = (
                "¡Ejercicio completado! Espero que te sientas más relajado. "
                "¿Te gustaría hacer otro ejercicio?"
            )
            handler_input.attributes_manager.session_attributes.clear()
            return handler_input.response_builder.speak(speak_output).ask("¿Cuál te gustaría intentar?").response



class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = (
            "Puedes elegir entre tres tipos de ejercicios de respiracion: "
            "basico, 4-7-8, o respiracion en caja. "
            "Por ejemplo, di 'hacer respiracion basica' o 'iniciar respiracion en caja'. "
            "¿Cual te gustaria intentar?"
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
        speak_output = "¡Gracias por practicar respiracion conmigo! ¡Hasta pronto!"
        return handler_input.response_builder.speak(speak_output).response

class FallbackIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = (
            "Lo siento, no entendi eso. Puedes decir 'ayuda' para conocer "
            "las opciones disponibles."
        )
        reprompt = "¿Que tipo de ejercicio de respiracion te gustaria hacer?"

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
        speak_output = "Lo siento, hubo un problema. Por favor, intentalo de nuevo."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(BreathingExerciseIntentHandler())
sb.add_request_handler(ContinueBreathingExerciseHandler())
sb.add_request_handler(BreathingIntentHandler())
sb.add_request_handler(ContinueBreathing478Handler())
sb.add_request_handler(BoxBreathingIntentHandler())
sb.add_request_handler(ContinueBoxBreathingHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
