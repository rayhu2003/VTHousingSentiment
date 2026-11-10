# VTHousingSentiment

Sentiment analysis of off-campus apartment complexes near Virginia Tech, built from Reddit discussion in r/VirginiaTech and r/Blacksburg.

Live site: https://rayhu2003.github.io/VTHousingSentiment

## What it does

For each of 11 apartment complexes near Virginia Tech, the project scores Reddit posts and comments on three categories — **maintenance**, **distance**, and **environment** — on a 1-10 scale (5 = neutral) using Google's Gemini model. The web app lists every complex with its scores and lets you sort by category.

## Run it locally (quickest way to see it working)

The web app doesn't need any API keys to run — `my-app/backend/app.py` just reads the `sentiments.json` already checked into the repo. No Reddit/MongoDB/Gemini credentials, no internet dependency on Render or GitHub Pages.

```bash
./run_local.bat        # Windows: double-click it, or run from a terminal
```

This starts the Flask backend in its own window, then starts the React dev server pointed at it (`REACT_APP_API_URL=http://localhost:5000`), which opens `http://localhost:3000` in your browser automatically.

Prerequisites: Python with `flask` and `flask-cors` installed (`pip install -r my-app/backend/requirements.txt`), and `npm install` already run once in `my-app/`.

To stop it, close both opened terminal windows (or Ctrl+C in each).

## Architecture

There are two halves: an offline data pipeline that runs by hand, and a web app that only ever reads the pipeline's output.

```
Offline pipeline (run manually, writes a JSON file):

  Reddit  --PRAW-->  MongoDB (RedditReviews)  --Gemini-->  apartment_sentiments.json
 (DataScraper.py)                              (SentimentFromDB.py)

Web app (reads that JSON file, no live Reddit/Gemini calls):

  React frontend (GitHub Pages)  <--HTTP-->  Flask API (Render)
        my-app/src                            my-app/backend/app.py
```

The pipeline runs in batch rather than on every page load because:
- Gemini calls are slow and cost money per request
- The site stays up even if Reddit, MongoDB, or Gemini are unreachable
- Scores only need to change when new posts are scraped, not on every visit

## Files

| Path | Purpose |
|---|---|
| `DataScraper.py` | Searches r/VirginiaTech and r/Blacksburg for each complex's name, saves matching posts and their top comments to MongoDB |
| `SentimentFromDB.py` | Pulls all saved text per complex from MongoDB, sends it to Gemini, writes `apartment_sentiments.json` |
| `apartment_sentiments.json` | Output of the last pipeline run — the source of truth for `my-app/backend/sentiments.json` |
| `my-app/backend/app.py` | Flask API: serves the sentiment data (plus hardcoded image/website URLs per complex) at `GET /sort?by=<overall\|maintenance\|distance\|environment>` |
| `my-app/src/Components/Sentiment.jsx` | Fetches from the Flask API and renders each complex as a sortable list with sentiment bars |
| `my-app/src/Components/NavBar.jsx` | Top navigation (Home / About Sentiment) |

## Setup

### 1. Pipeline (Python)

```bash
pip install -r requirements.txt
cp .env.example .env   # fill in your own values below
```

`.env` needs:
```
MONGODB_URI=            # MongoDB Atlas connection string
REDDIT_CLIENT_ID=       # from a Reddit "script" app at reddit.com/prefs/apps
REDDIT_CLIENT_SECRET=
GEMINI_API_KEY=         # from Google AI Studio
```

Run the pipeline:
```bash
python DataScraper.py       # scrape Reddit into MongoDB
python SentimentFromDB.py   # score the scraped text, write apartment_sentiments.json
```

Copy the result into the API:
```bash
cp apartment_sentiments.json my-app/backend/sentiments.json
```

### 2. Backend (Flask)

```bash
cd my-app/backend
pip install -r requirements.txt
python app.py
```

Runs on `http://localhost:5000` by default.

### 3. Frontend (React)

```bash
cd my-app
npm install
REACT_APP_API_URL=http://localhost:5000 npm start
```

Omit `REACT_APP_API_URL` to point at the deployed Render API instead of a local Flask server. The production build (`npm run deploy`) always targets the deployed API.

## Known limitations

- All of a complex's scraped text is sent to Gemini in a single prompt. This can't show which specific post drove a score, and could hit token limits as more data accumulates.
- Scores haven't been validated against human ratings — there's no accuracy measurement yet.
- The pipeline is run by hand; there's no scheduled job keeping the data current.
- The overall score is an unweighted average of the three categories.
- Some image/website URLs in `my-app/backend/app.py` are placeholders and may not match the actual complex.
