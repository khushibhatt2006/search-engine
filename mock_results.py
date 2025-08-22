import random

def mock_results(query: str):
    """Generate mock results with working URLs (Google search links)."""
    return [
        {
            "title": f"Result about {query} #{i+1}",
            "url": f"https://www.google.com/search?q={query.replace(' ', '+')}&start={i*10}",
            "snippet": f"This is a short description about {query} (result {i+1})."
        }
        for i in range(10)
    ]
