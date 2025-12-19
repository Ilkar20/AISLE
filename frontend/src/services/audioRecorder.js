const AUDIO_API_URL = "http://127.0.0.1:5000/audio/upload";

/**
 * Send recorded audio blob to backend for transcription + AI response.
 * @param {Blob} audioBlob - The recorded audio file (e.g., WAV).
 * @param {string} sessionId - Session identifier for conversation context.
 * @returns {Promise<{ userText: string, aiResponse: object }>}
 */
export async function sendAudioToBackend(audioBlob, sessionId = "session2") {
  try {
    const formData = new FormData();
    formData.append("file", audioBlob, "recording.wav");
    formData.append("session_id", sessionId);

    const response = await fetch(AUDIO_API_URL, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const text = await response.text().catch(() => "");
      const errMsg = text ? `${response.status} ${text}` : `Server error: ${response.status}`;
      throw new Error(errMsg);
    }

    const data = await response.json();

    // Backend returns: { userText: "...", aiResponse: {...} }
    const result = {
      userText: data.userText || "",
      aiResponse: data.aiResponse || {},
      raw: data,
    };

    return result;
  } catch (error) {
    console.error("Error sending audio to backend:", error);
    return {
      userText: "",
      aiResponse: { english: `⚠️ Unable to reach AI server. (${error.message || "network error"})`, finnish: "", state: "" },
      raw: null,
    };
  }
}
