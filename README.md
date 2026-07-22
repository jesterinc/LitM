# Legend in the Mist - Fan Project 🌫️🎲

Un'applicazione web per la gestione di campagne narrative basata sull'universo di *Legend in the Mist*. Questo strumento permette ai Narratori di organizzare sessioni, gestire NPC e schede, mentre i Giocatori possono accedere alle proprie avventure e personaggi.

> **Disclaimer:** Questo è un progetto fan-made a scopo educativo e non ha alcuna affiliazione ufficiale con Son of Oak Studio o Isola Illyone Edizioni.

## 🛠️ Stack Tecnologico

*   **Frontend:** Vue 3 (Composition API), CSS3
*   **Backend:** Django Rest Framework (Python)
*   **Database:** PostgreSQL
*   **Containerizzazione:** Docker & Docker Compose

## 🚀 Avvio Rapido (Docker)

1.  **Avvia i servizi:**
    ```bash
    docker compose up --build -d
    ```

2.  **Esegui le migrazioni:**
    ```bash
    docker compose exec backend python manage.py migrate
    docker compose exec backend python manage.py createsuperuser
    ```

3.  **Accedi all'app:**
    *   Frontend: `http://localhost:8090`
    *   API: `http://localhost:8000/api/`

## 📂 Struttura

*   `backend/`: Applicazione Django (Users, Campaigns)
*   `frontend/`: Applicazione Vue.js (Login, Dashboard, Views)
*   `docker-compose.yml`: Configurazione container

## 🎮 Funzionalità

*   Autenticazione ruoli (Giocatore/Narratore)
*   Dashboard dinamica
*   Gestione Campagne e Membri
