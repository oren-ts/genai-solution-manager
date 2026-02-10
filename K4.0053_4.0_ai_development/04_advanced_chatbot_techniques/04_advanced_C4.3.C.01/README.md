# Exercise 04.3.C.01 - Advanced Hotel Chatbot System Design

## Part (a) - Chatbot Architecture & Concept

### Overview

This document outlines the architectural design for an advanced hotel chatbot system capable of handling complex dialogues, remembering previous interactions, and providing personalized recommendations based on guest preferences and requirements.

### System Architecture

The chatbot is built on a modular architecture consisting of four core components that work together to process user inputs, manage conversations, and generate intelligent responses.

#### Architecture Diagram
```mermaid
flowchart TB
    User([User/Guest])
    
    subgraph ChatbotSystem["Hotel Chatbot System"]
        NLP["NLP Engine<br/>━━━━━━━━━━━<br/>• Intent Recognition<br/>• Entity Extraction<br/>• Language Understanding"]
        
        Dialog["Dialog Management<br/>━━━━━━━━━━━<br/>• Conversation Flow<br/>• Slot Filling<br/>• Multi-turn Handling"]
        
        Context["Context Management<br/>━━━━━━━━━━━<br/>• Immediate Context<br/>• Session Context<br/>• Persistent Context"]
        
        Response["Response Generation<br/>━━━━━━━━━━━<br/>• Natural Language Output<br/>• Hotel System Integration<br/>• Personalization"]
    end
    
    User -->|"User Input<br/>(Text/Voice)"| NLP
    NLP -->|"Intents + Entities"| Dialog
    Dialog <-->|"Read/Write Context"| Context
    Dialog -->|"Response Strategy"| Response
    Response -->|"Generated Response"| User
    
    style User fill:#e1f5ff
    style NLP fill:#fff4e6
    style Dialog fill:#f3e5f5
    style Context fill:#e8f5e9
    style Response fill:#fce4ec
```

### Component Breakdown

| Component | Primary Role | Key Functions | Technology Approach |
|-----------|-------------|---------------|-------------------|
| **NLP Engine** | Understanding user input | • Extract user intent (e.g., `book_room`, `ask_amenities`)<br/>• Identify entities (dates, room types, guest count)<br/>• Handle natural language variations<br/>• Process multiple languages | AI-based using pre-trained NLU models trained on hotel domain data |
| **Dialog Management System** | Controlling conversation flow | • Determine next dialog step based on context<br/>• Handle multi-turn conversations<br/>• Manage slot filling (collect missing information)<br/>• Maintain dialog state across turns | Hybrid: Rule-based for structured flows, AI-based for complex scenarios |
| **Context Management** | Storing and retrieving conversation memory | • Store immediate context (last 1-3 messages)<br/>• Maintain session context (current conversation)<br/>• Persist user preferences across sessions<br/>• Provide relevant context to other components | Database-backed storage with session IDs and user profiles |
| **Response Generation** | Producing natural, personalized outputs | • Generate contextually appropriate responses<br/>• Integrate with hotel systems (availability, pricing)<br/>• Personalize based on user profile<br/>• Format responses naturally | Hybrid: Template-based for standard responses, AI-based for dynamic content |

### Integration of Rule-Based and AI-Based Approaches

The chatbot employs a **hybrid approach** that strategically combines rule-based and AI-based techniques to optimize for both accuracy and natural interaction.

#### Rule-Based Approach

**Best suited for:**
- ✅ Simple, predictable interactions with clear structure
- ✅ Scenarios requiring 100% accuracy
- ✅ Standard FAQs with deterministic answers
- ✅ Fast response requirements

**Implementation examples:**

| Scenario | User Query | Rule-Based Response |
|----------|------------|-------------------|
| **Standard Information** | "What time is checkout?" | Direct lookup: "Checkout time is 11:00 AM" |
| **Simple Commands** | "Cancel booking #12345" | If valid booking ID → Execute cancellation |
| **Fixed Policies** | "What's the WiFi password?" | Return standard password from database |
| **Business Rules** | "Can I book for 20 people?" | If guests > room_capacity → Suggest alternatives |

#### AI-Based Approach

**Best suited for:**
- ✅ Natural language with high variation
- ✅ Complex queries requiring context understanding
- ✅ Extracting information from ambiguous sentences
- ✅ Handling unexpected phrasings

**Implementation examples:**

| Scenario | User Query | Why AI is Needed |
|----------|------------|------------------|
| **Complex Intent** | "I'm arriving really late, like maybe 2 AM, is that okay?" | AI understands this refers to late check-in despite indirect phrasing |
| **Context-Dependent** | "My kid is allergic to feathers, what kind of pillows do you have?" | AI extracts concern about pillow materials from allergy context |
| **Implicit Requests** | "We're celebrating our anniversary, any romantic touches you could add?" | AI recognizes this as a special request for room enhancements |
| **Multi-Entity Extraction** | "I need a quiet room on the top floor for two adults from December 15th to 18th" | AI extracts multiple entities: room_preference, floor, guests, dates |

#### Hybrid Decision Logic

The system uses the following logic to determine which approach to use:
```pseudocode
FUNCTION determine_approach(user_input, context):
    intent = NLP_Engine.extract_intent(user_input)
    
    IF intent in KNOWN_FAQ_LIST:
        RETURN rule_based_response(intent)
    
    ELSE IF intent.confidence_score < 0.7:
        RETURN ai_based_processing(user_input, context)
    
    ELSE IF requires_context_understanding(intent):
        RETURN ai_based_processing(user_input, context)
    
    ELSE IF intent in STRUCTURED_WORKFLOWS:
        RETURN rule_based_dialog_flow(intent)
    
    ELSE:
        RETURN ai_based_processing(user_input, context)
```

**Key advantages of hybrid approach:**
- **Reliability:** Rule-based ensures consistent handling of standard requests
- **Flexibility:** AI-based handles unexpected variations naturally
- **Efficiency:** Rules are faster for simple queries
- **Scalability:** AI handles growing complexity without manual rule creation

### Data Flow Example

**Scenario:** User asks: *"I need a quiet room on the top floor for two adults from December 15th to 18th"*

1. **NLP Engine** processes input:
   - Intent: `book_room`
   - Entities: `room_preference="quiet"`, `floor="top"`, `guests=2`, `check_in="Dec 15"`, `check_out="Dec 18"`

2. **Dialog Management** receives structured data:
   - Checks Context Management: Is this a new booking or modification?
   - Determines missing slots: payment method, contact information
   - Decides next step: Query availability

3. **Context Management** stores:
   - Session context: Current booking intent with collected entities
   - Prepares to store: Booking preferences for future sessions

4. **Response Generation** produces:
   - Natural response: "I've found quiet rooms on our top floor available for 2 guests from December 15-18. We have Superior and Deluxe options. Which would you prefer?"
   - Integrates with booking system to check real-time availability

## Summary

This modular architecture provides:
- **Scalability:** Components can be upgraded independently
- **Flexibility:** Hybrid approach adapts to different interaction types
- **Intelligence:** AI handles complexity while rules ensure reliability
- **Personalization:** Context management enables memory across sessions

---

## Part (b) - Context Management Implementation Plan

### Overview

Context management is the chatbot's memory system, enabling it to maintain coherent conversations across multiple turns and sessions. This plan outlines how the chatbot stores, retrieves, and utilizes conversational context to provide relevant and personalized responses.

### Context Types Comparison

The system implements three distinct types of context, each serving different temporal scopes and purposes:

| Context Type | Definition | Storage Method | Lifespan | Use Cases | Example |
|--------------|-----------|----------------|----------|-----------|---------|
| **Immediate Context** | Last 1-3 messages in the current exchange | In-memory buffer | Current conversation turn | • Pronoun resolution<br/>• Clarification questions<br/>• Follow-up responses | User: "Do you have sea view rooms?"<br/>Bot: "Yes, we have deluxe sea view rooms."<br/>User: "Book **it** for me" ← **"it"** resolved via immediate context |
| **Session Context** | All information within the current conversation | Session storage (Redis/memory cache) | Until conversation ends (timeout or explicit closure) | • Slot filling across turns<br/>• Intent tracking<br/>• Multi-step workflows | Entire booking conversation collecting: dates → guests → room type → payment |
| **Persistent Context** | User preferences and patterns across multiple visits | Database (user profile) | Indefinite (across sessions) | • Personalization<br/>• Preference learning<br/>• Historical patterns | Guest always books sea-view rooms, prefers late checkout, allergic to down pillows |

### Context Management Flow

The following flowchart illustrates how the chatbot determines which context type to use when processing user messages:
```mermaid
flowchart TD
    Start([New User Message Received])
    
    Start --> CheckImmediate{Is this a follow-up to<br/>last 1-3 messages?}
    
    CheckImmediate -->|Yes| UseImmediate["Use IMMEDIATE CONTEXT<br/>━━━━━━━━━━━<br/>• Resolve pronouns<br/>• Continue current topic<br/>• Use recent entities"]
    
    CheckImmediate -->|No| CheckSession{Is there an active<br/>session with ongoing intent?}
    
    CheckSession -->|Yes| UseSession["Use SESSION CONTEXT<br/>━━━━━━━━━━━<br/>• Retrieve current intent<br/>• Access collected slots<br/>• Maintain dialog state"]
    
    CheckSession -->|No| CheckProfile{Does user profile<br/>exist in database?}
    
    CheckProfile -->|Yes| UsePersistent["Use PERSISTENT CONTEXT<br/>━━━━━━━━━━━<br/>• Load user preferences<br/>• Access booking history<br/>• Apply learned patterns"]
    
    CheckProfile -->|No| NewUser["Start Fresh<br/>━━━━━━━━━━━<br/>• No context available<br/>• Begin new session<br/>• Create user profile"]
    
    UseImmediate --> Process[Process Message with Retrieved Context]
    UseSession --> Process
    UsePersistent --> Process
    NewUser --> Process
    
    Process --> Store["Store New Context<br/>━━━━━━━━━━━<br/>• Update immediate buffer<br/>• Update session data<br/>• Update user profile"]
    
    Store --> End([Generate Response])
    
    style Start fill:#e3f2fd
    style CheckImmediate fill:#fff3e0
    style CheckSession fill:#fff3e0
    style CheckProfile fill:#fff3e0
    style UseImmediate fill:#c8e6c9
    style UseSession fill:#b3e5fc
    style UsePersistent fill:#f8bbd0
    style NewUser fill:#e0e0e0
    style Process fill:#ede7f6
    style Store fill:#fff9c4
    style End fill:#e3f2fd
```

### Technical Implementation

#### 1. Storing Conversational Context

**Data Structure Design:**
```
Immediate Context Buffer {
  messages: [
    { role: "user", content: "Do you have sea view rooms?", timestamp: T1 },
    { role: "bot", content: "Yes, we have deluxe sea view rooms.", timestamp: T2 },
    { role: "user", content: "Book it for me", timestamp: T3 }
  ],
  max_size: 3  // Keep only last 3 exchanges
}

Session Context {
  session_id: "sess_abc123xyz",
  user_id: "user_456",
  start_time: "2024-12-15T10:30:00Z",
  current_intent: "book_room",
  collected_entities: {
    check_in: "2024-12-20",
    check_out: "2024-12-23",
    room_type: "deluxe_sea_view",
    guests: 2,
    special_requests: []
  },
  dialog_state: "awaiting_payment_confirmation",
  conversation_history: [ /* all messages */ ]
}

Persistent Context (User Profile) {
  user_id: "user_456",
  personal_info: {
    name: "Sarah Chen",
    email: "sarah.chen@email.com",
    loyalty_tier: "gold"
  },
  preferences: {
    room_types: ["sea_view", "quiet_floors"],
    floor_preference: "high_floors",
    amenities: ["late_checkout", "hypoallergenic_pillows"],
    communication: "email"
  },
  booking_history: [
    { date: "2024-09-10", room: "deluxe_sea_view", satisfaction: 5 },
    { date: "2024-06-15", room: "deluxe_sea_view", satisfaction: 5 },
    { date: "2024-03-20", room: "suite_sea_view", satisfaction: 4 }
  ],
  learned_patterns: {
    typical_stay_duration: 3,
    booking_lead_time: 14,  // days in advance
    price_sensitivity: "moderate"
  }
}
```

#### 2. Context Retrieval and Usage

**Pseudocode for Context Selection:**
```pseudocode
FUNCTION retrieve_context(user_id, session_id, current_message):
    // 1. Always load immediate context (last few messages)
    immediate_context = get_last_n_messages(session_id, n=3)
    
    // 2. Check if immediate context is sufficient
    IF current_message contains pronouns (it, that, them):
        RETURN immediate_context
    
    // 3. Load session context if active intent exists
    session_context = get_session_data(session_id)
    IF session_context.current_intent != NULL:
        RETURN merge(immediate_context, session_context)
    
    // 4. Load persistent context for personalization
    user_profile = get_user_profile(user_id)
    IF user_profile.exists():
        RETURN merge(immediate_context, session_context, user_profile)
    
    // 5. New user - minimal context
    RETURN immediate_context

FUNCTION update_context(user_id, session_id, new_data):
    // Update immediate buffer
    append_to_buffer(session_id, new_data.message)
    
    // Update session context
    IF new_data.contains_entities():
        update_session_entities(session_id, new_data.entities)
    
    // Update persistent context
    IF new_data.indicates_preference():
        update_user_preferences(user_id, new_data.preferences)
    
    IF new_data.completes_booking():
        add_to_booking_history(user_id, new_data.booking_details)
```

#### 3. Implementation with Session IDs and User Profiles

**Session Management:**
```
Session Lifecycle:
1. Session Creation:
   - Generate unique session_id when user initiates conversation
   - Link to user_id if authenticated, or create anonymous session
   - Initialize session context with empty state

2. Session Maintenance:
   - Store session data in fast-access cache (Redis)
   - Set timeout: 30 minutes of inactivity
   - Extend timeout with each user interaction

3. Session Closure:
   - Explicit: User says "goodbye" or completes transaction
   - Implicit: Timeout expires
   - Archive session to database for analytics
   - Extract learnings to update user profile
```

**User Profile Management:**
```
Profile Lifecycle:
1. Profile Creation:
   - Created on first booking or account registration
   - Initialize with basic information
   - Empty preferences (to be learned)

2. Profile Updates:
   - After each completed booking: Add to history
   - During conversations: Extract stated preferences
   - Pattern recognition: Identify behavioral patterns
   - Incremental learning: Confidence scores for preferences

3. Profile Usage:
   - Load at session start for returning users
   - Reference during conversation for personalization
   - Used by recommendation engine
   - Privacy-compliant: User can view/edit/delete
```

### Context Distinction in Practice

**Example Scenario:**
```
Conversation Flow:

Turn 1:
User: "I want to book a room"
Bot: "I'd be happy to help! For how many nights?"
→ SESSION CONTEXT created: { intent: "book_room" }

Turn 2:
User: "Three nights"
Bot: "Great! What dates were you planning to visit?"
→ SESSION CONTEXT updated: { intent: "book_room", duration: 3 }

Turn 3:
User: "Starting December 15th"
Bot: "Perfect! What type of room would you prefer?"
→ SESSION CONTEXT updated: { ..., check_in: "Dec 15", check_out: "Dec 18" }

Turn 4:
User: "Do you have rooms with sea view?"
Bot: "Yes, we have deluxe rooms with sea view available for Dec 15-18."
→ Uses SESSION CONTEXT to reference dates
→ Queries availability system

Turn 5:
User: "Book it"
Bot: "I'll book the deluxe sea view room for you..."
→ Uses IMMEDIATE CONTEXT: "it" = deluxe sea view room (from Turn 4)
→ Uses SESSION CONTEXT: dates, duration from earlier turns

--- Session Ends ---

Two Weeks Later:

Turn 1 (New Session):
User: "Hi, I'd like to book another room"
Bot: "Welcome back, Sarah! I see you enjoyed the sea view room last time. 
     Would you like another sea view room?"
→ Uses PERSISTENT CONTEXT: name, previous booking preference
→ Creates new SESSION CONTEXT for this booking
```

### Key Benefits of This Approach

| Benefit | Description |
|---------|-------------|
| **Coherent Conversations** | Immediate context enables natural follow-ups without repetition |
| **Multi-Turn Workflows** | Session context maintains state across complex interactions |
| **Personalization** | Persistent context enables tailored recommendations |
| **Scalability** | Tiered storage (memory → cache → database) optimizes performance |
| **Privacy Control** | Clear separation allows selective data retention policies |

---

