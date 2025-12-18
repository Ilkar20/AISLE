import { createIntroScreen } from "./components/IntroScreen";
import { ChatWindow } from "./components/ChatWindow";
import { render } from "./utils/dom";


function showChat() {
    render(ChatWindow());
}

function showIntro() {
    const intro = createIntroScreen(showChat);
    render(intro)
}

showIntro();
