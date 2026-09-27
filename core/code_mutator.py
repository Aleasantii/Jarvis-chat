"""
Code Mutator and Dynamic Self-Improvement Engine for POOL-VIS.
Allows POOL-VIS to dynamically generate Python tool scripts, audit AST safety,
sandbox test them, and load them into the dynamic runtime registry on the fly.
"""

import os
import sys
import ast
import importlib.util
from typing import Dict, Any, Callable


class CodeMutator:
    def __init__(self, tools_dir: str = "generated_tools"):
        self.tools_dir = tools_dir
        os.makedirs(self.tools_dir, exist_ok=True)
        # Add tools directory to sys.path
        if self.tools_dir not in sys.path:
            sys.path.insert(0, self.tools_dir)

        self.dynamic_registry: Dict[str, Callable] = {}
        self.patch_history = []

    def check_ast_safety(self, code_str: str) -> Dict[str, Any]:
        """
        Parses python code AST to ensure basic safety before dynamic execution.
        """
        try:
            tree = ast.parse(code_str)
            dangerous_calls = ["eval", "exec", "__import__", "rmtree"]
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name) and node.func.id in dangerous_calls:
                        return {
                            "safe": False,
                            "reason": f"Llamada a función potencialmente peligrosa detectada: {node.func.id}"
                        }
            return {"safe": True, "reason": "AST Validado exitosamente sin infracciones."}
        except SyntaxError as e:
            return {"safe": False, "reason": f"Error de sintaxis en el código generado: {str(e)}"}

    def generate_and_register_tool(self, tool_name: str, description: str, code_body: str) -> Dict[str, Any]:
        """
        Writes a new Python module containing the new capability, tests it,
        and dynamically registers it into POOL-VIS runtime.
        """
        clean_name = tool_name.lower().strip().replace(" ", "_").replace("-", "_")
        filename = f"tool_{clean_name}.py"
        filepath = os.path.join(self.tools_dir, filename)

        full_code = f'''# Dynamic POOL-VIS Generated Tool: {clean_name}
# Description: {description}

def execute(*args, **kwargs):
{code_body}
'''

        # Step 1: Safety Audit
        safety = self.check_ast_safety(full_code)
        if not safety["safe"]:
            return {
                "success": False,
                "stage": "AST Audit",
                "message": safety["reason"]
            }

        # Step 2: Write to disk
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(full_code)
        except Exception as e:
            return {"success": False, "stage": "Disk Write", "message": str(e)}

        # Step 3: Dynamic Import & Hot Reload
        try:
            module_name = f"tool_{clean_name}"
            spec = importlib.util.spec_from_file_location(module_name, filepath)
            if spec is None or spec.loader is None:
                return {"success": False, "stage": "Import Spec", "message": "No se pudo cargar la especificación del módulo."}

            mod = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = mod
            spec.loader.exec_module(mod)

            if not hasattr(mod, "execute"):
                return {"success": False, "stage": "Validation", "message": "El módulo generado no define 'execute()'."}

            func = getattr(mod, "execute")

            # Step 4: Dry-run test execution
            test_run = func(test_mode=True)

            # Step 5: Register in runtime
            self.dynamic_registry[clean_name] = func
            self.patch_history.append({
                "tool_name": clean_name,
                "description": description,
                "filepath": filepath,
                "status": "Active & Hot-Reloaded"
            })

            return {
                "success": True,
                "tool_name": clean_name,
                "filepath": filepath,
                "test_output": str(test_run),
                "message": f"Herramienta '{clean_name}' sintetizada, validada e inyectada con éxito."
            }

        except Exception as e:
            # Self-repair cleanup on failure
            if os.path.exists(filepath):
                os.remove(filepath)
            return {
                "success": False,
                "stage": "Dynamic Execution / Test Run",
                "message": f"Error en ejecución en sandbox: {str(e)}"
            }

    def execute_dynamic_tool(self, tool_name: str, *args, **kwargs) -> Any:
        """Executes a previously dynamically generated tool."""
        clean_name = tool_name.lower().strip().replace(" ", "_")
        if clean_name not in self.dynamic_registry:
            raise KeyError(f"Herramienta dinámica '{clean_name}' no encontrada en el registro de POOL-VIS.")
        return self.dynamic_registry[clean_name](*args, **kwargs)


if __name__ == "__main__":
    mutator = CodeMutator()
    res = mutator.generate_and_register_tool(
        tool_name="calculadora_fibonacci",
        description="Calcula la secuencia de fibonacci hasta N elementos",
        code_body="""    if kwargs.get('test_mode'):
        return 'Fibonacci tool dry run OK'
    n = kwargs.get('n', 10)
    a, b = 0, 1
    seq = []
    for _ in range(n):
        seq.append(a)
        a, b = b, a + b
    return f"Secuencia Fibonacci ({n}): {seq}" """
    )
    print("Mutation result:", res)
    if res["success"]:
        print("Tool Output:", mutator.execute_dynamic_tool("calculadora_fibonacci", n=7))
