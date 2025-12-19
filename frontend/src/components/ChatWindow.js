import { InputBox } from "./InputBox";
import { MessageBubble } from "./MessageBubble";
import { ThinkingBubble } from "./ThinkingBubble";
import { sendMessageToBackend } from "../services/chatService.js";

export function ChatWindow() {
  const container = document.createElement("div");
  container.className = "chat-container";

  const chatBox = document.createElement("div");
  chatBox.className = "chat-box";
  chatBox.id = "chat-box";

  const inputArea = document.createElement("div");
  inputArea.className = "input-area";

  // helper to scroll the whole page to bottom
  function scrollToBottom() {
    window.scrollTo({
      top: document.body.scrollHeight,
      behavior: "smooth"
    });
  }

  const inputBox = InputBox(
    async (message) => {
      // Append user's message
      const userMsg = MessageBubble(message, "user");
      chatBox.appendChild(userMsg);
      scrollToBottom();

      const thinking = ThinkingBubble();
      chatBox.appendChild(thinking);
      scrollToBottom();

      try {
        // Send message to backend and get response
        const aiReply = await sendMessageToBackend(message);

        const bubble = document.getElementById("thinking-bubble");
        if (bubble) bubble.remove();

        // Append AI response message
        const aiMsg = MessageBubble(aiReply, "ai");
        chatBox.appendChild(aiMsg);
        scrollToBottom();

      } catch (error) {
        // Handle network/backend errors gracefully
        const errorMsg = MessageBubble(
          "⚠️ Unable to reach AI service. Please try again later.",
          "ai"
        );
        chatBox.appendChild(errorMsg);
        scrollToBottom();
        console.error("Chat error:", error);
      }
    },
    async (audioBlob) => {
      // Upload recorded audio to backend and handle transcription + AI reply
      const formData = new FormData();
      formData.append("file", audioBlob, "recording.wav");
      // session_id currently not tracked on frontend; send empty for now
      formData.append("session_id", "");

      try {
        const resp = await fetch("http://127.0.0.1:5000/api/audio/upload", {
          method: "POST",
          body: formData,
        });

        if (!resp.ok) {
          // Try to parse JSON error message, otherwise fallback to text
          let text = "";
          try {
            const err = await resp.json();
            text = err && err.error ? err.error : JSON.stringify(err);
          } catch (e) {
            text = await resp.text().catch(() => "");
          }
          throw new Error(text || `Server error: ${resp.status}`);
        }

        const data = await resp.json();
        const userText = (data && data.userText) || "";
        const aiReply = (data && data.aiResponse) || "";

        if (userText) {
          const userMsg = MessageBubble(userText, "user");
          chatBox.appendChild(userMsg);
          scrollToBottom();
        }

        const thinking = ThinkingBubble();
        chatBox.appendChild(thinking);
        scrollToBottom();

        const bubble = document.getElementById("thinking-bubble");
        if (bubble) bubble.remove();

        const aiMsg = MessageBubble(aiReply, "ai");
        chatBox.appendChild(aiMsg);
        scrollToBottom();

      } catch (error) {
        console.error("Audio upload error:", error);
        const text = (error && error.message) ? error.message : "⚠️ Unable to process audio. Please try again later.";
        const errorMsg = MessageBubble(text, "ai");
        chatBox.appendChild(errorMsg);
        scrollToBottom();
      }
    }
  );

  inputArea.appendChild(inputBox);

  container.appendChild(chatBox);
  container.appendChild(inputArea);

  // Send an initial request automatically when the chat window is shown
  (async function sendInitialRequest() {
    const thinking = ThinkingBubble();
    chatBox.appendChild(thinking);
    scrollToBottom();

    try {
      // Send an empty message to trigger the assistant's initial reply
      const aiReply = await sendMessageToBackend("");

      const bubble = document.getElementById("thinking-bubble");
      if (bubble) bubble.remove();

      const aiMsg = MessageBubble(aiReply, "ai");
      chatBox.appendChild(aiMsg);
      scrollToBottom();
    } catch (error) {
      const errorMsg = MessageBubble(
        "⚠️ Unable to reach AI service. Please try again later.",
        "ai"
      );
      chatBox.appendChild(errorMsg);
      scrollToBottom();
      console.error("Chat initial request error:", error);
    }
  })();

  return container;
}
