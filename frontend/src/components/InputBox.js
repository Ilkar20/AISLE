export function InputBox(onSubmit) {
  const form = document.createElement("form");
  form.className = "input-box";
  form.id = "chat-form";

  const input = document.createElement("input");
  input.type = "text";
  input.id = "user-input";
  input.placeholder = "Type your message...";
  input.autocomplete = "off";

  const button = document.createElement("button");
  button.type = "submit";
  button.textContent = "Send";

  form.appendChild(input);
  form.appendChild(button);

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const text = input.value.trim();
    if (!text) return;

    onSubmit(text);
    input.value = "";
  });

  return form;
}
