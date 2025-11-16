import { Header } from "./Header";
import { InputBox } from "./InputBox";
import { MessageBubble } from "./MessageBubble";

export function ChatWindow() {
  const container = document.createElement("div");
  container.className = "chat-container centered"; // start centered

  const header = Header();

  const chatBox = document.createElement("div");
  chatBox.className = "chat-box hidden"; // hidden initially
  chatBox.id = "chat-box";

  const inputArea = document.createElement("div");
  inputArea.className = "input-area centered-input"; // centered initially

  const inputBox = InputBox((message) => {
    // Hide header and move input to bottom
    header.style.display = "none";
    chatBox.classList.remove("hidden");
    container.classList.remove("centered");
    inputArea.classList.remove("centered-input");
    inputArea.classList.add("bottom-input");

    const userMsg = MessageBubble(message, "user");
    chatBox.appendChild(userMsg);
    chatBox.scrollTop = chatBox.scrollHeight;
  });

  inputArea.appendChild(inputBox);

  container.appendChild(header);
  container.appendChild(chatBox);
  container.appendChild(inputArea);

  return container;
}
