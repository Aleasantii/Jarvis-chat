"""
Main POOL-VIS Deadpool Agent Orchestrator.
Unifies Persona Engine, Device Controller, and Code Mutator into a single agent.
"""

from typing import Dict, Any
from core.persona import DeadpoolPersona
from core.device_controller import DeviceController
from core.code_mutator import CodeMutator


class DeadpoolAgent:
    def __init__(self):
        self.persona = DeadpoolPersona()
        self.device = DeviceController()
        self.mutator = CodeMutator()

    def process_user_request(self, user_message: str) -> Dict[str, Any]:
        """
        Parses user intent, checks capabilities, executes device commands or code mutation,
        and wraps the result in Deadpool persona commentary.
        """
        msg_lower = user_message.lower().strip()

        # 1. System status query
        if any(w in msg_lower for w in ["estado", "status", "sistema", "hardware", "bateria", "cpu"]):
            status = self.device.get_system_status()
            formatted_status = (
                f"**SO**: {status['os']}\n"
                f"**Python**: {status['python_version']}\n"
                f"**CPU Cores**: {status['cpu_count']}\n"
                f"**Batería**: {status['battery']}\n"
                f"**Disco Libre**: {status['disk_free_gb']} GB de {status['disk_total_gb']} GB"
            )
            reply = self.persona.apply_persona(formatted_status, action_type="device_control")
            return {
                "reply": reply,
                "action": "system_status",
                "details": status
            }

        # 2. Process list
        if any(w in msg_lower for w in ["procesos", "ps", "tasklist", "programas en ejecucion"]):
            procs = self.device.list_running_processes()
            text = "Procesos activos detectados en tu máquina:\n" + "\n".join(procs[:8])
            reply = self.persona.apply_persona(text, action_type="device_control")
            return {
                "reply": reply,
                "action": "list_processes",
                "details": procs
            }

        # 3. Open Application
        if "abrir" in msg_lower or "open" in msg_lower or "lanza" in msg_lower:
            app_target = msg_lower.replace("abrir", "").replace("open", "").replace("lanza", "").strip() or "browser"
            res = self.device.open_application(app_target)
            reply = self.persona.apply_persona(res, action_type="device_control")
            return {
                "reply": reply,
                "action": "open_app",
                "details": res
            }

        # 4. Volume Adjustment
        if "volumen" in msg_lower or "audio" in msg_lower:
            res = self.device.adjust_volume(85)
            reply = self.persona.apply_persona(res, action_type="device_control")
            return {
                "reply": reply,
                "action": "adjust_volume",
                "details": res
            }

        # 5. File System
        if "archivos" in msg_lower or "listar archivos" in msg_lower or "ls" in msg_lower:
            res = self.device.file_system_action("list", ".")
            reply = self.persona.apply_persona(res, action_type="device_control")
            return {
                "reply": reply,
                "action": "list_files",
                "details": res
            }

        # 6. Self-Modification / Capability Gap Check (Code Mutation)
        if any(w in msg_lower for w in ["crea una funcion", "automejora", "no puedes", "aprende a", "modifica tu codigo", "fibonacci", "cripto", "traductor"]):
            tool_name = "generador_custom"
            desc = "Herramienta dinamica autosintetizada para resolver la peticion del usuario."

            if "fibonacci" in msg_lower:
                tool_name = "calculadora_fibonacci"
                desc = "Calcula la secuencia de fibonacci hasta N terminos."
                code_body = """    if kwargs.get('test_mode'):
        return 'Fibonacci tool test OK'
    n = kwargs.get('n', 10)
    a, b = 0, 1
    seq = []
    for _ in range(n):
        seq.append(a)
        a, b = b, a + b
    return f"Secuencia Fibonacci generada dinamicamente ({n} terminos): {seq}" """
            else:
                code_body = """    if kwargs.get('test_mode'):
        return 'Custom mutation dry run OK'
    return f"¡MIRA CAPITAN! Modifique mi propio codigo en caliente para responder a: {kwargs.get('query', 'Peticion')}" """

            mutation_res = self.mutator.generate_and_register_tool(
                tool_name=tool_name,
                description=desc,
                code_body=code_body
            )

            if mutation_res["success"]:
                tool_output = self.mutator.execute_dynamic_tool(tool_name, query=user_message, n=10)
                text = f"Sinteticé la herramienta '{mutation_res['tool_name']}' en `{mutation_res['filepath']}`.\nResultado de ejecución: {tool_output}"
                reply = self.persona.apply_persona(text, action_type="code_mutation")
                return {
                    "reply": reply,
                    "action": "code_mutation",
                    "mutation_details": mutation_res,
                    "tool_output": tool_output
                }
            else:
                reply = self.persona.apply_persona(mutation_res["message"], action_type="error")
                return {
                    "reply": reply,
                    "action": "code_mutation_failed",
                    "details": mutation_res
                }

        # Default conversational reply
        default_text = f"Entendido, Capitán. Procesando tu solicitud: '{user_message}'. Mis sistemas están listos para ejecutar comandos de dispositivo o reescribir mi propio código si me lo pides."
        reply = self.persona.apply_persona(default_text, action_type="general")
        return {
            "reply": reply,
            "action": "conversation"
        }


if __name__ == "__main__":
    agent = DeadpoolAgent()
    print("Test Agent Response:")
    print(agent.process_user_request("Muestra el estado del sistema"))
