# Restaurant Reservation Chatbot

AI-based chatbot for restaurant table reservations built with Python.

## Features

- 🤖 Natural language understanding (intent recognition + entity extraction)
- 💬 Multi-turn conversations with context management
- 📅 Flexible date parsing (today, tomorrow, weekdays)
- ⏰ Time extraction with ambiguity handling
- 👥 Party size validation (1-20 people)
- ✅ Reservation confirmation with unique IDs
- 🔄 Skip-ahead capability (provide all info at once)
- ♻️ Modification support (change details mid-conversation)

## Requirements

- Python 3.7+
- Optional: `python-dateutil` (falls back to basic parsing if not available)

## Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd reservation_chatbot

# Optional: Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
python3 reservation_chatbot.py
```

### Example Conversation

```
What's your name? Alice

Alice: I want a table for 4 people tomorrow at 7pm
Bot: Let me confirm: Table for 4 on February 12, 2026 (Thursday) at 19:00. Is this correct?

Alice: yes
Bot: Perfect! Your table for 4 on February 12, 2026 at 19:00 is confirmed. 
     Confirmation #A3B8D1B6. See you then!
```

## Architecture

- **Intent Recognition**: Keyword-based pattern matching with priority ordering
- **Entity Extraction**: Regex patterns for date, time, and people count
- **State Machine**: 6 states managing conversation flow
- **Context Management**: Session-based context for multi-user support

## Implementation

Built following an incremental development approach:
1. Phase 1: Intent recognition
2. Phase 2: Entity extraction (people count)
3. Phase 3: Entity extraction (date)
4. Phase 4: Entity extraction (time)
5. Phase 5: State machine and context management

## Exercise

This project was created for Exercise 04.5.C.01 - Advanced Chatbot Techniques.

## License

MIT
