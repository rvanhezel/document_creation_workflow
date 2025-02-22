
# Document Creation Workflow

## Overview

Python application using Open AI's API to automate a document creation workflow.

![Python Version](https://img.shields.io/badge/Python-3.12%2B-green)
<!-- ![License](https://img.shields.io/badge/License-MIT-yellow) -->

## 📦 Prerequisites

- Python 3.12+
- pip (Python Package Manager)
- Virtual Environment (recommended)

## 🔧 Installation

1.Clone the repository in a desired folder (or alternatively download from the same URL):

```bash
git clone https://github.com/rvanhezel/document_creation_workflow.git
cd document_creation_workflow
```

2.Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3.Install dependencies:

```bash
pip install -r requirements.txt
```

4.Set up environment variables for API keys:

```bash
# Create a .env file in the project root directory with:
OPENAI_API_KEY = your_openai_key
SERVICE_ACCOUNT_FILE = your_service_account_key
GDRIVE_FOLDER_ID = your_gdrive_key
```

## 🎬 Running the Application

```bash
# Run the app
python main.py
```
