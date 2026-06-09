from pathlib import Path
import pydantic
from bs4 import BeautifulSoup

class JobListing(pydantic.BaseModel):
	source_id: str # <meta property="og:url" content="https://<WEBSITE_URL>/job/91360026"> grab "91360026" as source_id 
	job_title: str # <h1 data-automation="job-detail-title">
	company: str # <span data-automation="advertiser-name">
	description: str # <div data-automation="jobAdDetails">

def html_to_json(html_file: Path, json_file: Path):
	try:
		with open(html_file, 'r', encoding='utf-8') as f:
			soup = BeautifulSoup(f, "html.parser")
	except FileNotFoundError:
		return (False, f"{html_file} was not found")
	except PermissionError:
		return (False, f"No permission to access {html_file}")
	

	source_id_element = soup.find("meta", attrs={"property": "og:url"})["content"]
	job_title_element = soup.find("h1", attrs={"data-automation": "job-detail-title"})
	company_element = soup.find("span", attrs={"data-automation": "advertiser-name"})
	description_element = soup.find("div", attrs={"data-automation": "jobAdDetails"})

	if (not source_id_element):
		return (False, f"Missing source_id in {html_file.name}")
	elif (not job_title_element):
		return (False, f"Missing job_title in {html_file.name}")
	elif (not company_element):
		return (False, f"Missing company in {html_file.name}")
	elif (not description_element):
		return (False, f"Missing description in {html_file.name}")
	
	joblisting = JobListing(
		source_id=source_id_element.rstrip('/').rsplit('/', -1)[-1],
		job_title=job_title_element.get_text(separator=" ", strip=True),
		company=company_element.get_text(separator=" ", strip=True),
		description=description_element.get_text(separator=" ", strip=True)
	)

	with open(json_file, 'w', encoding="utf-8") as f:
		f.write(joblisting.model_dump_json(indent=4))
	return (True, "Success")

def process_all_html(input_dir: Path, output_dir: Path):
	if (input_dir.exists() == False):
		print(f"Error: {input_dir} does not exist")
		return
	if (output_dir.exists() == False):
		print(f"⚠️  Warning: {output_dir} does not exist, creating the directory")
		output_dir.mkdir(parents=True, exist_ok=True)
	
	processed_total = 0
	skipped_total = 0

	for item in input_dir.glob("*.html"):
		status, msg = html_to_json(item, output_dir / f"{item.stem}.json")
		if (status == True):
			print(f"✅ Processed: {item.name}")
			processed_total += 1
		elif (status == False):
			print(f"⚠️  {msg}")
			skipped_total += 1
	
	print(f"📊 Silver Summary:\nTotal: {processed_total + skipped_total} | Processed: {processed_total} | Skipped: {skipped_total}")