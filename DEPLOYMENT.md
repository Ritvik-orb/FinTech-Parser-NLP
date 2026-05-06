# Vercel Deployment Guide

## Quick Start

Your project is now ready for Vercel deployment. Follow these steps:

### Option 1: Deploy via CLI (Fastest)

1. **Install Vercel CLI** (if not already installed)
   ```bash
   npm install -g vercel
   ```

2. **Navigate to your project directory**
   ```bash
   cd c:\Users\Thunderbolt\Desktop\NLP
   ```

3. **Login to Vercel**
   ```bash
   vercel login
   ```
   (Opens browser to authenticate with Vercel account)

4. **Deploy**
   ```bash
   vercel --prod
   ```
   This will:
   - Upload your project
   - Install dependencies from requirements.txt
   - Build and deploy the serverless API and static files
   - Provide you with a live URL

### Option 2: Deploy via GitHub (Recommended for long-term)

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit with Vercel config"
   git remote add origin https://github.com/yourusername/nlp-document-parser.git
   git branch -M main
   git push -u origin main
   ```

2. **Connect to Vercel**
   - Go to https://vercel.com/new
   - Click "Import Git Repository"
   - Select your GitHub repository
   - Click "Deploy"

3. **Automatic deployments**
   - Every push to `main` will automatically deploy
   - Preview deployments for pull requests

## What Gets Deployed

- **API**: `/api/upload` endpoint (serverless function)
- **Static Files**: HTML, CSS, JavaScript in `/public` folder
- **Health Check**: `/api/health` endpoint for monitoring

## Environment Details

- **Python Version**: 3.11
- **Runtime**: Vercel Serverless Functions
- **Memory**: 1024 MB
- **Timeout**: 30 seconds
- **Temporary Storage**: `/tmp` (for file processing)

## After Deployment

Your deployed application will be available at:
```
https://your-project-name.vercel.app
```

### Access Points:

1. **Web Interface**
   ```
   https://your-project-name.vercel.app
   ```

2. **API Upload Endpoint**
   ```
   POST https://your-project-name.vercel.app/api/upload
   ```

3. **Health Check**
   ```
   GET https://your-project-name.vercel.app/api/health
   ```

## Testing Your Deployment

### Test with curl:
```bash
curl -X POST -F "file=@your_document.pdf" \
  https://your-project-name.vercel.app/api/upload
```

### Test via web interface:
1. Open https://your-project-name.vercel.app in browser
2. Upload a PDF or image
3. View extracted entities and text

## Important Notes

1. **File Size Limits**: Vercel allows 50MB max payload per function call
2. **Processing Time**: Maximum 30 seconds per request (adjust in vercel.json if needed)
3. **Temporary Files**: Automatically cleaned up from `/tmp` after processing
4. **spaCy Model**: Pre-included in requirements.txt installation
5. **CORS**: Requests from your domain are allowed by default

## Troubleshooting

### spaCy Model Not Found
The model is downloaded during build. If issues occur:
- Check build logs in Vercel Dashboard
- Ensure `en_core_web_sm` is included in dependencies

### Upload Fails
- Check file size (< 50MB)
- Verify file is valid PDF or image
- Check browser console for error details

### API Returns 500 Error
- Check Vercel function logs in Dashboard
- Ensure all Python dependencies are in requirements.txt
- Verify OCR/NER modules are present

## Project Structure on Vercel

```
/
├── api/
│   └── index.py          (FastAPI app - serverless function)
├── public/
│   ├── index.html        (Web interface)
│   ├── web-style.css     (Styling)
│   └── web-script.js     (JavaScript)
├── ocr.py                (Text extraction)
├── ner.py                (Entity recognition)
├── requirements.txt      (Python dependencies)
└── vercel.json          (Deployment config)
```

## Monitoring & Logs

1. Visit your Vercel dashboard: https://vercel.com/dashboard
2. Click on your project
3. Go to "Deployments" tab to see all deployments
4. Click on a deployment to see logs and performance metrics
5. Check "Functions" tab for API function logs

## Custom Domain (Optional)

To add your own domain:
1. Go to project settings in Vercel
2. Click "Domains"
3. Add your custom domain
4. Update DNS records as instructed

## Next Steps

- Monitor the deployment in Vercel Dashboard
- Share your live URL: `https://your-project-name.vercel.app`
- Customize domain name if desired
- Set up GitHub Actions for additional CI/CD (optional)

---

**Questions?** Check Vercel docs at https://vercel.com/docs
