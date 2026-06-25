# Project Overview

The project the goal of the project is to implement FastAPI utilizing uvicorn for local server hosting. Using docker for containerization. As well as using frontend basics like HTML, CSS, Javascript and Bootstrap. Lastly, we have to integrate our week 2 AI modules into week 3.

## Setup instructions

Make sure that you're in the project directory week_3.

Prerequisites include installing uv and docker

Manual setup is not supported

Configure .env variables as per .env.example

`API_KEY=` The API key that you get from google ai studio

`GEMINI_MODEL=` The supported gemini models (gemini-2.5-flash, gemini-2.5-flash-lite, gemini-3-flash-preview)

`BACKEND_URL=` The url for the backend (http://backend:8001)

## Usage

Run the command `docker compose up --build`

Access the frontend by running `http://localhost:8000` on your preferred browser

There will be a chatbox that pops up, Type a message in the text chat, press Enter or the Send button to send the prompt, and press the upload button to the left to upload a PDF or txt file. Other file types are not supported.

## API / Function Reference

`http://localhost:8000` to access the website
`http://localhost:8000/*.js` endpoints for the html to grab the necessary js files

`async def chat(payload: dict[str, str]):` Is the POST /chat endpoint for the backend. It expects JSON formatted like: {
	message: "example message",
	file_contents: "pdf or txt file contents"
}

`async function getResponseAsync(text)` Manages the chat communication when user sends their prompt

`function createTextElement(text, alignment)` Manage the rendering of the text bubbles

The frontend javascript file will attempt a http request to the frontend fastapi service, then the frontend fastapi service will relay it to the backend fastapi service. Then the backend fastapi service will relay it back to the frontend api and back to the javascript.

This allows the backend to not need to expose anything as well as avoiding the CORS security restrictions.

## Data / Assumptions

{
	message: "message", 
	file_contents: "file_contents"
}

This is the format used for the front end to send to the backend.

{
	message: "message", 
}

This is the json format used for the back end to send a message to the front end.

The file_contents is assumed to be regular plaintext string of a pdf or txt file.

There are no arbitrary constraints on the message or file_contents.

Data flow is already explained above: 
The frontend javascript file will attempt a http request to the frontend fastapi service, then the frontend fastapi service will relay it to the backend fastapi service. Then the backend fastapi service will relay it back to the frontend api and back to the javascript.

## Testing

Minimal testing done to make sure everything works

## Limitations

It does not handle any corrupted/malicious client well. The website will not handle any file uploads that is not PDF or TXT file. AI model is rate limited. Backend server may crash sometimes for unknown reasons. Chat history is not saved.

## Architecture Reflection

Containerizing the backend and frontend separately allows both containers allows the frontend to specifically handle requests while the backend handles AI api and dealing with the database.

I chose ease of deployment of docker compose because it allowed me to test and deploy faster rather than fancy chat interface or advanced features which were not required

I could definitely make the application more robust with further testing and adding more constraints.