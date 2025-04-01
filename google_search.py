import argparse
import urllib.parse
import requests
import webbrowser
from bs4 import BeautifulSoup
from datetime import datetime
import psycopg2
import os

def get_google_search_url(query):
    query_encoded = urllib.parse.quote_plus(query)
    return f"https://www.google.com/search?q={query_encoded}&oq={query_encoded}&gs_lcrp=EgZjaHJvbWUyEQgAEEUYORhDGLEDGIAEGIoFMhIIARAAGEMYgwEYsQMYgAQYigUyEggCEAAYQxiDARixAxiABBiKBTINCAMQABiDARixAxiABDINCAQQABiDARixAxiABDIGCAUQRRg8MgYIBhBFGDwyBggHEEUYPNIBCDE4OTlqMGo5qAIAsAIB&sourceid=chrome&ie=UTF-8"

def get_duckduckgo_results(query, max_results=10):
    query_encoded = urllib.parse.quote_plus(query)
    url = f"https://html.duckduckgo.com/html/?q={query_encoded}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        results = []

        for result in soup.find_all("a", class_="result__a", limit=max_results):
            title = result.get_text()
            href = result.get("href")
            results.append((title, href))

        return results
    except Exception as e:
        print(f"Fehler beim Abrufen der Suchergebnisse: {e}")
        return []

def save_to_database(query, results):
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB", "searchdb"),
            user=os.getenv("POSTGRES_USER", "user"),
            password=os.getenv("POSTGRES_PASSWORD", "password"),
            host=os.getenv("DB_HOST", "db"),
            port=5432
        )
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS search_results (
                id SERIAL PRIMARY KEY,
                query TEXT,
                title TEXT,
                url TEXT,
                timestamp TIMESTAMP
            );
        """)
        timestamp = datetime.now()

        for title, url in results:
            cur.execute(
                "INSERT INTO search_results (query, title, url, timestamp) VALUES (%s, %s, %s, %s);",
                (query, title, url, timestamp)
            )

        conn.commit()
        cur.close()
        conn.close()
        print("Ergebnisse erfolgreich in der Datenbank gespeichert.")
    except Exception as e:
        print(f"Fehler beim Speichern in der Datenbank: {e}")

def main():
    parser = argparse.ArgumentParser(description="Search and Save to DB")
    parser.add_argument("query", type=str, help="Search query")
    args = parser.parse_args()

    print(f"Suche nach: {args.query}")
    results = get_duckduckgo_results(args.query)

    if results:
        print(f"{len(results)} Ergebnisse gefunden. Speichere in Datenbank...")
        save_to_database(args.query, results)
        
        # Öffne die Google-Suchergebnisseite im Browser
        google_url = get_google_search_url(args.query)
        print(f"Öffne die Google-Suche: {google_url}")
        webbrowser.open(google_url)
    else:
        print("Keine Ergebnisse gefunden.")

if __name__ == "__main__":
    main()
