from pathlib import Path
# from email import message_from_file
import email
import quopri
from email.message import EmailMessage

def extract_html_from_mhtml(mhtml_file: Path, html_file: Path):
	try:
		with open(mhtml_file, 'rb') as file:
			msg = email.message_from_binary_file(file)
	except FileNotFoundError:
		return (False, f"{mhtml_file} was not found")
	except PermissionError:
		return (False, f"No permission to access {mhtml_file}")

	for part in msg.walk():
		html_content = ""
		if (part.get_content_type() == "text/html"):
			html_content = quopri.decodestring(part.get_payload())
			if (not html_content):
				return (False, f"No HTML content found for text/html multipart in {mhtml_file}")
			with open(html_file, 'wb') as out:
				out.write(html_content)
			return (True, "Success")
	return (False, f"No HTML Multipart found in {mhtml_file}")

def ingest_all_mhtml(input_dir: Path, output_dir: Path):
	if (input_dir.exists() == False): # or no contents found
		print(f"Error: {input_dir} does not exist")
		return
	
	if (output_dir.exists() == False):
		print(f"⚠️  Warning: {output_dir} does not exist, creating the directory")
		output_dir.mkdir(parents=True, exist_ok=True)

	extracted_total = 0
	failed_total = 0

	for item in input_dir.glob("*.mhtml"):
		status, msg = extract_html_from_mhtml(item, output_dir / f"{item.stem}.html")
		if (status == True):
			print(f"✅ Extracted: {item.name}")
			extracted_total += 1
		elif (status == False):
			print(f"⚠️  {msg}")
			failed_total += 1
	
	print(f"📊 Bronze Summary:\nTotal: {extracted_total + failed_total} | Extracted: {extracted_total} | Failed: {failed_total}")
	