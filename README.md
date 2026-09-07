# Aternos Server Starter Web App

A simple web interface to start your Aternos Minecraft server with one click.

## How It Works

1. Visit the website
2. Click the **START SERVER** button
3. The app logs into your Aternos account (via headless Chrome)
4. Clicks the start button
5. Your server starts

## Setup

### Requirements
- GitHub account
- Render account (free tier works)
- Aternos shared account credentials

### Local Testing (Optional)

1. Clone/download this repo
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file:
   ```
   ATERNOS_EMAIL=your_email@example.com
   ATERNOS_PASSWORD=your_password
   ```
4. Run locally:
   ```bash
   python app.py
   ```
5. Visit `http://localhost:5000`

### Deploy to Render

1. **Push to GitHub**
   - Create a new GitHub repo
   - Push all files from this folder to it

2. **Create Render Web Service**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Choose the repository with these files

3. **Configure Build & Deploy**
   - **Build Command:**
     ```
     pip install -r requirements.txt && apt-get update && apt-get install -y chromium-browser
     ```
   - **Start Command:**
     ```
     gunicorn app:app
     ```

4. **Add Environment Variables** (Settings → Environment)
   - `ATERNOS_EMAIL` = `your_shared_account_email@example.com`
   - `ATERNOS_PASSWORD` = `your_shared_account_password`

5. **Deploy**
   - Click "Deploy"
   - Wait 2-3 minutes for build to complete
   - Visit your Render URL when it's done

## File Structure

```
aternos-web/
├── app.py              # Flask backend
├── index.html          # Web frontend
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
└── README.md           # This file
```

## How It Works Technically

- **Frontend (index.html):** Simple button and status display
- **Backend (app.py):** 
  - Receives button click via `/api/start` endpoint
  - Launches headless Chrome with Selenium
  - Logs into Aternos with shared account credentials
  - Clicks the start button
  - Returns success/error status back to frontend

## Troubleshooting

**"Missing ATERNOS_EMAIL or ATERNOS_PASSWORD"**
- You didn't set the environment variables in Render
- Go to Settings → Environment and add both

**"Failed to start server: timeout"**
- Aternos login might have changed
- Check if login form elements still have `name="user"` and `name="password"`
- May need to update XPath in `app.py`

**Button does nothing**
- Check browser console (F12) for errors
- Check Render logs for backend errors

**Still doesn't work**
- Double-check shared account email and password are correct
- Make sure the shared account has access to the server

## Security Notes

- **Never hardcode credentials** in code—always use environment variables
- Environment variables in Render are encrypted
- Only the shared account credentials are exposed to the server
- The app doesn't store or log credentials

## License

Do whatever you want with this.
