#!/usr/bin/env python3
"""
Web Search with Fallback
Tries Brave Search first, falls back to DuckDuckGo if rate limited
"""

import sys
import subprocess
import json
from ddgs import DDGS

def brave_search(query, count=5):
    """Try Brave Search via openclaw web_search"""
    try:
        result = subprocess.run(
            ['openclaw', 'web_search', query, '--count', str(count)],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
    except Exception as e:
        print(f"Brave search failed: {e}", file=sys.stderr)
    return None

def ddg_search(query, count=5):
    """Fallback to DuckDuckGo"""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=count, region='en-us'))
            return {
                'results': [
                    {
                        'title': r.get('title', ''),
                        'url': r.get('href', ''),
                        'description': r.get('body', '')
                    }
                    for r in results
                ],
                'source': 'duckduckgo',
                'query': query
            }
    except Exception as e:
        print(f"DuckDuckGo search failed: {e}", file=sys.stderr)
    return None

def search(query, count=5):
    """Search with automatic fallback"""
    # Try Brave first
    result = brave_search(query, count)
    if result and 'results' in result:
        return result
    
    # Fallback to DuckDuckGo
    print("⚠️  Brave rate limited, using DuckDuckGo fallback", file=sys.stderr)
    return ddg_search(query, count)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: web_search_fallback.py 'query' [count]", file=sys.stderr)
        sys.exit(1)
    
    query = sys.argv[1]
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    result = search(query, count)
    if result:
        print(json.dumps(result, indent=2))
    else:
        print(json.dumps({'error': 'All search methods failed'}))
        sys.exit(1)
