export function Header() {
  const header = document.createElement("div");
  header.className = "chat-header";
  header.textContent = "What can I help with?";
  return header;
}
