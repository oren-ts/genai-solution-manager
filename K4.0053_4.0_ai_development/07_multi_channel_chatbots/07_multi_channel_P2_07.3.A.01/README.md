# Multi-Channel Chatbot: Weather & Appointment Bot

A production-ready multi-channel chatbot accessible via **Telegram** and **Web Browser**, demonstrating clean architecture, code reuse, and modern web development practices.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Lessons Learned](#lessons-learned)
- [Future Enhancements](#future-enhancements)
- [License](#license)

---

## 🎯 Overview

This project implements a **multi-channel chatbot** that provides weather information and appointment booking through two distinct interfaces:

1. **Telegram Bot** - Conversational interface using Telegram Bot API
2. **Web Application** - Modern, AJAX-powered web interface using Flask

Both channels share the same business logic, demonstrating **separation of concerns** and **code reusability** principles.

---

## ✨ Features

### Core Functionality
- 🌤 **Real-time Weather Information**
  - Fetches current weather data from OpenWeatherMap API
  - Supports any city worldwide
  - Returns temperature (°C) and weather conditions
  - Handles invalid city names gracefully

- 📅 **Appointment Booking**
  - Accepts date and time input
  - Provides instant confirmation
  - Validates input format

### Technical Features
- ✅ **Multi-channel architecture** - Same logic, different interfaces
- ✅ **AJAX-powered web UI** - No page reloads, instant responses
- ✅ **Comprehensive error handling** - User-friendly error messages
- ✅ **Input validation** - Prevents invalid API calls
- ✅ **Environment-based configuration** - Secure API key management
- ✅ **Clean code architecture** - Separation of concerns

---

## 🏗 Architecture

### Design Pattern: Multi-Channel Architecture
```
┌─────────────────────────────────────────────┐
│         Business Logic Layer                │
│     (business_logic.py)                     │
│  - get_weather(city)                        │
│  - confirm_appointment(date, time)          │
└─────────────────┬───────────────────────────┘
                  │
         ┌────────┴────────┐
         │                 │
┌────────▼────────┐ ┌─────▼──────────┐
│  Telegram Bot   │ │   Web App      │
│ (telegram_bot.py│ │ (web_app.py)   │
│                 │ │                │
│ - /weather cmd  │ │ - /weather API │
│ - /appointment  │ │ - /appointment │
└─────────────────┘ └────────────────┘
```

### Key Principles

1. **Separation of Concerns**
   - Business logic isolated from channel-specific code
   - Easy to add new channels (Discord, Slack, etc.)

2. **DRY (Don't Repeat Yourself)**
   - Single source of truth for weather/appointment logic
   - Consistent behavior across all channels

3. **Error Handling**
   - Validation at business logic layer
   - User-friendly error messages
   - Graceful degradation for API failures

---

## 🛠 Tech Stack

### Backend
- **Python 3.8+** - Core language
- **Flask 3.0+** - Web framework
- **python-telegram-bot** - Telegram Bot API wrapper
- **requests** - HTTP library for API calls
- **python-dotenv** - Environment variable management

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with gradients and animations
- **JavaScript (ES6+)** - AJAX, async/await, Fetch API

### External APIs
- **OpenWeatherMap API** - Real-time weather data
- **Telegram Bot API** - Telegram messaging platform

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/multi-channel-chatbot.git
cd multi-channel-chatbot
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Create `requirements.txt`
If not included, create with:
```txt
Flask==3.0.0
python-telegram-bot==20.7
requests==2.31.0
python-dotenv==1.0.0
```

---

## ⚙️ Configuration

### Step 1: Get API Keys

#### OpenWeatherMap API Key
1. Go to [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for free account
3. Generate API key (free tier: 1000 calls/day)

#### Telegram Bot Token
1. Open Telegram, search for `@BotFather`
2. Send `/newbot` command
3. Follow prompts to create bot
4. Copy the token provided

### Step 2: Configure Environment Variables

Create `.env` file in project root:
```env
# OpenWeatherMap API Configuration
OPENWEATHER_API_KEY=your_openweather_api_key_here

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
```

⚠️ **Security Note:** Never commit `.env` to version control. The `.gitignore` file prevents this.

---

## 🚀 Usage

### Running the Telegram Bot
```bash
python telegram_bot.py
```

**Available Commands:**
- `/start` - Welcome message and help
- `/weather [city]` - Get weather for a city
  - Example: `/weather Berlin`
  - Example: `/weather New York`
- `/appointment [date] [time]` - Book appointment
  - Example: `/appointment 2024-03-15 14:00`

### Running the Web Application
```bash
python web_app.py
```

Open browser: `http://127.0.0.1:5000`

**Features:**
- Weather inquiry form
- Appointment booking form
- Real-time AJAX responses (no page reload)
- Color-coded responses (green = success, red = error)

---

## 📁 Project Structure
```
multi-channel-chatbot/
│
├── business_logic.py          # Core business logic (shared)
├── telegram_bot.py            # Telegram channel implementation
├── web_app.py                 # Flask web channel implementation
│
├── templates/
│   └── index.html             # Web UI template
│
├── .env                       # Environment variables (NOT in git)
├── .env.example               # Environment template (safe to commit)
├── .gitignore                 # Git ignore rules
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

---

## 📡 API Documentation

### Business Logic API

#### `get_weather(city: str) -> str`

Fetches current weather for a given city.

**Parameters:**
- `city` (str): City name (e.g., "Berlin", "New York")

**Returns:**
- `str`: Formatted weather message or error message

**Example:**
```python
>>> get_weather("Berlin")
"🌤 Weather in Berlin: 15.0°C, Clear sky"

>>> get_weather("")
"❌ Please provide a city name."
```

#### `confirm_appointment(date: str, time: str) -> str`

Creates a fictitious appointment confirmation.

**Parameters:**
- `date` (str): Appointment date (e.g., "2024-03-15")
- `time` (str): Appointment time (e.g., "14:00")

**Returns:**
- `str`: Confirmation message or error message

**Example:**
```python
>>> confirm_appointment("2024-03-15", "14:00")
"✅ Appointment confirmed for 2024-03-15 at 14:00."
```

### Web API Endpoints

#### `POST /weather`

**Request Body:**
```json
{
  "city": "Berlin"
}
```

**Response:**
```json
{
  "response": "🌤 Weather in Berlin: 15.0°C, Clear sky"
}
```

#### `POST /appointment`

**Request Body:**
```json
{
  "date": "2024-03-15",
  "time": "14:00"
}
```

**Response:**
```json
{
  "response": "✅ Appointment confirmed for 2024-03-15 at 14:00."
}
```

---

## 🧪 Testing

### Manual Testing Checklist

**Telegram Bot:**
- [ ] `/start` command shows welcome message
- [ ] `/weather Berlin` returns weather data
- [ ] `/weather` (empty) shows error
- [ ] `/weather InvalidCity123` shows "not found" error
- [ ] `/appointment 2024-03-15 14:00` shows confirmation
- [ ] `/appointment` (empty) shows error

**Web Application:**
- [ ] Weather form with valid city returns data
- [ ] Weather form with empty city shows error
- [ ] Appointment form with valid date/time shows confirmation
- [ ] Appointment form with missing date shows error
- [ ] No page reload on form submission (AJAX working)
- [ ] Responses styled correctly (green/red)

---

## 💡 Lessons Learned

### Technical Skills Developed

1. **Multi-Channel Architecture**
   - Learned to separate business logic from interface logic
   - Understood benefits of code reusability across channels

2. **API Integration**
   - Integrated external REST API (OpenWeatherMap)
   - Handled API errors gracefully

3. **Asynchronous Web Development**
   - Implemented AJAX for better user experience
   - Used modern JavaScript (async/await, Fetch API)

4. **Security Best Practices**
   - Managed sensitive data with environment variables
   - Prevented accidental exposure of API keys

### Design Patterns Applied

- **Separation of Concerns**: Business logic separate from presentation
- **DRY Principle**: Shared code across multiple channels
- **Error Handling**: Comprehensive validation at multiple layers
- **Configuration Management**: Environment-based configuration

---

## 🚀 Future Enhancements

### Planned Features
- [ ] **Weather Forecasts**: 5-day weather predictions
- [ ] **Location Detection**: Auto-detect user location
- [ ] **Appointment Storage**: Persist appointments in database
- [ ] **User Authentication**: Secure user accounts
- [ ] **Additional Channels**: Discord bot, Slack integration
- [ ] **Unit Tests**: Comprehensive test coverage
- [ ] **Deployment**: Docker containerization, cloud deployment

### Scalability Improvements
- [ ] Redis for session management
- [ ] Rate limiting for API calls
- [ ] Caching for frequently requested cities
- [ ] Database for appointment persistence
- [ ] Logging and monitoring

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your Name](https://linkedin.com/in/yourname)
- Portfolio: [yourwebsite.com](https://yourwebsite.com)

---

## 🙏 Acknowledgments

- [OpenWeatherMap](https://openweathermap.org/) for weather API
- [Telegram](https://telegram.org/) for Bot API
- Course: K4.0053_4.0 AI Development