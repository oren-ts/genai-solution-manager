# FlutterFlow Teilprüfung 1 - Event App Development

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
