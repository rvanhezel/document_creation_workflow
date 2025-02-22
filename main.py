import os
import requests
import PyPDF2
import openai
from io import BytesIO
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account
from logger import Logger
import logging


# Constants
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', 'WRONG-KEY')
SERVICE_ACCOUNT_FILE = os.environ.get('SERVICE_ACCOUNT_FILE', 'WRONG-KEY')
GDRIVE_FOLDER_ID = os.environ.get('GDRIVE_FOLDER_ID', 'WRONG-KEY')

PROMPTS = [
    "Summarize the key points of this document.",
    "What are the main arguments or conclusions in this document?",
    "List any statistics or key figures mentioned.",
    "Identify any named entities such as people, places, or organizations.",
    "Extract any legal or financial information from the document.",
    "What are the potential biases in this document?",
    "Summarize any recommendations given in the document.",
    "What questions does this document leave unanswered?",
    "Extract any dates, deadlines, or timelines mentioned.",
    "Give a brief critique of this document's clarity and completeness."
]

# Authenticate Google Drive API
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=["https://www.googleapis.com/auth/drive"]
)
drive_service = build("drive", "v3", credentials=creds)

def list_pdf_files():
    """List all PDFs in the specified Google Drive folder."""
    query = f"'{GDRIVE_FOLDER_ID}' in parents and mimeType='application/pdf'"
    results = drive_service.files().list(q=query).execute()
    return results.get("files", [])

def download_pdf(file_id):
    """Download a PDF from Google Drive and extract text."""
    request = drive_service.files().get_media(fileId=file_id)
    pdf_buffer = BytesIO()
    downloader = MediaIoBaseDownload(pdf_buffer, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    return extract_text_from_pdf(pdf_buffer)

def extract_text_from_pdf(pdf_buffer):
    """Extract text from a PDF file buffer."""
    pdf_reader = PyPDF2.PdfReader(pdf_buffer)
    text = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
    return text

def ask_chatgpt(prompt, text):
    """Query OpenAI's GPT API with a given prompt and text."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI assistant that processes document data."},
            {"role": "user", "content": f"{prompt}\n\n{text[:4000]}"}  # Truncate text for token limits
        ],
        api_key=OPENAI_API_KEY
    )
    return response["choices"][0]["message"]["content"].strip()

def process_pdfs():
    """Download, process PDFs, and query ChatGPT with prompts."""
    pdf_files = list_pdf_files()
    results = {}
    
    for pdf in pdf_files:
        file_id, file_name = pdf["id"], pdf["name"]
        logging.info(f"Processing {file_name}...")
        pdf_text = download_pdf(file_id)
        
        results[file_name] = {}
        for prompt in PROMPTS:
            response = ask_chatgpt(prompt, pdf_text)
            results[file_name][prompt] = response
        
        with open(f"results_{file_name}.txt", "w", encoding="utf-8") as f:
            for prompt, answer in results[file_name].items():
                f.write(f"Prompt: {prompt}\nResponse: {answer}\n\n")
        
    logging.info("Processing complete. Results saved.")

if __name__ == "__main__":
    Logger()
    process_pdfs()
