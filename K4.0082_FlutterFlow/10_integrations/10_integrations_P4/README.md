### *QuickFood – Real-Time Delivery Tracking System*

---

# **PART 1 — TECHNICAL IMPLEMENTATION SUMMARY (DETAILED)**

This section covers **every technical aspect** of the implementation across UI, logic, data, backend, Firestore, Actions, permissions, and custom functions.

---

# **1. Firebase Backend Setup**

### **1.1 Firebase Project Connection**

* FlutterFlow → *Settings → Firebase*
* Connected using Google account to an existing Firebase project
* Verified:

  * Firestore enabled
  * Authentication optional
  * API configuration stored in FF

### **1.2 Firestore Database Structure**

#### **Collection: `orders`**

| Field            | Type     | Purpose                                            |
| ---------------- | -------- | -------------------------------------------------- |
| orderId          | String   | Unique ID for order-level queries                  |
| customerId       | String   | Identifies the customer                            |
| driverId         | String   | Identifies the driver                              |
| status           | String   | Order state (“picked_up”, “on_the_way”, “arrived”) |
| etaMinutes       | Integer  | Calculated ETA (optional)                          |
| customerLocation | LatLng   | Customer's delivery position                       |
| createdAt        | DateTime | Creation timestamp                                 |
| updatedAt        | DateTime | Last modification time                             |

#### **Collection: `driverLocations`**

| Field | Type | Purpose |
| driverId | String | Used for client-side filtering |
| orderId | String | Associates driver location with order |
| position | LatLng | Driver's current GPS location |
| lastUpdated | DateTime | Stream order-by optimization |

#### **Collection: `messages`**

| Field | Type | Purpose |
| orderId | String | Groups messages under same order |
| senderId | String | Driver or Customer ID |
| text | String | Chat message content |
| timestamp | DateTime | Message ordering |

---

# **2. Google Maps Setup & Integration**

### **2.1 Google Cloud Console Configuration**

* APIs enabled:

  * Maps SDK for Android
  * Maps SDK for iOS
  * Maps JavaScript API
* Credentials:

  * Created API Key
  * Optional restrictions

### **2.2 FlutterFlow Maps Integration**

* Settings → *Integrations → Google Maps*
* Added API key into FF
* Verified:

  * GoogleMap widget loads on real device
  * macOS preview shows expected warning (“not supported”)

---

# **3. Location Services**

### **3.1 Driver Location Capture**

DriverNavigationPage → On Page Load:

1. **Start Periodic Action**

   * Interval: **5000 ms**
   * Executes immediately

2. **Action inside periodic loop → Create Document**

   * Collection: `driverLocations`
   * Fields:

     * driverId → App State → `currentDriverId`
     * orderId → App State → `currentOrderId`
     * position → LatLng → *driverPosition page state* (populated via device location widget binding earlier)
     * lastUpdated → Current time

This implements real-time driver location tracking.

---

# **4. Customer Tracking System**

### **4.1 Backend Query: driverLocations**

CustomerTrackingPage:

* Query Collection → `driverLocations`
* Filters:

  * orderId == App State → `currentOrderId`
  * driverId == App State → `currentDriverId`
* Order By → `lastUpdated` (Descending)
* Streaming enabled (continuous updates)

### **4.2 Order Document Acquisition**

Because FlutterFlow currently allows **only one backend query per page**, orders are fetched via **action**, not backend query.

#### On Page Load:

1. **Firestore Query → Single Document**

   * Collection: `orders`
   * Filter: orderId == App State → currentOrderId
   * Output: `loadedOrder`

2. **Update Page State**

   * orderStatus = loadedOrder.status
   * orderCustomerLocation = loadedOrder.customerLocation

This gives CustomerTrackingPage:

* order status
* customer delivery location
* ETA input data

### **4.3 ETA Calculation (Custom Function)**

Custom Function: `calculateEtaMinutes(driver, customer)`

Implementation uses **Haversine formula**:

* Converts degrees to radians
* Computes distance
* Assumes average delivery speed (30 km/h)
* Returns ETA in minutes (min = 1)

Integrated into CustomerTrackingPage:

* When driverLocations updates:

  * ETA text → set from variable: `calculateEtaMinutes(driverPos, customerLocation)`

---

# **5. Map Marker & Visual Tracking**

CustomerTrackingPage → GoogleMap Widget:

* Num Markers: **Single**
* Marker Type: **LatLng**
* Marker Location:

  * Set from Variable → driverLocations Query → first item → position
* Map Center:

  * Bound to same location for simplicity
* Additional UI:

  * Driver marker
  * Blurred macOS preview warning ignored (works on real device)

---

# **6. Driver Status Update System**

DriverNavigationPage includes 3 buttons:

* **Picked up**
* **On the way**
* **Arrived**

Each button:

Action → Backend → Update Document:

* Collection: `orders`
* Document: Query by orderId
* Field: `status`
* New value = corresponding string

All buttons trigger **instant update** on CustomerTrackingPage because it re-pulls orderStatus on load and displays streamed driverLocations.

---

# **7. Real-Time Chat System**

### **7.1 Backend Query**

ChatPage:

* Query Collection → `messages`
* Filter:

  * orderId == currentOrderId
* Order by: timestamp ascending
* Stream: enabled
* Query Name: `orderMessages`

### **7.2 UI Structure**

```
Column
   ListView (dynamic children from orderMessages)
       Row (repeated item)
           Text: senderId
           Text: message text
   Row
       TextField
       IconButton (send)
```

### **7.3 Send Message Flow**

On IconButton tap:

1. **Create Document**

   * Collection: `messages`
   * Fields:

     * orderId → currentOrderId
     * senderId → currentUserId
     * text → TextField value
     * timestamp → Current Time

2. **Reset Form Fields**

   * Clear the TextField after send
   * Rebuild: *No Rebuild* (best practice)

Messages appear instantly due to query streaming.

---

# **8. Page Variables / App State**

### App State (Global)

* `currentOrderId` (String)
* `currentCustomerId` (String)
* `currentDriverId` (String)
* `currentUserId` (String)

### CustomerTrackingPage Local Variables

* `orderStatus` (String)
* `orderCustomerLocation` (LatLng)

### DriverNavigationPage Local Variables

* `driverPosition` (LatLng)
* `orderCustomerLocation` (LatLng) *(optional for extension; not used in core features)*

---

# **9. Navigation Structure**

* **Login / Selection (optional)** → choose driver or customer.
* **CustomerTrackingPage**

  * Shows driver, ETA, order status, and chat button
* **DriverNavigationPage**

  * Shows map, position streaming, status buttons, chat icon
* **ChatPage**

  * Shared for both roles (driver & customer)
  * Uses App State to determine sender

Uses standard FF navigation transitions.

---

# **10. Permissions & Device Requirements**

### Customer + Driver:

* Location Permissions requested automatically when using GoogleMap + driver location streaming
* No custom permission handling required for the task scope

---
