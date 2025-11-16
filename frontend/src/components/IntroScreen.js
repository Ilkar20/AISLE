// IntroScreen.js

export function createIntroScreen(onStart) {
  // Create main container
  const container = document.createElement("div");
  container.className = "intro-container";

  // Header
  const header = document.createElement("header");
  header.className = "intro-header";

  const title = document.createElement("h1");
  title.className = "intro-title";
  title.textContent = "AISLE";

  const subtitle = document.createElement("h2");
  subtitle.className = "intro-subtitle";
  subtitle.textContent = "AI Supported Learning Environment";

  header.appendChild(title);
  header.appendChild(subtitle);

  // Description
  const desc = document.createElement("section");
  desc.className = "intro-description";

  desc.innerHTML = `
    <p><strong>AISLE</strong> is an AI-powered language learning companion designed to help you learn Finnish or Swedish through real-life work situations. It’s made especially for newcomers who want to feel confident communicating at work.</p>
    <p>You’ll go through small, interactive micro-lessons that combine short videos, vocabulary practice, and conversational AI feedback.</p>
    <p>Whether you’re starting from the basics or improving your fluency, AISLE will guide you step by step in your chosen language.</p>
  `;

  // Start Button
  const startButton = document.createElement("button");
  startButton.className = "intro-start-btn";
  startButton.textContent = "Start Learning";
  startButton.addEventListener("click", () => {
    if (typeof onStart === "function") {
      onStart();
    }
  });

  // Footer
  const footer = document.createElement("footer");
  footer.className = "intro-footer";
  footer.innerHTML = `
    <p>Developed by AISLE Team – Yilikaer Yihamujiang</p>
    <p>Supported by AI-driven education research initiative</p>
  `;

  // Append all to container
  container.appendChild(header);
  container.appendChild(desc);
  container.appendChild(startButton);
  container.appendChild(footer);

  return container;
}
