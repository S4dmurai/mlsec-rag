async function askQuestion() {

    const input = document.getElementById("question");
    const button = document.getElementById("submit-btn");
    const chat = document.getElementById("chat");
    const question = input.value.trim();

    if (!question) {
        return;
    }

    input.disabled = true;
    button.disabled = true;
    button.innerText = "Denkt nach ...";

    chat.innerHTML +=
    `<div class="question">
        ${question}
    </div >`;

    input.value = "";

    try {
        const response = await fetch(
            `/query?question=${encodeURIComponent(question)}`,
            {
                method: "POST"
            }
        );

        if (!response.ok) {
            throw new Error(`Server-Fehler: ${response.status}`);
        }

        const data = await response.json();

        chat.innerHTML += `<div class="answer">${data.answer}</div>`;
    } catch (error) {
        chat.innerHTML += `<div class="answer fehler">Fehler: ${error.message}</div>`;
    } finally {
        input.disabled = false;
        button.disabled = false;
        button.innerText = "Senden";
        input.focus();
    }
}