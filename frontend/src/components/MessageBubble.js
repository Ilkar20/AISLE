export function MessageBubble(content, type = "user") {
  const msg = document.createElement("div");
  msg.classList.add("message");

  if (type === "user") {
    msg.classList.add("user-message");
  } else if (type === "ai") {
    msg.classList.add("ai-message");
  } else if (type === "placeholder") {
    msg.classList.add("ai-message", "placeholder-message");
  }

  // Support either a plain text string OR a structured object { english, finnish }
  if (typeof content === "string" || typeof content === "number") {
    msg.textContent = content;
  } else if (content && typeof content === "object") {
    // Render bilingual response with labeled sections
    const englishText = content.english || "";
    const finnishText = content.finnish || "";

    if (englishText) {
      const enLabel = document.createElement("div");
      enLabel.className = "lang-label en-label";
      enLabel.textContent = "English:";

      const enBody = document.createElement("div");
      enBody.className = "lang-body en-body";
      enBody.textContent = englishText;

      msg.appendChild(enLabel);
      msg.appendChild(enBody);
    }

    if (finnishText) {
      const fiLabel = document.createElement("div");
      fiLabel.className = "lang-label fi-label";
      fiLabel.textContent = "Suomi:";

      const fiBody = document.createElement("div");
      fiBody.className = "lang-body fi-body";
      fiBody.textContent = finnishText;

      // Add a small spacer if both languages are present
      if (englishText) {
        const spacer = document.createElement("div");
        spacer.className = "lang-spacer";
        msg.appendChild(spacer);
      }

      msg.appendChild(fiLabel);
      msg.appendChild(fiBody);
    }

    // If neither field present, try raw fallback
    if (!englishText && !finnishText && content.raw) {
      msg.textContent = JSON.stringify(content.raw);
    }
  }
  return msg;
}
