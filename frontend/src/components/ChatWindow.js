import { InputBox } from "./InputBox";
import { MessageBubble } from "./MessageBubble";
import { ThinkingBubble} from "./ThinkingBubble"
import { sendMessageToBackend } from "../services/chatService.js";

export function ChatWindow() {
  const container = document.createElement("div");
  container.className = "chat-container";

  const chatBox = document.createElement("div");
  chatBox.className = "chat-box";
  chatBox.id = "chat-box";

  const inputArea = document.createElement("div");
  inputArea.className = "input-area";

  const inputBox = InputBox(async (message) => {

    // Append user's message
    const userMsg = MessageBubble(message, "user");
    chatBox.appendChild(userMsg);
    chatBox.scrollTop = chatBox.scrollHeight;

    const thinking = ThinkingBubble();
    chatBox.appendChild(thinking);
    chatBox.scrollTop = chatBox.scrollHeight;
        
    try {
      // Send message to backend and get response
      const aiReply = await sendMessageToBackend(message);

      const bubble = document.getElementById("thinking-bubble");
      if (bubble) bubble.remove();

      // Append AI response message
      const aiMsg = MessageBubble(aiReply, "ai");
      chatBox.appendChild(aiMsg);
      chatBox.scrollTop = chatBox.scrollHeight;

    } catch (error) {
      // Handle network/backend errors gracefully
      const errorMsg = MessageBubble(
        "⚠️ Unable to reach AI service. Please try again later.",
        "ai"
      );
      chatBox.appendChild(errorMsg);
      console.error("Chat error:", error);
    }
  });

  inputArea.appendChild(inputBox);

  container.appendChild(chatBox);
  container.appendChild(inputArea);

  return container;
}
