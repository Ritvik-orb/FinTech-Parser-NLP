# FinTech Document Parser

A sophisticated NLP-powered document parser for financial documents with dark violet premium theme.

## Features

- **OCR Processing**: Extract text from PDFs and images with pdfplumber and Tesseract
- **Entity Recognition**: Identify names, banks, dates, amounts, and account numbers
- **Document Classification**: Automatically classify documents (Bank Statement, Invoice, etc.)
- **Modern UI**: Dark violet theme with gold accents and premium typography
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Multiple Interfaces**: Streamlit web app and standalone HTML interface

## Local Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd NLP
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

4. **Run FastAPI backend** (Terminal 1)
   ```bash
   uvicorn main:app --reload --port 8000
   ```

5. **Run Streamlit frontend** (Terminal 2)
   ```bash
   streamlit run ui.py
   ```

6. **Access web interface**
   - Open `index.html` in your browser or serve with a local server

## Vercel Deployment

### Prerequisites
- Vercel account (free at https://vercel.com)
- Git repository connected to Vercel
- spaCy model downloaded locally

### Deploy Steps

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Deploy from command line**
   ```bash
   vercel
   ```
   Follow the prompts to connect your project.

3. **Or deploy via GitHub**
   - Push your code to GitHub
   - Visit https://vercel.com/new
   - Select your repository
   - Click "Deploy"

### Environment Variables

If needed, add to Vercel project settings:
```
PYTHON_VERSION=3.11
```

### API Endpoints

**Local:**
- `POST http://localhost:8000/upload/` - Upload document for processing

**Deployed on Vercel:**
- `POST https://your-domain.vercel.app/api/upload/` - Upload document for processing
- `GET https://your-domain.vercel.app/api/health` - Health check

### Request Format

```bash
curl -X POST -F "file=@document.pdf" \
  http://localhost:8000/upload/
```

### Response Format

```json
{
  "status": "success",
  "type": "Bank Statement",
  "entities": {
    "names": ["John Doe"],
    "banks": ["XYZ Bank"],
    "dates": ["2024-01-15"],
    "amounts": ["$5,000.00"],
    "accounts": ["123456789"]
  },
  "text": "Full extracted text from document..."
}
```

## Color Palette

- **Dark Background**: #0d0221, #1a0033
- **Primary Violet**: #5a189a
- **Light Violet**: #7b2cbf
- **Gold Accent**: #c77dff

## Typography

- **Headings**: Playfair Display (serif)
- **Body**: Inter (sans-serif)

## Technologies

- **Backend**: Python, FastAPI, Uvicorn
- **Processing**: pdfplumber, pytesseract, Pillow, spaCy
- **Frontend**: Streamlit, HTML5, CSS3, Vanilla JavaScript
- **Deployment**: Vercel (serverless)

## Files

- `main.py` - FastAPI server (local development)
- `api/index.py` - Vercel serverless function
- `ocr.py` - PDF/image text extraction
- `ner.py` - Entity recognition and classification
- `ui.py` - Streamlit interface
- `index.html` - Standalone web interface
- `web-script.js` - JavaScript functionality
- `web-style.css` - Styling
- `vercel.json` - Vercel deployment configuration

## Troubleshooting

### spaCy Model Issue
If you get "model not found" error, download it:
```bash
python -m spacy download en_core_web_sm
```

### File Upload Issues
- Ensure file size is within limits
- Check that PDF format is valid
- For Vercel, temporary files are stored in `/tmp`

### API Connection
- Development: Ensure FastAPI runs on port 8000
- Vercel: Check endpoint is `https://your-domain.vercel.app/api/upload/`
- Use CORS headers if frontend is on different domain

## License

MIT License - feel free to use and modify

## Support

For issues or questions, check the source code or update the configuration.
