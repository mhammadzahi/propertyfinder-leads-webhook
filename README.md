
# PropertyFinder Leads Webhook & Data Pipeline

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.120.0-green?logo=fastapi)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🚀 Overview

A robust, production-ready webhook and data processing solution for Property Finder leads. This project features a FastAPI-based webhook server for receiving and processing lead data, tools for fetching and enriching listing and agent information, CSV generation, and S3 integration for file management. Designed for automation, reliability, and easy deployment as a Linux service.

---

## ✨ Features
- **Webhook Receiver:** FastAPI server for Property Finder lead webhooks
- **Data Enrichment:** Fetches listing and agent details from Property Finder APIs
- **CSV Export:** Generates and updates CSVs with a stable schema
- **S3 Integration:** Upload/download utilities for AWS S3
- **Service Ready:** Includes a systemd service file for background operation
- **Modular Design:** Clean separation of logic in `functions/` and `others/`

---

## 📦 Project Structure

```text
.
├── app.py
├── functions
│   ├── agent.py
│   ├── csv_generator.py
│   ├── get_tocken.py
│   └── listing.py
├── others
│   ├── get_leads.py
│   ├── pf-webhook.service
│   ├── s3_downloader.py
│   ├── s3_uploader.py
│   └── webhook.py
├── pf-webhook.py
├── README.md
├── requirements.txt
└── todo
```

---

## ⚙️ Setup & Installation

1. **Clone the repository:**
	```bash
	git clone https://github.com/yourusername/propertyfinder-leads-webhook.git
	cd propertyfinder-leads-webhook
	```
2. **Create and activate a virtual environment:**
	```bash
	python3 -m venv env
	source env/bin/activate
	```
3. **Install dependencies:**
	```bash
	pip install -r requirements.txt
	```
4. **Configure environment variables:**
	- Create a `.env` file in the root directory with your API keys and secrets:
	  ```env
	  API_KEY=your_propertyfinder_api_key
	  API_SECRET=your_propertyfinder_api_secret
	  WEBHOOK_SECRET=your_webhook_secret
	  aws_access_key_id=your_aws_access_key_id
	  aws_secret_access_key=your_aws_secret_access_key
	  ```
5. **Run the FastAPI server:**
	```bash
	uvicorn pf-webhook:app --host 0.0.0.0 --port 8007
	```

---

## 🧩 Main Components

- **`pf-webhook.py`**: FastAPI server for receiving Property Finder lead webhooks.
- **`app.py`**: Batch processing script for enriching listings from CSV and saving results.
- **`functions/`**: Core logic for token management, listing/agent info, and CSV generation.
- **`others/`**: Utilities for S3 upload/download, webhook subscription, and service management.

---

## 📡 API Endpoints

### `POST /pf/lead-created`
Receives Property Finder lead webhook payloads.
- **Body:** JSON with lead data
- **Response:** `{ "status": "received" }`

### `GET /`
Health check endpoint.
- **Response:** `{ "message": "PF Webhook, V1.2.0" }`

#### Example:
```bash
curl -X POST http://localhost:8007/pf/lead-created \
	  -H "Content-Type: application/json" \
	  -d '{"id": "...", ...}'
```

---

## 🛠️ Service & Deployment

- The project includes a `pf-webhook.service` file for running the webhook as a systemd service.
- Update paths and environment variables as needed.
- Enable and start the service:
  ```bash
  sudo systemctl enable pf-webhook.service
  sudo systemctl start pf-webhook.service
  ```
- Logs are written to `pf-webhook.log` and `error-pf-webhook.log`.

---

## 📝 Todo & Roadmap
- [ ] Add more API endpoints for advanced lead processing
- [ ] Improve error handling and logging
- [ ] Add unit and integration tests
- [ ] Dockerize the application

---

## 👤 Contributors
- Mohammad Zahi

---

## 📄 License

This project is licensed under the MIT License.