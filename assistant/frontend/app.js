const chatForm = document.querySelector("#chat-form");
const messageInput = document.querySelector("#message-input");
const messages = document.querySelector("#messages");
const emptyState = document.querySelector("#empty-state");

function addMessage(role, text) {
  const message = document.createElement("article");
  const bubble = document.createElement("p");

  message.className = `message message--${role}`;
  bubble.className = "message-bubble";
  bubble.textContent = text;

  message.append(bubble);
  messages.append(message);
  message.scrollIntoView({ behavior: "smooth", block: "end" });
}

chatForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const userMessage = messageInput.value.trim();

  if (!userMessage) {
    return;
  }

  emptyState?.remove();
  addMessage("user", userMessage);

  chatForm.reset();
  messageInput.disabled = true;

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: userMessage }),
    });

    if (!response.ok) {
      throw new Error(`Request failed with status ${response.status}`);
    }

    const data = await response.json();
    addMessage("assistant", data.reply);
  } catch (error) {
    console.error(error);
    addMessage("assistant", "Something went wrong. Please try again.");
  } finally {
    messageInput.disabled = false;
    messageInput.focus();
  }
});

messageInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    chatForm.requestSubmit();
  }
});
