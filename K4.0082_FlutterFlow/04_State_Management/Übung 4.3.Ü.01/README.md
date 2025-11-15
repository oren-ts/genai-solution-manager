# FlutterFlow State Management Exercise — 4.3.Ü.01

---

## a) State Hierarchy

| State Variable | Scope | Data Type | Usage |
|----------------|-------|-----------|-------|
| Current user’s role | App State | String | Role-based access control |
| ID of the task being viewed | Page State | String | Load correct task on detail page |
| Filter panel open | Component State | Boolean | Toggle visibility in reusable panel |
| Title input text | Widget State | String | Capture user input in TextField |

> **Access**: Via **Set from Variable** → respective scope in dropdown.

---

## b) Page State Variables (`TaskDetailPage`)

| Name | Type | Initial | Reset on Exit? |
|------|------|---------|----------------|
| `selectedPriority` | String | `medium` | Yes |
| `isEditMode` | Boolean | `false` | Yes |
| `taskProgress` | Integer | `0` | Yes |
| `deadlineReminder` | Boolean | `true` | Yes |

> **Path**: Properties → Page State → + Add Variable  
> **Auto-reset** prevents data leakage between tasks.

---

## c) Conditional Logic

**1. Single Condition**  
- **Trigger**: Page Load  
- **Logic**: `task.deadline < Current Time`  
- **True**: Show “Overdue”  
- **False**: Hide “Overdue”

**2. AND Condition**  
- **Logic**: `(currentUserId == task.ownerId) AND (task.status != "completed")`  
- **True**: Enable Edit Mode  
- **False**: View-only

**3. OR Condition**  
- **Logic**: `(priority == "urgent") OR (deadline < Current Time + 24h)`  
- **True**: Show High Priority badge

> **Path**: Actions → Logic → Conditional

---

## d) Loops

**While Loop** (Progress Animation)  
- **Trigger**: Button Tap  
- **Condition**: `taskProgress < 100`  
- **Body**: `+10 → Wait 100ms → Update ProgressBar`  
- **Safety**: Break after 10 iterations

**Over List Loop**  
- **List**: `tasksList`  
- **Item**: `loopItem`  
- **Body**: If `loopItem.deadline < Current Time` → `loopItem.isOverdue = true`  
- **Safety**: Finite list → no infinite loop

---

## e) Conditional Values

| Property | Conditional Logic |
|---------|-------------------|
| **Background Color** | `high→red`, `medium→yellow`, `low→green`, else `grey` |
| **Icon** | `pending→schedule`, `inProgress→play`, `completed→check` |
| **Deadline Text** | `<1d → "TODAY!"`, `<7d → "This week"`, else date |

> **Path**: Widget → Property → Set from Variable → Conditional Value

---

**References**:  
[FlutterFlow Docs - State Management](https://docs.flutterflow.io/)  
[Conditional Logic Guide](https://docs.flutterflow.io/actions/logic/conditional)

---
