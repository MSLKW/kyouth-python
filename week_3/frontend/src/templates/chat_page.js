
const chatBox = document.getElementById("chat-box");
const textInput = document.getElementById("text-input");
const sendButton = document.getElementById("send-button");
const fileUpload = document.getElementById("file-upload");

async function getResponseAsync(text) {
	const url = new URL(import.meta.url);
	url.pathname = "/chat";
	const data = {message: text};

	let message = "Error fetching response";
	try {
		const response = await fetch(url, {
			method: "POST",
			headers: {
				"Content-Type": "application/json"
			},
			body: JSON.stringify(data)
		});

		if (response.ok === false) {
			console.log("Response returned non-ok");
		}
		const responseJSON = await response.json();
		message = responseJSON.message;
	}
	catch (error) { }
	return (message);
}

function createTextElement(text, alignment) {
	const textElement = document.createElement("p");
	textElement.textContent = text;
	textElement.className = "m-2 p-2 border w-auto text-break rounded-top-4";
	if (alignment === "left") {
		textElement.classList.add("align-self-start", "justify-content-start", "text-start", "rounded-end-4", "bg-white");
	}
	else if (alignment === "right") {
		textElement.classList.add("align-self-end", "justify-content-end", "text-end", "rounded-start-4", "bg-primary", "text-light");
	}
	return (textElement);
}

function sendMessage(text) {
	chatBox.append(createTextElement(text, "right"));
}

function receiveMessage(text) {
	chatBox.append(createTextElement(text, "left"));
}

async function sendButtonFunc() {
	const text = textInput.value
	if (text === "") {
		return ;
	}
	textInput.value = "";
	sendMessage(text);
	const response = await getResponseAsync(text);
	receiveMessage(response);
}

sendButton.addEventListener('click', () => {
	sendButtonFunc();
});

textInput.addEventListener("keypress", () => {
	if (event.key === "Enter") {
		event.preventDefault();
		sendButton.click();
	}
});

fileUpload.addEventListener("change", (event) => {
	const file = event.target.files[0];

	if (file) {
		sendMessage(`Sent file: ${file.name}`);
	}
})