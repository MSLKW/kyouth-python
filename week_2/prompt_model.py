import ollama
from google import genai
import sys
import os
import dotenv


# Must use a try except block to catch error exceptions
def prompt_model(model: str, prompt: str) -> str:
    if (
        model == "gemini-2.5-flash"
        or model == "gemini-2.5-flash-lite"
        or model == "gemini-3-flash-preview"
    ):
        dotenv.load_dotenv()
        client = genai.Client(api_key=os.environ.get("API_KEY"))
        response = client.models.generate_content(model=model, contents=prompt)
        return response.text

    ollama_response = ollama.generate(model=model, prompt=prompt)
    return ollama_response["response"]


def main():
    if len(sys.argv) != 3:
        print("Usage: uv run prompt_mode.py <model> <prompt>")
        sys.exit(1)

    try:
        result = prompt_model(sys.argv[1], sys.argv[2])
        print(f"\n--- RESPONSE ---\n\n{result}")
    except Exception:
        print("Encountered an error when prompting the model")


if __name__ == "__main__":
    main()
