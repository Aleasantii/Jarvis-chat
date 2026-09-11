const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");

const WEBHOOK_URL = "https://alesanti.app.n8n.cloud/webhook/jarvis-message";

function addMessage(text, type) {
  const div = document.createElement("div");
  div.className = `message ${type}`;
  div.textContent = text;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
  const text = userInput.value.trim();
  if (!text) return;

  addMessage(text, "user");
  userInput.value = "";
  sendBtn.disabled = true;

  try {
    const res = await fetch(WEBHOOK_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text }),
    });

    const data = await res.json();
    const reply = data.reply || "Sin respuesta.";
    addMessage(reply, "nexus");
  } catch (err) {
    addMessage("Error al conectar con NEXUS.", "nexus");
    console.error(err);
  } finally {
    sendBtn.disabled = false;
    userInput.focus();
  }
}

sendBtn.addEventListener("click", sendMessage);

userInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    sendMessage();
  }
});

// Mensaje inicial de NEXUS (opcional)
window.addEventListener("load", () => {
  addMessage("Sistema en línea. Soy NEXUS. ¿En qué puedo ayudarte, Jefe?", "nexus");
});
