import ollama
from ollama import ResponseError
from google import genai
import sys
import os
import dotenv

def prompt_model(model: str, prompt: str) -> str :
	if (model == "gemini-2.5-flash" or model == "gemini-2.5-flash-lite" or model == "gemini-3-flash-preview"):
		try:
			dotenv.load_dotenv()
			client = genai.Client(api_key=os.environ.get("API_KEY"))
			response = client.models.generate_content(
				model=model,
				contents=prompt
			)
		except ValueError as e:
			return (e)
		except Exception as e:
			return (e)
		return (response.text)

	try:
		ollama_response = ollama.generate(
			model=model,
			prompt=prompt
		)
		return (ollama_response['response'])
	except ResponseError as e:
		return (e)

def main():
	if (len(sys.argv) != 3):
		print("Usage: uv run prompt_mode.py <model> <prompt>")
		sys.exit(1)

	print(f"\n--- RESPONSE ---\n\n{prompt_model(sys.argv[1], sys.argv[2])}")
    
        
if __name__ == "__main__":
	main()
