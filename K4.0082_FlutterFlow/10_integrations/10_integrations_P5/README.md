# FitTracker - Firebase Analytics & Crashlytics Integration

## 📋 Project Overview

**FitTracker** is a comprehensive fitness tracking mobile application demonstrating advanced Firebase integration with emphasis on Google Analytics event tracking, Crashlytics monitoring, and systematic app quality assurance. This project showcases professional implementation of user behavior monitoring, error tracking, and performance optimization strategies.

**Course:** K4.0082 - No-Code Programming with FlutterFlow  
**Module:** Firebase Analytics & Crashlytics Integration  
**Development Platform:** FlutterFlow v6.4.31  
**Firebase SDK:** Latest stable version

---

## 🎯 Learning Objectives Achieved

### Part A: Firebase Integration & App Structure ✅
- ✅ Implemented Firebase Authentication with email/password
- ✅ Created Firestore database with proper schema design
- ✅ Developed multi-page navigation structure with bottom navigation
- ✅ Implemented CRUD operations for workout logging
- ✅ Established user profile management system

### Part B: Google Analytics Implementation ✅
- ✅ Integrated comprehensive event tracking system
- ✅ Configured automatic predefined events (screen_view, login, sign_up)
- ✅ Implemented custom events with parameters for user behavior analysis
- ✅ Set up user properties for segmentation
- ✅ Established analytics configuration for app usage insights

### Part C: Crashlytics Monitoring ✅
- ✅ Activated Firebase Crashlytics for app stability monitoring
- ✅ Implemented automatic crash detection and reporting
- ✅ Configured custom keys for enhanced debug information
- ✅ Established error tracking across critical user flows
- ✅ Set up performance monitoring for continuous quality assurance

---

## 🏗️ Technical Architecture

### 1. Data Layer - Firestore Schema

#### Collections Structure

```
users (Collection)
  └── {userId} (Document)
      ├── displayName: String          # User's full name
      ├── email: String                # Authentication email
      ├── createdAt: Timestamp         # Account creation date
      └── totalWorkouts: Integer       # Cached workout count (optional)

workouts (Collection)
  └── {workoutId} (Document - Auto-generated)
      ├── userId: String               # Reference to users/{userId}
      ├── activityType: String         # Running | Cycling | Gym | Yoga | Swimming | Walking
      ├── duration: Integer            # Duration in minutes
      ├── notes: String                # Optional workout notes
      ├── date: Timestamp              # Workout date/time
      └── createdAt: Timestamp         # Document creation timestamp (Server Timestamp)
```

#### Security Rules

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    
    // Users collection - users can only read/write their own data
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    // Workouts collection - users can only access their own workouts
    match /workouts/{workoutId} {
      allow create: if request.auth != null 
        && request.resource.data.userId == request.auth.uid
        && request.resource.data.duration is int
        && request.resource.data.duration > 0;
      
      allow read, update, delete: if request.auth != null 
        && resource.data.userId == request.auth.uid;
    }
  }
}
```

---

### 2. Logic Layer - Firebase Integration

#### Authentication Implementation

**LoginPage Action Flow:**

```
Step 1: Form Validation
  - Validate email format
  - Validate password minimum 6 characters
  - Show inline errors if validation fails

Step 2: Firebase Authentication
  Action: Firebase Auth → Login
  Input Email: [TextField Email]
  Input Password: [TextField Password]
  
  On Success:
    └─ Continue to Step 3
  
  On Failure:
    ├─ Show Snackbar: "Login failed: {error message}"
    ├─ Log Analytics Event: "login_failed"
    │   Parameters:
    │     - error_code: [Error code]
    └─ Stop execution

Step 3: Analytics Event Logging
  Action: Log Analytics Event
  Event Name: "login"  # Predefined Firebase event
  Parameters:
    - method: "email"
  
  Action: Set Analytics User Property
  Property Name: "user_id"
  Value: [Authenticated User → uid]

Step 4: Crashlytics Context Setting
  Action: Set Crashlytics Custom Key
  Key: "user_id"
  Value: [Authenticated User → uid]
  
  Action: Set Crashlytics Custom Key
  Key: "last_login_date"
  Value: [Current Timestamp]

Step 5: Navigation
  Action: Navigate To → HomePage
  Transition Type: Replace (clear back stack)
```

#### Workout Logging Implementation

**AddWorkoutPage - Save Workout Action Flow:**

```
Step 1: Form Validation
  IF duration <= 0:
    ├─ Show Snackbar: "Please enter a valid duration"
    └─ Stop execution

Step 2: Crashlytics Pre-Action Context
  Action: Set Crashlytics Custom Key
  Key: "current_action"
  Value: "saving_workout"
  
  Action: Set Crashlytics Custom Key
  Key: "workout_activity_type"
  Value: [Dropdown: activityType]

Step 3: Create Firestore Document
  Action: Create Document
  Collection: workouts
  Document ID: Auto-generate
  Fields:
    ├─ userId: [Authenticated User → uid]  # CRITICAL
    ├─ activityType: [Dropdown: selectedActivity]
    ├─ duration: [TextField: duration]
    ├─ notes: [TextField: notes]
    ├─ date: [Current Timestamp]
    └─ createdAt: [Server Timestamp]
  
  On Success:
    └─ Continue to Step 4
  
  On Failure:
    ├─ Log Non-Fatal Error to Crashlytics
    │   Message: "Failed to save workout"
    │   Error: [Error object]
    ├─ Show Snackbar: "Failed to save workout. Please try again."
    └─ Stop execution

Step 4: Analytics Event Logging
  Action: Log Analytics Event
  Event Name: "workout_logged"  # Custom event
  Parameters:
    ├─ activity_type: [Dropdown: selectedActivity]
    ├─ duration_minutes: [TextField: duration]
    ├─ has_notes: [notes.isNotEmpty ? true : false]
    └─ timestamp: [Current Timestamp]

Step 5: Crashlytics Post-Action Context
  Action: Set Crashlytics Custom Key
  Key: "last_workout_type"
  Value: [Dropdown: selectedActivity]

Step 6: User Feedback & Navigation
  Action: Show Snackbar
  Message: "Workout saved successfully!"
  Duration: 3 seconds
  
  Action: Navigate Back
  Destination: HomePage
  Transition: Pop with result
```

---

### 3. UI Layer - FlutterFlow Pages

#### Page Structure Overview

| Page | Purpose | Analytics Events | Crashlytics Keys |
|------|---------|------------------|------------------|
| **LoginPage** | User authentication | screen_view, login, login_failed | user_id, last_login_date |
| **HomePage** | Dashboard with recent workouts | screen_view, add_workout_initiated | current_screen, workouts_displayed |
| **AddWorkoutPage** | Workout creation form | screen_view, workout_logged, workout_save_failed | current_screen, current_action, workout_activity_type, last_workout_type |
| **HistoryPage** | Complete workout history | screen_view | current_screen, total_workouts_displayed |
| **ProfilePage** | User profile & logout | screen_view, logout | current_screen, user_total_workouts |

#### LoginPage

**Layout Structure:**
```
Column (Main container):
  ├─ Spacer (top padding)
  ├─ App Icon Container
  │   └─ Icon: Lock (primary color)
  ├─ Title Text: "Welcome Back"
  ├─ Subtitle Text: "Sign in to continue"
  ├─ Email TextField
  │   ├─ Label: "Email address"
  │   ├─ Prefix Icon: Email icon
  │   ├─ Keyboard Type: Email
  │   ├─ Validation: Email format
  │   └─ Store in: Page State → email
  ├─ Password TextField
  │   ├─ Label: "Password"
  │   ├─ Prefix Icon: Lock icon
  │   ├─ Suffix Icon: Eye icon (toggle visibility)
  │   ├─ Obscure Text: true
  │   ├─ Validation: Min 6 characters
  │   └─ Store in: Page State → password
  ├─ Forgot Password Link (optional)
  ├─ Login Button
  │   ├─ Text: "Login"
  │   ├─ Full Width: true
  │   └─ OnPressed: [Action Flow]
  └─ Sign Up Link
      └─ Text: "Don't have an account? Sign Up"
```

**Analytics Events:**
- `screen_view` (automatic) - When page loads
- `login` (manual) - On successful login
- `login_failed` (manual) - On authentication error

**Crashlytics Keys:**
- `user_id` - After successful login
- `last_login_date` - Login timestamp

#### HomePage

**Layout Structure:**
```
Column:
  ├─ AppBar / Custom Header
  │   ├─ Title: "FitTracker"
  │   └─ Subtitle: "Welcome back, [AuthUser.displayName]"
  │
  ├─ ScrollView / ListView
  │   │
  │   ├─ Weekly Summary Container
  │   │   ├─ Title: "Weekly Summary"
  │   │   ├─ Date Badge: "Nov 12 - 19"
  │   │   └─ Row (3 columns):
  │   │       ├─ Workouts Stat (Icon + Number + Label)
  │   │       ├─ Minutes Stat (Icon + Number + Label)
  │   │       └─ Streak Stat (Icon + Number + Label)
  │   │
  │   ├─ Recent Workouts Header
  │   │   └─ Text: "Recent Workouts"
  │   │
  │   └─ Workouts ListView
  │       ├─ Data Source: Firestore Query
  │       │   ├─ Collection: workouts
  │       │   ├─ Filter: userId == [AuthUser.uid]
  │       │   ├─ Order By: date (descending)
  │       │   └─ Limit: 4
  │       └─ List Item: WorkoutCard
  │           ├─ Activity Icon (conditional)
  │           ├─ Activity Name
  │           ├─ Date/Time
  │           └─ Duration
  │
  ├─ Floating Action Button
  │   ├─ Icon: Add icon
  │   ├─ Position: Bottom right
  │   └─ OnPressed: Navigate to AddWorkoutPage
  │
  └─ Bottom Navigation Bar
```

**Activity Icon Conditional Logic:**
```
Conditional Builder:
  Variable: [Workout Document → activityType]
  
  Conditions:
    ├─ IF activityType == "Running"
    │   ├─ Icon: directions_run
    │   └─ Background Color: Blue (#2196F3)
    ├─ IF activityType == "Cycling"
    │   ├─ Icon: directions_bike
    │   └─ Background Color: Orange (#FF9800)
    ├─ IF activityType == "Gym"
    │   ├─ Icon: fitness_center
    │   └─ Background Color: Purple (#9C27B0)
    ├─ IF activityType == "Yoga"
    │   ├─ Icon: self_improvement
    │   └─ Background Color: Green (#4CAF50)
    ├─ IF activityType == "Swimming"
    │   ├─ Icon: pool
    │   └─ Background Color: Teal (#009688)
    └─ ELSE (Walking or default)
        ├─ Icon: directions_walk
        └─ Background Color: Grey (#9E9E9E)
```

**Analytics Events:**
- `screen_view` (automatic) - Page load
- `add_workout_initiated` (manual) - FAB clicked

**Crashlytics Keys:**
- `current_screen: "home_page"` - On page load
- `workouts_displayed` - Count of workouts shown

#### AddWorkoutPage

**Layout Structure:**
```
Column:
  ├─ AppBar
  │   ├─ Leading: Back button
  │   └─ Title: "Log Workout" (centered)
  │
  ├─ Form (Scrollable)
  │   │
  │   ├─ Activity Type Section
  │   │   ├─ Label: "Activity Type"
  │   │   └─ Dropdown
  │   │       ├─ Options: [Running, Cycling, Gym, Yoga, Swimming, Walking]
  │   │       ├─ Initial Value: Running
  │   │       └─ Store in: Page State → selectedActivity
  │   │
  │   ├─ Duration Section
  │   │   ├─ Label: "Duration"
  │   │   └─ TextField
  │   │       ├─ Type: Number
  │   │       ├─ Suffix Text: "minutes"
  │   │       ├─ Placeholder: "0"
  │   │       ├─ Validation: Required, > 0
  │   │       └─ Store in: Page State → duration
  │   │
  │   └─ Notes Section
  │       ├─ Label: "Notes (Optional)"
  │       └─ TextField
  │           ├─ Multiline: true
  │           ├─ Max Lines: 4
  │           ├─ Placeholder: "Add any notes about your workout..."
  │           └─ Store in: Page State → notes
  │
  ├─ Save Button (Fixed at bottom)
  │   ├─ Text: "Save Workout"
  │   ├─ Full Width: true
  │   └─ OnPressed: [Action Flow]
  │
  └─ Bottom Navigation Bar
```

**Analytics Events:**
- `screen_view` (automatic) - Page load
- `workout_logged` (manual) - Successful save
- `workout_save_failed` (manual) - Save error

**Crashlytics Keys:**
- `current_screen: "add_workout_page"` - On page load
- `current_action: "saving_workout"` - Before Firestore write
- `workout_activity_type` - Activity being saved
- `last_workout_type` - After successful save

#### HistoryPage

**Layout Structure:**
```
Column:
  ├─ AppBar / Header
  │   ├─ Title: "Workout History"
  │   └─ Subtitle: "All your logged activities"
  │
  ├─ ListView (Full workout history)
  │   ├─ Data Source: Firestore Query
  │   │   ├─ Collection: workouts
  │   │   ├─ Filter: userId == [AuthUser.uid]
  │   │   └─ Order By: date (descending)
  │   └─ List Item: WorkoutCard
  │       ├─ Activity Icon (conditional - same as HomePage)
  │       ├─ Activity Name
  │       ├─ Duration
  │       └─ Date/Time
  │
  ├─ Floating Action Button
  │   ├─ Icon: Add icon
  │   └─ OnPressed: Navigate to AddWorkoutPage
  │
  └─ Bottom Navigation Bar
```

**Analytics Events:**
- `screen_view` (automatic) - Page load

**Crashlytics Keys:**
- `current_screen: "history_page"` - On page load
- `total_workouts_displayed` - Total count

#### ProfilePage

**Layout Structure:**
```
Column:
  ├─ AppBar / Header
  │   ├─ Title: "Profile"
  │   ├─ Subtitle: "Manage your account"
  │   └─ Action: Settings Icon (optional)
  │
  ├─ ScrollView
  │   │
  │   ├─ User Info Card
  │   │   ├─ Profile Avatar (First letter or icon)
  │   │   ├─ User Name Text
  │   │   │   └─ Source: [AuthUser.displayName]
  │   │   └─ Email Text
  │   │       └─ Source: [AuthUser.email]
  │   │
  │   ├─ Stats Card
  │   │   ├─ Icon: Dumbbell
  │   │   ├─ Total Workouts Number
  │   │   └─ Label: "Total Workouts"
  │   │
  │   └─ Logout Button
  │       ├─ Text: "Logout"
  │       ├─ Icon: Logout icon
  │       ├─ Full Width: true
  │       ├─ Color: Destructive (red)
  │       └─ OnPressed: [Action Flow]
  │
  └─ Bottom Navigation Bar
```

**Logout Action Flow:**
```
Step 1: Analytics Event Logging
  Action: Log Analytics Event
  Event Name: "logout"
  Parameters:
    - session_duration: [Time since login]

Step 2: Crashlytics Context Clear
  Action: Set Crashlytics Custom Key
  Key: "user_logged_out"
  Value: "true"

Step 3: Firebase Logout
  Action: Firebase Auth → Logout

Step 4: Navigation
  Action: Navigate To → LoginPage
  Transition Type: Replace (clear entire back stack)
```

**Analytics Events:**
- `screen_view` (automatic) - Page load
- `logout` (manual) - Logout button pressed

**Crashlytics Keys:**
- `current_screen: "profile_page"` - On page load
- `user_logged_out: "true"` - During logout

#### Bottom Navigation Bar

**Configuration:**
```
Bottom Navigation Bar:
  Type: Persistent across pages
  Items: 4
  
  Navigation Items:
    ├─ Item 1: Home
    │   ├─ Icon (Inactive): home_outline
    │   ├─ Icon (Active): home_filled
    │   ├─ Label: "Home"
    │   └─ Navigate To: HomePage
    │
    ├─ Item 2: Add Workout
    │   ├─ Icon (Inactive): fitness_center_outline
    │   ├─ Icon (Active): fitness_center_filled
    │   ├─ Label: "Add Workout"
    │   └─ Navigate To: AddWorkoutPage
    │
    ├─ Item 3: History
    │   ├─ Icon (Inactive): history_outline
    │   ├─ Icon (Active): history_filled
    │   ├─ Label: "History"
    │   └─ Navigate To: HistoryPage
    │
    └─ Item 4: Profile
        ├─ Icon (Inactive): person_outline
        ├─ Icon (Active): person_filled
        ├─ Label: "Profile"
        └─ Navigate To: ProfilePage
```

---

## 📊 Part B: Google Analytics Implementation

### Analytics Configuration Overview

**Firebase Analytics Settings (FlutterFlow):**
```
Location: Settings and Integrations → Integrations → Google Analytics

Configuration:
  ├─ Enable Google Analytics: ✅ ON
  ├─ Predefined Events Configuration:
  │   ├─ On Page Load (screen_view): ✅ ENABLED
  │   ├─ On Action Start: ✅ ENABLED (optional)
  │   ├─ On Each Individual Action: ❌ DISABLED (reduces noise)
  │   └─ On Authentication: ✅ ENABLED
  │
  └─ Custom Events: Manually configured in action flows
```

### Automatic Event Tracking (Predefined Events)

#### Screen View Events

**Purpose:** Track page navigation and user flow through the app

**Configuration:**
- Event Name: `screen_view` (Firebase standard)
- Trigger: Automatic on every page load
- Parameters (Automatic):
  - `screen_name`: Page name from FlutterFlow
  - `screen_class`: Flutter widget class
  - `firebase_screen`: Screen identifier

**Pages Tracked:**

| Page | screen_name Value | Tracked |
|------|-------------------|---------|
| LoginPage | "login_page" | ✅ Yes |
| HomePage | "home_page" | ✅ Yes |
| AddWorkoutPage | "add_workout_page" | ✅ Yes |
| HistoryPage | "history_page" | ✅ Yes |
| ProfilePage | "profile_page" | ✅ Yes |

#### Authentication Events

**Event: login**
- Trigger: User successfully authenticates
- Event Name: `login` (Firebase recommended name)
- Parameters:
  - `method`: "email"

**Event: sign_up** (if implemented)
- Trigger: New user account created
- Event Name: `sign_up` (Firebase recommended name)
- Parameters:
  - `method`: "email"

### Custom Event Tracking

#### Core Custom Events

**Event 1: workout_logged**
```
Purpose: Track successful workout creation with detailed context
Trigger: After Firestore document successfully created
Priority: HIGH (Core feature tracking)

Event Name: "workout_logged"

Parameters:
  ├─ activity_type: String
  │   Values: "Running" | "Cycling" | "Gym" | "Yoga" | "Swimming" | "Walking"
  │
  ├─ duration_minutes: Integer
  │   Range: 1 - 300
  │
  ├─ has_notes: Boolean
  │   Logic: notes.isNotEmpty ? true : false
  │
  └─ timestamp: Timestamp

Analytics Value:
  ├─ Identify most popular workout types
  ├─ Track workout duration patterns
  ├─ Measure user engagement with notes feature
  └─ Understand workout timing patterns
```

**Event 2: add_workout_initiated**
```
Purpose: Track workout creation funnel entry point
Trigger: User taps FAB or navigates to Add Workout page
Priority: HIGH (Funnel analysis)

Event Name: "add_workout_initiated"

Parameters:
  ├─ source_page: String ("home" | "history" | "bottom_nav")
  └─ timestamp: Timestamp

Analytics Value:
  ├─ Track conversion funnel (initiated → completed)
  └─ Identify which entry points are most effective
```

**Event 3: workout_save_failed**
```
Purpose: Track errors in workout creation process
Trigger: Firestore create document fails
Priority: HIGH (Error monitoring)

Event Name: "workout_save_failed"

Parameters:
  ├─ error_code: String
  ├─ error_message: String
  ├─ activity_type: String
  └─ duration_value: Integer

Analytics Value:
  ├─ Identify technical issues in workout creation
  ├─ Measure success/failure rate
  └─ Prioritize bug fixes based on frequency
```

**Event 4: logout**
```
Purpose: Track session end and user engagement duration
Trigger: User successfully logs out
Priority: MEDIUM

Event Name: "logout"

Parameters:
  ├─ session_duration_minutes: Integer
  └─ timestamp: Timestamp

Analytics Value:
  ├─ Measure average session duration
  └─ Track user engagement patterns
```

### User Properties Configuration

**User Property 1: user_id**
```
Property Name: "user_id"
Data Type: String
Value: [Authenticated User → uid]

Set When: Immediately after successful login
Set Location: LoginPage → Action Flow → After Authentication Success

Action: Set Analytics User Property
Property Name: "user_id"
Value: [Authenticated User → uid]

Analytics Value:
  ├─ Link events to specific users
  ├─ Track user lifetime value
  └─ Create user-specific insights
```

**User Property 2: account_created_date**
```
Property Name: "account_created_date"
Data Type: String (ISO 8601 format)
Value: [Users collection → createdAt]

Set When: After sign up or first login

Analytics Value:
  ├─ Calculate user tenure
  ├─ Cohort analysis
  └─ Retention metrics
```

### Analytics Events Summary Table

| Event Name | Type | Trigger | Parameters | Priority |
|------------|------|---------|------------|----------|
| `screen_view` | Predefined | Page load (automatic) | screen_name | AUTO |
| `login` | Predefined | Successful authentication | method | HIGH |
| `sign_up` | Predefined | Account creation | method | MEDIUM |
| `workout_logged` | Custom | Workout saved successfully | activity_type, duration_minutes, has_notes | HIGH |
| `add_workout_initiated` | Custom | FAB/nav to add workout | source_page | HIGH |
| `workout_save_failed` | Custom | Firestore create fails | error_code, activity_type | HIGH |
| `logout` | Custom | User logs out | session_duration_minutes | MEDIUM |

### Analytics Dashboard Configuration

**Firebase Console Setup:**
```
Navigate: Firebase Console → Analytics → Events

Key Metrics to Monitor:
  │
  ├─ Widget 1: Total Active Users (Last 7 Days)
  │   Metric: Active Users
  │   Time Range: Last 7 days
  │
  ├─ Widget 2: Workout Logging Funnel
  │   Events:
  │     ├─ add_workout_initiated
  │     ├─ workout_logged
  │     └─ Conversion Rate: (workout_logged / add_workout_initiated)
  │
  ├─ Widget 3: Most Popular Activities
  │   Event: workout_logged
  │   Group By: activity_type parameter
  │   Visualization: Pie chart
  │
  ├─ Widget 4: Daily Workout Volume
  │   Event: workout_logged
  │   Metric: Event count
  │   Time Range: Last 30 days
  │   Visualization: Line chart
  │
  └─ Widget 5: Screen Flow
      Start: screen_view (login_page)
      End: screen_view (profile_page)
      Visualization: Sankey diagram
```

### Event Verification Process

**Testing with DebugView:**
```
Step 1: Enable Debug View
  Location: Firebase Console → Analytics → DebugView
  Enable on test device: Add device to debug list

Step 2: Test Each Event
  For Each Event:
    ├─ Trigger event in app
    ├─ Verify appears in DebugView (real-time)
    ├─ Check all parameters are present
    └─ Verify parameter values are correct

Step 3: Wait for Dashboard Population
  Timeline: 24-48 hours for full data in main dashboard
  Note: DebugView is real-time, main dashboard has delay
```

---

## 🛡️ Part C: Crashlytics Implementation

### Crashlytics Activation

**FlutterFlow Configuration:**
```
Location: Settings and Integrations → Project Setup → Firebase → Crashlytics

Configuration:
  ├─ Enable Crashlytics: ✅ ON
  ├─ Platform Support:
  │   ├─ Android: ✅ Supported
  │   ├─ iOS: ✅ Supported
  │   └─ Web: ❌ Not Supported (by Firebase design)
  │
  └─ Automatic Features (Enabled by Default):
      ├─ Crash detection and reporting
      ├─ Stack trace collection
      ├─ Device information gathering
      └─ User breadcrumb tracking
```

**Post-Activation Verification:**
```
Step 1: Build and Run App
  Platform: Android or iOS (not web)
  Mode: Test or Run mode

Step 2: Force Test Crash (Optional)
  Method: Add crash test button in settings
  Code: throw Exception("Test crash for Crashlytics");

Step 3: Check Firebase Console
  Navigate: Firebase Console → Crashlytics
  Timeline: Crashes appear within 5-10 minutes
  View: Crash reports with stack traces

Step 4: Verify Automatic Data Collection
  Check: Device info, OS version, crash timestamp visible
```

### Automatic Crash Detection

**What Crashlytics Captures Automatically:**
```
Crash Information:
  ├─ Exception Type: Dart exception, native crash, ANR
  ├─ Stack Trace: Full call stack with line numbers
  ├─ Thread Information: Thread name and state
  └─ Memory State: Available memory at crash time

Device Information:
  ├─ Device Model: e.g., "iPhone 14", "Samsung Galaxy S22"
  ├─ OS Version: e.g., "iOS 17.1", "Android 13"
  ├─ App Version: Version name and build number
  ├─ Free Disk Space: Available storage
  ├─ Battery Level: Percentage at crash
  └─ Network Status: WiFi/Cellular, connection state

Session Information:
  ├─ Crash Timestamp: Exact time of crash
  ├─ Time Running: App runtime before crash
  ├─ Foreground/Background: App state
  └─ User Actions: Last 64 user interactions (breadcrumbs)

Impact Metrics:
  ├─ Affected Users: Number of users experiencing crash
  ├─ Crash-Free Users: Percentage unaffected
  ├─ Crash-Free Sessions: Session success rate
  └─ Event Count: Total occurrences
```

### Custom Keys Implementation

**Purpose:** Add contextual information to crash reports for faster debugging

#### Strategic Custom Key Placement

**Key 1: user_id** ⭐ CRITICAL
```
Purpose: Identify which users are experiencing crashes
Priority: CRITICAL

Implementation:
  Location: LoginPage → Login Success → Action Flow
  Timing: Immediately after successful authentication
  
  Action: Set Crashlytics Custom Key
  Key: "user_id"
  Value: [Authenticated User → uid]

Debug Value:
  ├─ Link crashes to specific user accounts
  ├─ Identify if crashes affect specific user types
  ├─ Enable personalized support for affected users
  └─ Track crash patterns by user segment
```

**Key 2: current_screen** ⭐ HIGH PRIORITY
```
Purpose: Know which page user was on when crash occurred
Priority: HIGH

Implementation:
  Location: Every page → Page Load → Initial Actions
  Timing: On page initialization
  
  Pages and Values:
    ├─ LoginPage: "login_page"
    ├─ HomePage: "home_page"
    ├─ AddWorkoutPage: "add_workout_page"
    ├─ HistoryPage: "history_page"
    └─ ProfilePage: "profile_page"

Action Configuration:
  Action: Set Crashlytics Custom Key
  Key: "current_screen"
  Value: [Page identifier string]

Debug Value:
  ├─ Identify which screens are most crash-prone
  ├─ Prioritize debugging efforts on problematic pages
  └─ Understand user flow leading to crashes
```

**Key 3: current_action** ⭐ HIGH PRIORITY
```
Purpose: Identify what action user was performing when crash occurred
Priority: HIGH

Implementation:
  Location: Before critical operations (especially Firestore writes)
  Timing: Immediately before action execution
  
  Example Locations and Values:
    ├─ AddWorkoutPage → Before save: "saving_workout"
    ├─ LoginPage → Before auth: "attempting_login"
    ├─ ProfilePage → Before logout: "logging_out"
    └─ Any API call: "fetching_data"

Action Configuration:
  Action: Set Crashlytics Custom Key
  Key: "current_action"
  Value: [Action description string]

Debug Value:
  ├─ Pinpoint exact operation causing crash
  ├─ Identify problematic code paths
  └─ Understand failure points in workflows
```

**Key 4: last_workout_type**
```
Purpose: Track activity type context for workout-related crashes
Priority: MEDIUM

Implementation:
  Location: AddWorkoutPage → After successful workout save
  Timing: Immediately after Firestore write succeeds
  
  Action: Set Crashlytics Custom Key
  Key: "last_workout_type"
  Value: [Dropdown: selectedActivity]
  
  Possible Values:
    ├─ "Running"
    ├─ "Cycling"
    ├─ "Gym"
    ├─ "Yoga"
    ├─ "Swimming"
    └─ "Walking"

Debug Value:
  ├─ Identify if certain workout types cause crashes
  ├─ Debug activity-specific rendering issues
  └─ Track context for subsequent crashes
```

**Key 5: workout_count**
```
Purpose: Understand user engagement level when crashes occur
Priority: LOW

Implementation:
  Location: ProfilePage → On page load
  Timing: After calculating or fetching total workouts
  
  Action: Set Crashlytics Custom Key
  Key: "workout_count"
  Value: [Total workouts integer]

Debug Value:
  ├─ Identify if crashes correlate with usage level
  ├─ Detect issues specific to power users
  └─ Understand impact on different user segments
```

**Key 6: firebase_operation**
```
Purpose: Track which Firebase operation was being performed
Priority: MEDIUM

Implementation:
  Location: Before any Firestore/Auth operation
  Timing: Immediately before Firebase API call
  
  Values:
    ├─ "auth_login"
    ├─ "auth_logout"
    ├─ "firestore_create"
    ├─ "firestore_read"
    ├─ "firestore_update"
    └─ "firestore_delete"

Debug Value:
  └─ Identify Firebase-related crash patterns
```

#### Custom Keys Summary Table

| Key Name | Priority | Set When | Value Type | Example Value |
|----------|----------|----------|------------|---------------|
| `user_id` | CRITICAL | After login | String | "abc123xyz..." |
| `current_screen` | HIGH | Page load | String | "home_page" |
| `current_action` | HIGH | Before operations | String | "saving_workout" |
| `last_workout_type` | MEDIUM | After workout save | String | "Running" |
| `workout_count` | LOW | Profile page load | Integer | "42" |
| `firebase_operation` | MEDIUM | Before Firebase calls | String | "firestore_create" |

### Non-Fatal Error Logging

**Purpose:** Track errors that don't crash the app but indicate problems

#### Firestore Operation Failures

```
Error Type: Firestore Write Failure
Location: AddWorkoutPage → Save Workout → On Failure

Implementation:
  IF Firestore create document fails:
    
    Action 1: Log Non-Fatal Error to Crashlytics
      Error Message: "Failed to save workout to Firestore"
      Error Details: [Error object from Firebase]
      
    Action 2: Set Context Keys
      Key: "failed_operation"
      Value: "firestore_create_workout"
      
      Key: "attempted_activity_type"
      Value: [Dropdown: selectedActivity]
    
    Action 3: User Feedback
      Show Snackbar: "Failed to save workout. Please try again."
    
    Action 4: Log Analytics Event
      Event: "workout_save_failed"
      Parameters:
        ├─ error_code: [Error code]
        └─ activity_type: [Activity value]

Debug Value:
  ├─ Track reliability of Firestore operations
  ├─ Identify network-related issues
  ├─ Measure user-facing error rate
  └─ Prioritize infrastructure improvements
```

#### Authentication Failures

```
Error Type: Login Failure
Location: LoginPage → Login Action → On Failure

Implementation:
  IF Firebase Auth login fails:
    
    Action: Log Non-Fatal Error
      Error Message: "Authentication failed"
      Error Code: [Firebase auth error code]
      
    Context Keys:
      ├─ failed_operation: "authentication"
      ├─ auth_method: "email"
      └─ error_type: [Error type]

Debug Value:
  └─ Monitor authentication reliability
```

#### Data Loading Failures

```
Error Type: Query Failure
Location: HomePage/HistoryPage → Firestore Query → On Error

Implementation:
  IF Firestore query fails:
    
    Action: Log Non-Fatal Error
      Error Message: "Failed to load workouts"
      Context: "HomePage workouts query"

Debug Value:
  └─ Track data layer reliability
```

### Performance Monitoring

#### ANR (Application Not Responding) Detection

```
What is ANR:
  Definition: App becomes unresponsive to user input
  Common Causes:
    ├─ Heavy computation on main thread
    ├─ Slow network requests blocking UI
    ├─ Inefficient database queries
    └─ Complex widget rebuilds

Crashlytics Detection:
  Automatic: Yes (Android only)
  Threshold: 5 seconds of unresponsiveness
  Reporting: Treated similar to crashes in dashboard

Prevention Strategies:
  ├─ Use async/await for network calls
  ├─ Optimize Firestore queries with indexes
  ├─ Limit ListView items with pagination
  └─ Use loading indicators for long operations
```

#### Critical Operation Monitoring

```
Operation: Workout Save Performance
Location: AddWorkoutPage → Save Action

Monitoring Strategy:
  Step 1: Record start time
    Set Key: "save_operation_start"
    Value: [Current timestamp milliseconds]
  
  Step 2: Perform operation
    Create Firestore document
  
  Step 3: Record end time & calculate duration
    Duration: end_time - start_time
    
  Step 4: Log if slow
    IF duration > 3000ms:
      Log Non-Fatal: "Slow workout save operation"
      Context:
        ├─ duration_ms: [Duration value]
        └─ network_type: [WiFi/Cellular]

Performance Threshold:
  ├─ Acceptable: < 1 second
  ├─ Warning: 1-3 seconds
  └─ Problem: > 3 seconds
```

### Crashlytics Dashboard Analysis

**Firebase Console Navigation:**
```
Access: Firebase Console → Crashlytics

Dashboard Sections:
  │
  ├─ Overview
  │   ├─ Crash-free users percentage
  │   ├─ Crash-free sessions percentage
  │   ├─ Total issues count
  │   └─ Trending crashes graph
  │
  ├─ Issues List
  │   For Each Issue:
  │     ├─ Issue title (exception type)
  │     ├─ Affected users count
  │     ├─ Event count (total occurrences)
  │     ├─ First/last seen dates
  │     └─ Priority indicator
  │
  ├─ Issue Detail View
  │   ├─ Stack trace with line numbers
  │   ├─ Custom keys panel
  │   ├─ Device breakdown
  │   ├─ OS version breakdown
  │   ├─ User breadcrumbs timeline
  │   ├─ Similar crashes grouping
  │   └─ Notes and status management
  │
  └─ Filters
      ├─ By status (open/closed)
      ├─ By platform (Android/iOS)
      ├─ By version
      └─ By date range
```

**Issue Prioritization Strategy:**
```
P0 - Critical (Fix Immediately):
  Criteria:
    ├─ Affects > 10% of users
    ├─ Crashes on critical path (login, workout save)
    └─ Reproducible 100% of the time

P1 - High (Fix This Week):
  Criteria:
    ├─ Affects 1-10% of users
    ├─ Impacts important features
    └─ Reproducible > 50% of the time

P2 - Medium (Fix This Sprint):
  Criteria:
    ├─ Affects < 1% of users
    ├─ Non-critical features
    └─ Reproducible < 50% of the time

P3 - Low (Backlog):
  Criteria:
    └─ Rare, low-impact, edge cases
```

### Testing Crashlytics Implementation

**Test Crash Button (Development Only):**
```
Purpose: Verify Crashlytics is working before production

Implementation:
  Location: Settings Page or Debug Menu (hidden in production)
  
  Test Button Action Flow:
    Action: Execute Custom Code
    Code:
      throw Exception("Test crash for Crashlytics verification");
  
  Expected Result:
    ├─ App crashes immediately
    ├─ Crash appears in Firebase Console within 5 minutes
    ├─ Stack trace shows Exception message
    └─ Custom keys visible in crash report

Production:
  ├─ Remove test button completely
  └─ Or hide behind developer menu
```

**Custom Keys Verification:**
```
Step 1: Set custom keys in normal flow
  Example: Login successfully
  Expected: user_id key set

Step 2: Force test crash
  Method: Trigger test crash button

Step 3: Check Firebase Console
  Navigate: Crashlytics → Issue Detail
  Verify: Custom keys panel shows:
    ├─ user_id: [Your test user ID]
    ├─ current_screen: [Page you were on]
    └─ Other context keys

Step 4: Validate all custom keys
  For each key configured:
    └─ Verify appears in crash report with correct value
```

---

## 🔍 Testing & Validation

### Pre-Submission Checklist

#### Firebase Configuration
- [ ] Firebase project created and connected to FlutterFlow
- [ ] Authentication enabled (Email/Password provider)
- [ ] Firestore database created with proper schema
- [ ] Google Analytics enabled in Firebase Console
- [ ] Crashlytics enabled in Firebase Console
- [ ] Firebase configuration downloaded to FlutterFlow
- [ ] All platforms configured (Android/iOS)

#### Analytics Validation
- [ ] Google Analytics enabled in FlutterFlow settings
- [ ] "On Page Load" predefined event enabled
- [ ] "On Authentication" predefined event enabled
- [ ] Test device added to Analytics DebugView
- [ ] All 5 pages show screen_view events in DebugView
- [ ] Login event appears after successful authentication
- [ ] workout_logged event appears after saving workout
- [ ] Event parameters visible and correct in DebugView
- [ ] User properties set correctly (user_id visible)
- [ ] Custom events appear within 24 hours in main dashboard

#### Crashlytics Validation
- [ ] Crashlytics enabled in FlutterFlow Firebase settings
- [ ] Test crash triggered successfully
- [ ] Crash appears in Firebase Console within 5 minutes
- [ ] Stack trace visible and readable
- [ ] Custom keys visible in crash report
- [ ] user_id custom key appears in crash report
- [ ] current_screen custom key appears in crash report
- [ ] current_action custom key appears in crash report
- [ ] Device information captured correctly
- [ ] Non-fatal errors logged successfully

#### Functionality Testing
- [ ] User can register/login successfully
- [ ] User can create workout and it appears in Firestore
- [ ] HomePage displays recent workouts from Firestore
- [ ] HistoryPage displays all workouts chronologically
- [ ] ProfilePage displays user information correctly
- [ ] Logout function works and returns to LoginPage
- [ ] Bottom navigation works between all pages
- [ ] FAB button navigates to AddWorkoutPage
- [ ] Form validation prevents invalid workout entries
- [ ] Loading indicators show during async operations

#### Data Layer Testing
- [ ] Firestore security rules allow authenticated users only
- [ ] Workout documents contain all required fields
- [ ] User documents created correctly on signup
- [ ] Queries filter by userId correctly
- [ ] Workouts appear in real-time without refresh
- [ ] Server timestamps set correctly on documents
- [ ] No permission errors in Firestore logs

---

## 📊 Implementation Evidence

### Analytics Dashboard Screenshots

**Required Screenshots:**

1. **Analytics DebugView - Real-time Events**
   - Screenshot showing screen_view events for all 5 pages
   - Screenshot showing login event with method parameter
   - Screenshot showing workout_logged event with parameters (activity_type, duration_minutes, has_notes)

2. **Analytics Dashboard - Event Overview**
   - Screenshot of Events dashboard showing all tracked events
   - Screenshot of event counts over time (last 7 days)
   - Screenshot of user engagement metrics

3. **Analytics Dashboard - Event Details**
   - Screenshot of workout_logged event detail with parameter breakdown
   - Screenshot of screen_view event detail showing all pages

4. **User Properties Configuration**
   - Screenshot showing user_id property set in console

### Crashlytics Dashboard Screenshots

**Required Screenshots:**

1. **Crashlytics Overview**
   - Screenshot of Crashlytics dashboard showing crash-free users percentage
   - Screenshot of issues list

2. **Crash Detail with Custom Keys**
   - Screenshot of crash detail page showing:
     - Stack trace
     - Custom keys panel with user_id, current_screen, current_action
     - Device information
     - User breadcrumbs

3. **Non-Fatal Errors**
   - Screenshot showing non-fatal errors logged (Firestore failures, authentication errors)

### Firestore Database Screenshots

**Required Screenshots:**

1. **Collections Structure**
   - Screenshot of Firestore console showing users and workouts collections

2. **Sample Documents**
   - Screenshot of sample user document with all fields
   - Screenshot of sample workout document with all fields

3. **Security Rules**
   - Screenshot of Firestore security rules configuration

---

## 💡 Lessons Learned & Best Practices

### Analytics Implementation

**Key Learnings:**

1. **Start with DebugView** - Real-time event verification is essential for catching configuration errors early
2. **Name events consistently** - Use lowercase_with_underscores (Firebase standard) for better dashboard organization
3. **Add meaningful parameters** - Raw events are less useful without context; parameters enable deeper analysis
4. **Don't over-track** - Focus on business-critical events, not every button press, to avoid noise in analytics
5. **User properties enable segmentation** - Set user_id and key attributes early to enable cohort analysis

**Common Pitfalls Avoided:**
- ❌ Using camelCase for event names (Firebase standard is snake_case)
- ❌ Forgetting to add event parameters (limits analysis capability significantly)
- ❌ Not testing in DebugView before deploying (catches configuration issues immediately)
- ❌ Enabling "On Each Individual Action" (creates excessive event noise)

### Crashlytics Implementation

**Key Learnings:**

1. **Custom keys are invaluable** - Context makes crashes debuggable; without keys, stack traces alone are often insufficient
2. **Set keys strategically** - Place before risky operations (Firestore writes, API calls), not after
3. **Log non-fatal errors** - Track problems before they become crashes to improve reliability proactively
4. **Test crash reporting early** - Verify setup works before production deployment
5. **Device context matters** - OS version and device model help prioritize fixes based on user impact

**Common Pitfalls Avoided:**
- ❌ Not setting user_id (impossible to contact affected users or provide personalized support)
- ❌ Setting too many keys (overwhelms crash reports and makes analysis difficult)
- ❌ Only tracking crashes (non-fatal errors are equally important for app quality)
- ❌ Testing only on web (Crashlytics doesn't support web platform)

### FlutterFlow Specific

**Optimization Strategies:**

1. **Use conditional builders** for dynamic icons/colors instead of custom code (visual, maintainable)
2. **Firestore real-time listeners** update UI automatically (no manual refresh needed)
3. **Page State for form fields**, App State for global data (proper scope management)
4. **Always validate forms** before Firestore operations (prevent invalid data, better UX)
5. **Use Server Timestamp** for createdAt fields (accurate, timezone-safe, consistent)

**Architecture Decisions:**

1. **No App State needed** - Authenticated User + Firestore queries provide sufficient state management
2. **No custom widgets required** - Standard FlutterFlow widgets handle all designs efficiently
3. **Bottom nav persistence** - Maintains context across pages, better UX
4. **Direct Firebase integration** - No backend API needed, reduces complexity
5. **Security rules in Firestore** - Protect data at database level, defense in depth

### Future Improvements

**Post-Exam Enhancements:**

1. Implement real-time weekly stats calculation (replace hardcoded values with Firestore aggregation)
2. Add edit/delete workout functionality with optimistic updates
3. Implement History page filtering by activity type with App State management
4. Add profile image upload with Firebase Storage integration
5. Create workout detail view with expanded information and notes
6. Implement workout streaks and achievements system
7. Add data visualization (charts showing workout trends over time)
8. Implement forgot password flow with email verification
9. Add social authentication (Google, Apple) for easier onboarding
10. Create comprehensive onboarding flow for new users

---

## 📚 Technical Specifications

### Development Environment
- **FlutterFlow Version:** 6.4.31
- **Flutter SDK:** Stable channel
- **Firebase SDK:** Latest (managed by FlutterFlow)
- **Target Platforms:** Android, iOS
- **Minimum SDK:** Android 21 (5.0 Lollipop), iOS 12.0

### Dependencies
- `firebase_core`: Firebase initialization
- `firebase_auth`: Authentication
- `cloud_firestore`: Database
- `firebase_analytics`: Event tracking
- `firebase_crashlytics`: Error monitoring
- FlutterFlow managed dependencies (automatic)

### Performance Considerations
- Firestore queries limited to prevent excessive reads
- ListView pagination on History page (future enhancement)
- Image optimization for profile pictures (if implemented)
- Efficient state management to minimize rebuilds
- Network-aware error handling for offline scenarios

---

## 📞 Project Information

**Project Name:** FitTracker  
**Course Code:** K4.0082  
**Module:** Firebase Analytics & Crashlytics Integration  
**Development Platform:** FlutterFlow  
**Firebase Project ID:** [Your Firebase Project ID]

**Repository:** [GitHub Repository URL]  
**Live Demo:** [App Store/Play Store Link if deployed]  
**Demo Video:** [Link to screen recording if available]

**Author:** [Your Name]  
**Email:** [Your Email]  
**Submission Date:** [Date]

---

## 📄 License

This project is created for educational purposes as part of the K4.0082 - No-Code Programming with FlutterFlow course.

---

## 🙏 Acknowledgments

- FlutterFlow documentation and community
- Firebase documentation for best practices
- Course instructors and teaching materials
- Course theory script (K4_0082_No_code_Programming_mit_FlutterFlow_Theorieskript.pdf)

---

# FitTracker - FlutterFlow Design System Configuration

## 🎨 Quick Start Guide

**How to apply this design system in FlutterFlow:**

1. Navigate to: **Theme Settings** (left sidebar)
2. Configure each section in order: **Colors → Typography → Design System**
3. Copy values from tables below directly into FlutterFlow
4. Use "Material Theme" or create custom theme

---

## 1. COLORS - Brand & Utility Colors

### Light Mode Theme

#### Brand Colors

| Color Name | Hex Code | RGB | FlutterFlow Field | Usage |
|------------|----------|-----|-------------------|-------|
| **Primary** | `#4b39ef` | rgb(75, 57, 239) | Primary | Buttons, active states, FAB, brand elements |
| **Secondary** | `#39d2c0` | rgb(57, 210, 192) | Secondary | Accent elements, highlights |
| **Tertiary** | `#ee8b60` | rgb(238, 139, 96) | Tertiary | Alternative accents |

#### Utility Colors - Text & Backgrounds

| Color Name | Hex Code | RGB | FlutterFlow Field | Usage |
|------------|----------|-----|-------------------|-------|
| **Primary Text** | `#14181b` | rgb(20, 24, 27) | Primary Text | Main text, headings |
| **Secondary Text** | `#57636c` | rgb(87, 99, 108) | Secondary Text | Subtitles, labels |
| **Primary Background** | `#f1f4f8` | rgb(241, 244, 248) | Primary Background | App background |
| **Secondary Background** | `#ffffff` | rgb(255, 255, 255) | Secondary Background | Cards, containers |
| **Border** | `#e0e3e7` | rgb(224, 227, 231) | - (use in widgets) | Borders, dividers |

#### Semantic Colors

| Color Name | Hex Code | RGB | FlutterFlow Field | Usage |
|------------|----------|-----|-------------------|-------|
| **Success** | `#249689` | rgb(36, 150, 137) | Success | Success messages, positive states |
| **Error** | `#ff5963` | rgb(255, 89, 99) | Error | Error messages, destructive actions |
| **Warning** | `#f9cf58` | rgb(249, 207, 88) | Warning | Warning messages, caution states |
| **Info** | `#4b39ef` | rgb(75, 57, 239) | Info | Information messages |

#### Activity-Specific Colors (Custom - Use in Conditional Logic)

| Activity | Background | Text | Hex Background | Hex Text |
|----------|------------|------|----------------|----------|
| **Running** | `blue-100` | `blue-600` | `#dbeafe` | `#2563eb` |
| **Cycling** | `orange-100` | `orange-600` | `#ffedd5` | `#ea580c` |
| **Gym** | `purple-100` | `purple-600` | `#f3e8ff` | `#9333ea` |
| **Yoga** | `emerald-100` | `emerald-600` | `#d1fae5` | `#059669` |
| **Swimming** | `teal-100` | `teal-600` | `#ccfbf1` | `#0d9488` |
| **Walking** | `gray-100` | `gray-600` | `#f3f4f6` | `#4b5563` |

### Dark Mode Theme (Optional)

#### Brand Colors (Same as Light)

| Color Name | Hex Code | FlutterFlow Field |
|------------|----------|-------------------|
| **Primary** | `#4b39ef` | Primary |
| **Secondary** | `#39d2c0` | Secondary |
| **Tertiary** | `#ee8b60` | Tertiary |

#### Utility Colors - Dark Mode

| Color Name | Hex Code | FlutterFlow Field | Usage |
|------------|----------|-------------------|-------|
| **Primary Text** | `#ffffff` | Primary Text | Main text |
| **Secondary Text** | `#95a1ac` | Secondary Text | Subtitles |
| **Primary Background** | `#1a2428` | Primary Background | App background |
| **Secondary Background** | `#14181b` | Secondary Background | Cards |

---

## 2. TYPOGRAPHY - Text Styles

### Font Families

| Font Type | Font Name | FlutterFlow Setting |
|-----------|-----------|---------------------|
| **Primary Font** | `Inter Tight` | Set in Typography → Primary Font Family |
| **Secondary Font** | `Inter` | Set in Typography → Secondary Font Family |
| **System Fallback** | `sans-serif` | Automatic |

### Text Style Configuration Table

**Copy these values into: Theme Settings → Typography & Icons**

| Style Name | Font Size | Font Weight | Color | Font Family | Line Height | Letter Spacing | FlutterFlow Usage |
|------------|-----------|-------------|-------|-------------|-------------|----------------|-------------------|
| **Display Large** | 64.0 | Semi Bold (600) | Primary Text | Inter Tight | 1.2 | -0.5 | Large hero text |
| **Display Medium** | 44.0 | Semi Bold (600) | Primary Text | Inter Tight | 1.2 | 0 | Hero sections |
| **Display Small** | 36.0 | Semi Bold (600) | Primary Text | Inter Tight | 1.2 | 0 | Page titles |
| **Headline Large** | 32.0 | Semi Bold (600) | Primary Text | Inter Tight | 1.3 | 0 | Section headers |
| **Headline Medium** | 28.0 | Semi Bold (600) | Primary Text | Inter Tight | 1.3 | 0 | Card headers |
| **Headline Small** | 24.0 | Semi Bold (600) | Primary Text | Inter Tight | 1.3 | 0 | Sub-headers (h1: "FitTracker", "Welcome Back") |
| **Title Large** | 20.0 | Semi Bold (600) | Primary Text | Inter Tight | 1.4 | 0 | Page titles |
| **Title Medium** | 18.0 | Semi Bold (600) | Primary Text | Inter Tight | 1.4 | 0 | Section titles (h2: "Weekly Summary", h3: "Recent Workouts") |
| **Title Small** | 16.0 | Semi Bold (600) | Primary Text | Inter Tight | 1.4 | 0 | Card titles |
| **Label Large** | 16.0 | Normal (400) | Secondary Text | Inter | 1.5 | 0 | Form labels (p: "Sign in to continue") |
| **Label Medium** | 14.0 | Normal (400) | Secondary Text | Inter | 1.5 | 0 | Input labels (label: "Email address", "Password") |
| **Label Small** | 12.0 | Medium (500) | Secondary Text | Inter | 1.5 | 0 | Small labels (span: "Nov 12 - 19", "Workouts", "Minutes") |
| **Body Large** | 16.0 | Normal (400) | Primary Text | Inter | 1.6 | 0 | Main content text |
| **Body Medium** | 14.0 | Normal (400) | Primary Text | Inter | 1.6 | 0 | Standard body text (h4: "Morning Run", "Cycling") |
| **Body Small** | 12.0 | Normal (400) | Secondary Text | Inter | 1.6 | 0 | Helper text (p: "Today, 7:30 AM", span: "5.2 km") |
| **Caption** | 10.0 | Medium (500) | Secondary Text | Inter | 1.5 | 0 | Bottom nav labels (span: "Home", "Add Workout") |

### Font Weight Reference

| Weight Name | Numeric Value | When to Use |
|-------------|---------------|-------------|
| Normal | 400 | Body text, labels, descriptions |
| Medium | 500 | Small labels, emphasized text, captions |
| Semi Bold | 600 | Headings, titles, buttons |
| Bold | 700 | Strong emphasis, primary buttons |

---

## 3. SPACING & SIZING SYSTEM

### Spacing Scale (Padding, Margins, Gaps)

| Token | Pixels | Rem | Usage in Code | FlutterFlow Value |
|-------|--------|-----|---------------|-------------------|
| `0.5` | 2px | 0.125rem | `mt-0.5` | 2 |
| `1` | 4px | 0.25rem | `gap-1`, `p-1` | 4 |
| `2` | 8px | 0.5rem | `mb-2`, `space-y-2` | 8 |
| `2.5` | 10px | 0.625rem | `px-2.5`, `py-2.5` | 10 |
| `3` | 12px | 0.75rem | `gap-3`, `mb-3` | 12 |
| `4` | 16px | 1rem | `p-4`, `gap-4`, `mb-4` | 16 |
| `6` | 24px | 1.5rem | `px-6`, `py-6`, `pb-6` | 24 |
| `8` | 32px | 2rem | `mb-8`, `pt-8` | 32 |
| `12` | 48px | 3rem | `pt-12`, `mb-12` | 48 |
| `24` | 96px | 6rem | `pb-24`, `bottom-24` | 96 |

### Size Scale (Width, Height)

| Token | Pixels | Usage in Code | FlutterFlow Value |
|-------|--------|---------------|-------------------|
| `size-5` | 20px | `size-5` (icons) | 20 |
| `size-6` | 24px | `size-6` (icons) | 24 |
| `size-8` | 32px | `size-8` (icons) | 32 |
| `size-10` | 40px | `size-10` (buttons) | 40 |
| `size-12` | 48px | `size-12` (icon containers) | 48 |
| `size-14` | 56px | `size-14` (FAB) | 56 |
| `size-16` | 64px | `size-16` (logo) | 64 |
| `h-14` | 56px | Input height | 56 |
| `h-full` | 100% | Full height | Match Parent |
| `w-full` | 100% | Full width | Match Parent |

### Border Radius Scale

| Token | Pixels | Usage in Code | FlutterFlow Value | Usage |
|-------|--------|---------------|-------------------|-------|
| `rounded-xl` | 12px | Input fields | 12 | TextFields, small containers |
| `rounded-2xl` | 16px | Cards, containers | 16 | Cards, main containers |
| `rounded-full` | 999px | Badges, pills, circular elements | 999 | FAB, badges, avatars |

---

## 4. DESIGN SYSTEM SETTINGS

### Component Configurations

#### Buttons

| Property | Value | FlutterFlow Setting |
|----------|-------|---------------------|
| **Primary Button Height** | 56px (h-14) | Button Height |
| **Primary Button Border Radius** | 12px (rounded-xl) | Border Radius |
| **Primary Button Font Size** | 18px (text-lg) | Text Style → Title Medium |
| **Primary Button Font Weight** | Bold (700) | Font Weight → Bold |
| **Primary Button Color** | Primary (#4b39ef) | Background Color → Primary |
| **Primary Button Text Color** | White | Text Color → Primary Foreground |
| **Button Shadow** | shadow-lg | Elevation → 4 |

#### Text Fields / Inputs

| Property | Value | FlutterFlow Setting |
|----------|-------|---------------------|
| **Input Height** | 56px (h-14) | TextField Height |
| **Input Border Radius** | 12px (rounded-xl) | Border Radius |
| **Input Border Color** | Border (#e0e3e7) | Border Color |
| **Input Background** | Secondary Background (#ffffff) | Fill Color |
| **Input Text Size** | 16px | Text Style → Body Large |
| **Input Placeholder Color** | Secondary Text (#57636c) | Hint Text Color |
| **Input Padding Horizontal** | 16px (px-4) | Padding Horizontal |
| **Label Font Size** | 14px (text-sm) | Text Style → Label Medium |
| **Label Font Weight** | Medium (500) | Font Weight |

#### Cards

| Property | Value | FlutterFlow Setting |
|----------|-------|---------------------|
| **Card Border Radius** | 16px (rounded-2xl) | Border Radius |
| **Card Padding** | 16px (p-4) | Padding |
| **Card Background** | Secondary Background (#ffffff) | Background Color |
| **Card Border** | 0.5px solid Border (#e0e3e7 at 50% opacity) | Border Width + Color |
| **Card Shadow** | shadow-sm | Elevation → 1 |

#### Bottom Navigation

| Property | Value | FlutterFlow Setting |
|----------|-------|---------------------|
| **Nav Height** | 72px (approximate with padding) | Height |
| **Nav Background** | Secondary Background (#ffffff) | Background Color |
| **Nav Border Top** | 1px solid Border | Border |
| **Nav Icon Size** | 24px (size-6) | Icon Size |
| **Nav Label Size** | 10px (text-[10px]) | Text Style → Caption |
| **Active Color** | Primary (#4b39ef) | Selected Item Color |
| **Inactive Color** | Secondary Text (#57636c) | Unselected Item Color |

#### Floating Action Button (FAB)

| Property | Value | FlutterFlow Setting |
|----------|-------|---------------------|
| **FAB Size** | 56px (size-14) | Width + Height |
| **FAB Border Radius** | 999px (rounded-full) | Border Radius → 999 |
| **FAB Background** | Primary (#4b39ef) | Background Color |
| **FAB Icon Size** | 32px (size-8) | Icon Size |
| **FAB Shadow** | shadow-lg | Elevation → 4 |
| **FAB Position** | Bottom: 96px, Right: 24px | Position |

---

## 5. ICON SYSTEM

### Icon Library
**Primary Icon Set:** Solar Icons (via Iconify)  
**FlutterFlow Implementation:** Use Material Icons or Font Awesome as closest alternatives

### Icon Size Reference

| Usage | Size | Pixels | FlutterFlow Setting |
|-------|------|--------|---------------------|
| **Small Icons** | `size-5` | 20px | Icon Size → 20 |
| **Regular Icons** | `size-6` | 24px | Icon Size → 24 |
| **Large Icons** | `size-8` | 32px | Icon Size → 32 |

### Icon Mapping (Solar → FlutterFlow Alternatives)

| Solar Icon | FlutterFlow Alternative | Usage |
|------------|------------------------|-------|
| `solar:home-2-bold` | `home` (Material) | Bottom nav - Home |
| `solar:dumbbell-large-linear` | `fitness_center` (Material) | Bottom nav - Add Workout |
| `solar:history-linear` | `history` (Material) | Bottom nav - History |
| `solar:user-circle-linear` | `account_circle` (Material) | Bottom nav - Profile |
| `solar:add-circle-bold` | `add_circle` (Material) | FAB button |
| `solar:running-bold` | `directions_run` (Material) | Running activity |
| `solar:bicycle-bold` | `directions_bike` (Material) | Cycling activity |
| `solar:dumbbell-large-bold` | `fitness_center` (Material) | Gym activity |
| `solar:meditation-round-bold` | `self_improvement` (Material) | Yoga activity |
| `solar:lock-password-bold` | `lock` (Material) | Login icon |
| `solar:letter-linear` | `email` (Material) | Email input |
| `solar:logout-2-bold` | `logout` (Material) | Logout button |

---

## 6. SHADOW SYSTEM

| Shadow Name | CSS Value | FlutterFlow Elevation | Usage |
|-------------|-----------|----------------------|-------|
| `shadow-sm` | Small subtle shadow | 1 | Cards, subtle elevation |
| `shadow-lg` | Larger shadow | 4 | Buttons, FAB, important elements |
| `shadow-primary/20` | Primary color shadow at 20% opacity | Custom (use Primary color) | Primary button, FAB |
| `shadow-primary/25` | Primary color shadow at 25% opacity | Custom | Login button |
| `shadow-primary/40` | Primary color shadow at 40% opacity | Custom | FAB hover state |

---

## 7. CONDITIONAL STYLING LOGIC

### Activity Type Conditional Colors

**Implementation in FlutterFlow:**  
Use **Conditional Builder** on activity icon containers

```
IF activityType == "Running"
  Background Color: #dbeafe (blue-100)
  Icon Color: #2563eb (blue-600)
  Icon: directions_run

ELSE IF activityType == "Cycling"
  Background Color: #ffedd5 (orange-100)
  Icon Color: #ea580c (orange-600)
  Icon: directions_bike

ELSE IF activityType == "Gym"
  Background Color: #f3e8ff (purple-100)
  Icon Color: #9333ea (purple-600)
  Icon: fitness_center

ELSE IF activityType == "Yoga"
  Background Color: #d1fae5 (emerald-100)
  Icon Color: #059669 (emerald-600)
  Icon: self_improvement

ELSE IF activityType == "Swimming"
  Background Color: #ccfbf1 (teal-100)
  Icon Color: #0d9488 (teal-600)
  Icon: pool

ELSE (Walking)
  Background Color: #f3f4f6 (gray-100)
  Icon Color: #4b5563 (gray-600)
  Icon: directions_walk
```

---

## 8. FLUTTERFLOW IMPLEMENTATION CHECKLIST

### Step-by-Step Configuration

**1. Colors Configuration** ✅
```
Navigate: Theme Settings → Colors
- [ ] Set Primary: #4b39ef
- [ ] Set Secondary: #39d2c0
- [ ] Set Tertiary: #ee8b60
- [ ] Set Primary Text: #14181b
- [ ] Set Secondary Text: #57636c
- [ ] Set Primary Background: #f1f4f8
- [ ] Set Secondary Background: #ffffff
- [ ] Set Success: #249689
- [ ] Set Error: #ff5963
- [ ] Set Warning: #f9cf58
```

**2. Typography Configuration** ✅
```
Navigate: Theme Settings → Typography & Icons
- [ ] Set Primary Font: Inter Tight
- [ ] Set Secondary Font: Inter
- [ ] Configure all text styles from Typography Table
- [ ] Test responsive sizing
```

**3. Design System** ✅
```
Navigate: Theme Settings → Design System
- [ ] Set Loading Indicator: Circular, Primary, Size 50
- [ ] Configure Button styles
- [ ] Configure TextField styles
- [ ] Set default border radius: 12px
```

**4. Theme Widgets** (Optional)
```
Navigate: Theme Settings → Theme Widgets
- [ ] Create reusable button styles
- [ ] Create reusable card styles
- [ ] Create activity icon component
```

---

## 9. QUICK COPY-PASTE VALUES

### Primary Colors (Copy-Paste Ready)
```
Primary: #4b39ef
Secondary: #39d2c0
Tertiary: #ee8b60
Primary Text: #14181b
Secondary Text: #57636c
Primary Background: #f1f4f8
Secondary Background: #ffffff
Success: #249689
Error: #ff5963
Warning: #f9cf58
```

### Activity Colors (Copy-Paste Ready)
```
Running Background: #dbeafe
Running Text: #2563eb
Cycling Background: #ffedd5
Cycling Text: #ea580c
Gym Background: #f3e8ff
Gym Text: #9333ea
Yoga Background: #d1fae5
Yoga Text: #059669
Swimming Background: #ccfbf1
Swimming Text: #0d9488
Walking Background: #f3f4f6
Walking Text: #4b5563
```

---

## 10. COMMON COMPONENT RECIPES

### Workout Card Component
```
Container:
  - Width: Match Parent
  - Height: Hug Contents
  - Padding: 16px
  - Border Radius: 16px
  - Background: Secondary Background
  - Border: 0.5px solid Border (50% opacity)
  - Shadow: Elevation 1

Row (inside container):
  - Spacing: 16px
  
  Icon Container:
    - Size: 48x48px
    - Border Radius: 12px
    - Background: Conditional (activity type)
    - Icon Size: 24px
    - Icon Color: Conditional (activity type)
  
  Column (flex: 1):
    - Title: Body Medium, Semi Bold, Primary Text
    - Subtitle: Body Small, Normal, Secondary Text
  
  Column (align right):
    - Duration: Body Medium, Bold, Primary Text
    - Details: Body Small, Normal, Secondary Text
```

### Primary Button Component
```
Container Button:
  - Width: Match Parent
  - Height: 56px
  - Border Radius: 12px
  - Background: Primary
  - Shadow: Elevation 4
  - Text: Title Medium, Bold, White
  - Press Effect: Scale 0.98
```

### Text Field Component
```
TextField:
  - Height: 56px
  - Border Radius: 12px
  - Border: 1px solid Border
  - Background: Secondary Background
  - Text Style: Body Large
  - Hint Text Color: Secondary Text
  - Padding: 16px horizontal, 12px vertical
  - Label Style: Label Medium, Medium weight
```

---

**Last Updated:** December 16, 2024  
**Design System Version:** 1.0  
**Based On:** FitTracker Vibe Coding Export
