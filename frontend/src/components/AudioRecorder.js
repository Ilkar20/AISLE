export function AudioRecorder(onRecord) {
    const recorderContainer = document.createElement("div");
    recorderContainer.className = "audio-recorder"; 
    recorderContainer.id = "audio-recorder";

    const recordButton = document.createElement("button");
    recordButton.type = "button"; // prevent form submit when inside the input form
    recordButton.id = "record-btn";
    recordButton.textContent = "Start Recording";
    recorderContainer.appendChild(recordButton);

    let mediaRecorder;
    let audioChunks = [];
    let isRecording = false;

    recordButton.addEventListener("click", async () => {
      if (!isRecording) {
        // Start recording
        if (!mediaRecorder) {
          const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
          mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.ondataavailable = (event) => {
                audioChunks.push(event.data);
            };
            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                audioChunks = [];
                onRecord(audioBlob);
            };
        }
        mediaRecorder.start();
        isRecording = true;
        recordButton.textContent = "Stop Recording";
      } else {
        // Stop recording
        mediaRecorder.stop();
        isRecording = false;
        recordButton.textContent = "Start Recording";
      }
    });

    return recorderContainer;
}