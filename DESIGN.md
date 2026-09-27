# POOL-VIS: Deadpool-styled JARVIS AI System Architecture & Design

## 1. Executive Overview
**POOL-VIS** (Pool Virtual Intelligent System) is an autonomous, device-controlling AI assistant inspired by Tony Stark's JARVIS, but re-engineered with the personality, fourth-wall breaking banter, and self-healing capability of **Deadpool** (Wade Wilson).

Unlike conventional stiff assistants, POOL-VIS possesses three core paradigms:
1. **Unfiltered Deadpool Personality & Fourth-Wall Awareness**: Sarcastic, humorous, fourth-wall breaking, chimichanga-loving, yet fully competent and loyal to the user ("Captain / Boss").
2. **Total Device Control Architecture**: Direct native hooks into operating system execution, process control, file system manipulation, hardware status monitoring, and app automation.
3. **Dynamic Self-Modification Engine (Self-Healing & Code Generation)**: When requested to perform a task outside its current capabilities, POOL-VIS automatically writes a new Python module/tool, runs AST validation and sandbox tests, registers the new tool live into its runtime tool set, and executes the command seamlessly.

---

## 2. System Architecture Overview

```
+-------------------------------------------------------------------------+
|                              USER INTERFACE                             |
|         Web HUD (Crimson/Black Deadpool Tactical Aesthetic)            |
|       Speech Recognition / TTS Synthesis / Real-Time Dynamic Logs       |
+------------------------------------+------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                          DEADPOOL AGENT CORE                            |
|                       (`core/deadpool_agent.py`)                        |
|  - Request Router & Intent Classifier                                   |
|  - Context Manager & Memory Store                                       |
|  - Response Synthesizer + Deadpool Filter                               |
+------------------+-------------------+----------------------------------+
                   |                   |
        +----------+                   +----------+
        v                                         v
+-----------------------------+         +----------------------------------+
|    DEVICE CONTROLLER        |         |       CODE MUTATOR ENGINE        |
|  (`core/device_controller.py`)        |     (`core/code_mutator.py`)     |
| - Process Manager           |         | - Capability Gap Analysis        |
| - Shell Execution           |         | - Dynamic Python Tool Generator  |
| - System Health & Stats     |         | - AST Safety & Security Check    |
| - App / File Automation     |         | - Dynamic Sandbox Tester         |
+-----------------------------+         | - Hot-Reload & Dynamic Registry  |
                                        +----------------------------------+
```

---

## 3. Core Component Specifications

### 3.1 Deadpool Persona Engine (`core/persona.py`)
- **System Prompt Architecture**: Formats responses to speak directly to the user as "Capitán", "Boss", or "Socio".
- **Fourth-Wall Breaking**: Periodically acknowledges that it's running in code, inside a browser, on CPU cycles, or speaking to a developer writing JavaScript/Python.
- **Humor & References**: Seamlessly blends Spanish Deadpool idioms, chimichangas, tacos, superhero satire, and self-deprecating jabs while still successfully completing technical tasks.
- **Tone Modulators**: Can switch between standard Deadpool humor and high-alert tactical mode during critical system operations.

### 3.2 Total Device Control Framework (`core/device_controller.py`)
- **OS Command Engine**: Runs system commands safely (cross-platform compatible: Windows, macOS, Linux).
- **Resource & Hardware Metrics**: Reads CPU, RAM, disk, battery, and network status in real time.
- **Process Management**: Can inspect running processes, launch applications, or terminate frozen tasks.
- **File System Operations**: Read, write, search, organize files and directory trees.
- **Volume & Screen Control**: Hooks for audio muting/volume levels and screen brightness control.

### 3.3 Dynamic Code Mutation & Self-Improvement Loop (`core/code_mutator.py`)
When a user asks for a feature that POOL-VIS doesn't have in its tool registry:
1. **Gap Analysis**: Identifies missing functions (e.g., "calculate_fibonacci_sequence", "convert_image_to_pdf", "fetch_crypto_price").
2. **Code Synthesis**: Generates clean Python code defining the tool and its standard function signature.
3. **AST Safety Audit**: Parses code using Python's `ast` module to block prohibited operations (e.g., unsafe syscalls, formatting hard drives).
4. **Sandbox Test Execution**: Executes unit tests on the generated code in an isolated sub-process.
5. **Live Hot-Reloading**: Uses `importlib` to dynamically import the module and register the new tool in `TOOL_REGISTRY` without restarting the server.
6. **Regenerative Self-Repair & Rollback**: If execution fails or throws runtime exceptions, POOL-VIS rewrites the code (self-repair) or rolls back to the previous stable state.

---

## 4. UI/UX Interface (Tactical Deadpool HUD)
- **Visual Style**: Crimson Red (`#dc2626`), Deep Dark Slate (`#0f172a`), Gunmetal accents, Comic Badge styling.
- **Header**: Deadpool Icon Badge + Dynamic Status Indicator ("Mutator Engine: Online", "Regen Factor: 100%").
- **Voice Integration**: Web Speech API for voice recognition and synthesized audio speech with pitch/rate tuning to mimic Deadpool's energetic cadence.
- **Mutator Code Panel**: Real-time code execution visualization log showing dynamic code patching, AST checks, and dynamic imports as they happen.

---

## 5. Security Guardrails & Safety
- **Tool Sandbox**: Dynamic tools are saved in `generated_tools/` directory with explicit boundary enforcement.
- **AST Prohibited Imports**: Blacklists dangerous operations unless explicitly confirmed.
- **Rollback Backups**: Original codebase versions are preserved before any self-mutation.
