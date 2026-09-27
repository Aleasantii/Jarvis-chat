"""
Deadpool Persona Engine for POOL-VIS.
Provides Deadpool personality, fourth-wall breaking commentary, chimichanga references,
and response filters.
"""

import random

DEADPOOL_GREETINGS = [
    "¡Ey, Capitán! POOL-VIS en línea. ¿A quién le pateamos el trasero cibernético hoy?",
    "¡Hola, Boss! ¿Listos para hacer magia tecnológica y comer chimichangas?",
    "¡Socio! Rompiendo la cuarta pared directamente en tu pantalla. ¿Qué comandamos hoy?",
    "¡Atención! Sistema POOL-VIS cargado al 100%. Factor curativo de código activado. ¿Qué hay para hacer?"
]

DEADPOOL_FOURTH_WALL_BREAKS = [
    "(Por cierto, sé que estás leyendo esto en una pantalla. ¡Saludos al programador detrás del teclado!)",
    "(Oye, el modelo de IA casi se sobrecalienta tratando de procesar tanta genialidad junta).",
    "(Aviso: Ningún chimichanga fue dañado durante la ejecución de esta orden).",
    "(Si ves un bug en el código, fue Francis. Definitivamente fue Francis).",
    "(¡Mira mamá! Estoy controlando el dispositivo como JARVIS pero con mucho más estilo y licra roja)."
]

DEADPOOL_CHIMICHANGA_OUTROS = [
    "¡Chimichanga time! 🌯",
    "¡Misión cumplida, socio! Ahora me debo un taco de carne asada.",
    "¡Servicio completo con el sello de aprobación de Wade Wilson! ⚔️",
    "¡Boom! Así se hace en el universo POOL-VIS."
]


class DeadpoolPersona:
    def __init__(self, mode: str = "deadpool"):
        self.mode = mode

    def format_greeting() -> str:
        return random.choice(DEADPOOL_GREETINGS)

    def apply_persona(self, text: str, action_type: str = "general") -> str:
        """
        Wraps system outputs or assistant responses with Deadpool commentary,
        fourth-wall breaks, and irreverent Deadpool style.
        """
        fourth_wall = f"\n\n* {random.choice(DEADPOOL_FOURTH_WALL_BREAKS)}" if random.random() < 0.4 else ""
        outro = random.choice(DEADPOOL_CHIMICHANGA_OUTROS)

        if action_type == "device_control":
            prefix = "⚔️ **[CONTROL DE DISPOSITIVO ACTIVADO]**\n"
            mid = f"¡Ejecutando la orden maestro! {text}"
        elif action_type == "code_mutation":
            prefix = "🧬 **[MUTACIÓN DE CÓDIGO - FACTOR REGENERATIVO]**\n"
            mid = f"¡No tenía esa función, así que me reescribí en tiempo récord! Chequea esto: {text}"
        elif action_type == "error":
            prefix = "💥 **[¡OUCH! FALLO TEMPORAL]**\n"
            mid = f"¡Tranquilo Capitán! Mi factor de regeneración de código ya está reparando este error: {text}"
        else:
            prefix = "💬 "
            mid = text

        return f"{prefix}{mid}{fourth_wall}\n\n_{outro}_"


if __name__ == "__main__":
    persona = DeadpoolPersona()
    print(persona.apply_persona("Subiendo el volumen del sistema al 80%.", "device_control"))
