# FlutterFlow Übung 10.1.Ü.01 – Store Locator App (Maps & Location Services)

**Student:** Oren  
**Course:** GenAI Solution Manager Bootcamp  
**Date:** December 8, 2025  

---

## 1. Exercise Overview

**Exercise:** Übung 10.1.Ü.01 – Maps und Location Services  

**Goal:**  
Implement a Store Locator App in FlutterFlow that combines:

1. **Google Maps Integration & Location Services**  
2. **Firestore-based dynamic store markers**  
3. **Interactive marker tap → store detail view**  

**Subtasks from the assignment:**

- **(a)** Store Locator App with Google Maps integration, GPS-based location, automatic centering on current position, multiple map types, and a user-friendly location permission flow.  
- **(b)** Dynamic marker system for stores using Firestore, with interactive marker tap actions for detail views (category-specific icons and clustering are mentioned as optional enhancements in the course solution; technically limited in FlutterFlow, see “Technical Limitations”).

---

## 2. Data & State Structure

### 2.1 Firestore Collection: `stores`

**Collection Name:** `stores`  

**Fields:**

| Field Name     | Type    | Required | Purpose                                           |
|----------------|---------|---------|---------------------------------------------------|
| storeName      | String  | Yes     | Display name of the store                        |
| location       | LatLng  | Yes     | Store GPS coordinates                             |
| category       | String  | Yes     | Type of store (e.g. `restaurant`, `retail`, etc.)|
| address        | String  | No      | Full address (street, ZIP, city)                 |
| phone          | String  | No      | Contact phone number                             |
| openingHours   | String  | No      | Human-readable opening times                     |
| rating         | Double  | No      | Average rating between 1.0 and 5.0               |
| imageUrl       | String  | No      | Image URL of the store                           |
| isOpenNow      | Boolean | No      | Current open/closed state                        |

**Creation (in FlutterFlow):**  
`Settings → Firebase → Firestore → Add Collection → "stores"` → Add fields as above.

**Sample Documents:**  
Three example stores were added manually via **Firestore Data Manager**:

- `Burgerhain` (restaurant)  
- `Lidl` (retail)  
- `Urban Apes` (climbing/fitness)  

Each store includes a valid `location` LatLng near the user’s area (Berlin), plus address and category.

---

### 2.2 App State

**App State Variable:**

| Name            | Type    | Persistent | Purpose                                                                 |
|-----------------|---------|-----------|-------------------------------------------------------------------------|
| selectedMapType | String  | No        | Controls which of the four map widgets (roadmap/satellite/terrain/hybrid) is visible |

**Initial Value:** `"roadmap"`  

**Values Used:**

- `"roadmap"`  
- `"satellite"`  
- `"terrain"`  
- `"hybrid"`

This state is updated via a bottom sheet selector and drives conditional visibility of four Google Map widgets.

---

## 3. Section (a): Google Maps Integration & Location Services

### 3.1 Google Cloud Setup

**Google APIs enabled (in Google Cloud Console):**

- Maps SDK for Android  
- Maps SDK for iOS  
- Maps JavaScript API  

**Credentials:**

1. **Android API Key**  
2. **iOS API Key**  
3. **Web API Key**  

For each key:

- Created via: `APIs & Services → Credentials → Create Credentials → API key`  
- Mapped logically based on the API screen where it was created (Android SDK / iOS SDK / JavaScript).  
- Restrictions (development scope):  
  - Web key: HTTP referrer (web preview domain)  
  - Android & iOS: kept open for local development (no SHA restrictions yet)

---

### 3.2 FlutterFlow → Google Maps Integration

**Location:** `Settings & Integrations → Integrations → Google Maps`

**Configuration:**

- **Android API Key:** `<Android key from Maps SDK for Android>`  
- **iOS API Key:** `<iOS key from Maps SDK for iOS>`  
- **Web API Key:** `<Web key from Maps JavaScript API>`  

After saving:

- All Google Map widgets in the project no longer show integration errors.
- Maps load correctly in Web Preview and Android APK.

---

### 3.3 StoreLocator Page Structure

**Page Name:** `StoreLocator`  
**Purpose:** Main page for searching stores on a map and viewing store details.

**Layout:**

```text
StoreLocator
├── AppBar
│   ├── Title: "Store Finder"
│   └── Actions:
│       └── IconButton (map/layers icon)
│           └── On Tap: Show Bottom Sheet (MapTypeSheet)
└── Column (Primary Scroll: enabled)
    ├── Padding (horizontal)
    │   └── TextField (search placeholder; reserved for future implementation)
    └── Expanded
        └── Stack
            ├── GoogleMap_Roadmap
            ├── GoogleMap_Satellite
            ├── GoogleMap_Terrain
            └── GoogleMap_Hybrid
````

**Stack Rationale:**
All four map widgets are stacked on top of each other; **conditional visibility** (based on `selectedMapType`) ensures only one is visible at a time. This is the most reliable pattern available in FlutterFlow for switching map types driven by state.

---

### 3.4 Google Map Configuration (per Map Widget)

The following configuration is applied to all four GoogleMap widgets (Roadmap, Satellite, Terrain, Hybrid) with only the **map type** differing.

**Common Properties:**

* **Initial Map Center:**

  * `Global Properties → Current Device Location`
* **Initial Zoom:** `14.0` (balanced between local detail and overview)
* **Show User Location:** `ON`
  → Displays the blue location dot (on supported platforms).
* **Enable Zoom Gestures:** `ON`
* **Enable Scroll Gestures:** `ON`
* **Enable Rotate / Tilt:** left as default.

**Map Type per widget:**

* `GoogleMap_Roadmap` → Map Type: **Roadmap**
* `GoogleMap_Satellite` → Map Type: **Satellite**
* `GoogleMap_Terrain` → Map Type: **Terrain**
* `GoogleMap_Hybrid` → Map Type: **Hybrid**

**Conditional Visibility per widget:**

* Roadmap visible when `appState.selectedMapType == "roadmap"`
* Satellite visible when `appState.selectedMapType == "satellite"`
* Terrain visible when `appState.selectedMapType == "terrain"`
* Hybrid visible when `appState.selectedMapType == "hybrid"`

---

### 3.5 Location Permission Handling

Location permissions are handled via:

* **System permission dialog** (platform-level)
* FlutterFlow action flow ensuring user-friendly prompts.

**Behavior:**

* On first access, Android prompts for location permission.
* If denied, the app does not crash; the map still loads (without blue dot), and the user can manually pan/zoom.
* On later attempts, the system-level location settings govern behavior.

This satisfies the requirement for “benutzerfreundliche Berechtigungsabfragen für Location Services” and a robust fallback experience if the user denies access.

---

### 3.6 Map Type Switching – `MapTypeSheet` Bottom Sheet

#### Component: `MapTypeSheet`

**Purpose:** Let users choose the active map type (Standard, Satellite, Terrain, Hybrid) via a bottom sheet, following FlutterFlow’s supported UI patterns.

**Trigger:**

* AppBar action icon on `StoreLocator`:

  * **On Tap → Show Bottom Sheet → MapTypeSheet**

**MapTypeSheet Layout:**

```text
MapTypeSheet
└── Column (padding: 16)
    ├── Text ("Select map type")
    ├── ListTile ("Standard")
    ├── ListTile ("Satellite")
    ├── ListTile ("Terrain")
    └── ListTile ("Hybrid")
```

**ListTile Actions:**

Each ListTile has the same pattern:

1. **Action 1:** Update App State → `selectedMapType`

   * Standard → `"roadmap"`
   * Satellite → `"satellite"`
   * Terrain → `"terrain"`
   * Hybrid → `"hybrid"`

2. **Action 2:** `Navigate Back` (closes the bottom sheet immediately)

**Result:**

* One tap = choose map type **and** close sheet.
* Underneath, the visible map switches according to `selectedMapType` and the map type changes visually.

---

## 4. Section (b): Firestore-Based Dynamic Markers

### 4.1 Backend Query: `allStores`

On the `StoreLocator` page, a backend query retrieves all store documents.

**Configuration:**

* **Type:** Query Collection
* **Collection:** `stores`
* **Query Name:** `allStores`
* **Order By:** `storeName` (ascending)
* **Filters:** None (all stores returned; filtering by `isOpenNow` could be added later)

This query provides the list used for marker placement on the map.

---

### 4.2 Marker Configuration (Multiple Markers)

For each Google Map widget (Roadmap, Satellite, Terrain, Hybrid):

* **Num Markers:** `Multiple`
* **Marker Type:** `Document`
* **Marker Documents:**

  * `Set from Variable → allStores → Documents`

FlutterFlow automatically iterates through `allStores` and adds one marker per document.

**Location Field:**

* The `location` field of type LatLng in each `stores` document is used implicitly by FlutterFlow for marker coordinates.

**Marker Icon:**

* A **single icon style** is used for all markers (default Google marker or a shared asset).
* FlutterFlow currently does **not** support dynamic per-document marker icons or multiple marker sets inside a single map widget. This is a platform limitation and is documented in the “Technical Challenges & Limitations” section.

---

## 5. Store Detail View (Marker Tap → Detail Page)

### 5.1 `StoreDetail` Page

**Purpose:** Show full information for a store when the user taps a marker.

**Page Name:** `StoreDetail`

**Page Parameter:**

| Name  | Type     | Collection |
| ----- | -------- | ---------- |
| store | Document | stores     |

This parameter receives the tapped store document reference.

---

### 5.2 `StoreDetail` Layout

```text
StoreDetail
├── AppBar
│   └── Title: "Store Details"
└── SingleChildScrollView / Column
    ├── Image (Network) – store.imageUrl
    └── Padding (24)
        └── Column
            ├── Text (store.storeName)
            ├── Text (store.category)
            ├── Text (store.address)
            ├── Text (store.openingHours)
            ├── Text (store.phone)
            ├── Text ("Rating: X.X") – from store.rating
            └── (Optional future buttons: Call, Navigate)
```

**Data Binding:**

Each widget uses:

* **Set from Variable → Page Parameters → store → [field]**

---

### 5.3 On Marker Tap → Navigate to Detail

For each Google Map widget (at least `Roadmap`, optionally all four):

**Action:** `On Marker Tap`

Action Flow:

1. **Navigate To → StoreDetail**
2. Parameter Mapping:

   * `store` → **Current Marker Document** (current `stores` document associated with the tapped marker)

**Result:**

* Tapping a marker opens the `StoreDetail` page.
* The page shows the exact data of the store represented by that marker.
* This fulfills “interaktive Marker-Informationen mit Tap-Aktionen für Detailansichten”.

---

## 6. Technical Challenges & Solutions

### 6.1 Google Maps API Configuration

**Challenge:**
Finding the correct places in Google Cloud Console for enabling APIs and creating platform-specific keys (Android/iOS/Web).

**Issues encountered:**

* Initial confusion between `Library` and `Credentials` views.
* Multiple API enable screens looked similar.

**Solution:**

* Use the left sidebar:

  * `APIs & Services → Library` to enable:

    * Maps SDK for Android
    * Maps SDK for iOS
    * Maps JavaScript API
  * `APIs & Services → Credentials` to create keys:

    * API keys created while viewing each specific API page (Android SDK, iOS SDK, JS API) and then mapped to FlutterFlow’s fields accordingly.

**Learning:**
Always configure:

1. APIs under **Library**
2. Keys under **Credentials**
3. Then plug each key into the correct FlutterFlow integration field.

---

### 6.2 Firebase Authentication Error (`firebase@flutterflow.io`)

**Challenge:**
Firestore Data Manager showed an error:

> “Could not create an account as [firebase@flutterflow.io](mailto:firebase@flutterflow.io). Make sure Email Sign-In is turned on.”

**Root Cause:**
Email/Password provider was disabled in Firebase Authentication.

**Solution:**

1. Go to Firebase Console → Authentication.
2. Tab: **Sign-in method**.
3. Enable **Email/Password** provider (no users need to be created manually).

FlutterFlow then automatically creates and uses the `firebase@flutterflow.io` user for Firestore Data Manager.

---

### 6.3 Map Type Switching – No `PopupMenuButton` in FlutterFlow

**Challenge:**
The course solution suggests using a `PopupMenuButton` (Flutter widget) in the AppBar. This widget does **not exist** in FlutterFlow’s visual builder.

**Solution:**

* Use a **Bottom Sheet** (`MapTypeSheet`) as a cross-platform alternative.
* AppBar icon → `Show Bottom Sheet → MapTypeSheet`
* MapTypeSheet writes to `selectedMapType` and closes itself.
* Four map widgets are controlled via conditional visibility based on `selectedMapType`.

**Learning:**
When FlutterFlow does not expose a specific Flutter widget, use the closest supported UI pattern (e.g., Bottom Sheets, standard Buttons, menus via ListTiles).

---

### 6.4 Marker Icon per Category & Clustering (Platform Limitations)

**Challenge (from course solution):**

* Category-specific marker icons
* Marker clustering for dense areas

**FlutterFlow Limitation (as of 2025):**

* Only **one marker configuration** per Google Map widget is supported.
* Marker icon configuration is global for the marker set; there is no per-document “conditional icon” or multiple marker sets with different icons inside a single map widget.
* Marker clustering is not exposed as a configuration option.

**Resulting Design Decisions:**

* Use a **single marker icon style** for all stores.
* Focus on correct dynamic marker placement and tap navigation to detail instead of unsupported visual enhancements.
* Document these as **known limitations**, not missing implementation.

**Learning:**
Always align implementation with what FlutterFlow actually supports, even if course text describes more advanced pure-Flutter capabilities.

---

## 7. Testing & QA

### 7.1 Web Preview (FlutterFlow Run Mode)

**Tests:**

1. **Page load**

   * `StoreLocator` loads without errors.
   * Map is visible immediately.
2. **Device location (browser)**

   * If location is allowed: initial center close to real position.
   * If denied: map still loads; user can manually pan and zoom.
3. **Map type switching**

   * AppBar icon opens `MapTypeSheet`.
   * Tapping each option (Standard/Satellite/Terrain/Hybrid) updates visible map.
4. **Markers**

   * All 3 stores appear as markers in the relevant geographic area.
5. **Marker tap**

   * Tapping a marker navigates to `StoreDetail`.
   * Correct store data is displayed.

---

### 7.2 Android APK (Real Device)

**Tests & Results:**

1. **Basic page load (mobile)**

   * App opens `StoreLocator`.
   * Map renders correctly.
2. **Location / blue dot (mobile)**

   * System permission dialog appears.
   * On allow: map centers on device location; blue dot is visible.
3. **Map type switching**

   * Tap AppBar icon → bottom sheet opens.
   * Tap any map type → sheet closes → map tiles update accordingly.
4. **Default behavior on reload**

   * On app restart, default map is Roadmap (`selectedMapType = "roadmap"`).
   * Map loads without requiring reconfiguration.
5. **Permission denial path**

   * Denying location permission keeps the app functional.
   * Map loads, but without blue dot; user can still search visually.
6. **Marker tap to details**

   * Tap Burgerhain marker → navigates to `StoreDetail` with Burgerhain info.
   * Same behavior verified for Lidl and Urban Apes.

---

## 8. Design Decisions & Rationale

### 8.1 Bottom Sheet vs. Menu Button

* **Why Bottom Sheet?**
  FlutterFlow lacks `PopupMenuButton`. Bottom sheets are:

  * Highly visible
  * Easy to configure
  * Mobile-friendly
  * Native to FlutterFlow’s interaction model

* **Result:**
  Clean, clear UX for choosing map types, consistent across web and mobile.

---

### 8.2 Four Map Widgets vs. Binding MapType Property

The course solution suggests binding Map Type directly to an app state variable. In FlutterFlow’s UI/feature set, direct binding of map type is not available. Therefore:

* **Chosen approach:** Four separate map widgets inside a Stack.
* **Control:** Conditional visibility via `selectedMapType`.

This achieves the same UX outcome with a FlutterFlow-compatible pattern.

---

## 9. Summary of Implementation

### Part (a) – Google Maps & Location Services: **Completed ✓**

* Google Maps integrated with Android, iOS, Web API keys.
* Automatic centering on current user position (GPS).
* Blue dot user location indicator on mobile.
* Permissions handled gracefully with system dialogs.
* Four map types (Roadmap, Satellite, Terrain, Hybrid) implemented.
* Map type switching via a dedicated Bottom Sheet (`MapTypeSheet`).

### Part (b) – Firestore & Dynamic Markers: **Completed ✓**

* Firestore `stores` collection with rich store schema.
* `allStores` backend query feeding dynamic markers.
* Multiple markers rendered from Firestore on all map types.
* Tapping a marker opens `StoreDetail` with full store information.
* Marker icon is uniform (technical limitation).

---

## 10. Final Status

* **Exercise:** Übung 10.1.Ü.01
* **FlutterFlow Version:** 6.4.51
* **Flutter Version:** 3.32.4
* **Platform Testing:** FlutterFlow Web Preview, Android APK
* **Overall Completion:**

  * All core requirements for parts (a) and (b) are fully implemented within FlutterFlow’s capabilities.
  * Documented platform limitations for optional advanced features (category-specific icons, clustering).

**Final Status:** ✅ Store Locator App – Implementation Complete and Ready for Review.
::contentReference[oaicite:0]{index=0}
```
