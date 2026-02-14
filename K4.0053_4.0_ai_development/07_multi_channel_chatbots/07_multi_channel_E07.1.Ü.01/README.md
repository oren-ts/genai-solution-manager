# Exercise 07.1.Ü.01 - Multi-Channel Chatbot Architecture

**Date:** 2025-02-14  
**Status:** ✅ Complete  
**Topic:** Multi-channel chatbot architecture design

---

## Exercise Overview

**Scenario:** Develop a chatbot for a small café that communicates with customers via WhatsApp, Telegram, and its website. The chatbot answers queries about opening hours, menu, and table reservations.

**Challenge:** Design an architecture where different platform requirements are handled without changing the core chatbot logic.

---

## Solution

### Goal

Provide one chatbot for **opening hours**, **menu**, and **reservations** across **WhatsApp, Telegram, and website** while keeping the **core logic unchanged** as channels are added.

---

## Architecture Overview

### Three-Layer Architecture with Shared Infrastructure

```
┌──────────────────────────────────────────────────────────────────┐
│                         Platform Layer                            │
│  WhatsApp Adapter     Telegram Adapter         Website Chat UI     │
└───────────────↕────────────────────↕────────────────────↕─────────┘
                ↕ events/responses    ↕ events/responses    ↕ events/responses
┌──────────────────────────────────────────────────────────────────┐
│                  Translation / Adapter Layer                       │
│  Inbound: normalize + identity map + event→slots                   │
│  Outbound: render + format + paginate/split + channel fallbacks     │
└───────────────────────────────↕───────────────────────────────────┘
                                ↕ normalized requests/responses
┌──────────────────────────────────────────────────────────────────┐
│                 Business Logic Layer (Core Chatbot)                │
│  Intent handling + slot filling + dialog policy + domain services  │
│  Produces channel-neutral response objects (incl. recovery options)│
└───────────────────────────────↕───────────────────────────────────┘
                                ↕ via interfaces
┌──────────────────────────────────────────────────────────────────┐
│            Shared Infrastructure (Storage/APIs)                    │
│  Session Store (Redis/DB + TTL) │ User/Identity Service            │
│  Menu DB/CMS                    │ Reservation DB/Calendar          │
└──────────────────────────────────────────────────────────────────┘
```

**Key Separation:**
- **State logic** lives in business logic (what to store, when to expire, what's next)
- **State storage** is shared infrastructure (enables horizontal scaling)

---

## Example Message Flow

### Happy Path: Cross-Platform Continuation

**Step 1: User starts on WhatsApp**
```
User (WhatsApp): "Reserve a table for 4"
```

1. **Platform Layer** → WhatsApp adapter receives message, sends event upward
2. **Translation Layer** → Normalizes to:
   ```
   {
     channel: "whatsapp",
     channel_user_id: "+49...",
     text: "Reserve a table for 4"
   }
   ```
3. **Translation Layer** → Calls UserService to resolve:
   ```
   channel_user_id (+49...) → global_user_id (user_123)
   ```
4. **Business Logic** →
   - Detects intent: `reserve_table`
   - Updates session state: `{people: 4, date: ?, time: ?}`
   - Returns response object:
     ```json
     {
       "type": "slot_request",
       "missing": ["date", "time"],
       "presentation_hint": "guided"
     }
     ```
5. **Translation Layer** → Renders for WhatsApp:
   ```
   "For which date and time?"
   [Quick replies: "Today" "Tomorrow" "Other"]
   ```

**Step 2: User continues on website**
```
User (Website): "Tomorrow 7pm"
```

1. **Platform Layer** → Website adapter sends event with logged-in user identity
2. **Translation Layer** → Maps website user to same `global_user_id (user_123)`
3. **Business Logic** →
   - Fills missing slots: `{people: 4, date: "tomorrow", time: "19:00"}`
   - Checks availability via ReservationService
   - Returns confirmation response
4. **Translation Layer** → Renders rich confirmation UI on website with edit options

---

### Failure Case: Identity Linking Unavailable

**Scenario:** User is not logged in on website, no verified link to WhatsApp exists

**Result:**
- Translation layer cannot safely map to same `global_user_id`
- Website starts a **new session**
- Optionally offers linking: "To continue your WhatsApp reservation here, enter the code we sent to your phone."

**Rationale:** Privacy-first approach prevents accidentally merging different users' data.

---

## Part (a): Business Logic Layer Design

### Purpose
Process customer requests the same way regardless of which platform they originate from.

### Components

**1. Intent Router**
- Identifies user goals: opening hours, menu, reservation
- Routes to appropriate handler

**2. Dialog Manager**
- Slot filling (party size, date, time, contact info)
- Decides next question to ask
- Manages conversation flow state machine

**3. Domain Services**
- `OpeningHoursService` - Retrieves current hours, holiday schedules
- `MenuService` - Fetches menu items, categories, prices
- `ReservationService` - Checks availability, creates bookings

**4. Conversation State Model**
- Defines state machine: `collecting → confirming → booked`
- Timeout rules (e.g., abandon after 20 minutes of inactivity)
- Tracks conversation context and filled slots

**5. Infrastructure Interfaces**
- `SessionStore` interface - Get/set session by `global_user_id`
- `UserService` interface - Identity resolution and profiles
- Database connections for menu/reservations

---

### Inputs

Platform-neutral request object:
```python
{
  "global_user_id": "user_123",
  "message_text": "Reserve a table for 4",  # OR structured_event
  "locale": "de_DE",
  "timezone": "Europe/Berlin",
  "conversation_state": {...}
}
```

---

### Outputs

Channel-neutral response object:
```python
{
  "type": "text" | "menu" | "slot_request" | "confirmation" | "error",
  "payload": {
    # Structured data: menu items, hours, booking details
  },
  "recovery_options": {
    # Alternative actions if error occurred
    "alternatives": [...],
    "escalation": ["call_cafe", "leave_phone_number"]
  },
  "presentation_hints": {
    # Recommendations (not requirements)
    "preferred_presentation": "paginate",
    "preview_items": 10,
    "group_by": "category"
  }
}
```

---

### What Business Logic Does NOT Know

- ❌ Which platform the user is on (WhatsApp vs Telegram vs Website)
- ❌ UI widget capabilities (date pickers, buttons, forms)
- ❌ Message formatting details and character limits
- ❌ Webhook mechanics, retries, rate limiting
- ❌ Platform-specific authentication flows

---

### Session Storage Architecture

**Why Shared Storage Matters:**

The business logic must support:
- Thousands of concurrent conversations
- Multiple application server instances (horizontal scaling)
- Cross-platform conversation continuity

**Solution:**
- Business logic **cannot keep state only in server memory** (next message might go to different server)
- Business logic owns the **rules and structure** of conversation state
- State is **persisted via `SessionStore` interface** backed by shared infrastructure (Redis/PostgreSQL)

**Benefits:**
- Any server instance can resume any conversation
- Enables cross-platform continuity when identity is linked
- Survives server restarts/deployments

**Example:**
```python
# Business logic reads state
session = session_store.get(global_user_id)

# Updates state based on message
session.slots['date'] = parse_date(message)

# Saves updated state
session_store.set(global_user_id, session, ttl=1800)  # 30 min TTL
```

---

## Part (b): Translation Layer Design

### Purpose
Mediate between platform-specific messages/events and platform-agnostic business logic.

---

### Inbound Responsibilities (Platform → Business)

**1. Event Normalization**

Convert all incoming events to one common schema:
- Text messages
- Button clicks / quick reply payloads
- Form submissions
- Voice messages (if supported)

**Example transformations:**
```python
# WhatsApp quick reply
{"text": "Reserve", "button_payload": "action=reserve"}
# →
{"intent": "reserve_table", "structured_event": True}

# Telegram callback query
{"callback_data": "people_4"}
# →
{"slot_update": {"people": 4}}

# Website form submit
{"form_data": {"date": "2025-02-15", "time": "19:00", "people": 4}}
# →
{"slot_update": {"date": "2025-02-15", "time": "19:00", "people": 4}}
```

---

**2. Identity Mapping**

Resolve channel-specific user IDs to global user identity:

```python
# Call UserService (or mapping table)
channel_user_id = "+491234567890"  # WhatsApp phone
global_user_id = user_service.resolve(
    channel="whatsapp",
    channel_user_id=channel_user_id
)
# → "user_123"
```

**First-time user:** Create new mapping entry
```python
{
  "channel": "whatsapp",
  "channel_user_id": "+491234567890",
  "global_user_id": "user_123",  # newly generated
  "created_at": "2025-02-14T10:00:00Z"
}
```

---

**3. Identity Linking Strategies**

How to link identities across channels:

| Strategy | Description | Use Case |
|----------|-------------|----------|
| **Login-based** | Website login (email/phone) → strong identity | User has account |
| **OTP verification** | Send code to WhatsApp → verify on website | Link anonymous chat |
| **Magic link** | Email link that authenticates web session | Passwordless linking |
| **Account settings** | User manually links in profile settings | Optional, user-initiated |

**Privacy-First Principle:**
If no verified link exists, treat as **separate sessions** to avoid merging wrong users.

---

**4. Locale/Timezone Normalization**

Ensure consistent handling across platforms:
```python
# Telegram might send: "Europe/Berlin"
# WhatsApp might infer from phone: "+49" → "Europe/Berlin"
# Website might use browser: "de-DE" + UTC offset

# Normalize to:
{
  "locale": "de_DE",
  "timezone": "Europe/Berlin"
}
```

---

### Outbound Responsibilities (Business → Platform)

**1. Response Rendering**

Convert channel-neutral responses to platform-specific payloads:

```python
# Business returns:
{
  "type": "slot_request",
  "missing": ["date", "time"],
  "text": "For which date and time?"
}

# WhatsApp rendering:
{
  "text": "For which date and time?",
  "quick_replies": ["Today", "Tomorrow", "Other"]
}

# Telegram rendering:
{
  "text": "For which date and time?",
  "inline_keyboard": [
    [{"text": "Today", "callback_data": "date_today"}],
    [{"text": "Tomorrow", "callback_data": "date_tomorrow"}],
    [{"text": "Pick date", "callback_data": "date_custom"}]
  ]
}

# Website rendering:
{
  "text": "For which date and time?",
  "ui_component": {
    "type": "datetime_picker",
    "min_date": "today",
    "time_slots": ["17:00", "18:00", "19:00", "20:00", "21:00"]
  }
}
```

---

**2. Constraint Handling**

Apply platform-specific limitations:

**Message Length:**
```python
# Business returns full menu (3000 chars)
# WhatsApp/Telegram: 4096 char limit

if len(text) > 4000:
    # Option 1: Split into multiple messages
    messages = split_preserving_formatting(text, max_length=4000)
    
    # Option 2: Paginate with controls
    messages = [
        create_page(items[0:10]) + "\n[1/5] Reply NEXT",
        # ... more pages
    ]
    
    # Option 3: Summarize + offer full version
    summary = create_summary(items)
    message = summary + "\n\nReply MENU to see full list"
```

**UI Capabilities:**
```python
# If platform supports buttons:
if channel_capabilities.supports_buttons:
    render_as_button_menu()
else:
    render_as_text_with_instructions()
```

---

**3. Presentation Decisions**

Translation layer decides HOW to present based on:
- Channel capabilities
- User context (mobile vs desktop)
- Content size
- UX best practices per platform

**Example: Menu Display**

| Platform | Presentation Choice |
|----------|-------------------|
| WhatsApp | Category list → selected category items → "More?" |
| Telegram | Inline keyboard with categories → items with photos |
| Website | Full menu with search, filters, scrollable categories |

---

### Presentation Hints Philosophy

**Hints are RECOMMENDATIONS, not requirements.**

Translation layer may override hints based on:
- Platform constraints (message limits, UI support)
- UX optimization (reduce cognitive load, adapt to screen size)
- Performance (slow connection → simpler rendering)
- Privacy/safety (avoid revealing sensitive linked identity details)

**Example:**
```python
# Business suggests:
{
  "presentation_hints": {
    "preview_items": 10
  }
}

# Translation decisions:
# - WhatsApp: Show 5 items (better mobile readability)
# - Telegram: Show 10 items (as suggested)
# - Website: Show 15 items with lazy loading (larger screen)
```

---

## Part (c): Platform Layer Design

### Purpose
Handle communication plumbing for each channel - the "how to send/receive" not the "what to say."

---

### WhatsApp Adapter

**Technical Integration:**
- WhatsApp Business API (often via provider like Twilio, MessageBird)
- Webhook verification and signature validation
- Message delivery status tracking
- Retry logic with exponential backoff

**Platform Constraints:**
- Stricter rate limiting than Telegram
- Message templates required for proactive messages (after 24h window)
- Limited interactive elements (quick replies, list messages, buttons)
- 4096 character limit per message

**UI Adjustments:**
- **Guided prompts** - Step-by-step questions work best
- **Concise messages** - Mobile users expect brevity
- **Quick replies** - When available, offer 1-3 common options
- **Fallback to text** - Always support pure text input

**User Expectations:**
- Fast, conversational experience
- Minimal friction (avoid complex multi-step flows)
- Short, scannable messages
- Familiar messaging app patterns

---

### Telegram Adapter

**Technical Integration:**
- Telegram Bot API (webhook or long polling)
- Callback query handling for inline buttons
- Command support (`/start`, `/menu`, `/reserve`)
- File/photo sharing capabilities

**Platform Constraints:**
- 4096 character limit (same as WhatsApp)
- Rich markdown formatting supported
- Inline keyboards (up to 8 columns)
- Good support for bot-specific UX patterns

**UI Adjustments:**
- **Inline keyboards** - Primary interaction method
- **Commands** - Users expect `/command` style navigation
- **Rich formatting** - Bold, italic, links, code blocks
- **Pagination controls** - "Next page" buttons work well

**User Expectations:**
- Bot-like interactions (not purely conversational)
- Button-driven navigation
- Quick access to common actions
- Support for commands and menus

**Example Telegram-specific pattern:**
```python
# Reservation flow with inline keyboard
message = "Great! When would you like to reserve?"
keyboard = [
    [
        {"text": "Today 18:00", "callback_data": "reserve_today_18"},
        {"text": "Today 19:00", "callback_data": "reserve_today_19"}
    ],
    [
        {"text": "Tomorrow 18:00", "callback_data": "reserve_tomorrow_18"},
        {"text": "Tomorrow 19:00", "callback_data": "reserve_tomorrow_19"}
    ],
    [{"text": "⏰ Pick custom time", "callback_data": "reserve_custom"}]
]
```

---

### Website Chat Adapter

**Technical Integration:**
- Chat widget embedded in web app
- WebSocket or HTTP polling for real-time updates
- Authentication integration (optional but recommended)
- Session management tied to user account

**Platform Constraints:**
- No message length limits (practical limit: user attention)
- Full HTML/CSS control
- Rich UI components available
- Persistent session with browser storage

**UI Adjustments:**
- **Rich components** - Date pickers, dropdowns, form fields
- **Visual menu** - Cards with photos, descriptions, prices
- **Inline editing** - Easy to change previous inputs
- **History view** - Show conversation history and past bookings
- **Search & filters** - Power user features

**User Expectations:**
- App-like experience (not just chat bubbles)
- Ability to see and edit details easily
- Rich visual presentation
- Fast navigation without back-and-forth
- Integration with account features

**Example Website-specific UI:**
```html
<!-- Reservation form (rich UI instead of conversational) -->
<div class="reservation-widget">
  <h3>Reserve a Table</h3>
  <form>
    <input type="date" min="today" />
    <select name="time">
      <option>17:00</option>
      <option>18:00</option>
      <option>19:00</option>
    </select>
    <input type="number" min="1" max="10" placeholder="Number of guests" />
    <button>Check Availability</button>
  </form>
</div>
```

---

## Error Handling Strategy

### Typed Errors with Recovery Options

**Business logic returns structured errors:**
```python
{
  "type": "error",
  "code": "NO_AVAILABILITY",
  "message": "No tables available at 19:00 tomorrow",
  "alternatives": [
    {"time": "18:00", "available": True},
    {"time": "20:00", "available": True}
  ],
  "escalation": ["call_cafe", "leave_phone_number"]
}
```

---

### Fallback Strategy Ownership

**Clear responsibility split:**

| Layer | Responsibility |
|-------|---------------|
| **Business Logic** | Decides *what* recovery options are valid (alternatives, escalation actions) |
| **Translation Layer** | Decides *how* to present them (buttons on Telegram/web, text on WhatsApp) |

**Important:** Translation layer should NOT invent business decisions.

**Examples:**

❌ **Wrong** - Translation inventing alternatives:
```python
# Business returns: alternatives=[]
# Translation adds: "Maybe try 8pm instead?"
# → This is a business decision, not presentation!
```

✅ **Correct** - Translation presents approved options:
```python
# Business returns: escalation=["call_cafe"]
# WhatsApp: "No availability. Call us at +49-123-456789"
# Telegram: "No availability. [Call us] (button with phone number)"
# Website: "No availability. [Call now] (click-to-call button)"
```

---

## State Management & Cleanup

### Conversation State vs UI State

**Persist in session store (conversation-level):**
- ✅ Active intent (`reserve_table`)
- ✅ Filled slots (`{people: 4, date: "2025-02-15", time: "19:00"}`)
- ✅ Next required slot (`contact_phone`)
- ✅ Reservation flow step (`confirming`)

**Do NOT persist (UI-level):**
- ❌ "Menu page 3 on website"
- ❌ Scroll position
- ❌ Layout state (expanded/collapsed sections)
- ❌ Temporary UI animations

---

**Rationale:**

UI state is channel-specific and shouldn't leak across platforms.

**Example scenario:**
1. User browses menu on website (reaches page 3)
2. Switches to WhatsApp: "Reserve a table"
3. WhatsApp should NOT "remember page 3" - that's web UI state

Conversation state (intent, slots) should carry over.  
UI state (menu browsing position) should not.

---

### Timeout Handling Without Memory Leaks

**Two-layer approach:**

**1. Logical Expiration (Lazy Check)**
```python
# On each incoming message, business logic checks:
if now - session.last_updated_at > 20 * 60:  # 20 minutes
    # Conversation expired - reset to new session
    session = create_new_session()
    response = "Welcome back! How can I help you today?"
```

**2. Storage TTL (Automatic Cleanup)**
```python
# When saving session:
session_store.set(
    key=global_user_id,
    value=session,
    ttl=1800  # 30 minutes - auto-expires even if user never returns
)
```

**Why both?**
- Lazy expiration: Provides graceful UX ("Welcome back!")
- TTL: Prevents abandoned sessions from filling storage indefinitely

**Optional:** Background cleanup jobs (infrastructure-level, not platform layer)

---

## Menu Pagination Architecture

### Decision Flow

**1. Who decides to paginate?**
- **Business logic** returns full menu as structured data
- May include recommendation: `"preferred_presentation": "paginate"`
- **Translation layer** decides actual pagination strategy per channel

**2. Pagination strategies by channel:**

| Platform | Strategy |
|----------|----------|
| **WhatsApp** | Show categories → selected category items → "More?" |
| **Telegram** | First page + "Next" inline button |
| **Website** | Full scrollable list with lazy loading |

**3. Where does pagination state live?**

**Answer: UI-level state, per channel** (not main conversation session)

**Rationale:**
- Menu browsing is UI navigation, not conversation context
- If user switches from web (viewing page 3) to WhatsApp (making reservation), WhatsApp shouldn't inherit "page 3"
- Keeps reservation flow state clean and portable across channels

**Implementation options:**

**Option A:** Lightweight adapter state
```python
# Translation layer maintains per-channel UI state
adapter_state = {
    "user_123_whatsapp": {"menu_page": 2},
    "user_123_website": {"menu_page": 3}
}
```

**Option B:** Short-lived view state
```python
# Separate from main session, keyed to channel + user
menu_view_state = redis.get(f"menu_view:{channel}:{global_user_id}")
# TTL: 5 minutes (UI-only, short-lived)
```

**Key principle:** Don't pollute main conversation session with UI-only state unless menu browsing IS the active conversational task.

---

## Architectural Design Decisions Summary

### Q1: Can translation layer override presentation hints?

**Answer:** Yes. Hints are **recommendations**, not requirements.

**Reasoning:**
- Translation layer knows channel constraints (message limits, UI support)
- Can optimize for UX (screen size, connection speed)
- Should preserve semantic meaning while adapting presentation

**Example:**
```python
# Business suggests: preview_items=10
# Translation overrides:
# - WhatsApp: 5 items (mobile readability)
# - Website: 15 items (desktop screen real estate)
```

---

### Q2: Who owns error recovery strategy?

**Answer:** Business logic owns *what* recovery options exist. Translation layer owns *how* to present them.

**Reasoning:**
- Business logic understands domain constraints (availability, business rules)
- Translation layer understands UX patterns per channel
- Clear separation prevents translation from inventing business decisions

**Example:**
```python
# Business decides: alternatives=[18:00, 20:00]
# Translation decides:
# - Telegram: Show as inline keyboard buttons
# - WhatsApp: Show as numbered list with "Reply 1 or 2"
# - Website: Show as clickable time cards
```

---

### Q3: Where's the boundary between conversation state and UI state?

**Answer:**
- **Conversation state:** Intent, slots, dialog position (business-relevant context)
- **UI state:** Menu pages, scroll position, layout preferences (channel-specific navigation)

**Reasoning:**
- Conversation state must survive channel switching
- UI state is ephemeral and channel-locked
- Mixing them creates tight coupling and portability issues

---

## Key Takeaways

### Architecture Patterns Learned

1. **Three-layer separation** enables platform independence
2. **Translation layer** is the key to scalability (normalize + adapt)
3. **Presentation hints** provide flexibility without coupling
4. **State separation** (conversation vs UI) keeps architecture clean
5. **Shared infrastructure** enables horizontal scaling

---

### Reusable Design Principles

- ✅ Business logic should never know specific platforms
- ✅ Translation layer enables flexibility through normalization
- ✅ Error recovery should be business-driven, presentation-adapted
- ✅ Scalability requires externalized state storage
- ✅ Identity linking must be privacy-first
- ✅ Hints are recommendations that can be overridden for UX

---

### Real-World Applications

This architecture pattern applies to:
- Multi-channel customer support systems
- Omnichannel e-commerce experiences
- Cross-platform notification systems
- Any system needing platform-independent business logic

---

## Next Steps

1. **Study companion diagrams** - Review detailed visual architecture
2. **Explore implementation guide** - See how this translates to code
3. **Practice with variations** - Design for additional channels (SMS, voice, mobile app)
4. **Build a prototype** - Implement a simple version with one platform first

---

**Exercise completed successfully! 🎉**
