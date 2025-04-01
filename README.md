# M122-LB1

1. Terminal öffnen

2. In dein Projektverzeichnis wechseln

Wo deine docker-compose.yml liegt:

cd Users\Moreno (SchoolWork)\Downloads\M122-LB1-main\M122-LB1-main\Scraper

3. Docker Compose starten

docker-compose up --build

Warte, bis beide Container hochgefahren sind. Danach kannst du ein neues Terminal-Fenster öffnen oder im bestehenden Terminal mit Strg+C abbrechen und folgendes tun:

4. Laufende Container checken

docker ps

Beispielausgabe:

CONTAINER ID   IMAGE           ...   NAMES
cabc1234ab     postgres:15           scraper-db-1

5. Jetzt: In die Datenbank reinspringen

docker exec -it scraper-db-1 psql -U user -d searchdb

Hinweis: Ersetze scraper-db-1 mit dem Namen, den du bei docker ps siehst.

Wenn alles passt, landest du in der Postgres-Konsole:

searchdb=#
Dann kannst du z. B. das hier machen:

SELECT * FROM search_results;



docker-compose run app python main.py "Ferrari"
