# Design Thinking Coach 🎯

Ein AI-basierter Design-Thinking-Coach, der Menschen dabei hilft, komplexe Probleme systematisch zu durchdenken und innovative Lösungsansätze zu entwickeln.

## 🚀 Features

- **Systematische Problemanalyse** mit 5-Why-Technik
- **Lösungsorientierte Fragestellung** mit How-Might-We-Fragen
- **Strukturierte Ausgabe** als Gherkin User Stories mit Akzeptanzkriterien
- **Azure OpenAI Integration** für natürliche Konversation
- **Moderne Web-UI** mit Tailwind CSS und Alpine.js
- **Konfigurierbare Prompts** über YAML und Markdown-Dateien
- **Session-Management** für mehrere parallele Gespräche

## 🏗️ Technologie-Stack

- **Backend**: FastAPI (Python ≥3.9)
- **Frontend**: HTML + Tailwind CSS + Alpine.js
- **LLM**: Azure OpenAI (GPT-4)
- **Konfiguration**: YAML + Markdown
- **Deployment**: Uvicorn ASGI Server

## 📁 Projektstruktur

```
design-thinking-coach/
├── backend/
│   ├── main.py                 # FastAPI Server
│   ├── config/
│   │   ├── config.yaml         # Hauptkonfiguration
│   │   └── prompts/
│   │       ├── system.md       # System-Prompt für Design-Thinking
│   │       └── examples.md     # Few-Shot Beispiele
├── chatbot/
│   ├── core.py                 # Hauptklasse für Chat-Logik
│   ├── prompt_engine.py        # Prompt-Management
│   └── utils.py                # Hilfsfunktionen
├── frontend/
│   └── index.html              # Chat-UI
├── conversations/              # Gespeicherte Gespräche
├── logs/                       # Log-Dateien
├── requirements.txt            # Python-Dependencies
├── start_server.py             # Server-Start-Script
├── run_model.py                # Standalone Model Test
└── .env                        # Umgebungsvariablen (zu erstellen)
```

## 🛠️ Setup & Installation

### 1. Repository klonen
```bash
git clone <repository-url>
cd design-thinking-coach
```

### 2. Python-Umgebung einrichten
```bash
# Conda-Umgebung aktivieren
conda activate design-thinking-coach

# Dependencies installieren
pip install -r requirements.txt
```

### 3. Umgebungsvariablen konfigurieren
```bash
# .env-Datei erstellen
cp .env.example .env

# .env bearbeiten und Azure OpenAI Credentials eintragen:
# AZURE_OPENAI_API_KEY=your_api_key_here
# ENDPOINT_URL=https://your-endpoint.cognitiveservices.azure.com/
# DEPLOYMENT_NAME=gpt-4.1-mini
```

### 4. Konfiguration anpassen (optional)
Bearbeiten Sie `backend/config/config.yaml` für:
- Model-Parameter (temperature, max_tokens)
- Prompt-Dateipfade
- Conversation-Settings

## 🚀 Server starten

### Einfacher Start
```bash
python start_server.py
```

### Manueller Start mit Uvicorn
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Zugriff auf die Anwendung
- **Chat-Interface**: http://localhost:8000
- **API-Dokumentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📋 API-Endpunkte

### POST /api/chat
Chat-Nachricht senden
```json
{
  "message": "Unsere Mitarbeiter sind unmotiviert",
  "session_id": "optional-session-id"
}
```

**Response:**
```json
{
  "reply": "Ich verstehe, dass es Herausforderungen mit der Mitarbeitermotivation gibt...",
  "session_id": "session-123",
  "usage": {"prompt_tokens": 150, "completion_tokens": 200}
}
```

### GET /api/config
Aktuelle Konfiguration abrufen

### GET /api/sessions
Alle aktiven Sessions auflisten

### DELETE /api/sessions/{session_id}
Bestimmte Session löschen

## 🎛️ Konfiguration

### config.yaml
```yaml
model: "gpt-4.1-mini"
temperature: 0.3
max_tokens: 1000
system_prompt: "backend/config/prompts/system.md"
few_shot: "backend/config/prompts/examples.md"
save_history: true
```

### System-Prompt anpassen
Bearbeiten Sie `backend/config/prompts/system.md` um:
- Rolle und Verhalten des Coaches zu definieren
- Methoden und Techniken festzulegen
- Output-Format zu spezifizieren

### Few-Shot Beispiele
Erweitern Sie `backend/config/prompts/examples.md` mit:
- Beispiel-Gesprächen
- Gewünschten Antwortmustern
- Spezifischen Anwendungsfällen

## 🐛 Debugging & Logs

### Log-Dateien
- **Application Logs**: `logs/app.log`
- **Console Output**: Terminal

### Standalone Model Test
```bash
python run_model.py
```

### Environment Validation
```bash
python -c "from chatbot.utils import validate_environment; print(validate_environment())"
```

## 🔧 Entwicklung

### Code-Struktur
- **FastAPI Routes**: `backend/main.py`
- **Chat Logic**: `chatbot/core.py`
- **Prompt Management**: `chatbot/prompt_engine.py`
- **Utilities**: `chatbot/utils.py`
- **Frontend**: `frontend/index.html`

### Testing
```bash
# Install test dependencies
pip install pytest httpx

# Run tests
pytest
```

### Hot Reload
Der Server startet automatisch mit `--reload` für Entwicklung.

## 📝 Usage Examples

### Beispiel-Gespräch

**User**: "Unsere Kunden beschweren sich über den Support"

**Coach**: 
Ich verstehe, dass es Herausforderungen mit dem Kundenservice gibt. Lass uns das systematisch durchdenken.

**5-Why-Analyse:**
1. Warum beschweren sich Kunden über den Support?
2. Warum dauern Antworten zu lange?
3. Warum ist das Team überlastet?
...

**How-Might-We-Fragen:**
- Wie könnten wir Antwortzeiten verkürzen?
- Wie könnten wir Self-Service-Optionen verbessern?
...

## 🚀 Deployment

### Lokale Produktion
```bash
# Mit Gunicorn
pip install gunicorn
gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Docker (optional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🤝 Contributing

1. Fork das Repository
2. Feature-Branch erstellen (`git checkout -b feature/amazing-feature`)
3. Changes committen (`git commit -m 'Add amazing feature'`)
4. Branch pushen (`git push origin feature/amazing-feature`)
5. Pull Request erstellen

## 📄 License

Dieses Projekt steht unter der MIT License - siehe [LICENSE](LICENSE) Datei für Details.

## 🆘 Support

Bei Fragen oder Problemen:
1. Prüfen Sie die [API-Dokumentation](http://localhost:8000/docs)
2. Checken Sie die Log-Dateien
3. Validieren Sie Ihre Umgebungsvariablen
4. Erstellen Sie ein GitHub Issue

---

**Made with ❤️ for systematic problem solving**