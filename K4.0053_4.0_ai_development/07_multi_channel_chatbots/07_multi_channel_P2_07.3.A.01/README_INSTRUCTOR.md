# Exercise 07.3.A.01 - Multi-Channel Chatbot

## 📋 Exercise Requirements

Develop a multi-channel chatbot accessible via Telegram and web application that provides:
- Weather information using OpenWeatherMap API
- Appointment booking confirmations

---

## ✅ Implementation Summary

### a) Telegram Bot
- ✅ Implemented using Telegram Bot API
- ✅ `/weather [city]` command fetches real weather data
- ✅ `/appointment [date] [time]` command provides fictitious confirmation
- ✅ Proper error handling for invalid inputs

### b) Web Application
- ✅ Built with Flask framework
- ✅ Forms for weather inquiries and appointment booking
- ✅ AJAX implementation for asynchronous processing
- ✅ No page reload on form submission
- ✅ Color-coded response display (green/red)

---

## 🏗 Architecture

**Multi-Channel Design:**
```
business_logic.py (shared logic)
    ↑           ↑
telegram_bot.py  web_app.py
```

**Key Design Decisions:**
- Separated business logic from channel-specific code
- Enabled code reuse across both channels
- Single source of truth for weather/appointment functionality

---

## 🛠 Technologies Used

- **Python 3.8+**
- **Flask** - Web framework
- **python-telegram-bot** - Telegram integration
- **OpenWeatherMap API** - Weather data
- **AJAX** - Asynchronous web requests
- **python-dotenv** - Environment variable management

---

## 📦 Installation & Setup

### Prerequisites
```bash
pip install Flask python-telegram-bot requests python-dotenv
```

### Configuration
Create `.env` file with:
```env
OPENWEATHER_API_KEY=your_api_key
TELEGRAM_BOT_TOKEN=your_bot_token
```

### Running the Application

**Telegram Bot:**
```bash
python telegram_bot.py
```

**Web Application:**
```bash
python web_app.py
# Open: http://127.0.0.1:5000
```

---

## 📁 Project Structure
```
exercise_07_3_a_01/
├── business_logic.py          # Core functions (shared)
├── telegram_bot.py            # Telegram channel
├── web_app.py                 # Web channel
├── templates/
│   └── index.html             # Web UI
├── .env                       # API keys (not committed)
├── .env.example               # Template
└── README.md                  # Documentation
```

---

## 🧪 Testing Results

### Telegram Bot Tests
✅ `/start` - Welcome message displayed  
✅ `/weather Berlin` - Returns: "Weather in Berlin: 0.03°C, Broken clouds"  
✅ `/weather` - Returns: "Please provide a city name"  
✅ `/weather InvalidCity` - Returns: "City not found"  
✅ `/appointment 2024-03-15 14:00` - Returns: "Appointment confirmed"  
✅ `/appointment` - Returns: "Please provide a date"  

### Web Application Tests
✅ Weather form (valid city) - Displays weather data  
✅ Weather form (empty) - Shows error message  
✅ Appointment form (valid) - Shows confirmation  
✅ Appointment form (partial) - Shows validation errors  
✅ AJAX functionality - No page reload confirmed  
✅ Response styling - Green for success, red for errors