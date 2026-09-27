const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const micBtn = document.getElementById("mic-btn");
const voiceToggleBtn = document.getElementById("voice-toggle-btn");
const clearChatBtn = document.getElementById("clear-chat-btn");
const patchLogBanner = document.getElementById("patch-log-banner");
const patchLogText = document.getElementById("patch-log-text");
const quickBtns = document.querySelectorAll(".quick-btn");

let voiceEnabled = false;
let isRecording = false;
let recognition = null;

// Speech Recognition setup (Web Speech API)
if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  recognition = new SpeechRecognition();
  recognition.lang = 'es-ES';
  recognition.continuous = false;
  recognition.interimResults = false;

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    userInput.value = transcript;
    sendMessage();
  };

  recognition.onend = () => {
    isRecording = false;
    micBtn.classList.remove('recording');
  };

  recognition.onerror = (err) => {
    console.error("Error de voz:", err);
    isRecording = false;
    micBtn.classList.remove('recording');
  };
}

function speakText(text) {
  if (!voiceEnabled || !('speechSynthesis' in window)) return;
  window.speechSynthesis.cancel(); // Stop prior speech
  const cleanText = text.replace(/[*_#`~⚔️🧬💥💬🌯]/g, '');
  const utterance = new SpeechSynthesisUtterance(cleanText);
  utterance.lang = 'es-ES';
  utterance.pitch = 1.1; // Slightly energetic pitch for Deadpool
  utterance.rate = 1.05;
  window.speechSynthesis.speak(utterance);
}

function addMessage(text, type, meta = "") {
  const div = document.createElement("div");
  div.className = `message ${type}`;

  const contentSpan = document.createElement("span");
  contentSpan.innerHTML = formatMarkdown(text);
  div.appendChild(contentSpan);

  if (meta) {
    const metaSpan = document.createElement("small");
    metaSpan.className = "message-meta";
    metaSpan.textContent = meta;
    div.appendChild(metaSpan);
  }

  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;

  if (type === "poolvis") {
    speakText(text);
  }
}

function formatMarkdown(str) {
  return str
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/`(.*?)`/g, '<code style="background:#111827;padding:2px 5px;border-radius:4px;color:#f87171;">$1</code>')
    .replace(/\n/g, '<br>');
}

function showPatchingBanner(toolName) {
  patchLogText.textContent = `🧬 [FACTOR REGENERATIVO] Reescritura de código en proceso para: '${toolName}'...`;
  patchLogBanner.classList.remove("hidden");
  setTimeout(() => {
    patchLogBanner.classList.add("hidden");
  }, 3500);
}

// Client-side POOL-VIS Simulator for instant standalone web operation & webhook fallback
async function processPoolvisCommand(text) {
  const lower = text.toLowerCase().trim();

  // Show dynamic code patching animation when dynamic tool/mutation is requested
  if (lower.includes("automejora") || lower.includes("fibonacci") || lower.includes("no puedes") || lower.includes("codigo") || lower.includes("crea una funcion")) {
    showPatchingBanner(lower.includes("fibonacci") ? "calculadora_fibonacci" : "dynamic_code_patch");
  }

  // Simulated backend latency for realism
  await new Promise(r => setTimeout(r, 600));

  if (lower.includes("estado") || lower.includes("sistema") || lower.includes("hardware")) {
    return {
      reply: "⚔️ **[CONTROL DE DISPOSITIVO ACTIVADO]**\n" +
             "¡Chequeando las entrañas cibernéticas de tu máquina, Socio!\n\n" +
             "**SO**: macOS / Linux x86_64\n" +
             "**Python**: 3.11.2 (Núcleo POOL-VIS actvo)\n" +
             "**CPU**: 8 Núcleos corriendo a tope\n" +
             "**Batería**: 100% (Poder ilimitado de Deadpool)\n" +
             "**Disco Libre**: 142.5 GB disponibles\n\n" +
             "*(Por cierto, tu procesador está más caliente que taco de jalapeño, pero todo estable).* \n\n_¡Chimichanga time! 🌯_",
      meta: "Acción: Device Control"
    };
  }

  if (lower.includes("procesos") || lower.includes("ps") || lower.includes("tasklist")) {
    return {
      reply: "⚔️ **[CONTROL DE DISPOSITIVO ACTIVADO]**\n" +
             "Procesos en ejecución detectados en el sistema:\n" +
             "`1. poolvis_core.py (PID 1042)`\n" +
             "`2. node_server (PID 2088)`\n" +
             "`3. chrome_browser (PID 3401)`\n" +
             "`4. spotify_audio (PID 4110)`\n\n" +
             "*(Si quieres cierro el navegador para que no vean tus búsquedas raras, guiño guiño).* \n\n_¡Misión cumplida, socio! 🌯_",
      meta: "Acción: List OS Processes"
    };
  }

  if (lower.includes("volumen") || lower.includes("audio")) {
    return {
      reply: "⚔️ **[CONTROL DE DISPOSITIVO ACTIVADO]**\n" +
             "¡Volumen ajustado al 85% con estilo sangriento!\n\n" +
             "*(Asegúrate de tener buenos audífonos para escuchar mi hermosa voz sintética).* \n\n_¡Boom! Así se hace en POOL-VIS. 🌯_",
      meta: "Acción: Adjust Audio Volume"
    };
  }

  if (lower.includes("fibonacci") || lower.includes("automejora") || lower.includes("no puedes")) {
    return {
      reply: "🧬 **[MUTACIÓN DE CÓDIGO - FACTOR REGENERATIVO]**\n" +
             "¡No tenía esa función en mi registro, así que reescribí mi propio código Python en caliente!\n\n" +
             "Sinteticé la herramienta `tool_calculadora_fibonacci.py` en `./generated_tools/`.\n" +
             "**Resultado de ejecución**: `Secuencia Fibonacci (10 términos): [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]`\n\n" +
             "*(¡Toma esa, JARVIS! A ti te toma 3 películas actualizarte y yo lo hice en 0.4 segundos).* \n\n_¡Servicio completo con el sello de Wade Wilson! ⚔️_",
      meta: "Acción: Hot Code Patching & Self-Improvement"
    };
  }

  return {
    reply: `💬 ¡Entendido Capitán! Recibí tu comando: **"${text}"**.\nMis sistemas de control de dispositivo y factor regenerativo de código están listos para lo que me pidas.\n\n*(¿Quieres que ajustemos el volumen, veamos los procesos o creemos un script nuevo? Tú mandas, jefe).* \n\n_¡Chimichanga time! 🌯_`,
    meta: "Acción: Conversación POOL-VIS"
  };
}

async function sendMessage() {
  const text = userInput.value.trim();
  if (!text) return;

  addMessage(text, "user");
  userInput.value = "";
  sendBtn.disabled = true;

  try {
    const responseData = await processPoolvisCommand(text);
    addMessage(responseData.reply, "poolvis", responseData.meta);
  } catch (err) {
    addMessage("💥 **[OUCH]** Hubo una interferencia en el factor curativo de POOL-VIS.", "poolvis");
    console.error(err);
  } finally {
    sendBtn.disabled = false;
    userInput.focus();
  }
}

// Event Listeners
sendBtn.addEventListener("click", sendMessage);

userInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    sendMessage();
  }
});

quickBtns.forEach(btn => {
  btn.addEventListener("click", () => {
    const cmd = btn.getAttribute("data-cmd");
    if (cmd) {
      userInput.value = cmd;
      sendMessage();
    }
  });
});

micBtn.addEventListener("click", () => {
  if (!recognition) {
    alert("El reconocimiento de voz no está soportado en este navegador.");
    return;
  }
  if (!isRecording) {
    recognition.start();
    isRecording = true;
    micBtn.classList.add('recording');
  } else {
    recognition.stop();
    isRecording = false;
    micBtn.classList.remove('recording');
  }
});

voiceToggleBtn.addEventListener("click", () => {
  voiceEnabled = !voiceEnabled;
  voiceToggleBtn.classList.toggle("active", voiceEnabled);
  const icon = voiceToggleBtn.querySelector("i");
  if (voiceEnabled) {
    icon.className = "fa-solid fa-volume-high";
    speakText("¡Sintetizador de voz POOL-VIS activado! Prepárate para escuchar la voz de la victoria.");
  } else {
    icon.className = "fa-solid fa-volume-xmark";
    window.speechSynthesis.cancel();
  }
});

clearChatBtn.addEventListener("click", () => {
  chatBox.innerHTML = "";
  addMessage("¡Chat limpiado, Capitán! Listo para nuevas chimichangas y comandos.", "poolvis");
});

// Initial Welcome Message
window.addEventListener("load", () => {
  addMessage(
    "¡Ey, Capitán! POOL-VIS v3.0 en línea.\n" +
    "Control de dispositivo total activado + Factor regenerativo de código en caliente en el aire.\n\n" +
    "¿Qué comandamos hoy o a qué función le hacemos un 'upgrade' instantáneo? 🌯⚔️",
    "poolvis",
    "Sistema POOL-VIS en línea"
  );
});
