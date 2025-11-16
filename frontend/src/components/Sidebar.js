export function Sidebar() {
  return `
    <div class="sidebar" id= "sidebar">
      <button class="sidebar-toggle" id="toggle-sidebar">☰</button>
      
      <div class="sidebar-top">
        <button id="new-chat-btn">New Chat</button>
        <button id="search-chat-btn">Search Chats</button>
      </div>

      <div class="chat-list" id="chat-list">
        <!-- Chat history items will be loaded here -->
      </div>
    </div>
  `;
}

// Initialize sidebar logic
window.addEventListener("DOMContentLoaded", () => {
  const sidebar = document.getElementById("sidebar");
  const toggleBtn = document.getElementById("toggle-sidebar");
  const chatList = document.getElementById("chat-list");

  // Dummy chat history
  const mockChats = [
    "Learning Finnish greetings",
    "Finnish grammar tips",
    "Travel conversation practice",
  ];

  // Render chats
  chatList.innerHTML = mockChats
    .map((title, i) => `<button class="chat-item" data-id="${i}">${title}</button>`)
    .join("");
  
  // Sidebar collapse/expand toggle
  toggleBtn.addEventListener("click", () => {
    sidebar.classList.toggle("collapsed");
    toggleBtn.textContent = sidebar.classList.contains("collapsed") ? "▶" : "☰";
  });

  // Handle new chat button
  document.getElementById("new-chat-btn").addEventListener("click", () => {
    alert("New chat started (functionality coming soon)");
  });

  // Handle search chats
  document.getElementById("search-chat-btn").addEventListener("click", () => {
    alert("Search chats clicked (search UI coming soon)");
  });

  // Handle chat selection
  chatList.addEventListener("click", (e) => {
    if (e.target.classList.contains("chat-item")) {
      alert(`Opening chat: ${e.target.textContent}`);
    }
  });
});
