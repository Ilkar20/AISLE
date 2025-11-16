export function render(component, targetSelector = "#app") {
  const target = document.querySelector(targetSelector);
  target.innerHTML = "";
  target.appendChild(component);
}
