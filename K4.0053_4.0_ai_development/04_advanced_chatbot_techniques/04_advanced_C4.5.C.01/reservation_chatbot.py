"""
Restaurant Reservation Chatbot
Exercise 04.5.C.01 - Advanced Chatbot Techniques

TARGET TEST CONVERSATIONS - See end of file for test scenarios
"""

import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum

# Try to import dateutil for advanced date parsing
try:
    from dateutil import parser as date_parser
    DATEUTIL_AVAILABLE = True
except ImportError:
    DATEUTIL_AVAILABLE = False
    print("Note: python-dateutil not available. Using basic date parsing.")


class ConversationState(Enum):
    """Conversation states for the reservation flow"""
    IDLE = "idle"
    AWAITING_DATE = "awaiting_date"
    AWAITING_TIME = "awaiting_time"
    AWAITING_PEOPLE = "awaiting_people"
    READY_TO_CONFIRM = "ready_to_confirm"
    CONFIRMED = "confirmed"


class ConversationContext:
    """Manages conversation state and collected entities for a single user session"""
    
    def __init__(self):
        """Initialize empty context"""
        self.state = ConversationState.IDLE
        self.entities = {
            "date": None,
            "time": None,
            "people": None
        }
        self.history = []
        self.last_activity = datetime.now()
    
    def update_activity(self):
        """Update last activity timestamp"""
        self.last_activity = datetime.now()
    
    def is_expired(self, timeout_minutes=30):
        """Check if context has expired"""
        if timeout_minutes is None:
            return False
        return datetime.now() - self.last_activity > timedelta(minutes=timeout_minutes)
    
    def reset(self):
        """Reset context to initial state"""
        self.state = ConversationState.IDLE
        self.entities = {"date": None, "time": None, "people": None}
        self.history = []
        self.last_activity = datetime.now()
    
    def has_all_entities(self):
        """Check if all required entities are collected"""
        return all(v is not None for v in self.entities.values())
    
    def get_missing_entities(self):
        """Get list of missing entity names"""
        return [k for k, v in self.entities.items() if v is None]


class ReservationChatbot:
    """AI-based chatbot for restaurant table reservations"""
    
    def __init__(self):
        """Initialize the chatbot with empty context storage"""
        self.contexts = {}  # session_id -> ConversationContext
        self.reservations = []  # List of confirmed reservations
        self.session_timeout_minutes = None  # Disabled for demo
        
        # Intent keywords for pattern matching
        self.intent_keywords = {
            "cancel": ["cancel", "nevermind", "stop", "forget it"],
            "confirm": ["yes", "correct", "confirm", "that's right", "yep", "yeah"],
            "greeting": ["hi", "hello", "hey", "greetings"],
            "opening_hours": ["hours", "open", "when are you open", "opening hours"],
            "make_reservation": ["reservation", "table", "book", "reserve", "want"],
        }
    
    def recognize_intent(self, text: str, context=None) -> str:
        """
        Phase 1: Implement basic intent recognition
        
        Args:
            text: User input text
            context: Optional conversation context for context-aware recognition
            
        Returns:
            Intent label as string
        """
        # Normalize input
        text_lower = text.lower().strip()
        
        # Priority 1: Cancel intent (highest priority)
        for keyword in self.intent_keywords["cancel"]:
            if keyword in text_lower:
                return "cancel"
        
        # Priority 2: Confirm intent (context-dependent)
        for keyword in self.intent_keywords["confirm"]:
            if keyword in text_lower:
                # Only treat as confirm if we're in confirmation state
                if context and hasattr(context, 'state'):
                    if context.state == ConversationState.READY_TO_CONFIRM:
                        return "confirm"
                # Otherwise might just be conversational
        
        # Priority 3: Greeting
        for keyword in self.intent_keywords["greeting"]:
            if keyword in text_lower:
                return "greeting"
        
        # Priority 4: Opening hours query
        for keyword in self.intent_keywords["opening_hours"]:
            if keyword in text_lower:
                return "opening_hours"
        
        # Priority 5: Make reservation
        for keyword in self.intent_keywords["make_reservation"]:
            if keyword in text_lower:
                return "make_reservation"
        
        # If we're in the middle of a conversation, assume they're providing info
        if context and hasattr(context, 'state'):
            if context.state in [ConversationState.AWAITING_DATE, 
                                ConversationState.AWAITING_TIME, 
                                ConversationState.AWAITING_PEOPLE]:
                return "provide_information"
        
        # Fallback
        return "unknown"
    
    def extract_people_count(self, text: str) -> Optional[int]:
        """
        Phase 2: Extract number of people from user input
        
        Args:
            text: User input text
            
        Returns:
            Number of people (1-20) or None if not found/invalid
        """
        text_lower = text.lower().strip()
        
        # Pattern 1: "4 people", "6 guests", "8 persons"
        pattern1 = r'(\d+)\s*(?:people|guests|persons|ppl)'
        match = re.search(pattern1, text_lower)
        if match:
            count = int(match.group(1))
            if 1 <= count <= 20:
                return count
        
        # Pattern 2: "party of 6", "group of 4"
        pattern2 = r'(?:party|group)\s*of\s*(\d+)'
        match = re.search(pattern2, text_lower)
        if match:
            count = int(match.group(1))
            if 1 <= count <= 20:
                return count
        
        # Pattern 3: "table for 5"
        pattern3 = r'table\s*for\s*(\d+)'
        match = re.search(pattern3, text_lower)
        if match:
            count = int(match.group(1))
            if 1 <= count <= 20:
                return count
        
        # Pattern 4: Just a standalone number (risky, use carefully)
        # Only if the text is mostly just a number
        pattern4 = r'\b(\d+)\b'
        matches = re.findall(pattern4, text_lower)
        if len(matches) == 1:  # Only one number in the text
            count = int(matches[0])
            if 1 <= count <= 20:
                return count
        
        return None
    
    def extract_date(self, text: str) -> Optional[datetime]:
        """
        Phase 3: Extract date from user input
        
        Args:
            text: User input text
            
        Returns:
            datetime object or None if not found/invalid
        """
        text_lower = text.lower().strip()
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Pattern 1: "today"
        if "today" in text_lower:
            return today
        
        # Pattern 2: "tomorrow"
        if "tomorrow" in text_lower:
            return today + timedelta(days=1)
        
        # Pattern 3: Day of week (e.g., "friday", "next friday")
        weekdays = {
            "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3,
            "friday": 4, "saturday": 5, "sunday": 6
        }
        
        for day_name, day_num in weekdays.items():
            if day_name in text_lower:
                current_weekday = today.weekday()
                days_ahead = day_num - current_weekday
                
                # If the day has already passed this week, go to next week
                if days_ahead <= 0:
                    days_ahead += 7
                
                # If "next" is mentioned, add another week
                if "next" in text_lower:
                    days_ahead += 7
                
                return today + timedelta(days=days_ahead)
        
        # Pattern 4: Try dateutil if available
        if DATEUTIL_AVAILABLE:
            try:
                parsed_date = date_parser.parse(text, fuzzy=True, default=today)
                # Only accept if it's a reasonable date
                if parsed_date.date() >= today.date():
                    if parsed_date.date() <= (today + timedelta(days=90)).date():
                        return parsed_date.replace(hour=0, minute=0, second=0, microsecond=0)
            except:
                pass
        
        return None
    
    def extract_time(self, text: str) -> Optional[str]:
        """
        Phase 4: Extract time from user input
        
        Args:
            text: User input text
            
        Returns:
            Time string in HH:MM format (24-hour) or None if not found/invalid
        """
        text_lower = text.lower().strip()
        
        # Opening hours: 11 AM - 10 PM (11:00 - 22:00)
        MIN_HOUR = 11
        MAX_HOUR = 22
        
        # Pattern 1: "7pm", "7:30pm", "7:30 pm"
        pattern1 = r'(\d{1,2})(?::(\d{2}))?\s*(am|pm)'
        match = re.search(pattern1, text_lower)
        if match:
            hour = int(match.group(1))
            minute = int(match.group(2)) if match.group(2) else 0
            period = match.group(3)
            
            # Convert to 24-hour format
            if period == 'pm' and hour != 12:
                hour += 12
            elif period == 'am' and hour == 12:
                hour = 0
            
            # Validate within opening hours
            if MIN_HOUR <= hour <= MAX_HOUR:
                return f"{hour:02d}:{minute:02d}"
        
        # Pattern 2: "19:00", "19:30" (24-hour format)
        pattern2 = r'\b(\d{1,2}):(\d{2})\b'
        match = re.search(pattern2, text_lower)
        if match:
            hour = int(match.group(1))
            minute = int(match.group(2))
            
            if MIN_HOUR <= hour <= MAX_HOUR and 0 <= minute < 60:
                return f"{hour:02d}:{minute:02d}"
        
        # Pattern 3: Just a number "7", "8", "10"
        pattern3 = r'\b(\d{1,2})\b'
        matches = re.findall(pattern3, text_lower)
        if len(matches) == 1:  # Only one number
            hour = int(matches[0])
            
            # Ambiguity handling
            if hour == 11:
                # 11 PM is outside hours, must be 11 AM
                return "11:00"
            elif hour == 10:
                # Default to 10 PM (dinner time, last seating)
                return "22:00"
            elif 1 <= hour <= 9:
                # Default to PM for dinner reservations
                hour += 12
                if MIN_HOUR <= hour <= MAX_HOUR:
                    return f"{hour:02d}:00"
            elif 12 <= hour <= MAX_HOUR:
                return f"{hour:02d}:00"
        
        return None
    
    def handle_message(self, user_input: str, session_id: str) -> str:
        """
        Phase 5: Main message handling with state machine
        
        Args:
            user_input: User's message
            session_id: Unique session identifier
            
        Returns:
            Bot's response message
        """
        # Get or create context
        if session_id not in self.contexts:
            self.contexts[session_id] = ConversationContext()
        
        context = self.contexts[session_id]
        context.update_activity()
        context.history.append(user_input)
        
        # Recognize intent
        intent = self.recognize_intent(user_input, context)
        
        # Handle cancel intent
        if intent == "cancel":
            context.reset()
            return "No problem! Your reservation has been cancelled. Let me know if you'd like to make a new one."
        
        # Handle greeting
        if intent == "greeting":
            return "Hello! Welcome to our restaurant. Would you like to make a reservation?"
        
        # Handle opening hours query
        if intent == "opening_hours":
            return "We're open daily from 11:00 AM to 10:00 PM. Would you like to make a reservation?"
        
        # Handle confirmation
        if intent == "confirm" and context.state == ConversationState.READY_TO_CONFIRM:
            return self._create_reservation(context, session_id)
        
        # Handle reservation request or providing information
        if intent in ["make_reservation", "provide_information"]:
            # Extract all entities from input
            extracted_entities = self._extract_all_entities(user_input)
            
            # Update context with new entities
            for entity_type, value in extracted_entities.items():
                if value is not None:
                    context.entities[entity_type] = value
            
            # Determine next state
            context.state = self._determine_next_state(context)
            
            # Generate appropriate response
            return self._generate_response(context)
        
        # Unknown intent
        return "I'm sorry, I didn't understand that. You can make a reservation or ask about our opening hours."
    
    def _extract_all_entities(self, text: str) -> Dict[str, any]:
        """Extract all entities from text"""
        return {
            "date": self.extract_date(text),
            "time": self.extract_time(text),
            "people": self.extract_people_count(text)
        }
    
    def _determine_next_state(self, context: ConversationContext) -> ConversationState:
        """
        Determine next state based on collected entities
        Data-driven: only advance when we actually have the data
        """
        if context.entities["date"] is None:
            return ConversationState.AWAITING_DATE
        elif context.entities["time"] is None:
            return ConversationState.AWAITING_TIME
        elif context.entities["people"] is None:
            return ConversationState.AWAITING_PEOPLE
        else:
            # All entities collected
            return ConversationState.READY_TO_CONFIRM
    
    def _generate_response(self, context: ConversationContext) -> str:
        """Generate response based on current state"""
        if context.state == ConversationState.AWAITING_DATE:
            return "Great! What date would you like to reserve? (e.g., tomorrow, Friday, Feb 14)"
        
        elif context.state == ConversationState.AWAITING_TIME:
            # Acknowledge what we have
            date_str = context.entities["date"].strftime("%B %d") if context.entities["date"] else ""
            if context.entities["people"]:
                return f"Perfect! What time works for you? We're open from 11 AM to 10 PM."
            else:
                return "What time works for you? We're open from 11 AM to 10 PM."
        
        elif context.state == ConversationState.AWAITING_PEOPLE:
            return "Excellent! How many people will be dining?"
        
        elif context.state == ConversationState.READY_TO_CONFIRM:
            # Format confirmation message
            date = context.entities["date"]
            time = context.entities["time"]
            people = context.entities["people"]
            
            date_str = date.strftime("%B %d, %Y (%A)")
            
            return f"Let me confirm: Table for {people} on {date_str} at {time}. Is this correct?"
        
        return "I'm processing your request..."
    
    def _create_reservation(self, context: ConversationContext, session_id: str) -> str:
        """Create and confirm reservation"""
        import uuid
        
        # Create reservation ID
        reservation_id = str(uuid.uuid4())[:8].upper()
        
        # Store reservation
        reservation = {
            "id": reservation_id,
            "session_id": session_id,
            "date": context.entities["date"],
            "time": context.entities["time"],
            "people": context.entities["people"],
            "created_at": datetime.now()
        }
        self.reservations.append(reservation)
        
        # Format confirmation
        date_str = context.entities["date"].strftime("%B %d, %Y")
        time_str = context.entities["time"]
        people = context.entities["people"]
        
        # Reset context for next reservation
        context.reset()
        
        return (f"Perfect! Your table for {people} on {date_str} at {time_str} is confirmed. "
                f"Confirmation #{reservation_id}. See you then!")
    
    def reset_session(self, session_id: str) -> str:
        """Reset a user's session"""
        if session_id in self.contexts:
            self.contexts[session_id].reset()
        return "Conversation reset. How can I help you?"


# Interactive Chatbot
if __name__ == "__main__":
    chatbot = ReservationChatbot()
    
    print("=" * 60)
    print("🍽️  RESTAURANT RESERVATION CHATBOT")
    print("=" * 60)
    print("\nWelcome! I can help you make a table reservation.")
    print("Commands: 'quit' to exit, 'reset' to start over\n")
    print("=" * 60)
    
    # Get session ID
    session_id = input("\nWhat's your name? ").strip().lower()
    if not session_id:
        session_id = "guest"
    
    print(f"\nHello {session_id.title()}! How can I help you today?\n")
    
    # Main conversation loop
    while True:
        try:
            user_input = input(f"{session_id.title()}: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == 'quit':
                print("\nThank you for using our reservation system. Goodbye!")
                break
            
            if user_input.lower() == 'reset':
                response = chatbot.reset_session(session_id)
                print(f"Bot: {response}\n")
                continue
            
            # Process message and get response
            response = chatbot.handle_message(user_input, session_id)
            print(f"Bot: {response}\n")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}\n")
    
    # Show all reservations made
    if chatbot.reservations:
        print("\n" + "=" * 60)
        print("CONFIRMED RESERVATIONS")
        print("=" * 60)
        for res in chatbot.reservations:
            date_str = res["date"].strftime("%B %d, %Y")
            print(f"#{res['id']}: {res['people']} people on {date_str} at {res['time']}")
        print("=" * 60)


"""
TARGET TEST CONVERSATIONS
========================
These are the gold standard conversations the chatbot should handle by the end.

=== Scenario 1: Complete Happy Path ===
User: "Hi"
Bot: "Hello! Welcome to our restaurant. Would you like to make a reservation?"
User: "Yes, I need a table"
Bot: "Great! What date would you like to reserve?"
User: "Tomorrow"
Bot: "Perfect! What time works for you? We're open from 11 AM to 10 PM."
User: "7pm"
Bot: "Excellent! How many people will be dining?"
User: "4 people"
Bot: "Let me confirm: Table for 4 on February 12, 2026 at 7:00 PM. Is this correct?"
User: "Yes"
Bot: "Perfect! Your table for 4 on February 12, 2026 at 7:00 PM is confirmed. 
      Confirmation #12345. See you then!"

=== Scenario 2: All Info at Once (Skip-Ahead) ===
User: "I want a table for 6 people tomorrow at 8pm"
Bot: "Let me confirm: Table for 6 on February 12, 2026 at 8:00 PM. Is this correct?"
User: "Yes"
Bot: "Perfect! Your table for 6 on February 12, 2026 at 8:00 PM is confirmed.
      Confirmation #12346. See you then!"

=== Scenario 3: Partial Info + Modification ===
User: "I need a reservation for Friday"
Bot: "Great! What time works for you? We're open from 11 AM to 10 PM."
User: "7:30pm"
Bot: "Excellent! How many people will be dining?"
User: "Actually, make it 8pm instead"
Bot: "Updated to 8:00 PM. How many people will be dining?"
User: "5"
Bot: "Let me confirm: Table for 5 on February 14, 2026 at 8:00 PM. Is this correct?"
User: "Yes"
Bot: "Perfect! Your table for 5 on February 14, 2026 at 8:00 PM is confirmed.
      Confirmation #12347. See you then!"

=== Scenario 4: Cancellation ===
User: "I want to make a reservation"
Bot: "Great! What date would you like to reserve?"
User: "Actually, nevermind"
Bot: "No problem! Your reservation has been cancelled. Let me know if you'd like to make a new one."

=== Scenario 5: Opening Hours Query ===
User: "What are your opening hours?"
Bot: "We're open daily from 11:00 AM to 10:00 PM. Would you like to make a reservation?"

=== Scenario 6: Error Handling - Invalid Date ===
User: "I want a table"
Bot: "Great! What date would you like to reserve?"
User: "Yesterday"
Bot: "I'm sorry, but I can't make reservations for dates in the past. 
      Please choose today or a future date."
User: "Tomorrow"
Bot: "Perfect! What time works for you? We're open from 11 AM to 10 PM."

=== Scenario 7: Error Handling - Invalid Time ===
User: "I need a table tomorrow"
Bot: "Great! What time works for you? We're open from 11 AM to 10 PM."
User: "6am"
Bot: "I'm sorry, but we're only open from 11:00 AM to 10:00 PM. 
      Please choose a time within our opening hours."
User: "6pm"
Bot: "Excellent! How many people will be dining?"
"""
