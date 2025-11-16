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

## Section (d): Complex Control Flow Logic

### Overview

Complex control flow logic enables the event app to handle sophisticated business rules, dynamic data loading, and conditional calculations. This section demonstrates three critical implementation patterns: multi-condition validation, iterative data loading with different loop types, and dynamic price calculation based on multiple factors.

### 1. Event Registration with Multiple Conditions

#### Business Requirements

When a user attempts to register for an event, the system must verify four critical conditions before allowing registration:

1. **Authentication Status:** User must be logged in (currentUser exists in App State)
2. **Event Availability:** Event must be active (Event.isActive == true)
3. **Capacity Check:** Seats must be available (Event.currentAttendees < Event.maxAttendees)
4. **Duplicate Prevention:** User must not already be registered (Event.eventId not in User.registeredEvents)

#### Implementation Approach: Sequential Validation with Specific Feedback

**Design Decision:** Use **nested conditional checks** (Option B) rather than a single combined AND statement (Option A).

**Rationale:**
- **User Experience:** Each failed condition provides specific, actionable feedback rather than a generic error
- **Debugging:** Easier to identify which condition failed during testing
- **Maintainability:** Clear separation of concerns makes logic easier to modify
- **User Guidance:** Specific error messages help users understand what they need to do (e.g., "Please log in" vs. "Registration failed")

#### Conditional Logic Flow

```
User clicks "Register for Event" button
↓
Trigger: On Button Click Action

Check 1: Authentication
IF currentUser == null OR currentUser is not set:
  → Display error: "Please log in to register for events"
  → STOP (do not proceed)

Check 2: Event Status
ELSE IF Event.isActive == false:
  → Display error: "This event is no longer available for registration"
  → STOP

Check 3: Capacity
ELSE IF Event.currentAttendees >= Event.maxAttendees:
  → Display error: "Sorry, this event is sold out"
  → STOP

Check 4: Duplicate Registration
ELSE IF Event.eventId exists in currentUser.registeredEvents:
  → Display error: "You are already registered for this event"
  → STOP

All Checks Passed:
ELSE:
  → Create new Ticket record
  → Add Event.eventId to currentUser.registeredEvents
  → Increment Event.currentAttendees by 1
  → Display success: "Registration successful!"
```

#### Error Message Design

Each error message serves a specific purpose:

| Condition Failed | Error Message | User Action Enabled |
|-----------------|---------------|---------------------|
| Not logged in | "Please log in to register for events" | Redirect to login page |
| Event inactive | "This event is no longer available for registration" | Browse other events |
| Sold out | "Sorry, this event is sold out" | Add to waitlist (future feature) |
| Already registered | "You are already registered for this event" | View ticket details |

#### Timing of Validation

**Validation occurs AFTER button click** rather than before (e.g., disabling button preemptively).

**Reasoning:**
- **Data freshness:** Conditions could change between page load and button click (event could sell out)
- **User trigger:** Validation happens at the moment of user intent
- **Real-time accuracy:** Always checking against current database state
- **Clear feedback:** User receives immediate response to their action

**Optional Enhancement:** Button could show a loading state during validation to indicate processing.

---

### 2. Dynamic Event Loading with Loops

#### Business Requirements

The app must load events from an API in an organized, efficient manner:
- Group events by category (conference, workshop, concert, sports, networking)
- Support pagination for large result sets
- Respect maximum event limits to avoid overwhelming users
- Handle cases where some categories have no events

#### Loop Type Selection

Different loop structures serve different purposes based on what is known at design time:

**FOR EACH Loop (Category Iteration):**
- **Use Case:** Iterating through EventCategory enum values
- **Reason:** We have a **fixed, known list** of exactly 5 categories
- **Advantage:** Clean, readable syntax for finite collections
- **FlutterFlow Implementation:** "Generate Dynamic Children" with EventCategory enum as source

**WHILE Loop (Pagination):**
- **Use Case:** Loading paginated event results until condition met
- **Reason:** We **don't know in advance** how many pages exist for each category
- **Advantage:** Continues until **dynamic stopping condition** (maxEvents reached OR no more results)
- **FlutterFlow Implementation:** Action loop with conditional break

#### Implementation Logic

```
Initialize: 
- allEvents = empty list
- maxEventsPerCategory = 20

FOR EACH category IN EventCategory enum values:
  ↓
  Initialize pagination for this category:
  - currentPage = 1
  - categoryEvents = empty list
  - moreResultsAvailable = true
  
  WHILE (categoryEvents.length < maxEventsPerCategory AND moreResultsAvailable):
    ↓
    API Call:
    - Endpoint: /api/events
    - Parameters: 
      * category = current category
      * page = currentPage
      * pageSize = 10
    
    Response Processing:
    - pageResults = API response events
    
    IF pageResults is empty:
      → moreResultsAvailable = false
      → BREAK (exit while loop, move to next category)
    
    ELSE:
      → Add pageResults to categoryEvents
      → currentPage = currentPage + 1
      
      IF categoryEvents.length >= maxEventsPerCategory:
        → BREAK (limit reached for this category)
  
  END WHILE
  
  Add categoryEvents to allEvents
  
END FOR EACH

Result: allEvents now contains up to maxEventsPerCategory events for each of the 5 categories
```

#### Loop Type Justification

**Why FOR EACH for categories?**
- **Known collection:** EventCategory enum has exactly 5 values defined at design time
- **Predictable iteration:** Must process all categories exactly once
- **Code clarity:** Intent is clear - "process each category"

**Why WHILE for pagination?**
- **Unknown iteration count:** Number of pages varies by category and changes over time
- **Conditional continuation:** Keep going until a condition fails (no more results OR limit reached)
- **Dynamic stopping:** Can't use FOR loop because total page count is unknown

**Engineering Principle:** "Start simple first, complication is easy" - use the simplest loop structure that fits the use case.

---

### 3. Ticket Price Calculation with Conditional Values

#### Business Requirements

Calculate ticket price dynamically based on ticket type, with clear discount/premium rules:

**Base Price:** Each event has an Event.basePrice (e.g., €100)

**Price Modifiers by Ticket Type:**
- **Early Bird:** -20% (€80 for €100 base)
- **Student:** -50% (€50 for €100 base)
- **VIP:** +100% (€200 for €100 base)
- **Regular:** No modification (€100 for €100 base)

#### Implementation Approach: Simple Conditional Logic

**Design Philosophy:** Start with straightforward ticket type-based pricing. Complexity (date-based early bird windows, role verification, discount stacking) can be added incrementally if business rules require it.

#### Calculation Logic

```
FUNCTION calculateTicketPrice(basePrice, ticketType):
  
  Input Validation:
  IF basePrice <= 0:
    → Return error: "Invalid base price"
  
  Price Calculation:
  
  IF ticketType == TicketType.early:
    finalPrice = basePrice × 0.8
    discount = "20% Early Bird discount applied"
  
  ELSE IF ticketType == TicketType.student:
    finalPrice = basePrice × 0.5
    discount = "50% Student discount applied"
  
  ELSE IF ticketType == TicketType.vip:
    finalPrice = basePrice × 2.0
    premium = "VIP upgrade: +100%"
  
  ELSE IF ticketType == TicketType.regular:
    finalPrice = basePrice
    discount = "Standard pricing"
  
  ELSE:
    → Return error: "Invalid ticket type"
  
  RETURN {
    originalPrice: basePrice,
    finalPrice: finalPrice,
    modifier: discount OR premium,
    savings: basePrice - finalPrice (if discount applied)
  }
```

#### Example Calculations

| Event Base Price | Ticket Type | Calculation | Final Price | Modifier |
|-----------------|-------------|-------------|-------------|----------|
| €100 | Early Bird | 100 × 0.8 | €80 | -20% |
| €100 | Student | 100 × 0.5 | €50 | -50% |
| €100 | VIP | 100 × 2.0 | €200 | +100% |
| €100 | Regular | 100 × 1.0 | €100 | 0% |
| €50 | Student | 50 × 0.5 | €25 | -50% |
| €200 | VIP | 200 × 2.0 | €400 | +100% |

#### User Experience Considerations

**Price Transparency:**
- Always display both original price and final price when discounts apply
- Show savings amount: "You save €50 with your Student discount"
- For VIP, clarify premium value: "VIP access includes exclusive perks"

**Ticket Type Selection:**
- Only show ticket types that are currently available for the event
- Validate user eligibility (e.g., require student verification for student tickets)
- Clearly label early bird availability window

#### Future Complexity Considerations

**The current simple implementation can be extended to handle:**

**Time-Based Early Bird:**
```
IF ticketType == TicketType.early:
  IF current_date > event.earlyBirdDeadline:
    → Show error: "Early bird period has ended"
    → Suggest: "Regular tickets are still available"
  ELSE:
    → Apply 20% discount
```

**User Role Verification:**
```
IF ticketType == TicketType.student:
  IF currentUser.role != UserRole.student:
    → Require student verification
    → Show: "Please verify your student status"
  ELSE:
    → Apply 50% discount
```

**Discount Stacking:**
```
IF ticketType == TicketType.early AND currentUser.role == UserRole.student:
  → Apply best available discount (50% student) OR
  → Stack discounts (20% + additional 30%) depending on business rules
  → Requires policy decision
```

**Engineering Principle Applied:** "Complication is easy - start simple first." Begin with clear, maintainable logic that handles the core use case. Add complexity only when business requirements demand it, and add it incrementally with proper testing at each stage.

---

### Control Flow Best Practices Demonstrated

**1. User-Centered Error Handling:**
- Specific error messages guide users toward resolution
- Sequential validation provides clear feedback at each decision point
- Errors explain both what went wrong and what the user should do

**2. Appropriate Loop Selection:**
- FOR EACH for known, finite collections (categories)
- WHILE for unknown, conditional iterations (pagination)
- Choice driven by what is known at design time vs. runtime

**3. Maintainable Conditional Logic:**
- Clear, readable IF-ELSE chains
- Each condition handles one concern
- Easy to extend with new ticket types or validation rules

**4. Scalable Architecture:**
- Simple foundation that can grow in complexity
- Each component (validation, loading, pricing) is independently testable
- Clear separation between business logic and UI

---

## Section (c): Multi-Step Registration Form

### Overview

The user registration process is implemented as a progressive, multi-step form within a single page. This approach breaks down the registration into three manageable steps, reducing cognitive load and improving completion rates by presenting information sequentially rather than overwhelming users with a long form. Each step focuses on a specific category of information, with validation ensuring data quality before progression.

### Form Structure

The registration form consists of three distinct steps, all contained within a single FlutterFlow page using conditional visibility:

#### Step 1: Personal Data
**Purpose:** Collect core user identification information

**Fields:**
- **Name** (TextField)
  - Validation: Required field
  - Error message: "Name is required"
  
- **Email** (TextField with Email validator)
  - Validation: Required + valid email format
  - Format check: Must contain @ symbol and valid domain
  - Error message: "Please enter a valid email address"

**Next Button Behavior:** Validates both fields before allowing progression to Step 2

---

#### Step 2: Event Preferences
**Purpose:** Collect user's event interests and communication preferences

**Fields:**
- **Event Categories** (Multi-select component)
  - Options: Conference, Workshop, Concert, Sports, Networking
  - Allows users to select multiple categories of interest
  - Validation: At least one category must be selected
  
- **Notifications** (Toggle/Switch)
  - Boolean choice: Enable or disable event notifications
  - Default value: Can be set to true (opt-in) or false (opt-out)

**Navigation:**
- **Back Button:** Returns to Step 1 without validation
- **Next Button:** Validates selections before moving to Step 3

---

#### Step 3: Confirmation and Summary
**Purpose:** Allow users to review their registration details before final submission

**Display Elements:**
- **Summary Section:** Shows all collected data for review
  - Personal Data: Name, Email
  - Selected Categories: List of chosen event types
  - Notification Preference: Enabled/Disabled status
  
- **Edit Option:** Users can click "Back" to modify any information

**Final Action:**
- **Complete Registration Button:** 
  - Saves all data to the database (User data type)
  - Shows success confirmation
  - Navigates to main app experience or home page

---

### State Management - registrationStep Variable

**Page State Variable:**
- **Name:** `registrationStep`
- **Type:** Integer
- **Possible Values:** 0, 1, 2
- **Initial Value:** 0 (Step 1)

**Purpose:** Acts as a controller that determines which step container is currently visible to the user.

**Value Mapping:**
- `registrationStep = 0` → Step 1 (Personal Data) visible
- `registrationStep = 1` → Step 2 (Preferences) visible
- `registrationStep = 2` → Step 3 (Confirmation) visible

**How It Works:**
Each step container has a conditional visibility expression:
- Step 1 container: Show when `registrationStep == 0`
- Step 2 container: Show when `registrationStep == 1`
- Step 3 container: Show when `registrationStep == 2`

Only ONE container is visible at any time, creating the illusion of step progression while remaining on a single page.

---

### Validation Strategy

Validation ensures data quality and prevents users from progressing with incomplete or invalid information.

#### Step 1: Personal Data Validation

**Name Field:**
- **Validation Type:** Required field check
- **Implementation:** TextField's "Required" property enabled
- **Trigger:** On "Next" button click
- **Behavior if invalid:**
  - Error message appears below field: "Name is required"
  - registrationStep remains at 0
  - User cannot advance to Step 2

**Email Field:**
- **Validation Type:** Required + Email format
- **Implementation:** TextField's Email validator
- **Format Requirements:** 
  - Must contain @ symbol
  - Must have valid domain structure (e.g., user@domain.com)
- **Auto-validation:** FlutterFlow's built-in email validator checks format automatically
- **Trigger:** On "Next" button click
- **Behavior if invalid:**
  - Error message appears: "Please enter a valid email address"
  - registrationStep remains at 0
  - User cannot advance to Step 2

**Combined Validation:**
- BOTH fields must be valid for "Next" button to increment registrationStep
- If either field is invalid, errors display and progression is blocked

#### Step 2: Preferences Validation

**Event Categories:**
- **Validation Type:** At least one selection required
- **Trigger:** On "Next" button click
- **Behavior if invalid:**
  - Error message: "Please select at least one event category"
  - registrationStep remains at 1

**Notifications Toggle:**
- **No validation required** - Boolean value always valid (true or false)

#### Step 3: Confirmation

**No validation required** - This is a review-only step. All data has already been validated in previous steps.

---

### Navigation Logic

Navigation between steps is controlled by button actions that update the `registrationStep` variable with validation checks.

#### "Next" Button Behavior

**Step 1 → Step 2:**
```
Action: On "Next" button click
1. Validate Name field (required check)
2. Validate Email field (required + format check)
3. IF both valid:
     Update State: registrationStep = 1
   ELSE:
     Display error messages on invalid fields
     registrationStep remains 0
```

**Step 2 → Step 3:**
```
Action: On "Next" button click
1. Validate at least one category selected
2. IF valid:
     Update State: registrationStep = 2
   ELSE:
     Display error message
     registrationStep remains 1
```

#### "Back" Button Behavior

**No validation when going backward** - Users should be able to freely return to previous steps to review or edit information without restrictions.

**Step 2 → Step 1:**
```
Action: On "Back" button click
Update State: registrationStep = registrationStep - 1 (becomes 0)
```

**Step 3 → Step 2:**
```
Action: On "Back" button click
Update State: registrationStep = registrationStep - 1 (becomes 1)
```

**Step 1 Back Button:**
- **Hidden or Disabled** when registrationStep = 0
- Prevents registrationStep from becoming negative
- UX consideration: First step has no previous step to return to

#### "Complete Registration" Button (Step 3 only)

```
Action: On "Complete Registration" button click
1. Create User record in database with collected data:
   - firstName: [name entered]
   - lastName: [if collected]
   - email: [email entered]
   - preferences: [selected categories and notification setting]
2. Update App State: currentUser = newly created User
3. Show success message: "Registration successful!"
4. Navigate to: Main app page or user dashboard
```

---

### Progress Indicator Implementation

A visual progress indicator helps users understand how far they've progressed through the registration process.

**Calculation Formula:**
```
Progress Percentage = ((registrationStep + 1) / totalSteps) × 100
```

Where:
- `registrationStep` = current step (0, 1, or 2)
- `totalSteps` = 3 (total number of steps)

**Progress Values:**

| Current Step | registrationStep Value | Calculation | Progress % |
|-------------|----------------------|-------------|-----------|
| Step 1 (Personal Data) | 0 | (0 + 1) / 3 × 100 | 33% |
| Step 2 (Preferences) | 1 | (1 + 1) / 3 × 100 | 66% |
| Step 3 (Confirmation) | 2 | (2 + 1) / 3 × 100 | 100% |

**Visual Implementation:**
- Linear progress bar component
- Value bound to the calculated percentage
- Updates automatically when registrationStep changes
- Optional: Display text "Step X of 3" alongside progress bar

---

### Conditional Button Labels

Button labels change based on the current step to provide clear context about the action being performed.

**Implementation Logic:**

**"Next" Button (Steps 1 & 2):**
```
Conditional Display:
IF registrationStep < 2:
  Button Text = "Next"
  Button Visible = True
ELSE:
  Button Visible = False
```

**"Complete Registration" Button (Step 3 only):**
```
Conditional Display:
IF registrationStep == 2:
  Button Text = "Complete Registration"
  Button Visible = True
ELSE:
  Button Visible = False
```

**Reasoning:**
- **"Next"** indicates more steps remain (Steps 1 & 2)
- **"Complete Registration"** clearly signals the final action (Step 3)
- Different labels prevent user confusion about whether the form is finished
- Explicit completion terminology increases user confidence when submitting

---

### User Experience Benefits

**Progressive Disclosure:**
- Reduces cognitive load by presenting information in digestible chunks
- Users focus on one category of information at a time
- Less overwhelming than a single long form

**Validation Feedback:**
- Immediate error messages prevent invalid data submission
- Users correct errors before moving forward
- Reduces frustration of discovering errors after lengthy form completion

**Review Before Submission:**
- Step 3 confirmation allows users to verify their information
- Reduces registration errors and support requests
- Builds user confidence before final commitment

**Progress Transparency:**
- Visual progress indicator shows users how much remains
- Encourages completion by showing advancement
- Reduces form abandonment rates

**Flexible Navigation:**
- Back button allows users to edit previous responses
- No validation penalty when reviewing earlier steps
- Accommodates users who change their minds or notice errors

---

---

## Section (d): Complex Control Flow Logic
## Section (d): Complex Control Flow Logic

### Overview

Complex control flow logic enables the event app to handle sophisticated business rules, dynamic data loading, and conditional calculations. This section demonstrates three critical implementation patterns: multi-condition validation, iterative data loading with different loop types, and dynamic price calculation based on multiple factors.

### 1. Event Registration with Multiple Conditions

#### Business Requirements

When a user attempts to register for an event, the system must verify four critical conditions before allowing registration:

1. **Authentication Status:** User must be logged in (currentUser exists in App State)
2. **Event Availability:** Event must be active (Event.isActive == true)
3. **Capacity Check:** Seats must be available (Event.currentAttendees < Event.maxAttendees)
4. **Duplicate Prevention:** User must not already be registered (Event.eventId not in User.registeredEvents)

#### Implementation Approach: Sequential Validation with Specific Feedback

**Design Decision:** Use **nested conditional checks** (Option B) rather than a single combined AND statement (Option A).

**Rationale:**
- **User Experience:** Each failed condition provides specific, actionable feedback rather than a generic error
- **Debugging:** Easier to identify which condition failed during testing
- **Maintainability:** Clear separation of concerns makes logic easier to modify
- **User Guidance:** Specific error messages help users understand what they need to do (e.g., "Please log in" vs. "Registration failed")

#### Conditional Logic Flow

```
User clicks "Register for Event" button
↓
Trigger: On Button Click Action

Check 1: Authentication
IF currentUser == null OR currentUser is not set:
  → Display error: "Please log in to register for events"
  → STOP (do not proceed)

Check 2: Event Status
ELSE IF Event.isActive == false:
  → Display error: "This event is no longer available for registration"
  → STOP

Check 3: Capacity
ELSE IF Event.currentAttendees >= Event.maxAttendees:
  → Display error: "Sorry, this event is sold out"
  → STOP

Check 4: Duplicate Registration
ELSE IF Event.eventId exists in currentUser.registeredEvents:
  → Display error: "You are already registered for this event"
  → STOP

All Checks Passed:
ELSE:
  → Create new Ticket record
  → Add Event.eventId to currentUser.registeredEvents
  → Increment Event.currentAttendees by 1
  → Display success: "Registration successful!"
```

#### Error Message Design

Each error message serves a specific purpose:

| Condition Failed | Error Message | User Action Enabled |
|-----------------|---------------|---------------------|
| Not logged in | "Please log in to register for events" | Redirect to login page |
| Event inactive | "This event is no longer available for registration" | Browse other events |
| Sold out | "Sorry, this event is sold out" | Add to waitlist (future feature) |
| Already registered | "You are already registered for this event" | View ticket details |

#### Timing of Validation

**Validation occurs AFTER button click** rather than before (e.g., disabling button preemptively).

**Reasoning:**
- **Data freshness:** Conditions could change between page load and button click (event could sell out)
- **User trigger:** Validation happens at the moment of user intent
- **Real-time accuracy:** Always checking against current database state
- **Clear feedback:** User receives immediate response to their action

**Optional Enhancement:** Button could show a loading state during validation to indicate processing.

---

### 2. Dynamic Event Loading with Loops

#### Business Requirements

The app must load events from an API in an organized, efficient manner:
- Group events by category (conference, workshop, concert, sports, networking)
- Support pagination for large result sets
- Respect maximum event limits to avoid overwhelming users
- Handle cases where some categories have no events

#### Loop Type Selection

Different loop structures serve different purposes based on what is known at design time:

**FOR EACH Loop (Category Iteration):**
- **Use Case:** Iterating through EventCategory enum values
- **Reason:** We have a **fixed, known list** of exactly 5 categories
- **Advantage:** Clean, readable syntax for finite collections
- **FlutterFlow Implementation:** "Generate Dynamic Children" with EventCategory enum as source

**WHILE Loop (Pagination):**
- **Use Case:** Loading paginated event results until condition met
- **Reason:** We **don't know in advance** how many pages exist for each category
- **Advantage:** Continues until **dynamic stopping condition** (maxEvents reached OR no more results)
- **FlutterFlow Implementation:** Action loop with conditional break

#### Implementation Logic

```
Initialize: 
- allEvents = empty list
- maxEventsPerCategory = 20

FOR EACH category IN EventCategory enum values:
  ↓
  Initialize pagination for this category:
  - currentPage = 1
  - categoryEvents = empty list
  - moreResultsAvailable = true
  
  WHILE (categoryEvents.length < maxEventsPerCategory AND moreResultsAvailable):
    ↓
    API Call:
    - Endpoint: /api/events
    - Parameters: 
      * category = current category
      * page = currentPage
      * pageSize = 10
    
    Response Processing:
    - pageResults = API response events
    
    IF pageResults is empty:
      → moreResultsAvailable = false
      → BREAK (exit while loop, move to next category)
    
    ELSE:
      → Add pageResults to categoryEvents
      → currentPage = currentPage + 1
      
      IF categoryEvents.length >= maxEventsPerCategory:
        → BREAK (limit reached for this category)
  
  END WHILE
  
  Add categoryEvents to allEvents
  
END FOR EACH

Result: allEvents now contains up to maxEventsPerCategory events for each of the 5 categories
```

#### Loop Type Justification

**Why FOR EACH for categories?**
- **Known collection:** EventCategory enum has exactly 5 values defined at design time
- **Predictable iteration:** Must process all categories exactly once
- **Code clarity:** Intent is clear - "process each category"

**Why WHILE for pagination?**
- **Unknown iteration count:** Number of pages varies by category and changes over time
- **Conditional continuation:** Keep going until a condition fails (no more results OR limit reached)
- **Dynamic stopping:** Can't use FOR loop because total page count is unknown

**Engineering Principle:** "Start simple first, complication is easy" - use the simplest loop structure that fits the use case.

---

### 3. Ticket Price Calculation with Conditional Values

#### Business Requirements

Calculate ticket price dynamically based on ticket type, with clear discount/premium rules:

**Base Price:** Each event has an Event.basePrice (e.g., €100)

**Price Modifiers by Ticket Type:**
- **Early Bird:** -20% (€80 for €100 base)
- **Student:** -50% (€50 for €100 base)
- **VIP:** +100% (€200 for €100 base)
- **Regular:** No modification (€100 for €100 base)

#### Implementation Approach: Simple Conditional Logic

**Design Philosophy:** Start with straightforward ticket type-based pricing. Complexity (date-based early bird windows, role verification, discount stacking) can be added incrementally if business rules require it.

#### Calculation Logic

```
FUNCTION calculateTicketPrice(basePrice, ticketType):
  
  Input Validation:
  IF basePrice <= 0:
    → Return error: "Invalid base price"
  
  Price Calculation:
  
  IF ticketType == TicketType.early:
    finalPrice = basePrice × 0.8
    discount = "20% Early Bird discount applied"
  
  ELSE IF ticketType == TicketType.student:
    finalPrice = basePrice × 0.5
    discount = "50% Student discount applied"
  
  ELSE IF ticketType == TicketType.vip:
    finalPrice = basePrice × 2.0
    premium = "VIP upgrade: +100%"
  
  ELSE IF ticketType == TicketType.regular:
    finalPrice = basePrice
    discount = "Standard pricing"
  
  ELSE:
    → Return error: "Invalid ticket type"
  
  RETURN {
    originalPrice: basePrice,
    finalPrice: finalPrice,
    modifier: discount OR premium,
    savings: basePrice - finalPrice (if discount applied)
  }
```

#### Example Calculations

| Event Base Price | Ticket Type | Calculation | Final Price | Modifier |
|-----------------|-------------|-------------|-------------|----------|
| €100 | Early Bird | 100 × 0.8 | €80 | -20% |
| €100 | Student | 100 × 0.5 | €50 | -50% |
| €100 | VIP | 100 × 2.0 | €200 | +100% |
| €100 | Regular | 100 × 1.0 | €100 | 0% |
| €50 | Student | 50 × 0.5 | €25 | -50% |
| €200 | VIP | 200 × 2.0 | €400 | +100% |

#### User Experience Considerations

**Price Transparency:**
- Always display both original price and final price when discounts apply
- Show savings amount: "You save €50 with your Student discount"
- For VIP, clarify premium value: "VIP access includes exclusive perks"

**Ticket Type Selection:**
- Only show ticket types that are currently available for the event
- Validate user eligibility (e.g., require student verification for student tickets)
- Clearly label early bird availability window

#### Future Complexity Considerations

**The current simple implementation can be extended to handle:**

**Time-Based Early Bird:**
```
IF ticketType == TicketType.early:
  IF current_date > event.earlyBirdDeadline:
    → Show error: "Early bird period has ended"
    → Suggest: "Regular tickets are still available"
  ELSE:
    → Apply 20% discount
```

**User Role Verification:**
```
IF ticketType == TicketType.student:
  IF currentUser.role != UserRole.student:
    → Require student verification
    → Show: "Please verify your student status"
  ELSE:
    → Apply 50% discount
```

**Discount Stacking:**
```
IF ticketType == TicketType.early AND currentUser.role == UserRole.student:
  → Apply best available discount (50% student) OR
  → Stack discounts (20% + additional 30%) depending on business rules
  → Requires policy decision
```

**Engineering Principle Applied:** "Complication is easy - start simple first." Begin with clear, maintainable logic that handles the core use case. Add complexity only when business requirements demand it, and add it incrementally with proper testing at each stage.

---

### Control Flow Best Practices Demonstrated

**1. User-Centered Error Handling:**
- Specific error messages guide users toward resolution
- Sequential validation provides clear feedback at each decision point
- Errors explain both what went wrong and what the user should do

**2. Appropriate Loop Selection:**
- FOR EACH for known, finite collections (categories)
- WHILE for unknown, conditional iterations (pagination)
- Choice driven by what is known at design time vs. runtime

**3. Maintainable Conditional Logic:**
- Clear, readable IF-ELSE chains
- Each condition handles one concern
- Easy to extend with new ticket types or validation rules

**4. Scalable Architecture:**
- Simple foundation that can grow in complexity
- Each component (validation, loading, pricing) is independently testable
- Clear separation between business logic and UI

---
## Section (e): Advanced User Interactivity Features

### Overview

Advanced user interactivity transforms a basic form-based app into a responsive, intelligent system that anticipates user needs and provides immediate feedback. This section covers two categories of interactive features: dynamic filtering systems that allow users to refine content views in real-time, and smart form behaviors that reduce friction and prevent data loss.

---

## Part 1: Dynamic Event Filters

### Business Requirements

Users browsing events need powerful filtering capabilities to quickly find relevant events from potentially large datasets. The filtering system must be intuitive, responsive, and provide clear feedback about filter states and results.

### Filter Components

#### 1. Multi-Select Category Filter (Choice Chips)

**Widget Type:** ChoiceChips or CheckboxGroup with horizontal scroll

**Purpose:** Allow users to select multiple event categories simultaneously

**Implementation:**
```
State Variable (Page State):
- selectedCategories: List<EventCategory>
- Initial value: Empty list (show all categories by default)

Display:
- FOR EACH category in EventCategory enum:
  → Render chip/checkbox with category name
  → Visual state: Selected (highlighted) or Unselected
  
User Interaction:
- Click/tap on category chip
- Toggle selection (add to or remove from selectedCategories list)
- Multiple categories can be selected simultaneously

Visual Feedback:
- Selected chips: Primary color, checkmark icon
- Unselected chips: Secondary/gray color
- Show count: "3 categories selected"
```

**UX Consideration:** Start with no categories selected (show all events) rather than pre-selecting any, giving users full control from the start.

---

#### 2. Price Range Filter (Slider)

**Widget Type:** RangeSlider (dual-handle slider)

**Purpose:** Allow users to define minimum and maximum price boundaries

**Implementation:**
```
State Variables (Page State):
- minPrice: Double (initial: 0)
- maxPrice: Double (initial: 1000 or max event price in database)

Slider Configuration:
- Min value: 0
- Max value: Highest ticket price across all events (dynamic)
- Divisions: 10 (or calculate based on price range)
- Show labels: Display current min/max values

User Interaction:
- Drag left handle → adjust minPrice
- Drag right handle → adjust maxPrice
- Values update in real-time as user drags

Visual Feedback:
- Display current range: "€50 - €200"
- Show how many events match this range
- Highlight selected range on slider track
```

**Advanced Feature:** Show distribution histogram beneath slider indicating how many events fall within each price band.

---

#### 3. Availability Filter (Switch)

**Widget Type:** Switch or Toggle

**Purpose:** Allow users to show only events with available seats

**Implementation:**
```
State Variable (Page State):
- showOnlyAvailable: Boolean
- Initial value: false (show all events by default)

Logic:
IF showOnlyAvailable == true:
  → Filter events where: currentAttendees < maxAttendees
ELSE:
  → Show all events regardless of availability

Visual Feedback:
- Switch label: "Only show available events"
- When enabled: Show count "127 available events"
- Sold out events: Gray out or hide based on switch state
```

**UX Consideration:** Default to `false` (show all) so users see the full catalog, but can easily toggle to see only bookable events.

---

### Filter Update Strategy: Hybrid Approach

**Design Decision:** Combine immediate visual feedback with explicit apply action for better user control.

**Rationale:**
- **User Control:** Prevents frustration from accidental filter changes or mistypes
- **Thoughtful Selection:** Users can adjust multiple filters before seeing results
- **Performance:** Avoids excessive API calls or database queries on every single change
- **Clear Intent:** Explicit "Apply Filters" action confirms user's filtering choices

#### Implementation Flow

```
Phase 1: Filter Selection (Immediate Visual Feedback)

User interacts with any filter:
→ Update Page State variable immediately
→ Show preview of filter state:
  * "3 categories selected"
  * "Price range: €50-€200"
  * "Only available: ON"
→ Display: "~ 42 events match your filters" (approximate count)
→ "Apply Filters" button becomes highlighted/enabled

Phase 2: Apply Filters Action

User clicks "Apply Filters" button:
→ Trigger filter logic:
  1. Build filter query based on all Page State filter values
  2. Query events from database/API with filters applied
  3. Update filteredEvents Page State variable
  4. Re-render event list with filtered results

→ Show results summary: "Showing 42 events"
→ Button returns to normal state

Phase 3: Clear Filters Option

"Clear All Filters" button:
→ Reset all filter Page State variables to defaults
→ Reload full event list
→ Visual confirmation: "All filters cleared"
```

**Benefits of Hybrid Approach:**
- **Control:** User makes multiple adjustments before committing
- **Feedback:** Preview shows what will happen without commitment
- **Performance:** Single query after all filters set, not per-filter-change
- **Flexibility:** User can experiment with filter combinations

---

### Filter State Management

**Storage Location:** Page State (EventListPage)

**Rationale:**
- **Page-Specific Context:** Filters are relevant only while browsing events on this page
- **Fresh Start:** Each visit to EventListPage starts with default filters (user expectations)
- **No Persistence Needed:** Users typically want to re-evaluate filters each session
- **Memory Efficiency:** Don't clutter App State with temporary browsing preferences

**Alternative Consideration:** If user research shows that users repeatedly apply the same filters, consider adding "Save Filter Preset" feature that stores to App State for quick recall.

---

## Part 2: Smart Form Features

### Business Requirements

Form interactions should feel intelligent and helpful, reducing user effort through predictive features, real-time validation, flexible input options, and automatic data preservation.

---

### 1. Auto-Complete for City Input

**Purpose:** Help users quickly select cities where events exist, reducing typos and standardizing location data.

**Data Source:** Existing Event.city data from database

**Rationale for Using Existing Event Data:**
- **Relevance:** Only suggest cities where events actually exist in the app
- **User Value:** Implicit information - "Berlin has events you can attend"
- **Data Quality:** Ensures consistency in city naming (no "NYC" vs "New York City" issues)
- **Performance:** Local database query, no external API costs or latency
- **Privacy:** No data sent to third-party services

#### Implementation

```
Input Field Configuration:
- TextField for city input
- Enable auto-complete/suggestions dropdown

Suggestion Logic:

User types in city field:
→ Trigger: onChange event (with debounce - 300ms delay)

Query:
SELECT DISTINCT city 
FROM Events 
WHERE city LIKE 'user_input%'
ORDER BY 
  (SELECT COUNT(*) FROM Events e WHERE e.city = Events.city) DESC
LIMIT 5

Result Processing:
→ Returns: List of cities matching input, ordered by event count
→ Display in dropdown below input field:
  * Berlin (12 events)
  * Bern (3 events)

User Interaction:
→ User types "Ber"
→ Sees suggestions appear
→ Clicks suggestion OR continues typing
→ Selected city populates field
```

**Enhancement:** Show event count next to each city to help users make informed choices about location.

**Edge Case Handling:**
- User types city not in database → Allow custom entry (for creating first event in new city)
- No suggestions found → Show message: "No events in this city yet. Be the first!"

---

### 2. Real-Time Availability Check During Event Registration

**Purpose:** Prevent registration failures by checking seat availability as user completes the registration form.

**Timing:** Check availability at multiple points, not just final submission

#### Implementation Strategy

```
Availability Check Points:

Point 1: Form Load
When registration form opens:
→ Query current Event.currentAttendees and Event.maxAttendees
→ Display availability status:
  * "23 seats remaining"
  * "Last 5 seats!"
  * "Sold out - Join waitlist"
→ If sold out: Disable registration, offer waitlist

Point 2: During Form Completion (Periodic)
Every 15-30 seconds while form is open:
→ Background API call to check current availability
→ Update availability display if changed
→ If becomes sold out while user filling form:
  * Show alert: "This event just sold out"
  * Disable submit button
  * Offer alternative actions

Point 3: Form Submission (Final Check)
User clicks "Complete Registration":
→ Final real-time availability check before creating Ticket
→ IF still available:
  * Proceed with registration
  * Atomically increment currentAttendees
→ IF sold out:
  * Block registration
  * Show: "Sorry, the last seat was just taken"
  * Offer waitlist or similar events
```

**Technical Consideration:** Use optimistic locking or database transactions to prevent race conditions where multiple users register for the last seat simultaneously.

**UX Benefits:**
- **Transparency:** Users always see current availability
- **No Surprises:** Failed registration at end is prevented by early warnings
- **Alternatives:** System proactively offers solutions if event becomes unavailable

---

### 3. Dynamic Field Creation (Multiple Phone Numbers)

**Purpose:** Allow users to add multiple contact phone numbers without predetermined limits.

**Use Case:** User might want to provide: mobile, work, emergency contact numbers

#### Implementation

```
Initial State:
- Show one phone number TextField
- "Add Another Phone Number" button below

Data Structure (Page State):
- phoneNumbers: List<String>
- Initial value: [""] (one empty string)

Add Phone Number Flow:

User clicks "Add Another Phone Number":
→ Action: Add empty string to phoneNumbers list
→ UI updates: New TextField appears
→ Each TextField bound to phoneNumbers[index]
→ "Remove" button appears next to each field (except if only 1)

Remove Phone Number Flow:

User clicks "Remove" icon next to a field:
→ Action: Remove item at that index from phoneNumbers list
→ UI updates: TextField disappears
→ Remaining fields re-index automatically

Validation:
FOR EACH phone number in phoneNumbers:
  IF not empty:
    → Validate format (e.g., 10+ digits)
    → Show error if invalid
  IF empty:
    → Skip validation (optional field)

Data Submission:
→ Filter out empty entries before saving
→ Save as List<String> in User data or Event organizer contact info
```

**UX Considerations:**
- **No Arbitrary Limit:** Let users add as many as needed (reasonable max: 5-10)
- **Visual Hierarchy:** Primary phone number labeled differently from additional numbers
- **Placeholder Text:** Guide format: "+1 (555) 123-4567"
- **Smart Defaults:** If user has phone numbers from profile, pre-populate first field

---

### 4. Auto-Save Form Every 30 Seconds

**Purpose:** Prevent data loss from accidental navigation, browser crashes, or session timeouts.

**Save Frequency:** Every 30 seconds + on navigation events

#### Implementation Strategy

**Timer-Based Auto-Save:**

```
Page Load:
→ Start timer (30-second interval)

Timer Trigger (Every 30 Seconds):
→ Collect all form field values:
  * Name, email, description, city, date, price, etc.
→ Create formDraft object with timestamp
→ Save to Page State: formDraft = {
    fields: {field1: value1, field2: value2, ...},
    lastSaved: currentTimestamp
  }
→ Show subtle feedback: "Draft saved" (toast/indicator)

Continuous Loop:
→ Timer repeats every 30 seconds while user on page
→ Each save overwrites previous draft with current state
```

**Navigation-Triggered Save:**

```
User navigates away from form page:
→ Intercept navigation event (onPageWillUnload)
→ Trigger immediate save of current form state
→ Rationale: User may have entered data < 30 seconds ago

Benefits:
- Prevents data loss if user accidentally leaves page
- Captures recent changes not yet covered by timer
- No "Are you sure?" dialog needed - data is safe
```

**Save Location:** Page State

**Rationale:**
- **Page-Specific:** Draft is relevant only to this particular form instance
- **Temporary Nature:** Form draft is meant for immediate session recovery, not long-term storage
- **Clean State:** When user successfully submits form, draft is cleared automatically
- **No Clutter:** Doesn't pollute App State with temporary form data

**Alternative Enhancement:** For critical forms (event creation), could save to App State or local database for cross-session recovery: "You have an unsaved draft from yesterday. Would you like to restore it?"

#### Draft Recovery

```
Page Load:
→ Check if formDraft exists in Page State
→ IF formDraft found AND not expired (< 1 hour old):
  * Show dialog: "Restore unsaved changes?"
  * User clicks "Restore":
    → Populate all form fields with draft values
    → Show indicator: "Draft restored from [time]"
  * User clicks "Start Fresh":
    → Clear formDraft
    → Show empty form

→ IF no draft OR expired:
  * Show empty form
  * Start fresh auto-save cycle
```

**User Control:**
- Always ask before restoring draft (don't assume user wants it)
- Provide clear timestamp of when draft was saved
- Allow user to discard draft if they want fresh start

---

## Advanced Interactivity Patterns Demonstrated

### 1. Predictive Assistance
- **Auto-complete:** System anticipates user needs based on existing data
- **Real-time checks:** Proactive validation prevents future errors
- **Smart defaults:** Pre-populate fields when possible

### 2. Progressive Enhancement
- **Dynamic fields:** UI adapts to user needs (add phone numbers as needed)
- **Contextual feedback:** Show relevant information at decision points
- **Flexible interactions:** Support both power users and beginners

### 3. Data Preservation
- **Auto-save:** Automatic protection against data loss
- **Draft recovery:** Restore interrupted work
- **Multiple save triggers:** Timer + navigation ensures coverage

### 4. User Control with Intelligence
- **Hybrid filtering:** Balance between automatic and explicit control
- **Confirmation dialogs:** Ask before destructive or surprising actions
- **Clear feedback:** Always show what system is doing and why

### 5. Performance Optimization
- **Debouncing:** Wait for user to finish typing before triggering searches
- **Throttling:** Limit frequency of availability checks to reduce server load
- **Local-first:** Use cached/local data for suggestions before hitting API
- **Batching:** Apply all filters at once rather than per-filter queries

---

## Implementation Priorities

**Tier 1 (Must-Have):**
1. Auto-save functionality (prevents data loss)
2. Real-time availability checking (prevents registration failures)
3. Basic filtering with Apply button (core feature)

**Tier 2 (High Value):**
4. Auto-complete for city (significantly improves data quality and UX)
5. Dynamic phone number fields (flexible, professional appearance)

**Tier 3 (Nice to Have):**
6. Advanced filter features (histograms, saved presets)
7. Draft recovery across sessions
8. Predictive suggestions based on user behavior

---

## User Experience Impact

**Reduced Friction:**
- Auto-complete eliminates typing effort
- Auto-save eliminates anxiety about losing work
- Real-time checks prevent wasted effort on unavailable events

**Increased Confidence:**
- Clear feedback at every interaction point
- Transparent availability information
- Explicit control over filter application

**Professional Polish:**
- Intelligent behaviors feel modern and considerate
- Responsive feedback shows system is working
- Flexible inputs accommodate diverse user needs

**Error Prevention:**
- Early validation catches problems before submission
- Standardized data (cities) reduces downstream issues
- Atomic operations prevent race conditions

---
