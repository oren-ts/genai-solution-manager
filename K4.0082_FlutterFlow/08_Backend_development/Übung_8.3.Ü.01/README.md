# 🌦️ Weather App with OpenWeather API - Exercise 8.3.Ü.01

## Project Overview

A mobile weather application built with FlutterFlow v6.4.x that consumes the OpenWeather REST API, parses JSON responses, manages UI state, and implements a simple caching strategy for repeated city lookups.[1][2]

**Course:** GenAI Solution Manager Bootcamp - FlutterFlow Module (K4.0082_2.0)  
**Exercise:** REST API Calls & State Management  
**Status:** ✅ Complete

***

## 🎯 Learning Objectives Achieved

- ✅ Configured a REST `GET` API Call to OpenWeather with dynamic query parameters.[2][1]
- ✅ Implemented JSON path parsing for nested API responses.  
- ✅ Built a weather UI that reacts to API output and page state.  
- ✅ Managed loading, success, and error states with page variables and conditional visibility.[3]
- ✅ Implemented a simple client-side caching strategy to avoid redundant API calls.  
- ✅ Performed structured API testing (success, failure, and invalid input scenarios).[4][2]

***

## 🏗️ Application Architecture

### Page Structure

```
📱 HomePage (Weather App)
   ├─ AppBar: "Weather App"
   ├─ Column (Main Content)
   │  ├─ Container (Input Section)
   │  │  ├─ TextField (city input)
   │  │  └─ Button "Get Weather"
   │  ├─ Helper Text ("Type a city and tap Get Weather")
   │  ├─ Text (Error message, conditional)
   │  ├─ CircularProgressIndicator (conditional)
   │  └─ Card (Weather Result, conditional)
   └─ Snackbars (success, error, cached-info)
```

### Data Flow Overview

1. User types a city name into the TextField.  
2. TextField `On Change` updates page state variable `cityName`.  
3. Button `On Tap` runs an action flow:  
   - Checks if the city matches `lastSearchedCity` (cache check).  
   - If cached: shows Snackbar and reuses existing state.  
   - If not cached: sets loading state, calls `getWeatherData` API, then updates state on success or error.  
4. Card and helper/error/loading widgets react via conditional visibility bound to `hasData`, `isLoading`, and `errorMessage`.

***

## 🌐 API Call Configuration

### API: `getWeatherData`

**Definition:**

- **Method:** `GET`  
- **URL:** `https://api.openweathermap.org/data/2.5/weather`[2]
- **Auth Type:** Standard (not private, free API key).  

### Headers

| Header Name | Value | Purpose |
|------------|-------|---------|
| `Accept` | `application/json` | Request JSON response format.[2] |

### Query Parameters

| Name | Value Source | Type | Example Value | Purpose |
|------|--------------|------|---------------|---------|
| `q` | From Variable (`cityName` API variable) | String | `Berlin` | City name to query. |
| `appid` | Specific Value | String | `<OPENWEATHER_API_KEY>` | API key for authentication.[5][2] |
| `units` | Specific Value | String | `metric` | Celsius units. |
| `lang` | Specific Value | String | `de` | German weather descriptions. |

### API Variables

| Variable | Type | Default | Used In |
|----------|------|---------|---------|
| `cityName` | String | `Berlin` | Bound to query parameter `q` in the API Call editor. |

***

## 🧾 JSON Schema & Parsing

### Example Response (simplified)

OpenWeather’s current weather endpoint returns structured JSON including `main`, `weather`, and `name` sections for temperature, humidity, description, and city name.[2]

### JSON Paths

Configured under **Response & Test → JSON Paths**:

| JSON Path | Name | Type | Description |
|-----------|------|------|-------------|
| `$.main.temp` | `temperature` | Number | Current temperature in °C. |
| `$.weather[0].description` | `description` | String | Textual weather description (German). |
| `$.main.humidity` | `humidity` | Number | Relative humidity in %. |
| `$.name` | `cityName` | String | Resolved city name. |
| `$.message` | `errorMessage` | String | Error message for failed requests (e.g., city not found). |

These paths are then available for binding in UI widgets and state updates.[1][2]

***

## 🧠 State Management

### Page State Variables

| Variable | Type | Default | Purpose |
|----------|------|---------|---------|
| `cityName` | String | `Berlin` | Current city input used for API requests. |
| `isLoading` | Boolean | `false` | Indicates an in-progress API call. |
| `hasData` | Boolean | `false` | Indicates valid weather data is available. |
| `errorMessage` | String | `""` | Stores latest error message from API. |
| `weatherData` | JSON / Map | empty | Holds the last successful full API response. |
| `lastSearchedCity` | String | `""` | Caching: name of last successful city query. |

### Widget State

| Widget | State | Purpose |
|--------|-------|---------|
| TextField | text value | Captures raw user input before syncing to `cityName`. |

***

## 🎨 User Interface Components

### Input & Instructions

**Container (Input Section):**

- `TextField`  
  - Hint: `Enter city name`  
  - `On Change` action: Update Page State → `cityName = TextField value`.  

- `Button` – **Get Weather**  
  - Primary style, full-width within container.  
  - `On Tap`: executes full action flow (cache check → API call → state updates → Snackbars).

**Helper Text:**

- Text: `Type a city and tap Get Weather`.  
- Visibility condition: `hasData == false && isLoading == false`.

**Error Text (Optional Display):**

- Text bound to page `errorMessage`.  
- Visibility: `errorMessage != "" && hasData == false`.

### Loading Indicator

- `CircularProgressIndicator` centered near the card area.  
- Visibility: `isLoading == true`.  

### Weather Card

**Layout:**

```
Card
└─ Padding (16)
   └─ Column (centered)
      ├─ Text: cityName (size ~20, bold)
      ├─ Text: temperature + "°C"
      ├─ Text: description
      └─ Text: humidity + "%"
```

**Data Bindings:**

- City: JSON Path `cityName` from API response or `weatherData.cityName`.  
- Temperature: `temperature` with suffix `°C`.  
- Description: `description`.  
- Humidity: `humidity` with suffix `%`.

**Visibility:**

- Condition: `hasData == true`.

Snackbars provide immediate feedback:
- Success: `Weather data loaded!`.  
- Error: `Error: <errorMessage>` or fallback text.  
- Cache hit: `Using cached weather data`.

***

## ⚙️ Button Action Flow & Logic

### Overview

The **Get Weather** button action flow uses a top-level conditional for caching, followed by state updates and API handling.

```text
Button OnTap
  ├─ Conditional 1: cityName == lastSearchedCity
  │   ├─ TRUE:
  │   │   └─ Action: Show Snackbar ("Using cached weather data")
  │   └─ FALSE:
  │       ├─ Action 1: Update Page State
  │       │   ├─ isLoading = true
  │       │   ├─ hasData = false
  │       │   └─ errorMessage = ""
  │       ├─ Action 2: Backend Call → getWeatherData (cityName from page state)
  │       └─ Conditional 2: API Result Succeeded?
  │           ├─ TRUE:
  │           │   ├─ Update Page State:
  │           │   │   ├─ isLoading = false
  │           │   │   ├─ hasData = true
  │           │   │   ├─ weatherData = full API response
  │           │   │   └─ lastSearchedCity = cityName
  │           │   └─ Show Snackbar ("Weather data loaded!")
  │           └─ FALSE:
  │               ├─ Update Page State:
  │               │   ├─ isLoading = false
  │               │   ├─ hasData = false
  │               │   └─ errorMessage = API errorMessage path (e.g., "city not found")
  │               └─ Show Snackbar ("Error loading weather data")
```

### Notes

- `hasData` is reset to `false` when starting a fresh non‑cached request so stale data is not displayed for the new city.  
- Caching branch (TRUE) does **not** toggle `isLoading`, so UI remains stable when reusing existing data.  

***

## 🧪 API Testing & Scenarios

Testing was conducted both in the browser and in FlutterFlow’s **Response & Test** tab for `getWeatherData`.[4][2]

### Browser Sanity Check

- URL format:  
  `https://api.openweathermap.org/data/2.5/weather?q=Berlin&appid=YOUR_KEY&units=metric&lang=de`  
- Verified status `200` and realistic JSON for Berlin and other cities.  
- Verified error response for invalid city (e.g., “Toda Raba”) with `{"cod":"404","message":"city not found"}`.[2]

### FlutterFlow Test Cases

**1. Valid city – Berlin**

- Input: `Berlin`  
- Expected: Status `200`, populated `main`, `weather`, and `name`.  
- UI: Card shows Berlin data, Snackbar “Weather data loaded!”, `hasData=true`, `isLoading=false`.

**2. Valid city – Stockholm**

- Input: `Stockholm`  
- Expected: Status `200`, city name “Stockholm”, different temperature/humidity.  
- UI: Card updates with Stockholm values; state variables confirm new data.

**3. Invalid city – nonsense string**

- Input: `Toda Raba` (nonexistent city)  
- Expected: Status `404`, JSON `message` field “city not found”.  
- UI: No card, error Snackbar, `hasData=false`, `errorMessage="city not found"`.

**4. Repeated city – caching**

- Input sequence: `Berlin` → `Berlin` again within same session.  
- Expected: Second tap triggers cache branch: no new API request, Snackbar “Using cached weather data”, card unchanged.  
- UI: No visible loading spinner on second tap; state inspector shows `lastSearchedCity="Berlin"` and `weatherData` reused.

*(Additional cases such as empty string and umlauts can be added as future test documentation.)*

***

## 🧊 Caching Strategy

The app implements a simple, state-based caching strategy tailored for frequently repeated city lookups.

### Mechanism

- `weatherData` stores the last successful API response JSON.  
- `lastSearchedCity` stores the city name of that response.  
- Before each API call, a conditional compares `cityName` and `lastSearchedCity`.  
  - If equal → assume cached data is still valid; skip API call and just notify user.  
  - If different → perform full flow: loading state, API call, data/state update.

### Rationale

- Reduces unnecessary API calls when users repeatedly check the same city.  
- Keeps implementation simple and transparent within the Action Flow editor, without relying on version-specific query cache toggles.[6][7]

***

## 🔍 Debugging & Troubleshooting Notes

During development, several key issues were identified and resolved:

- **Issue:** 401 "Invalid API key" from OpenWeather.  
  - **Resolution:** Verified URL and key by calling the endpoint directly in the browser, confirmed activation delay, and ensured no extra whitespace in `appid` query parameter.[5][8]

- **Issue:** Different cities showing the same data.  
  - **Resolution:** Ensured the API variable `cityName` was correctly bound to the button’s Backend Call (not left at default “Berlin”) and that TextField `On Change` updated page state.

- **Issue:** Confusion about JSON Path types.  
  - **Resolution:** Ran a successful test first (status 200) so FlutterFlow could infer types, then explicitly set types: Number for `temperature`/`humidity`, String for textual fields.[1]

- **Issue:** Understanding of caching vs. state reset.  
  - **Resolution:** Reordered Action Flow so the cache check runs *before* setting `isLoading` or calling the API; this prevents unnecessary loading states on cache hits.

***

## 🎓 Key Learning Outcomes

### FlutterFlow Skills

- REST API integration with query parameters, headers, and test tooling.[4][1]
- JSON Path configuration and type assignment for nested responses.[1]
- Page-level state management for loading, data, error, and caching flags.[3]
- Visual Action Flow design with conditionals, backend calls, and user feedback.  
- Conditional visibility patterns for loading, empty, error, and data states.[9][10]

### API & Backend Concepts

- Understanding HTTP status codes (`200`, `401`, `404`) and interpreting OpenWeather error payloads.[5][2]
- Safe handling of API keys via query parameters rather than headers in this specific API.  
- Practical use of simple caching to balance responsiveness and network usage.[7][6]

***

## 👨‍💻 Development Information

**Developer:** Oren (GenAI Solution Manager Bootcamp Student)  
**Development Period:** November 2025  
**FlutterFlow Version:** v6.4.x  
**External Service:** OpenWeather – Current Weather Data API (free tier).[2]

**Exercise Completion:** ✅ 100% for core API, UI, state, error handling, and caching requirements.

[1](https://docs.flutterflow.io/resources/backend-logic/rest-api)
[2](https://www.reddit.com/r/FlutterFlow/comments/1aw1a56/need_more_info_on_conditional_visibility/)
[3](https://docs.flutterflow.io/resources/backend-query/)
[4](https://docs.flutterflow.io/resources/backend-logic/create-test-api)
[5](https://www.youtube.com/watch?v=JNy-6xckc5M)
[6](https://community.flutterflow.io/database-and-apis/post/api-call-caching-and-pull-to-refresh-kYPAxa7urtFo7Wd)
[7](https://www.reddit.com/r/FlutterFlow/comments/1cj3134/caching_data_and_where_to_place_the_api_call_in/)
[8](https://stackoverflow.com/questions/72653892/invalid-api-key-in-openweathermap-error-401)
[9](https://www.youtube.com/watch?v=OUVZ-p7IzW8)
[10](https://www.youtube.com/watch?v=YFFdfhNn3hw)
