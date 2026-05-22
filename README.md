News Sentiment Analyzer
This is a web application I built that grabs news articles from different sources and figures out if they sound positive, negative, or neutral. It uses some basic AI (well, Natural Language Processing) to do that.

What It Can Do
->Get News from Multiple Places
->Pulls articles from two free news APIs (NewsAPI and NewsData.io)
->Lets you search by keywords or browse by category
->Shows article images, sources, and publication dates
->Figure Out the Tone
  --Automatically reads each article title and description to determine if it feels positive, negative, or neutral
  --Displays a colored badge on each article (green for positive, red for negative, gray for neutral)
->Gives you a quick summary of sentiment stats for your search
->Easy to Use
  --Works on computers, tablets, and phones
  --Search and see results immediately
  --Tells you nicely if something goes wrong (slow internet, no results, etc.)
->Handles Problems Gracefully
  --Waits 5 seconds max for an API to respond - if it's too slow, it moves on
  --Doesn't crash if an article is missing an image or description
  --Shows helpful error messages instead of just breaking
  --Checks that you actually typed something before searching

Requirements
->Python 3.8 or newer
->Internet connection
->Free API keys (explained below)

Setup Instructions
->Step 1: Get the Project
  If you're using Git:

  git clone <repository-url>
  cd news-sentiment-analyzer

  If you downloaded it as a ZIP file, just extract it somewhere you'll remember.

->Step 2: Make Sure Python is Installed
  You can download Python from python.org. During installation, make sure you check the box that says "Add Python to PATH" - this makes it work from the command line.
  To check if it's installed, open your terminal (Command Prompt on Windows, Terminal on Mac/Linux) and type:

  python --version
  
  If you see something like "Python 3.12.x", you're good.

->Step 3: Create a Virtual Environment
  This is basically a clean workspace for your project so it doesn't mess up other Python stuff on your computer.
  --On Windows:

  python -m venv venv
  venv\Scripts\activate
  
  --On Mac/Linux:

  python3 -m venv venv
  source venv/bin/activate
  
  You'll know it worked when you see (venv) at the beginning of your terminal line.

->Step 4: Install the Libraries
  One command installs everything you need:

  pip install -r requirements.txt
  
  This might take a minute or two.

->Step 5: Get Your Free API Keys
  --NewsAPI (you need this one):

  Go to newsapi.org
  Click "Get API Key" and sign up with your email
  Copy the key they give you

--NewsData (optional but nice to have):

  Go to newsdata.io
  Sign up for a free account
  Copy your API key
  
  Both have free tiers that are fine for this project.

->Step 6: Create the .env File
  In your project folder, create a new file called .env (just that name, no extra stuff at the end). Open it in Notepad and add this:

  NEWSAPI_KEY=paste_your_newsapi_key_here
  NEWSDATA_KEY=paste_your_newsdata_key_here
  
  Replace the placeholder text with your actual keys. Save the file.
  Important: Never share this file or upload it anywhere - these keys are like passwords.

->Step 7: Run the Application
  --On Windows:

  python app.py
  
  --On Mac/Linux:

  python3 app.py
  
  You should see a message saying something like "Running on http://127.0.0.1:5000".

->Step 8: Open It in Your Browser
  Open your web browser (Chrome, Firefox, Edge, whatever) and go to:

  http://127.0.0.1:5000
  
  You should see the News Sentiment Analyzer interface.

->Step 9: Try a Search
  Type something you want news about - like "climate change" or "space exploration"
  Pick a category if you want (or leave it on "All Categories")
  Click the Search button
  Wait a few seconds for the articles to load
  Look at the colored badges on each article - green means positive, red means negative, gray means neutral

  To Stop the Application
  Press Ctrl+C in your terminal where it's running.

How the Sentiment Analysis Works
  I used a Python library called TextBlob. It looks at words in the article title and description and gives a score from -1 (very negative) to +1 (very positive). Then I turn that into simple labels:

->  Positive score > 0.1 -> green badge (article feels optimistic or happy)
->  Negative score < -0.1 -> red badge (article feels pessimistic or sad)
->  Everything in between -> gray badge (just facts, no strong emotion)

  It's not perfect - it can't detect sarcasm or very subtle emotions - but for news headlines it works pretty well.

Things I Handled Carefully
  --Slow or Broken APIs
  If an API takes longer than 5 seconds to respond, the app gives up and either tries the other API or just shows what it got. This way you don't sit there waiting forever.

  --Missing Information
  Sometimes APIs return articles without images or with empty descriptions. The app substitutes placeholder images and "No description" text instead of just crashing.

  --Bad User Input
  The search box won't let you search with just one letter, and it protects against people trying to inject malicious code into the search box.

  --Duplicate Articles
  Since I'm pulling from two different APIs, sometimes the same article appears twice. The app checks for duplicate titles and only shows each article once.

Project Structure
  Here's what all the files do:

  ->  app.py - This is the main brain. It handles the web server, talks to the APIs, runs the sentiment analysis, and sends data to the frontend.
  ->  templates/index.html - This is the webpage structure. It builds the search box, article cards, and stats dashboard.
  ->  static/style.css - This makes everything look nice - colors, spacing, responsive layout for phones.
  ->  requirements.txt - Just a list of Python packages needed so you can install them all at once.
  ->  .env - Stores your API keys (you create this file yourself)
  ->  .gitignore - Tells Git which files to ignore (like the .env file so you don't accidentally share your keys)

Common Problems and How to Fix Them
  "ModuleNotFoundError" when trying to run
  This means the required libraries aren't installed. Make sure your virtual environment is activated (you see (venv) in your terminal) and run pip install -r requirements.txt again.

  "NEWSAPI_KEY not found" or API key errors
  Either you forgot to create the .env file, or you put it in the wrong place. The .env file should be in the same folder as app.py. Also check that you didn't put quotes around your API key.

  No articles found when searching
  This could be a few things. Your internet might be down, the API keys might be wrong, or you might have hit the rate limit (free accounts have daily limits). Try a different search term or wait a few minutes.

  Page won't load in browser
  Check that your terminal still shows Flask is running. If you closed the terminal or pressed Ctrl+C, the server stops. Also make sure you're using http://127.0.0.1:5000 not https://.

  Sentiment badges are all neutral
  Some articles are just factual with no strong emotional words. Try searching for something more opinion-heavy like "controversial" or "breakthrough" - you should see more variety.

What I Used to Build This
  Python 3 - the programming language
  Flask - a lightweight web framework that handles requests and serves pages
  Requests - a library for calling external APIs
  TextBlob - the sentiment analysis library
  HTML/CSS - for the user interface
  JavaScript - for loading data without refreshing the page

Where I Got the News From
  NewsAPI (newsapi.org) gives me access to hundreds of news sources. Free tier gives me 100 requests per day, which is plenty for testing and regular use.
  NewsData.io (newsdata.io) is similar - 200 requests per day on the free plan. I use both so if one fails or runs out of requests, the other might still work.

  Both APIs just return JSON data - structured lists of articles with titles, descriptions, URLs, and images.

What I'd Add With More Time
  If I had another week, I would add:
  --A way to save favorite articles (using a small database)
  --Export search results to CSV so you can analyze them in Excel
  --Email alerts - get notified when there's news on a topic you care about
  --A graph showing how sentiment changes over time for a topic
  --Caching so repeated searches don't hit the APIs as much (saving your daily quota)

Known Limitations
  The sentiment analysis is pretty basic - it just looks at individual words and doesn't understand context very well. For example, "This is sick!" could be positive slang or literally talking about illness. It's good enough for news headlines but wouldn't work for something like analyzing social media comments.
  The free API tiers also have rate limits. If you search too many times in a short period, they'll start rejecting requests. That's why there are error messages explaining what happened.

Getting Help
  If something isn't working:
  --Read the error messages in your terminal - they usually tell you what's wrong
  --Make sure your API keys are correct and the .env file is in the right place
  --Check that you have an internet connection
  --Try restarting the application
  --The API documentation is also helpful:
    NewsAPI docs: newsapi.org/docs
    NewsData docs: newsdata.io/docs

That's everything. Follow the setup steps and you should have it running in about 10 minutes. Good luck!
