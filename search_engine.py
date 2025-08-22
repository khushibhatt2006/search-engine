import os
from dotenv import load_dotenv
from serpapi import GoogleSearch
from groq import Groq
from .utils import clean_query

# Load API keys from .env
load_dotenv()

def fetch_serpapi_results(query: str, search_type: str = "all"):
    """Fetch results from SerpAPI by type: all | images | news"""
    serpapi_key = os.getenv("SERPAPI_KEY")
    if not serpapi_key:
        raise ValueError("⚠️ SERPAPI_KEY missing in .env file")

    params = {"q": query, "api_key": serpapi_key}

    if search_type == "images":
        params["tbm"] = "isch"  # Image search
    elif search_type == "news":
        params["tbm"] = "nws"   # News search

    search = GoogleSearch(params)
    return search.get_dict()


def search(query: str):
    """Fetch Google results (all, images, news) and summarize organic results with Groq"""
    query = clean_query(query)

    # --- All results (organic search) ---
    results_dict = fetch_serpapi_results(query, "all")
    organic_results = results_dict.get("organic_results", [])
    formatted_results = [
        {
            "title": r.get("title", ""),
            "url": r.get("link", ""),
            "snippet": r.get("snippet", "")
        }
        for r in organic_results
    ]

    # --- Summarize with Groq ---
    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key:
        raise ValueError("⚠️ GROQ_API_KEY missing in .env file")

    client = Groq(api_key=groq_key)
    joined = "\n".join([f"{r['title']} - {r['snippet']} ({r['url']})" for r in formatted_results[:5]])

    summary_prompt = f"""
    You are a helpful search assistant.
    Here are search results about "{query}":
    {joined}

    Summarize these results in a clear, concise paragraph.
    """

    summary_resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": summary_prompt}],
    )
    summary_text = summary_resp.choices[0].message.content

    formatted_results.insert(0, {
        "title": "AI Summary",
        "url": "",
        "snippet": summary_text
    })

    # --- Images ---
    images_dict = fetch_serpapi_results(query, "images")
    image_results = images_dict.get("images_results", [])

    formatted_images = [
        {"title": img.get("title", ""), "url": img.get("original", ""), "source": img.get("source", "")}
        for img in image_results[:12]  # limit to 12
    ]

    # --- News ---
    news_dict = fetch_serpapi_results(query, "news")
    news_results = news_dict.get("news_results", [])

    formatted_news = [
        {"title": n.get("title", ""), "url": n.get("link", ""), "snippet": n.get("snippet", "")}
        for n in news_results[:10]
    ]

    return {
        "all": formatted_results,
        "images": formatted_images,
        "news": formatted_news
    }
