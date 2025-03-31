import webbrowser
import argparse
import urllib.parse

def open_google_search(query):
    # Den Suchbegriff URL-codieren
    query_encoded = urllib.parse.quote(query)
    # Die Google-Such-URL zusammenstellen
    url = f"https://www.google.com/search?q={query_encoded}&oq={query_encoded}"
    
    # Debugging-Ausgabe zur Überprüfung
    print(f"Generated URL: {url}")
    
    # Versuche die URL im Standardbrowser zu öffnen
    try:
        webbrowser.open(url)
        print(f"Opening Google search for: {query}")
    except Exception as e:
        print(f"Error opening browser: {e}")

def main():
    parser = argparse.ArgumentParser(description="Google Search URL Opener")
    parser.add_argument("query", type=str, help="Search query")
    args = parser.parse_args()
    
    # Google-Such-URL öffnen
    open_google_search(args.query)

if __name__ == "__main__":
    main()
