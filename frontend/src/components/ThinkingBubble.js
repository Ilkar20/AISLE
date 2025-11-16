import { MessageBubble } from "./MessageBubble";

export function ThinkingBubble() {
  const bubble = MessageBubble("", "ai"); 
  bubble.classList.add("thinking-bubble"); 
  bubble.id = "thinking-bubble";
  
  // Add the text
  const text = document.createElement("span");
  text.textContent = "Thinking";
  bubble.appendChild(text);

  // Add animated dots
  const dots = document.createElement("span");
  dots.className = "dots"
  dots.innerHTML = "<span>.</span><span>.</span><span>.</span>";
  bubble.appendChild(dots);
  
  return bubble;
}
