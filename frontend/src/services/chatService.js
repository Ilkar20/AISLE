const API_URL = "http://127.0.0.1:5000/api/chat";
const HEALTH_URL = "http://127.0.0.1:5000/api/health";

async function checkBackend() {
  try {
    const r = await fetch(HEALTH_URL, { method: "GET" });
    if (r.ok) return { ok: true };
    let body = "";
    try { body = await r.text(); } catch (e) { body = ""; }
    return { ok: false, status: r.status, body };
  } catch (e) {
    return { ok: false, error: e.message };
  }
}

export async function sendMessageToBackend(message) {
  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });

    if (!response.ok) {
      const text = await response.text().catch(() => "");
      const errMsg = text ? `${response.status} ${text}` : `Server error: ${response.status}`;
      throw new Error(errMsg);
    }

    const data = await response.json();
    
    const result = {
      english: (data && data.english) || "",
      finnish: (data && data.finnish) || (data && data.reply) || "",
      state: (data && data.state) || "",
      raw: data,
    };

    return result;
  } catch (error) {
    console.error("Error communicating with backend:", error);

    // Attempt to check backend health to provide a clearer message
    const health = await checkBackend().catch(() => ({ ok: false, error: "health check failed" }));

    let messageText = "⚠️ Unable to reach AI server. (network error)";

    if (health && health.ok) {
      messageText = `⚠️ Backend reachable but request failed. (${error.message || 'request error'})`;
    } else if (health && health.status) {
      messageText = `⚠️ Backend returned ${health.status}. ${health.body || ''}`;
    } else if (health && health.error) {
      messageText = `⚠️ Cannot reach backend at http://127.0.0.1:5000 (${health.error})`;
    }

    return { english: messageText, finnish: "", state: "", raw: null };
  }
}
