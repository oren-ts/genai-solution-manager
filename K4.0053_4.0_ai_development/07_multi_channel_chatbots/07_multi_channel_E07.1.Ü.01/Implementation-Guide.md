# Multi-Channel Chatbot - Implementation Guide

**Exercise:** 07.1.Ü.01  
**Purpose:** Translate architectural concepts into practical code structure

---

## Overview

This guide shows how the three-layer architecture translates into actual Python code structure. While this is not a complete implementation, it demonstrates:
- Directory organization
- Key classes and interfaces
- Data flow between layers
- Best practices for maintainability

---

## Project Structure

```
cafe-chatbot/
│
├── src/
│   ├── platform_layer/          # Platform-specific adapters
│   │   ├── __init__.py
│   │   ├── base_adapter.py      # Abstract base for all adapters
│   │   ├── whatsapp_adapter.py
│   │   ├── telegram_adapter.py
│   │   └── website_adapter.py
│   │
│   ├── translation_layer/       # Normalization & rendering
│   │   ├── __init__.py
│   │   ├── inbound_translator.py
│   │   ├── outbound_translator.py
│   │   ├── identity_resolver.py
│   │   └── renderers/           # Channel-specific renderers
│   │       ├── __init__.py
│   │       ├── whatsapp_renderer.py
│   │       ├── telegram_renderer.py
│   │       └── website_renderer.py
│   │
│   ├── business_logic/          # Core chatbot logic
│   │   ├── __init__.py
│   │   ├── intent_router.py
│   │   ├── dialog_manager.py
│   │   ├── state_machine.py
│   │   └── services/            # Domain services
│   │       ├── __init__.py
│   │       ├── opening_hours_service.py
│   │       ├── menu_service.py
│   │       └── reservation_service.py
│   │
│   ├── infrastructure/          # Shared infrastructure
│   │   ├── __init__.py
│   │   ├── session_store.py
│   │   ├── user_service.py
│   │   └── database/
│   │       ├── __init__.py
│   │       ├── menu_repository.py
│   │       └── reservation_repository.py
│   │
│   └── models/                  # Shared data models
│       ├── __init__.py
│       ├── request.py           # NormalizedRequest
│       ├── response.py          # NormalizedResponse
│       ├── session.py           # ConversationSession
│       └── user.py              # User, Identity
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── config/
│   ├── development.yaml
│   ├── production.yaml
│   └── channels/                # Per-channel configuration
│       ├── whatsapp.yaml
│       ├── telegram.yaml
│       └── website.yaml
│
├── requirements.txt
├── docker-compose.yml           # Redis, PostgreSQL, etc.
└── README.md
```

---

## Core Data Models

### 1. Normalized Request (models/request.py)

```python
from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime

@dataclass
class NormalizedRequest:
    """Platform-agnostic request format."""
    
    # Identity
    global_user_id: str
    channel: str  # "whatsapp" | "telegram" | "website"
    channel_user_id: str
    
    # Content
    text: Optional[str] = None
    structured_event: Optional[Dict[str, Any]] = None  # Button clicks, form submits
    
    # Metadata
    locale: str = "en_US"
    timezone: str = "UTC"
    timestamp: datetime = None
    
    # Context
    conversation_state: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()
```

### 2. Normalized Response (models/response.py)

```python
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from enum import Enum

class ResponseType(Enum):
    TEXT = "text"
    MENU = "menu"
    SLOT_REQUEST = "slot_request"
    CONFIRMATION = "confirmation"
    ERROR = "error"

@dataclass
class PresentationHints:
    """Recommendations for how to present the response."""
    preferred_presentation: Optional[str] = None  # "paginate", "summary", "full"
    preview_items: Optional[int] = None
    group_by: Optional[str] = None
    allow_inline_editing: bool = False
    urgency: Optional[str] = None  # "low", "medium", "high"

@dataclass
class RecoveryOptions:
    """Error recovery alternatives."""
    alternatives: List[Dict[str, Any]] = field(default_factory=list)
    escalation: List[str] = field(default_factory=list)  # ["call_cafe", "leave_phone"]

@dataclass
class NormalizedResponse:
    """Platform-agnostic response format."""
    
    type: ResponseType
    payload: Dict[str, Any]
    
    # Optional metadata
    presentation_hints: Optional[PresentationHints] = None
    recovery_options: Optional[RecoveryOptions] = None
    
    # Session updates
    update_session: Optional[Dict[str, Any]] = None
```

### 3. Conversation Session (models/session.py)

```python
from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from datetime import datetime
from enum import Enum

class DialogState(Enum):
    START = "start"
    COLLECTING = "collecting"
    CONFIRMING = "confirming"
    BOOKED = "booked"
    FINISHED = "finished"

@dataclass
class ConversationSession:
    """Tracks conversation state for a user."""
    
    global_user_id: str
    current_intent: Optional[str] = None
    dialog_state: DialogState = DialogState.START
    
    # Slot filling
    slots: Dict[str, Any] = field(default_factory=dict)
    required_slots: List[str] = field(default_factory=list)
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_updated_at: datetime = field(default_factory=datetime.utcnow)
    locale: str = "en_US"
    timezone: str = "UTC"
    
    # Context
    context: Dict[str, Any] = field(default_factory=dict)
    
    def is_expired(self, timeout_seconds: int = 1200) -> bool:
        """Check if session has timed out (default: 20 minutes)."""
        elapsed = (datetime.utcnow() - self.last_updated_at).total_seconds()
        return elapsed > timeout_seconds
    
    def missing_slots(self) -> List[str]:
        """Get list of required slots that aren't filled yet."""
        return [slot for slot in self.required_slots if slot not in self.slots]
```

---

## Platform Layer Implementation

### Base Adapter (platform_layer/base_adapter.py)

```python
from abc import ABC, abstractmethod
from typing import Dict, Any

class BasePlatformAdapter(ABC):
    """Abstract base class for all platform adapters."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.channel_name = self.__class__.__name__.replace('Adapter', '').lower()
    
    @abstractmethod
    async def receive_event(self) -> Dict[str, Any]:
        """
        Receive an event from the platform.
        
        Returns:
            Raw platform event (webhook payload, poll result, etc.)
        """
        pass
    
    @abstractmethod
    async def send_message(self, channel_user_id: str, payload: Dict[str, Any]) -> bool:
        """
        Send a message via the platform.
        
        Args:
            channel_user_id: Platform-specific user identifier
            payload: Platform-specific message payload
            
        Returns:
            Success status
        """
        pass
    
    @abstractmethod
    def verify_webhook(self, request_data: Dict[str, Any]) -> bool:
        """
        Verify webhook authenticity (signature, token, etc.)
        
        Args:
            request_data: Incoming webhook request
            
        Returns:
            True if authentic
        """
        pass
```

### WhatsApp Adapter (platform_layer/whatsapp_adapter.py)

```python
import hmac
import hashlib
from typing import Dict, Any
import aiohttp

class WhatsAppAdapter(BasePlatformAdapter):
    """WhatsApp Business API adapter."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_url = config['api_url']
        self.access_token = config['access_token']
        self.verify_token = config['verify_token']
        self.app_secret = config['app_secret']
    
    async def receive_event(self) -> Dict[str, Any]:
        """
        Receive WhatsApp webhook event.
        Called by web framework (FastAPI, Flask) when webhook is hit.
        """
        # In practice, this is called from your web framework
        # Here we just show the structure
        pass
    
    async def send_message(
        self, 
        channel_user_id: str,  # Phone number
        payload: Dict[str, Any]
    ) -> bool:
        """
        Send message via WhatsApp Business API.
        
        Example payload from translation layer:
        {
            "text": "Hello!",
            "quick_replies": ["Option 1", "Option 2"]  # Optional
        }
        """
        # Convert to WhatsApp API format
        whatsapp_payload = {
            "messaging_product": "whatsapp",
            "to": channel_user_id,
            "type": "text",
            "text": {
                "body": payload["text"]
            }
        }
        
        # Add interactive elements if present
        if "quick_replies" in payload:
            whatsapp_payload["type"] = "interactive"
            whatsapp_payload["interactive"] = {
                "type": "button",
                "body": {"text": payload["text"]},
                "action": {
                    "buttons": [
                        {"type": "reply", "reply": {"id": f"btn_{i}", "title": btn}}
                        for i, btn in enumerate(payload["quick_replies"][:3])  # Max 3
                    ]
                }
            }
        
        # Send via API
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.api_url}/messages",
                headers={
                    "Authorization": f"Bearer {self.access_token}",
                    "Content-Type": "application/json"
                },
                json=whatsapp_payload
            ) as response:
                return response.status == 200
    
    def verify_webhook(self, request_data: Dict[str, Any]) -> bool:
        """Verify WhatsApp webhook signature."""
        signature = request_data.get("signature", "")
        body = request_data.get("body", "")
        
        expected_signature = hmac.new(
            self.app_secret.encode(),
            body.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(signature, expected_signature)
    
    def extract_user_message(self, webhook_event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract user message from WhatsApp webhook event.
        
        Returns:
            {
                "channel_user_id": "+49123...",
                "text": "Hello",
                "button_payload": None  # or button ID if button clicked
            }
        """
        entry = webhook_event["entry"][0]
        changes = entry["changes"][0]
        value = changes["value"]
        
        if "messages" not in value:
            return None
        
        message = value["messages"][0]
        
        result = {
            "channel_user_id": message["from"],
            "text": None,
            "button_payload": None,
            "timestamp": message["timestamp"]
        }
        
        if message["type"] == "text":
            result["text"] = message["text"]["body"]
        elif message["type"] == "button":
            result["button_payload"] = message["button"]["payload"]
            result["text"] = message["button"]["text"]  # Button label
        
        return result
```

### Telegram Adapter (platform_layer/telegram_adapter.py)

```python
from typing import Dict, Any
import aiohttp

class TelegramAdapter(BasePlatformAdapter):
    """Telegram Bot API adapter."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.bot_token = config['bot_token']
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}"
    
    async def send_message(
        self,
        channel_user_id: str,  # Telegram chat_id
        payload: Dict[str, Any]
    ) -> bool:
        """
        Send message via Telegram Bot API.
        
        Example payload:
        {
            "text": "Choose a time:",
            "inline_keyboard": [
                [{"text": "18:00", "callback_data": "time_18"}],
                [{"text": "19:00", "callback_data": "time_19"}]
            ]
        }
        """
        telegram_payload = {
            "chat_id": channel_user_id,
            "text": payload["text"],
            "parse_mode": "Markdown"
        }
        
        # Add inline keyboard if present
        if "inline_keyboard" in payload:
            telegram_payload["reply_markup"] = {
                "inline_keyboard": payload["inline_keyboard"]
            }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.api_url}/sendMessage",
                json=telegram_payload
            ) as response:
                return response.status == 200
    
    def extract_user_message(self, update: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract message from Telegram update.
        
        Handles both regular messages and callback queries (button clicks).
        """
        result = {
            "channel_user_id": None,
            "text": None,
            "button_payload": None
        }
        
        # Regular message
        if "message" in update:
            message = update["message"]
            result["channel_user_id"] = str(message["chat"]["id"])
            result["text"] = message.get("text")
        
        # Callback query (button click)
        elif "callback_query" in update:
            query = update["callback_query"]
            result["channel_user_id"] = str(query["from"]["id"])
            result["button_payload"] = query["data"]
            # Answer callback query to remove loading state
            # (separate API call needed)
        
        return result
    
    def verify_webhook(self, request_data: Dict[str, Any]) -> bool:
        """Telegram doesn't use signatures, security is via secret URL."""
        # In production, use a secret path for webhook
        # e.g., /webhook/{SECRET_TOKEN}
        return True
```

---

## Translation Layer Implementation

### Inbound Translator (translation_layer/inbound_translator.py)

```python
from typing import Dict, Any
from models.request import NormalizedRequest
from infrastructure.user_service import UserService

class InboundTranslator:
    """Translates platform-specific events to normalized requests."""
    
    def __init__(self, user_service: UserService):
        self.user_service = user_service
    
    async def translate(
        self,
        channel: str,
        raw_event: Dict[str, Any]
    ) -> NormalizedRequest:
        """
        Convert platform event to normalized request.
        
        Args:
            channel: "whatsapp" | "telegram" | "website"
            raw_event: Platform-specific event data
                {
                    "channel_user_id": "...",
                    "text": "...",
                    "button_payload": None,  # or payload data
                    ...
                }
        
        Returns:
            NormalizedRequest ready for business logic
        """
        # 1. Resolve identity
        global_user_id = await self.user_service.resolve_identity(
            channel=channel,
            channel_user_id=raw_event["channel_user_id"]
        )
        
        # 2. Extract content
        text = raw_event.get("text")
        structured_event = None
        
        # If button click, convert to structured event
        if raw_event.get("button_payload"):
            structured_event = self._parse_button_payload(
                raw_event["button_payload"]
            )
        
        # 3. Build normalized request
        return NormalizedRequest(
            global_user_id=global_user_id,
            channel=channel,
            channel_user_id=raw_event["channel_user_id"],
            text=text,
            structured_event=structured_event,
            locale=raw_event.get("locale", "en_US"),
            timezone=raw_event.get("timezone", "UTC")
        )
    
    def _parse_button_payload(self, payload: str) -> Dict[str, Any]:
        """
        Parse button payload into structured event.
        
        Examples:
            "time_18" → {"slot_update": {"time": "18:00"}}
            "action_reserve" → {"intent": "reserve_table"}
        """
        parts = payload.split("_")
        
        if parts[0] == "time":
            return {"slot_update": {"time": f"{parts[1]}:00"}}
        elif parts[0] == "people":
            return {"slot_update": {"people": int(parts[1])}}
        elif parts[0] == "action":
            return {"intent": parts[1]}
        
        # Default: return raw payload
        return {"payload": payload}
```

### Outbound Translator (translation_layer/outbound_translator.py)

```python
from typing import Dict, Any
from models.response import NormalizedResponse
from translation_layer.renderers.whatsapp_renderer import WhatsAppRenderer
from translation_layer.renderers.telegram_renderer import TelegramRenderer
from translation_layer.renderers.website_renderer import WebsiteRenderer

class OutboundTranslator:
    """Translates normalized responses to platform-specific payloads."""
    
    def __init__(self):
        self.renderers = {
            "whatsapp": WhatsAppRenderer(),
            "telegram": TelegramRenderer(),
            "website": WebsiteRenderer()
        }
    
    def translate(
        self,
        channel: str,
        response: NormalizedResponse
    ) -> Dict[str, Any]:
        """
        Convert normalized response to platform payload.
        
        Args:
            channel: Target platform
            response: Business logic response
        
        Returns:
            Platform-specific message payload
        """
        renderer = self.renderers.get(channel)
        if not renderer:
            raise ValueError(f"Unknown channel: {channel}")
        
        return renderer.render(response)
```

### WhatsApp Renderer (translation_layer/renderers/whatsapp_renderer.py)

```python
from typing import Dict, Any
from models.response import NormalizedResponse, ResponseType

class WhatsAppRenderer:
    """Renders responses for WhatsApp."""
    
    MAX_TEXT_LENGTH = 4096
    MAX_QUICK_REPLIES = 3
    
    def render(self, response: NormalizedResponse) -> Dict[str, Any]:
        """Convert normalized response to WhatsApp payload."""
        
        if response.type == ResponseType.TEXT:
            return self._render_text(response)
        elif response.type == ResponseType.SLOT_REQUEST:
            return self._render_slot_request(response)
        elif response.type == ResponseType.MENU:
            return self._render_menu(response)
        elif response.type == ResponseType.CONFIRMATION:
            return self._render_confirmation(response)
        elif response.type == ResponseType.ERROR:
            return self._render_error(response)
        
        # Fallback
        return {"text": str(response.payload)}
    
    def _render_text(self, response: NormalizedResponse) -> Dict[str, Any]:
        """Simple text message."""
        text = response.payload.get("text", "")
        
        # Split if too long
        if len(text) > self.MAX_TEXT_LENGTH:
            text = text[:self.MAX_TEXT_LENGTH - 50] + "\n\n[Message truncated]"
        
        return {"text": text}
    
    def _render_slot_request(self, response: NormalizedResponse) -> Dict[str, Any]:
        """Render a question asking for missing slot."""
        prompt = response.payload.get("prompt", "Please provide information.")
        options = response.payload.get("options", [])
        
        payload = {"text": prompt}
        
        # Add quick replies if options provided (max 3)
        if options and len(options) <= self.MAX_QUICK_REPLIES:
            payload["quick_replies"] = options[:self.MAX_QUICK_REPLIES]
        elif options:
            # Too many options, render as numbered list
            options_text = "\n".join(
                f"{i+1}. {opt}" for i, opt in enumerate(options[:10])
            )
            payload["text"] = f"{prompt}\n\n{options_text}\n\nReply with number (1-{len(options[:10])})"
        
        return payload
    
    def _render_menu(self, response: NormalizedResponse) -> Dict[str, Any]:
        """
        Render menu - WhatsApp needs to paginate or show categories.
        
        Strategy: Show categories first, then items when category selected.
        """
        categories = response.payload.get("categories", [])
        items = response.payload.get("items", [])
        
        # If categories exist, show category selection
        if categories:
            text = "📋 Menu Categories:\n\n"
            text += "\n".join(f"{i+1}. {cat}" for i, cat in enumerate(categories))
            text += "\n\nReply with category number"
            
            return {"text": text}
        
        # Otherwise, show items (with pagination if needed)
        if len(items) > 10:
            # Show first 10 + "more" option
            items_text = self._format_menu_items(items[:10])
            return {
                "text": f"🍽️ Menu:\n\n{items_text}\n\n[Showing 10/{len(items)} items]\nReply NEXT for more",
                "quick_replies": ["Next", "Categories"]
            }
        else:
            items_text = self._format_menu_items(items)
            return {"text": f"🍽️ Menu:\n\n{items_text}"}
    
    def _format_menu_items(self, items: list) -> str:
        """Format menu items as text."""
        lines = []
        for item in items:
            line = f"• {item['name']}"
            if 'price' in item:
                line += f" - €{item['price']}"
            if 'description' in item:
                line += f"\n  {item['description']}"
            lines.append(line)
        return "\n\n".join(lines)
    
    def _render_confirmation(self, response: NormalizedResponse) -> Dict[str, Any]:
        """Render booking confirmation."""
        details = response.payload.get("booking_details", {})
        
        text = "✅ Reservation Summary:\n\n"
        text += f"👥 Party size: {details.get('people')}\n"
        text += f"📅 Date: {details.get('date')}\n"
        text += f"🕐 Time: {details.get('time')}\n"
        text += f"📍 Location: {details.get('location', 'Main Cafe')}\n\n"
        text += "Confirm this reservation?"
        
        return {
            "text": text,
            "quick_replies": ["✓ Confirm", "✗ Cancel"]
        }
    
    def _render_error(self, response: NormalizedResponse) -> Dict[str, Any]:
        """Render error with recovery options."""
        message = response.payload.get("message", "An error occurred")
        recovery = response.recovery_options
        
        text = f"❌ {message}\n\n"
        
        # Add alternatives if available
        if recovery and recovery.alternatives:
            text += "Alternative options:\n"
            for i, alt in enumerate(recovery.alternatives[:3], 1):
                text += f"{i}. {self._format_alternative(alt)}\n"
            text += "\nReply with option number"
        
        # Add escalation options
        if recovery and recovery.escalation:
            text += "\n\nOr:\n"
            if "call_cafe" in recovery.escalation:
                text += "• Call us: +49-123-456789\n"
            if "leave_phone_number" in recovery.escalation:
                text += "• Send your number, we'll call you\n"
        
        return {"text": text}
    
    def _format_alternative(self, alt: Dict[str, Any]) -> str:
        """Format alternative option (e.g., different time)."""
        if "time" in alt:
            return f"Time: {alt['time']}"
        elif "date" in alt:
            return f"Date: {alt['date']}"
        return str(alt)
```

---

## Business Logic Layer Implementation

### Intent Router (business_logic/intent_router.py)

```python
from typing import Dict, Any
from models.request import NormalizedRequest
from models.response import NormalizedResponse, ResponseType

class IntentRouter:
    """Routes requests to appropriate handlers based on intent."""
    
    def __init__(self, dialog_manager, services: Dict[str, Any]):
        self.dialog_manager = dialog_manager
        self.services = services
    
    async def route(self, request: NormalizedRequest) -> NormalizedResponse:
        """
        Determine intent and route to handler.
        
        Uses simple keyword matching for this example.
        In production, use trained NLU model (e.g., Rasa, spaCy).
        """
        text = (request.text or "").lower()
        
        # Check for structured event (button click)
        if request.structured_event:
            if "intent" in request.structured_event:
                intent = request.structured_event["intent"]
            elif "slot_update" in request.structured_event:
                # Continue current intent with slot update
                return await self.dialog_manager.handle_slot_update(
                    request,
                    request.structured_event["slot_update"]
                )
        else:
            # Detect intent from text
            intent = self._detect_intent(text)
        
        # Route to handler
        if intent == "opening_hours":
            return await self._handle_opening_hours(request)
        elif intent == "menu":
            return await self._handle_menu(request)
        elif intent == "reserve_table":
            return await self.dialog_manager.handle_reservation(request)
        else:
            return self._handle_unknown(request)
    
    def _detect_intent(self, text: str) -> str:
        """Simple keyword-based intent detection."""
        if any(word in text for word in ["open", "hours", "opening", "when"]):
            return "opening_hours"
        elif any(word in text for word in ["menu", "food", "drink", "eat"]):
            return "menu"
        elif any(word in text for word in ["reserve", "book", "table", "reservation"]):
            return "reserve_table"
        return "unknown"
    
    async def _handle_opening_hours(self, request: NormalizedRequest) -> NormalizedResponse:
        """Handle opening hours query."""
        hours_service = self.services["opening_hours"]
        hours = await hours_service.get_hours()
        
        return NormalizedResponse(
            type=ResponseType.TEXT,
            payload={
                "text": f"🕐 Our opening hours:\n\n{hours}"
            }
        )
    
    async def _handle_menu(self, request: NormalizedRequest) -> NormalizedResponse:
        """Handle menu request."""
        menu_service = self.services["menu"]
        categories = await menu_service.get_categories()
        items = await menu_service.get_all_items()
        
        return NormalizedResponse(
            type=ResponseType.MENU,
            payload={
                "categories": categories,
                "items": items
            },
            presentation_hints=PresentationHints(
                preferred_presentation="paginate",
                preview_items=10,
                group_by="category"
            )
        )
    
    def _handle_unknown(self, request: NormalizedRequest) -> NormalizedResponse:
        """Handle unrecognized intent."""
        return NormalizedResponse(
            type=ResponseType.TEXT,
            payload={
                "text": "I can help you with:\n• Opening hours\n• Menu\n• Table reservations\n\nWhat would you like to know?"
            }
        )
```

### Dialog Manager (business_logic/dialog_manager.py)

```python
from typing import Dict, Any, List
from models.request import NormalizedRequest
from models.response import NormalizedResponse, ResponseType, RecoveryOptions
from models.session import ConversationSession, DialogState
from infrastructure.session_store import SessionStore

class DialogManager:
    """Manages multi-turn conversations with slot filling."""
    
    def __init__(self, session_store: SessionStore, services: Dict[str, Any]):
        self.session_store = session_store
        self.services = services
    
    async def handle_reservation(self, request: NormalizedRequest) -> NormalizedResponse:
        """
        Handle table reservation flow with slot filling.
        
        Required slots: people, date, time, contact
        """
        # 1. Load or create session
        session = await self.session_store.get(request.global_user_id)
        if session is None or session.is_expired():
            session = self._create_reservation_session(request.global_user_id)
        
        # 2. Extract entities from request
        if request.text:
            extracted_slots = self._extract_slots(request.text)
            session.slots.update(extracted_slots)
        
        # 3. Check what's missing
        missing_slots = session.missing_slots()
        
        if missing_slots:
            # Ask for next missing slot
            next_slot = missing_slots[0]
            response = self._prompt_for_slot(next_slot, session)
            
            # Update session state
            session.dialog_state = DialogState.COLLECTING
            await self.session_store.set(request.global_user_id, session)
            
            return response
        else:
            # All slots filled, check availability
            return await self._check_availability_and_confirm(request, session)
    
    async def handle_slot_update(
        self,
        request: NormalizedRequest,
        slot_update: Dict[str, Any]
    ) -> NormalizedResponse:
        """Handle explicit slot update from button/form."""
        session = await self.session_store.get(request.global_user_id)
        if session is None:
            return self._handle_expired_session()
        
        # Update slots
        session.slots.update(slot_update)
        await self.session_store.set(request.global_user_id, session)
        
        # Continue reservation flow
        return await self.handle_reservation(request)
    
    def _create_reservation_session(self, user_id: str) -> ConversationSession:
        """Create new reservation session with required slots."""
        return ConversationSession(
            global_user_id=user_id,
            current_intent="reserve_table",
            dialog_state=DialogState.COLLECTING,
            required_slots=["people", "date", "time", "contact"]
        )
    
    def _extract_slots(self, text: str) -> Dict[str, Any]:
        """
        Extract slot values from natural language.
        
        In production, use NER (Named Entity Recognition) model.
        This is simplified for demonstration.
        """
        slots = {}
        text_lower = text.lower()
        
        # Extract number of people
        for num_word in ["2", "3", "4", "5", "6", "two", "three", "four"]:
            if num_word in text_lower:
                slots["people"] = self._word_to_number(num_word)
                break
        
        # Extract time (simplified)
        import re
        time_match = re.search(r'\b(\d{1,2})\s*(pm|am|:00)?\b', text_lower)
        if time_match:
            hour = int(time_match.group(1))
            if "pm" in text_lower and hour < 12:
                hour += 12
            slots["time"] = f"{hour:02d}:00"
        
        # Extract date (simplified)
        if "today" in text_lower:
            from datetime import date
            slots["date"] = str(date.today())
        elif "tomorrow" in text_lower:
            from datetime import date, timedelta
            slots["date"] = str(date.today() + timedelta(days=1))
        
        return slots
    
    def _word_to_number(self, word: str) -> int:
        """Convert number word to int."""
        mapping = {"two": 2, "three": 3, "four": 4, "five": 5, "six": 6}
        return mapping.get(word, int(word) if word.isdigit() else 0)
    
    def _prompt_for_slot(
        self,
        slot_name: str,
        session: ConversationSession
    ) -> NormalizedResponse:
        """Generate prompt for missing slot."""
        prompts = {
            "people": {
                "prompt": "How many people will be dining?",
                "options": ["2", "3", "4", "5", "6"]
            },
            "date": {
                "prompt": "Which date would you prefer?",
                "options": ["Today", "Tomorrow", "Pick date"]
            },
            "time": {
                "prompt": "What time would you like to reserve?",
                "options": ["17:00", "18:00", "19:00", "20:00"]
            },
            "contact": {
                "prompt": "Please provide your phone number for confirmation.",
                "options": []
            }
        }
        
        slot_config = prompts.get(slot_name, {"prompt": f"Please provide {slot_name}"})
        
        return NormalizedResponse(
            type=ResponseType.SLOT_REQUEST,
            payload={
                "missing_slot": slot_name,
                "prompt": slot_config["prompt"],
                "options": slot_config.get("options", [])
            },
            presentation_hints=PresentationHints(
                preferred_presentation="buttons" if slot_config.get("options") else "text"
            )
        )
    
    async def _check_availability_and_confirm(
        self,
        request: NormalizedRequest,
        session: ConversationSession
    ) -> NormalizedResponse:
        """Check if table is available and ask for confirmation."""
        reservation_service = self.services["reservation"]
        
        # Check availability
        is_available = await reservation_service.check_availability(
            date=session.slots["date"],
            time=session.slots["time"],
            people=session.slots["people"]
        )
        
        if is_available:
            # Update state and ask for confirmation
            session.dialog_state = DialogState.CONFIRMING
            await self.session_store.set(request.global_user_id, session)
            
            return NormalizedResponse(
                type=ResponseType.CONFIRMATION,
                payload={
                    "booking_details": session.slots,
                    "confirmation_required": True
                }
            )
        else:
            # No availability - offer alternatives
            alternatives = await reservation_service.find_alternatives(
                date=session.slots["date"],
                time=session.slots["time"],
                people=session.slots["people"]
            )
            
            return NormalizedResponse(
                type=ResponseType.ERROR,
                payload={
                    "code": "NO_AVAILABILITY",
                    "message": f"No tables available for {session.slots['people']} at {session.slots['time']}"
                },
                recovery_options=RecoveryOptions(
                    alternatives=alternatives,
                    escalation=["call_cafe", "leave_phone_number"]
                )
            )
    
    def _handle_expired_session(self) -> NormalizedResponse:
        """Handle case where session has expired."""
        return NormalizedResponse(
            type=ResponseType.TEXT,
            payload={
                "text": "Your session has expired. Let's start over! How can I help you?"
            }
        )
```

---

## Infrastructure Layer

### Session Store (infrastructure/session_store.py)

```python
import json
import redis.asyncio as redis
from typing import Optional
from models.session import ConversationSession
from datetime import datetime

class SessionStore:
    """Manages conversation sessions in Redis."""
    
    def __init__(self, redis_url: str, ttl_seconds: int = 1800):
        self.redis_client = redis.from_url(redis_url)
        self.ttl_seconds = ttl_seconds  # Default: 30 minutes
    
    async def get(self, global_user_id: str) -> Optional[ConversationSession]:
        """Retrieve session for user."""
        key = f"session:{global_user_id}"
        data = await self.redis_client.get(key)
        
        if data is None:
            return None
        
        # Deserialize
        session_dict = json.loads(data)
        return ConversationSession(**session_dict)
    
    async def set(
        self,
        global_user_id: str,
        session: ConversationSession,
        ttl: Optional[int] = None
    ) -> bool:
        """Save session for user with TTL."""
        key = f"session:{global_user_id}"
        
        # Update last_updated_at
        session.last_updated_at = datetime.utcnow()
        
        # Serialize
        data = json.dumps(session.__dict__, default=str)
        
        # Save with TTL
        ttl = ttl or self.ttl_seconds
        await self.redis_client.setex(key, ttl, data)
        
        return True
    
    async def delete(self, global_user_id: str) -> bool:
        """Delete session."""
        key = f"session:{global_user_id}"
        await self.redis_client.delete(key)
        return True
```

### User Service (infrastructure/user_service.py)

```python
from typing import Optional
import redis.asyncio as redis
import uuid

class UserService:
    """Manages user identities and cross-channel linking."""
    
    def __init__(self, redis_url: str):
        self.redis_client = redis.from_url(redis_url)
    
    async def resolve_identity(
        self,
        channel: str,
        channel_user_id: str
    ) -> str:
        """
        Resolve channel-specific ID to global user ID.
        
        Creates new global ID if user is new.
        """
        # Check mapping
        mapping_key = f"identity:{channel}:{channel_user_id}"
        global_user_id = await self.redis_client.get(mapping_key)
        
        if global_user_id:
            return global_user_id.decode('utf-8')
        
        # New user - create global ID
        global_user_id = f"user_{uuid.uuid4().hex[:12]}"
        
        # Store bidirectional mapping
        await self.redis_client.set(mapping_key, global_user_id)
        await self.redis_client.sadd(
            f"user:{global_user_id}:channels",
            f"{channel}:{channel_user_id}"
        )
        
        return global_user_id
    
    async def link_accounts(
        self,
        primary_global_id: str,
        channel: str,
        channel_user_id: str
    ) -> bool:
        """
        Link a new channel to existing global user ID.
        
        Used after OTP verification or login-based linking.
        """
        mapping_key = f"identity:{channel}:{channel_user_id}"
        
        # Check if already linked to different user
        existing_id = await self.redis_client.get(mapping_key)
        if existing_id and existing_id.decode('utf-8') != primary_global_id:
            # Conflict - would need to merge users or reject
            return False
        
        # Create link
        await self.redis_client.set(mapping_key, primary_global_id)
        await self.redis_client.sadd(
            f"user:{primary_global_id}:channels",
            f"{channel}:{channel_user_id}"
        )
        
        return True
```

---

## Main Application Entry Point

### app.py

```python
from fastapi import FastAPI, Request
from typing import Dict, Any
import asyncio

# Import layers
from platform_layer.whatsapp_adapter import WhatsAppAdapter
from platform_layer.telegram_adapter import TelegramAdapter
from translation_layer.inbound_translator import InboundTranslator
from translation_layer.outbound_translator import OutboundTranslator
from business_logic.intent_router import IntentRouter
from business_logic.dialog_manager import DialogManager
from infrastructure.session_store import SessionStore
from infrastructure.user_service import UserService

# Services
from business_logic.services.opening_hours_service import OpeningHoursService
from business_logic.services.menu_service import MenuService
from business_logic.services.reservation_service import ReservationService

# Configuration
import yaml

app = FastAPI()

# Load configuration
with open("config/production.yaml") as f:
    config = yaml.safe_load(f)

# Initialize infrastructure
session_store = SessionStore(config["redis"]["url"])
user_service = UserService(config["redis"]["url"])

# Initialize services
services = {
    "opening_hours": OpeningHoursService(),
    "menu": MenuService(),
    "reservation": ReservationService()
}

# Initialize business logic
dialog_manager = DialogManager(session_store, services)
intent_router = IntentRouter(dialog_manager, services)

# Initialize translation layer
inbound_translator = InboundTranslator(user_service)
outbound_translator = OutboundTranslator()

# Initialize platform adapters
whatsapp_adapter = WhatsAppAdapter(config["channels"]["whatsapp"])
telegram_adapter = TelegramAdapter(config["channels"]["telegram"])

# Webhook endpoints

@app.post("/webhook/whatsapp")
async def whatsapp_webhook(request: Request):
    """Handle WhatsApp webhook."""
    body = await request.json()
    
    # Verify signature
    # (implementation depends on your setup)
    
    # Extract message
    raw_event = whatsapp_adapter.extract_user_message(body)
    if not raw_event:
        return {"status": "ok"}
    
    # Process message
    response = await process_message("whatsapp", raw_event)
    
    # Send response
    await whatsapp_adapter.send_message(
        raw_event["channel_user_id"],
        response
    )
    
    return {"status": "ok"}

@app.post("/webhook/telegram")
async def telegram_webhook(request: Request):
    """Handle Telegram webhook."""
    update = await request.json()
    
    # Extract message
    raw_event = telegram_adapter.extract_user_message(update)
    if not raw_event:
        return {"status": "ok"}
    
    # Process message
    response = await process_message("telegram", raw_event)
    
    # Send response
    await telegram_adapter.send_message(
        raw_event["channel_user_id"],
        response
    )
    
    return {"status": "ok"}

async def process_message(channel: str, raw_event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main message processing pipeline.
    
    1. Inbound translation (platform → normalized)
    2. Business logic (intent routing + dialog management)
    3. Outbound translation (normalized → platform)
    """
    # 1. Translate to normalized request
    normalized_request = await inbound_translator.translate(channel, raw_event)
    
    # 2. Process with business logic
    normalized_response = await intent_router.route(normalized_request)
    
    # 3. Translate to platform payload
    platform_payload = outbound_translator.translate(channel, normalized_response)
    
    return platform_payload

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## Key Takeaways

### Architecture Benefits Demonstrated

1. **Platform Independence**
   - Business logic never knows which platform it's serving
   - Adding new channel = new adapter + renderer, zero business logic changes

2. **Separation of Concerns**
   - Platform layer: Communication plumbing
   - Translation layer: Adaptation
   - Business logic: Decision making
   - Infrastructure: Storage

3. **Scalability**
   - Stateless request processing (session in Redis)
   - Horizontal scaling (any server handles any user)
   - TTL-based cleanup prevents memory leaks

4. **Maintainability**
   - Update opening hours once, affects all channels
   - Change response format without touching adapters
   - Test business logic without mocking platforms

5. **Flexibility**
   - Presentation hints allow UX optimization per channel
   - Error recovery adapts to platform capabilities
   - Identity linking enables cross-channel continuity

---

## Next Steps for Implementation

1. **Enhance NLU**
   - Replace keyword matching with trained models (Rasa, spaCy)
   - Add entity extraction (dateutil, spaCy NER)

2. **Add Testing**
   - Unit tests for each layer independently
   - Integration tests for full pipeline
   - Mock platform adapters for testing

3. **Production Readiness**
   - Add logging and monitoring
   - Implement retry logic with backoff
   - Add rate limiting
   - Set up error alerting

4. **Advanced Features**
   - Context carryover across sessions
   - Personalization based on history
   - Multi-language support
   - Analytics and insights

---

**This implementation guide provides a solid foundation for building production-grade multi-channel chatbots!**
