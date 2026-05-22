ANSWERS.md

1. How to run
Here are the exact steps to run this project on a fresh Windows machine:

->Step 1: Install Python
Download Python 3.8 or newer from python.org. During installation, check "Add Python to PATH".

->Step 2: Open Terminal and Navigate to Project Folder

cd C:\path\to\my-news-app

->Step 3: Create Virtual Environment

python -m venv venv
venv\Scripts\activate

You should see (venv) appear at the beginning of your command line.

->Step 4: Install Required Packages

pip install flask requests textblob python-dotenv
python -m textblob.download_corpora

->Step 5: Set Up API Keys
Create a file named .env in the project folder with this content:

NEWSAPI_KEY=your_actual_key_here
NEWSDATA_KEY=your_actual_key_here

Get free keys from newsapi.org and newsdata.io.

->Step 6: Run the Application

python app.py

->Step 7: Open Browser
Go to http://127.0.0.1:5000

On Mac/Linux:
Replace venv\Scripts\activate with source venv/bin/activate and use python3 instead of python.

2. Stack choice
Why I picked this stack:

Python was an obvious choice because it has excellent libraries for API calls (requests) and sentiment analysis (TextBlob). I didn't want to build sentiment analysis from scratch - that would take weeks.
Flask is lightweight and perfect for small projects like this. Unlike Django which comes with a lot of extra stuff I don't need, Flask lets me just focus on what matters: getting news and analyzing it.
TextBlob is simple. There are more accurate sentiment analyzers like VADER, Stanza or Hugging Face, but they are larger and are more complex. For a student project, TextBlob works fine and installs quickly.
HTML/CSS + simple JavaScript works everywhere. No need for React or Angular which would add complexity. I wanted anyone to be able to open the page without waiting for heavy frameworks to load.

What would have been a worse choice:

C++ would be terrible (even though I am much more adept at it). It has no built-in HTTP libraries for API calls, no sentiment analysis libraries, and you'd have to manually parse JSON. A simple task that takes 5 lines in Python would take 200 lines in C++.
Java would also be worse. While it has libraries for HTTP, setting up a Java web server requires more configuration than Flask. The code would be much longer and harder to read.
Pure JavaScript running in the browser (no backend) would expose my API keys to anyone who opens the page. That's a security risk because someone could steal my keys and use up my API quota.

3. One real edge case
Edge case: API timeout handling

File: app.py
Lines: Approximately line 85-89 (in the fetch_news_from_newsapi function)

Here is the exact code:

response = requests.get(url, params=params, timeout=5)

What this does:
The timeout=5 parameter tells Python to wait a maximum of 5 seconds for the NewsAPI server to respond. If the server doesn't respond within 5 seconds, Python raises a Timeout exception.

What would happen without this handling:
If I didn't include timeout=5, the program would wait forever for the API to respond. If NewsAPI had server problems or was very slow, the user's browser would just keep loading and loading with no feedback. They wouldn't know if the app was working or broken. Eventually they might just close the browser tab.

How I handle the timeout:
Later in the code (around line 113-115), I have:

except requests.exceptions.Timeout:
    print("NewsAPI was too slow")
    return []
    
When the timeout happens, I catch it, print a message (for debugging), and return an empty list. Then the app tries the second API (NewsData) instead. The user sees results from the working API without waiting forever.

Why this matters for the assessment:
The evaluator specifically said they will test "the API being slow". This is exactly the handling they're looking for.

4. AI usage
I used ChatGPT to help build this project. Here's exactly where and how:

Place 1: Understanding Flask routes
What I asked: "How do I create a search endpoint in Flask that reads a query parameter from the URL?"
What AI gave me: Example code using request.args.get()
What I changed: I added validation for empty queries and minimum length checks. The AI example just assumed the parameter existed.

Place 2: Sentiment analysis with TextBlob (sreached the library on internet)
What I asked: "How does TextBlob calculate sentiment and how do I interpret the polarity score?"
What AI gave me: Explanation that polarity ranges from -1 to +1, with 0 being neutral
What I changed: The AI suggested using -0.05 and 0.05 as thresholds. I changed these to -0.1 and 0.1 because I noticed many articles were being marked as neutral when they were slightly positive. The wider threshold gives more clear results.

Place 3: HTML+CSS styling
What I asked: "Give me HTML and CSS for a modern news card layout with sentiment badges"
What AI gave me: Complete HTML and CSS with gradients, shadows, and responsive design
What I changed: I removed some animations that were causing performance issues on my laptop. The cards had fade-in effects that made scrolling feel laggy. I also adjusted colors to have better contrast for readability.

Place 4: Git workflow (previously I knew how to use GitHub through Graphics, but had no ideas about CLI Git/Github and commiting) 

What I asked: "How do I commit my changes and push to GitHub after I made updates?"
What AI gave me: Step by step git commands
What I changed: I asked follow-up questions about what each command actually does instead of just copying. I didn't change the commands themselves but I organized my commits differently - smaller commits with specific messages instead of one big commit.

How AI helped me learn:
I didn't just copy-paste. For each piece of code, I asked the AI to explain what each line does. Then I typed it myself. This helped me understand Flask, API calls, and error handling much better than just reading documentation.

5. Honest gap
What's not good enough:
My app doesn't have any way to save or cache results. Every time someone searches for the same keyword, the app calls the APIs again. This wastes my daily API quota and makes searches slower because the app waits for fresh data each time.
For example, if five different people search for "technology" on the same day, the app calls the APIs five separate times. The articles from the first search and the fifth search are probably very similar, but the app doesn't know that.

What I would do with one more day:
I would add a caching system using SQLite (a simple file-based database that comes with Python). Here's exactly what I would build:
--Create a cache table in the database with columns: query, timestamp, and results (stored as JSON text)
--When a user searches, first check if there's a cached result for that query from less than 1 hour ago
--If yes, show the cached results immediately (fast!)
--In the background, fetch fresh results and update the cache
--If the cached results are older than 1 hour, show a message like "Fetching latest news..." while getting fresh data

Why this would make the submission better:

Saves API quota (I can handle more searches without hitting limits)
Faster response time for users (cached results load instantly)
Shows database skills (employers like seeing SQL knowledge)
Handles API downtime better (if APIs are down, cached results still work)

Why I didn't do this already:

I ran out of time focusing on getting the sentiment analysis and error handling working properly and also beacuse I went down with a Flu. The assessment required handling API errors and bad input, so I prioritized those. Caching was a "nice to have" but not required for the basic submission.
