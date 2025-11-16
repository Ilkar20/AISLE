// services/chatService.js

const API_URL = "http://127.0.0.1:5000/api/chat";

export async function sendMessageToBackend(message) {
  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });

    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }

    const data = await response.json();
    return data.reply || "No response from AI.";
  } catch (error) {
    console.error("Error communicating with backend:", error);
    return "⚠️ Unable to reach AI server. Please try again later.";
  }
}
