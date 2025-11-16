export function MessageBubble(text, type = "user") {
  const msg = document.createElement("div");
  msg.classList.add("message");

  if (type === "user") {
    msg.classList.add("user-message");
  } else if (type === "ai") {
    msg.classList.add("ai-message");
  } else if (type === "placeholder") {
    msg.classList.add("ai-message", "placeholder-message");
  }

  msg.textContent = text;
  return msg;
}
