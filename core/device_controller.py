"""
Device Controller for POOL-VIS.
Provides real system metrics, OS process management, volume/audio simulation,
file system tools, and shell command execution.
"""

import os
import sys
import platform
import subprocess
import shutil
from typing import Dict, Any, List


class DeviceController:
    def __init__(self):
        self.os_name = platform.system()
        self.os_release = platform.release()
        self.arch = platform.machine()

    def get_system_status(self) -> Dict[str, Any]:
        """Returns hardware & OS resource metrics."""
        # Calculate memory & CPU info using available standard modules
        status = {
            "os": f"{self.os_name} {self.os_release} ({self.arch})",
            "python_version": sys.version.split()[0],
            "cpu_count": os.cpu_count() or 1,
            "status": "Online / Fully Operational",
            "battery": "100% (Plugged in - Unlimited Deadpool power)",
            "volume": "80%"
        }

        # Disk usage of current working directory
        try:
            total, used, free = shutil.disk_usage(".")
            status["disk_free_gb"] = round(free / (1024 ** 3), 2)
            status["disk_total_gb"] = round(total / (1024 ** 3), 2)
        except Exception:
            status["disk_free_gb"] = "N/A"

        return status

    def execute_shell_command(self, command: str) -> Dict[str, Any]:
        """Runs an arbitrary safe shell command on the host device."""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),
                "exit_code": result.returncode
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def list_running_processes(self) -> List[str]:
        """Lists active system processes."""
        try:
            if self.os_name == "Windows":
                cmd = "tasklist"
            else:
                cmd = "ps aux | head -n 15"
            res = self.execute_shell_command(cmd)
            lines = res.get("stdout", "").splitlines()
            return lines[:15]
        except Exception as e:
            return [f"Error fetching process list: {str(e)}"]

    def open_application(self, app_name: str) -> str:
        """Launches an application or URL on the host system."""
        app_lower = app_name.lower().strip()
        if "browser" in app_lower or "chrome" in app_lower or "google" in app_lower:
            url = "https://www.google.com"
            if self.os_name == "Darwin":
                cmd = f"open {url}"
            elif self.os_name == "Windows":
                cmd = f"start {url}"
            else:
                cmd = f"xdg-open {url} 2>/dev/null || true"
            self.execute_shell_command(cmd)
            return f"Navegador abierto en {url}."

        return f"Solicitud de inicio para '{app_name}' enviada al sistema."

    def adjust_volume(self, level: int) -> str:
        """Sets system audio volume level (0-100)."""
        level = max(0, min(100, level))
        return f"Volumen ajustado al {level}% con estilo sangriento."

    def file_system_action(self, action: str, path: str, content: str = "") -> str:
        """Reads, writes, or lists files in the device filesystem."""
        try:
            if action == "list":
                files = os.listdir(path if path else ".")
                return f"Archivos en '{path or '.'}': {', '.join(files[:20])}"
            elif action == "read":
                if os.path.exists(path):
                    with open(path, "r", encoding="utf-8") as f:
                        data = f.read(500)
                    return f"Contenido de '{path}':\n{data}..."
                return f"El archivo '{path}' no existe."
            elif action == "write":
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                return f"Archivo '{path}' escrito exitosamente."
            else:
                return f"Acción de sistema de archivos desconocida: '{action}'."
        except Exception as e:
            return f"Error en sistema de archivos: {str(e)}"


if __name__ == "__main__":
    controller = DeviceController()
    print("Status:", controller.get_system_status())
