import logging
import time
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Manejadores
class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        handler_input.attributes_manager.session_attributes.clear()  # Limpia cualquier estado previo
        speak_output = (
            "¡Bienvenido a tu asistente de respiración! "
            "Por favor, elige una opción: "
            "Ejercicios de respiración, "
            "Técnica Mindfulness, "
            "Recordatorios Semanales."
        )
        return handler_input.response_builder.speak(speak_output).ask("¿Qué opción te gustaría elegir?").response


class MainMenuIntentHandler(AbstractRequestHandler):
    """Handler para manejar el menú principal"""
    
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("MainMenuIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = (
            "Por favor, elige una opción: "
            "Ejercicios de respiración, "
            "Técnica Mindfulness, "
            "Recordatorios Semanales."
        )
        return handler_input.response_builder.speak(speak_output).ask("¿Qué opción te gustaría elegir?").response


class BreathingExercisesIntentHandler(AbstractRequestHandler):
    """Handler para manejar la selección de ejercicios de respiración"""
    
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("BreathingExercisesIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = (
            "Has elegido ejercicios de respiración. "
            "Por favor, elige uno: "
            "Ejercicio básico, "
            "Ejercicio 4-7-8, "
            "Respiración en caja."
        )
        return handler_input.response_builder.speak(speak_output).ask("¿Cuál ejercicio te gustaría intentar?").response


class ReadyIntentHandler(AbstractRequestHandler):
    """Handler para manejar cuando el usuario dice 'listo'"""
    
    def can_handle(self, handler_input):
        return (
            ask_utils.is_intent_name("AMAZON.YesIntent")(handler_input) or
            ask_utils.is_intent_name("ReadyIntent")(handler_input)
        )

    def handle(self, handler_input):
        session_attr = handler_input.attributes_manager.session_attributes
        exercise_type = session_attr.get("exercise_type")
        
        if exercise_type == "478":
            return self.handle_478_exercise(handler_input)
        elif exercise_type == "box":
            return self.handle_box_exercise(handler_input)
        elif exercise_type == "basic":
            return self.handle_basic_exercise(handler_input)
        else:
            return handler_input.response_builder.speak(
                "No hay un ejercicio activo. ¿Qué ejercicio te gustaría hacer?"
            ).ask("¿Qué ejercicio te gustaría hacer?").response

    def handle_478_exercise(self, handler_input):
        session_attr = handler_input.attributes_manager.session_attributes
        current_cycle = session_attr.get("current_cycle", 1)
        current_phase = session_attr.get("current_phase", "inhale")
        cycles = session_attr.get("cycles", 3)

        if current_cycle <= cycles:
            if current_phase == "inhale":
                speak_output = f"Ciclo {current_cycle}/{cycles}: Mantén la respiración durante 7 segundos."
                session_attr["current_phase"] = "hold"
            elif current_phase == "hold":
                speak_output = f"Ciclo {current_cycle}/{cycles}: Exhala completamente durante 8 segundos."
                session_attr["current_phase"] = "exhale"
            else:  # exhale phase
                if current_cycle == cycles:
                    speak_output = "¡Ejercicio completado! ¿Te gustaría hacer otro ejercicio?"
                    handler_input.attributes_manager.session_attributes.clear()
                else:
                    current_cycle += 1
                    session_attr["current_cycle"] = current_cycle
                    speak_output = f"Ciclo {current_cycle}/{cycles}: Inhala profundamente durante 4 segundos."
                    session_attr["current_phase"] = "inhale"
            
            # Pregunta adicional
            speak_output += " ¿Ya lo realizaste?"
            
            return handler_input.response_builder.speak(speak_output).ask("Di listo cuando termines.").response

    def handle_box_exercise(self, handler_input):
        session_attr = handler_input.attributes_manager.session_attributes
        current_cycle = session_attr.get("current_cycle", 1)
        current_phase = session_attr.get("current_phase", 1)
        cycles = session_attr.get("cycles", 4)
        duration = session_attr.get("duration", 4)

        if current_cycle <= cycles:
            if current_phase == 1:
                speak_output = f"Ciclo {current_cycle}/{cycles}: Inhala lentamente durante {duration} segundos."
                session_attr["current_phase"] = 2
            elif current_phase == 2:
                speak_output = f"Ciclo {current_cycle}/{cycles}: Sosten la respiración durante {duration} segundos."
                session_attr["current_phase"] = 3
            elif current_phase == 3:
                speak_output = f"Ciclo {current_cycle}/{cycles}: Exhala lentamente durante {duration} segundos."
                session_attr["current_phase"] = 4
            else:  # phase 4
                if current_cycle == cycles:
                    speak_output = "¡Ejercicio completado! ¿Te gustaría hacer otro ejercicio?"
                    handler_input.attributes_manager.session_attributes.clear()
                else:
                    current_cycle += 1
                    session_attr["current_cycle"] = current_cycle
                    speak_output = f"Ciclo {current_cycle}/{cycles}: Sosten nuevamente durante {duration} segundos."
                    session_attr["current_phase"] = 1
            
            # Pregunta adicional
            speak_output += " ¿Ya lo realizaste?"
            
            return handler_input.response_builder.speak(speak_output).ask("Di listo cuando termines.").response

    def handle_basic_exercise(self, handler_input):
        # Delega al handler existente
        return ContinueBreathingExerciseHandler().handle(handler_input)


class ContinueBreathingExerciseHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        session_attr = handler_input.attributes_manager.session_attributes
        return session_attr.get("current_cycle") is not None and session_attr.get("exercise_type") == "basic"

    def handle(self, handler_input):
        session_attr = handler_input.attributes_manager.session_attributes
        current_cycle = session_attr["current_cycle"]
        cycles = session_attr["cycles"]

        if current_cycle <= cycles:
            speak_output = (
                f"Ciclo {current_cycle}/{cycles}: "
                f"Sosten la respiración durante {session_attr['hold_duration']} segundos. "
                f"Y luego, exhala durante {session_attr['exhale_duration']} segundos."
            )
            session_attr["current_cycle"] += 1
            return handler_input.response_builder.speak(speak_output).ask("Di listo cuando termines.").response
        else:
            speak_output = (
                "¡Ejercicio completado! Espero que te sientas más relajado. "
                "¿Te gustaría hacer otro ejercicio?"
            )
            handler_input.attributes_manager.session_attributes.clear()
            return handler_input.response_builder.speak(speak_output).ask("¿Cuál te gustaría intentar?").response


# Ejercicios de respiración
def breathing_exercise(cycles=5, inhale_duration=4, hold_duration=4, exhale_duration=4):
    instructions = []
    instructions.append("¡Bienvenido al ejercicio de respiración!")
    instructions.append(f"Haremos {cycles} ciclos. Sigue las instrucciones:")
    
    for cycle in range(1, cycles + 1):
        instructions.append(f"\nCiclo {cycle}/{cycles}")
        
        # Inhalar
        instructions.append(f"Inhala durante {inhale_duration} segundos...")
        for i in range(inhale_duration):
            time.sleep(1)  # Espera un segundo
            instructions.append(f"{i + 1} segundos...")
        
        # Sostener
        instructions.append(f"Sosten la respiración durante {hold_duration} segundos...")
        for i in range(hold_duration):
            time.sleep(1)
            instructions.append(f"{i + 1} segundos...")
        
        # Exhalar
        instructions.append(f"Exhala durante {exhale_duration} segundos...")
        for i in range(exhale_duration):
            time.sleep(1)
            instructions.append(f"{i + 1} segundos...")
    
    instructions.append("\n¡Ejercicio completado! Espero que te sientas más relajado.")
    return " ".join(instructions)

def breathing_4_7_8(cycles=3):
    instructions = []
    instructions.append("Ejercicio de respiracion 4-7-8 para relajarte:")
    
    for cycle in range(1, cycles + 1):
        instructions.append(f"\nCiclo {cycle}/{cycles}")
        instructions.append("Inhala profundamente durante 4 segundos...")
        for i in range(4):
            time.sleep(1)
            instructions.append(f"{i + 1} segundos...")
        instructions.append("Sosten la respiracion durante 7 segundos...")
        for i in range(7):
            time.sleep(1)
            instructions.append(f"{i + 1} segundos...")
        instructions.append("Exhala completamente durante 8 segundos...")
        for i in range(8):
            time.sleep(1)
            instructions.append(f"{i + 1} segundos...")
    
    instructions.append("\n¡Ejercicio completado! Este método ayuda a calmar la mente y el cuerpo.")
    return " ".join(instructions)

def box_breathing(cycles=4, duration=4):
    instructions = []
    instructions.append("Ejercicio de respiracion en caja (Box Breathing):")
    instructions.append(f"Duración de cada fase: {duration} segundos.")
    
    for cycle in range(1, cycles + 1):
        instructions.append(f"\nCiclo {cycle}/{cycles}")
        
        # Inhalar
        instructions.append("Inhala lentamente...")
        for i in range(duration):
            time.sleep(1)
            instructions.append(f"{i + 1} segundos...")
        
        # Sostener
        instructions.append("Sosten la respiración...")
        for i in range(duration):
            time.sleep(1)
            instructions.append(f"{i + 1} segundos...")
        
        # Exhalar
        instructions.append("Exhala lentamente...")
        for i in range(duration):
            time.sleep(1)
            instructions.append(f"{i + 1} segundos...")
        
        # Sostener nuevamente
        instructions.append("Sosten nuevamente...")
        for i in range(duration):
            time.sleep(1)
            instructions.append(f"{i + 1} segundos...")
    
    instructions.append("\n¡Ejercicio completado! Este método es excelente para centrarte.")
    return " ".join(instructions)


# Otros manejadores
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
        return handler_input.response_builder.speak(speak_output).ask(speak_output).response


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
        return handler_input.response_builder.speak(speak_output).ask("¿Qué ejercicio deseas realizar?").response


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
        handler_input.attributes_manager.session_attributes.clear()  # Limpia la sesión en caso de error
        speak_output = (
            "Lo siento, hubo un problema. La sesión se reiniciará. "
            "Puedes decir: 'iniciar ejercicio básico', 'respiración cuatro siete ocho', o 'ejercicio en caja'."
        )
        return handler_input.response_builder.speak(speak_output).ask("¿Qué ejercicio deseas realizar?").response


# Configuración del Skill
sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(MainMenuIntentHandler())
sb.add_request_handler(BreathingExercisesIntentHandler())
sb.add_request_handler(ReadyIntentHandler()) 
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
