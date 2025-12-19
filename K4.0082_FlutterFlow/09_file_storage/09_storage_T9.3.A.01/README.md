# 📘 Voice Memo App — Full Technical Implementation Guide  
### FlutterFlow + Firebase (Storage, Firestore, Anonymous Auth)  
**Assignment: Transferaufgabe 09.3.A.01 — Files & Storage**

---

## 🔥 Overview

The **Voice Memo App** is a cross-platform mobile/web prototype built entirely in **FlutterFlow**, designed to demonstrate:

1. **Audio recording (Start/Stop)**
2. **Microphone permissions**
3. **Real-time recording timer**
4. **Audio upload to Firebase Storage**
5. **Metadata storage in Firestore**
6. **Anonymous Authentication**
7. **Dynamic voice memo list**
8. **In-app audio playback (AudioPlayer)**
9. **User-friendly recording UI & snackbars**

This README documents all technical implementation steps in detail.

---

# 🚀 1. Project Setup

## 1.1 Create FlutterFlow Project
- Project name: **VoiceMemoApp**
- Platforms enabled:
  - **Android** (required for recording)
  - Web (optional)
  - iOS (optional)

---

# 🔐 2. Firebase Setup

## 2.1 Create Firebase Project
In FlutterFlow → **Settings → Firebase**  
Use the automatic setup wizard (recommended by FF).

FlutterFlow creates:
- Firebase project
- Android app registration
- Storage bucket
- Firestore database

---

## 2.2 Enable Authentication
Firebase Console → Authentication → Sign-in methods → Enable:

### ✔ Anonymous Authentication

Used so each device can upload to a secure personal folder.

---

## 2.3 Firestore Rules

FlutterFlow → Firebase → Firestore → Deploy Rules:

```js
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /voiceMemos/{docId} {
      allow read, write: if request.auth != null;
    }
  }
}
````

---

## 2.4 Storage Rules

FlutterFlow → Firebase → Storage → Deploy Rules:

```js
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /voice_memos/{userId}/{allPaths=**} {
      allow read, write: if request.auth != null
        && request.auth.uid == userId;
    }
  }
}
```

These rules enforce:

* uploads only inside `/voice_memos/<uid>/`
* each user can read/write only their own memos

---

# 📱 3. Page Structure

Create page **VoiceMemoApp**

```
AppBar  
  └ Text: Voice Memos  
  └ Icon (mic)

Column  
  └ Container (Recording UI)  
       └ Column  
            └ Text (Timer 00:00)  
            └ Icon (Recording Dot)

  └ ListView (voice memos list)  
       └ Card (dynamic item)  
            └ Column  
                 └ Row  
                      └ Icon  
                      └ Text: title  
                      └ Text: duration  
                 └ Divider  
                 └ AudioPlayer (Network)

FloatingActionButton  
  └ Icon (mic/stop — conditional)
```

---

# 🧠 4. App State Variables

| Variable                            | Type    | Default | Purpose                    |
| ----------------------------------- | ------- | ------- | -------------------------- |
| `isRecording`                       | Boolean | false   | Determines recording state |
| `recordingDuration`                 | Integer | 0       | Timer value in seconds     |
| *(optional)* `currentRecordingName` | String  | ""      | Store generated filename   |

---

# 🎤 5. Audio Recording Logic

## 5.1 Page Load Actions

### A. Check Microphone Permission

Conditional workflow:

* IF microphone permission granted → continue
* ELSE request permission
* IF denied → show Snackbar/Alert

### B. Ensure Anonymous Login

Conditional:

* IF user is not logged in → **Log In (Anonymous)**
* ELSE → continue

---

# 🎛️ 6. UI Recording State

### Recording Container Color

```
IF isRecording == true → light red (#FFE0E0)
ELSE → grey (#EFEFEF)
```

### FAB Icon

```
IF isRecording == true → Icons.stop
ELSE → Icons.mic
```

---

# ⏱️ 7. Start/Stop Recording (FAB Action)

Open **FloatingActionButton → On Tap**:

## Conditional: IF `isRecording == true`

→ **STOP RECORDING**

1. **Stop Audio Recording**

   * Output: Recorded File (Widget State)

2. **Update App State**

   * isRecording = false

3. **Stop Timer**

4. **Upload file to Firebase Storage**

   * Upload Type: Firebase
   * File Type: Uploaded File
   * File to Upload: Recorded File
   * Path:

     ```
     voice_memos/${authUser.uid}/
     ```
   * File Name (fx):

     ```
     "memo_" + CurrentTimeMilliseconds + ".m4a"
     ```

5. **Create Firestore Document**
   Collection: `voiceMemos`

   Fields:

   | Field     | Value                          |
   | --------- | ------------------------------ |
   | audioUrl  | UploadedFileUrl                |
   | duration  | AppState.recordingDuration     |
   | createdAt | Current Time                   |
   | title     | "Voice Memo " + formatted date |
   | userId    | authUser.uid                   |

---

## ELSE → **START RECORDING**

1. **Start Audio Recording**
2. **Update App State**

   * isRecording = true
   * recordingDuration = 0
3. **Start Timer (every 1s)**

   * recordingDuration += 1

---

# ☁️ 8. Firebase Upload Validation

On Android:

* all recordings successfully uploaded
* storage files stored under `/voice_memos/<uid>/`
* Firestore documents properly created

---

# 🎵 9. Voice Memo List (Firestore Query)

Select **ListView** → Set Backend Query:

* Collection: `voiceMemos`
* Filter:

  ```
  userId == authUser.uid
  ```
* Sort:

  ```
  createdAt DESC
  ```

---

# 🔈 10. Audio Playback

Inside ListView → Card → AudioPlayer:

* **Audio Type:** Network
* **Path (fx):**
  From Variable → `recordingItems Item` → `audioUrl`

Player then retrieves the uploaded Firebase URL.

---

# ⭐ 11. UX Enhancements

### Empty State

Displayed when no memos exist:

```
Icon: mic_off
Text: "No voice memos yet. Tap the mic to start recording!"
```

### Upload Snackbar

```
"Voice memo uploaded successfully!"
```

### Permission Error

```
"Microphone permission required."
```

---

# 🧪 12. QA Test Plan (Passed)

✔ Permissions
✔ Start/Stop recording
✔ Timer increments
✔ Firebase Storage upload
✔ Firestore metadata
✔ User-filtered list
✔ Audio playback
✔ Android APK test successful

---

# 🎓 Summary

This README documents a complete Voice Memo App implementation using:

* FlutterFlow
* Firebase Storage
* Firestore
* Anonymous Authentication
* AudioPlayer widget
* Recording/timer UI
* Secure per-user storage paths
