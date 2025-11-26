// services/chatService.js

// Backend's chat route (matches backend/router.py which serves /chat)
const API_URL = "http://127.0.0.1:5000/chat";

export async function sendMessageToBackend(message) {
  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });

    if (!response.ok) {
      // Try to extract any helpful error text from the server for diagnostics
      const text = await response.text().catch(() => "");
      const errMsg = text ? `${response.status} ${text}` : `Server error: ${response.status}`;
      throw new Error(errMsg);
    }

    const data = await response.json();

    // Normalize server response into a consistent object shape
    // Backend normally returns { english, finnish, state }
    const result = {
      english: (data && data.english) || "",
      finnish: (data && data.finnish) || (data && data.reply) || "",
      state: (data && data.state) || "",
      raw: data,
    };

    return result;
  } catch (error) {
    // Provide a more informative message for debugging while keeping user-friendly text short
    console.error("Error communicating with backend:", error);
    return { english: `⚠️ Unable to reach AI server. (${error.message || 'network error'})`, finnish: "", state: "", raw: null };
  }
}
