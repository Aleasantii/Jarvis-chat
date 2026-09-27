"""
Unit tests for POOL-VIS (Deadpool JARVIS AI Assistant core).
"""

import os
import unittest
from core.persona import DeadpoolPersona
from core.device_controller import DeviceController
from core.code_mutator import CodeMutator
from core.deadpool_agent import DeadpoolAgent


class TestPoolVisCore(unittest.TestCase):

    def setUp(self):
        self.persona = DeadpoolPersona()
        self.device = DeviceController()
        self.mutator = CodeMutator(tools_dir="test_generated_tools")
        self.agent = DeadpoolAgent()

    def test_deadpool_persona(self):
        output = self.persona.apply_persona("Prueba de mensaje", action_type="device_control")
        self.assertIn("CONTROL DE DISPOSITIVO", output)
        self.assertIn("Prueba de mensaje", output)

    def test_device_controller_status(self):
        status = self.device.get_system_status()
        self.assertIn("os", status)
        self.assertIn("python_version", status)
        self.assertIn("battery", status)

    def test_device_controller_shell(self):
        res = self.device.execute_shell_command("echo 'Hello POOL-VIS'")
        self.assertTrue(res["success"])
        self.assertIn("Hello POOL-VIS", res["stdout"])

    def test_code_mutator_generation_and_execution(self):
        res = self.mutator.generate_and_register_tool(
            tool_name="test_addition",
            description="Adds two numbers",
            code_body="""    if kwargs.get('test_mode'):
        return 'Test add OK'
    a = kwargs.get('a', 0)
    b = kwargs.get('b', 0)
    return a + b"""
        )
        self.assertTrue(res["success"])
        out = self.mutator.execute_dynamic_tool("test_addition", a=5, b=10)
        self.assertEqual(out, 15)

    def test_agent_orchestrator_status(self):
        response = self.agent.process_user_request("Muestra el estado del sistema")
        self.assertEqual(response["action"], "system_status")
        self.assertIn("reply", response)

    def test_agent_orchestrator_mutation(self):
        response = self.agent.process_user_request("Calcula la secuencia fibonacci por favor")
        self.assertEqual(response["action"], "code_mutation")
        self.assertIn("calculadora_fibonacci", response["mutation_details"]["tool_name"])


if __name__ == "__main__":
    unittest.main()
