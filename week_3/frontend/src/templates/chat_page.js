import * as pdfjsLib from './pdf.mjs';

pdfjsLib.GlobalWorkerOptions.workerSrc = './pdf.worker.mjs';

const chatBox = document.getElementById("chat-box");
const textInput = document.getElementById("text-input");
const sendButton = document.getElementById("send-button");
const fileUpload = document.getElementById("file-upload");

let gFile = undefined;

async function readPdfFile(event) {
    if (!gFile) return;

    try {
        const arrayBuffer = await gFile.arrayBuffer();

        const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
        let fullText = "";

        for (let i = 1; i <= pdf.numPages; i++) {
            const page = await pdf.getPage(i);
            const textContent = await page.getTextContent();
            const pageText = textContent.items.map(item => item.str).join(" ");
            fullText += `${pageText}`;
        }
		return (fullText);
    } catch (error) {
        console.error("Error processing PDF:", error);
        return ("");
    }
}

function readTextFile(file) {
  return new Promise((resolve, reject) => {
    if (!file) {
      reject(new Error("No file provided."));
      return;
    }

    const reader = new FileReader();

    reader.onload = (event) => {
      const content = event.target.result;
      resolve(content);
    };

    reader.onerror = (event) => {
      reject(event.target.error);
    };

    reader.readAsText(file);
  });
}

async function getResponseAsync(text) {
	const url = new URL(import.meta.url);
	url.pathname = "/chat";
	let fileText = "";
	if (gFile) {
		const ext = gFile.name.split('.').pop().toLowerCase();
		if (ext == "pdf")
			fileText = await readPdfFile(gFile);
		else if (ext == "txt")
			fileText = await readTextFile(gFile);
		else
			console.warn("File type not supported");
		console.log(fileText);
	}
	const data = {message: text, file_contents: fileText};

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
			return (message);
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
	gFile = event.target.files[0];

	if (gFile) {
		sendMessage(`Selected file: ${gFile.name}`);
	}
})