import re

def clean_query(query: str) -> str:
    """Clean query input."""
    return re.sub(r"[^a-zA-Z0-9 ]", "", query).strip()

def format_results(results: list) -> str:
    """Return HTML string for rendering search results."""
    html = ""
    for res in results:
        html += f"""
        <div class="result">
            <a href="{res['url']}" target="_blank" class="result-title">{res['title']}</a>
            <div class="result-url">{res['url']}</div>
            <div class="result-snippet">{res['snippet']}</div>
        </div>
        """
    return html
