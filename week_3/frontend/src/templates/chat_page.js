
const chatBox = document.getElementById("chat-box");
const textInput = document.getElementById("text-input");
const sendButton = document.getElementById("send-button");

function getResponse(text) {
	return ("Response Text");
}

function createTextElement(text, alignment) {
	const textElement = document.createElement("p");
	textElement.textContent = text;
	textElement.className = "text-end m-2 p-2 border w-auto text-break rounded-3";
	if (alignment === "left") {
		textElement.classList.add("align-self-start", "justify-content-start");
	}
	else if (alignment === "right") {
		textElement.classList.add("align-self-end", "justify-content-end");
	}
	return (textElement);
}

sendButton.addEventListener('click', () => {
	const text = textInput.value
	chatBox.append(createTextElement(text, "right"));
	const responseText = getResponse(text);
	chatBox.append(createTextElement(responseText, "left"));
	textInput.value = "";
});
