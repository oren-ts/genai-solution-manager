# FlutterFlow Teilprüfung 1 - Event App Development

**Student:** Oren  
**Course:** GenAI Solution Manager Bootcamp  
**Section:** K4.0082_2.0 - FlutterFlow Development  
**Date:** November 16, 2025

---

## Section (a): Data Model Design

### Overview

The event app data structure is built on three main entities: **Event**, **User**, and **Ticket**. By combining these entities, users can attend and purchase tickets to multiple events. The User data structure supports different roles with varying access levels and app configurations (e.g., organizers can create new events or modify ticket types, while attendees can browse and purchase).

### Creation Order

**Implementation sequence:**
1. **Enums first:** EventCategory, UserRole, TicketType
2. **Custom Data Types second:** Event, User, Ticket

**Reasoning:** Custom Data Types use Enums as field types. Therefore, Enums must be created first so that Custom Data Types can reference them during field configuration.

---

### Enums

#### EventCategory
**Values:** conference, workshop, concert, sports, networking

**Purpose:** Defines the available event categories. Using an enum ensures type safety and prevents typos or inconsistent category names across the application.

#### UserRole
**Values:** attendee, organizer, admin, speaker

**Purpose:** Defines the types of users who can interact with the app. Using an enum restricts roles to these predefined values, ensuring proper access control and preventing invalid role assignments.

#### TicketType
**Values:** early, regular, vip, student

**Purpose:** Defines the ticket types the app currently supports. Using an enum prevents typo mistakes and ensures consistency when assigning ticket types to events or purchases.

---

### Custom Data Types

#### Event
| Field Name | Data Type | Explanation |
|------------|-----------|-------------|
| eventId | String | A unique identifier for each event |
| title | String | The event's display name |
| description | String | Detailed information about the event |
| category | EventCategory | Event classification using predefined enum values |
| startDate | DateTime | Allows flexible date formatting, comparison, and calculations (e.g., "days until event") |
| endDate | DateTime | Event conclusion timestamp |
| maxAttendees | Integer | Maximum capacity for the event |
| currentAttendees | Integer | Tracks the current number of registered attendees; can trigger "sold out" status when it reaches maxAttendees |
| isActive | Boolean | Indicates whether the event is currently available for registration |
| ticketTypes | List\<TicketType\> | Allows each event to offer multiple ticket type options (e.g., Event A offers VIP and Student; Event B offers Early Bird and Regular) |

#### User
| Field Name | Data Type | Explanation |
|------------|-----------|-------------|
| userId | String | Unique identifier for each user |
| firstName | String | User's first name |
| lastName | String | User's last name |
| email | String | User's email address |
| role | UserRole | User's role assignment using predefined enum values |
| registeredEvents | List\<String\> | Stores event IDs for all events the user has registered for |
| preferences | String | User's personal preferences (theme, notifications, etc.) |

#### Ticket
| Field Name | Data Type | Explanation |
|------------|-----------|-------------|
| ticketId | String | Unique identifier for each ticket |
| eventId | String | Links this ticket to a specific Event (foreign key relationship) |
| userId | String | Links this ticket to a specific User (foreign key relationship) |
| ticketType | TicketType | The type of ticket purchased (early, regular, vip, student) |
| purchaseDate | DateTime | Timestamp of when the ticket was purchased |
| price | Double | The actual purchase price (allows for discounted pricing scenarios) |
| isValid | Boolean | Indicates whether the ticket is still valid (supports ticket cancellation) |

---

### Data Relationships

The three Custom Data Types connect through unique identifier fields:

**User ↔ Event Connection:**
- The User's `registeredEvents` field (List\<String\>) stores event IDs
- This creates a one-to-many relationship: one user can register for multiple events

**Ticket as the Bridge:**
- Each Ticket contains both `eventId` and `userId` fields
- This creates a many-to-many relationship between Users and Events
- The Ticket represents a specific user's registration for a specific event with a specific ticket type

**Example Flow:**
1. User "U123" wants to attend Event "E456"
2. User selects "VIP" ticket type from Event's available ticketTypes
3. System creates Ticket with: ticketId="T789", eventId="E456", userId="U123", ticketType="vip"
4. Event's currentAttendees count increases by 1
5. User's registeredEvents list adds "E456"

This relational structure allows the app to:
- Find all events a user has registered for (search User.registeredEvents)
- Find all attendees for a specific event (search all Tickets where eventId matches)
- Track individual ticket purchases with pricing and validity status

---

## Section (b): State Management Architecture

### Overview

State management is crucial for determining which data persists across the application versus which data remains temporary. This architectural decision directly impacts both user experience and application memory efficiency. App-level state ensures consistent data availability throughout the user's session, while page-level state provides context-specific functionality without unnecessary data persistence.

### App State Variables

App State maintains data across the entire application lifecycle and remains accessible from any page within the app. The following variables are defined at the app level:

| Variable Name | Data Type | Persistent | Reasoning |
|--------------|-----------|------------|-----------|
| currentUser | User | ✓ Yes | Keeps users logged in across sessions, reducing friction and frustration from repeated login requirements |
| userPreferences | UserPreferences | ✓ Yes | Preserves user-selected theme, language, and notification settings to provide a consistent, personalized experience |
| favoriteEvents | List\<String\> | ✓ Yes | Maintains the user's curated list of favorite events, eliminating the need to re-select favorites after each session |
| cartItems | List\<Ticket\> | ✗ No | Intentionally cleared on app restart to prevent accidental purchases of tickets users may have forgotten about or for events that might have sold out |

### Persistence Decision Rationale

**Persistent State (Survives App Restart):**

The following data is saved to device storage and survives app restarts, providing continuity in the user experience:

- **currentUser:** Maintaining login state eliminates repeated authentication friction. Users expect to remain logged in unless they explicitly log out. This is standard practice for modern mobile applications and significantly improves user satisfaction.

- **userPreferences:** Theme selection (light/dark mode), language preference, and notification settings are personal choices that should persist. Re-configuring these settings on every app launch would create unnecessary friction and poor UX.

- **favoriteEvents:** Users invest time in curating their favorite events. Losing this data on app restart would be frustrating and could lead to users abandoning the favoriting feature entirely.

**Non-Persistent State (Cleared on App Restart):**

The following data is intentionally cleared when the app closes, prioritizing safety and clean user experience:

- **cartItems:** Shopping carts are cleared on app restart as a safety mechanism. This prevents several negative scenarios:
  - Users accidentally purchasing tickets they added days ago but forgot about
  - Users purchasing tickets for events that sold out while the cart sat dormant
  - Stale pricing information (if ticket prices changed)
  - Cart containing tickets for past events
  
  Users who genuinely want to purchase tickets will complete the transaction in the same session, while clearing the cart protects against unintended purchases.

### Page State Variables (EventListPage)

Page State maintains temporary data that only exists while the user is on a specific page. When the user navigates away from the page, this data automatically resets, providing a clean slate upon return.

| Variable Name | Data Type | Purpose |
|--------------|-----------|---------|
| selectedCategory | EventCategory | Filters the event list to show only events matching the selected category (conference, workshop, concert, sports, or networking) |
| searchQuery | String | Stores the user's free-text search input to filter events by keywords in title or description |
| currentPage | Integer | Tracks pagination state when browsing through multiple pages of event results |
| isGridView | Boolean | Toggles the display layout between grid view (card-based) and list view (row-based) for event presentation |
| filteredEvents | List\<Event\> | Contains the dynamically filtered event results based on the combination of selectedCategory, searchQuery, and other applied filters |

### User Experience Impact

**Scenario: User Journey Example**

**Day 1 - Initial Session:**
1. User logs in → `currentUser` saved to device storage (persistent)
2. User navigates to settings and selects dark theme → `userPreferences` updated and saved (persistent)
3. User browses events and adds 3 events to favorites → `favoriteEvents` list updated and saved (persistent)
4. User adds 2 concert tickets to cart → `cartItems` stored in memory only (non-persistent)
5. User navigates to EventListPage and searches for "conference" → `searchQuery` stored as page state
6. User selects "networking" category filter → `selectedCategory` updated as page state
7. User closes the app completely

**Day 2 - User Returns:**
- ✓ **Still logged in:** `currentUser` data persisted → user immediately accesses their account
- ✓ **Dark theme active:** `userPreferences` persisted → app opens in their preferred dark mode
- ✓ **Favorites intact:** `favoriteEvents` persisted → all 3 favorited events still visible in favorites list
- ✗ **Cart is empty:** `cartItems` cleared → fresh cart prevents accidental purchases
- ✗ **Search cleared:** `searchQuery` reset → clean browsing experience with no stale filters
- ✗ **Category filter reset:** `selectedCategory` reset → user sees all event categories by default

**UX Benefits Analysis:**

**Persistent Login (currentUser):**
- Reduces friction: Users authenticate once and maintain access across sessions
- Industry standard: Matches user expectations from other modern apps
- Security balance: Provides convenience while still requiring re-authentication after extended inactivity (handled by authentication tokens)

**Persistent Preferences (userPreferences):**
- Personalization: App remembers user's visual and functional preferences
- Consistency: Every app launch reflects the user's choices
- Accessibility: Particularly important for users who require specific themes (e.g., dark mode for light sensitivity)

**Persistent Favorites (favoriteEvents):**
- Investment protection: Users spent time curating their favorites; data should be preserved
- Quick access: Enables rapid access to preferred events across sessions
- Engagement: Encourages users to build a personalized event collection

**Non-Persistent Cart (cartItems):**
- Safety mechanism: Prevents accidental purchases of forgotten items
- Data freshness: Ensures users review current availability and pricing before purchase
- Clean slate: Each shopping session starts fresh, reducing confusion
- Business logic: Aligns with the transactional nature of ticket purchases (intended to be completed in one session)

**Non-Persistent Page State (search/filters):**
- Clean browsing: Each visit to EventListPage starts with a neutral, unfiltered view
- Discoverability: Users can discover new event categories without being locked into previous filters
- Context reset: Page-specific state shouldn't carry over when navigating away and returning

### State Scope Decisions

**Why App State for User Data?**

The `currentUser` object needs to be accessible throughout the entire application because:
- Multiple pages require user information (profile display, authentication checks, personalized content)
- User role determines access permissions across different features
- User preferences affect the behavior of many components app-wide

Storing this in App State eliminates the need to pass user data through navigation parameters or fetch it repeatedly from storage.

**Why Page State for Filters and Display Preferences?**

Search queries, category filters, and display preferences (like `isGridView`) are **context-specific** to the EventListPage:
- These settings are only relevant when actively browsing the event list
- Different pages may have different filtering needs
- Resetting these values when leaving the page provides a clean, predictable browsing experience
- Users expect to start fresh when returning to a list view

**Trade-offs Considered:**

**isGridView Display Preference:**
The current implementation uses Page State for the grid/list view toggle, which resets to the default view each session. This design choice prioritizes **consistency** (all users see the same default layout initially).

*Alternative approach:* This could be moved to App State (persistent) or even a field in `userPreferences` if user research indicates that power users prefer to maintain their display preference permanently. The decision depends on:
- User feedback and analytics on view-switching behavior
- Whether the default view provides better discoverability for most users
- Product goals (consistency vs. personalization)

This represents a product decision that can be revisited based on real user behavior data.

---
