# =============================================================================
# Task C: Rule-Based vs AI-Based Chatbot
# =============================================================================
# Purpose: Demonstrate the differences between rule-based and AI-based chatbots
#          using the example question: "What time is it?"
# =============================================================================

# =============================================================================
# APPROACH 1: RULE-BASED CHATBOT
# =============================================================================
"""
Characteristics:
- Uses predefined patterns/rules
- Direct string matching
- No learning involved
- Deterministic behavior
"""

# Define all possible time-related patterns
rules = [
    "time", 
    "what time is it", 
    "what is the time", 
    "current time",
    "tell me the time"
]

# Process user input
user_input = "What time is it?"
input_lower = user_input.lower()

# Check if input matches any rule
for rule in rules:
    if rule in input_lower:
        time = get_current_time()
        return time

# If no rule matched
return "I don't understand"

"""
Strengths:
- Simple to implement
- Predictable and controllable
- Fast execution
- No training required

Weaknesses:
- Brittle (fails on unexpected phrasings)
- Requires manual rule updates
- Cannot handle variations not explicitly coded
- Maintenance-heavy as complexity grows
"""

# =============================================================================
# APPROACH 2: AI-BASED CHATBOT
# =============================================================================
"""
Characteristics:
- Learns patterns from training data
- Uses machine learning models
- Can generalize to new phrasings
- Probabilistic behavior
"""

# -----------------------------------------------------------------------------
# PHASE 1: TRAINING (Done Once, Offline)
# -----------------------------------------------------------------------------

# 1. Prepare training data with labeled intents
training_data = [
    ("what time is it", "get_time"),
    ("tell me the time", "get_time"),
    ("current time please", "get_time"),
    ("time now", "get_time"),
    ("what's the weather", "get_weather"),
    ("how are you", "greeting"),
    # ... hundreds/thousands more examples
]

# 2. Extract features from text (convert text to numbers)
vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform([text for text, intent in training_data])
y_train = [intent for text, intent in training_data]

# 3. Train classifier
model = MultinomialNB()
model.fit(X_train, y_train)

# -----------------------------------------------------------------------------
# PHASE 2: INFERENCE (Every User Query)
# -----------------------------------------------------------------------------

# 1. Receive user input
user_input = "hey what time is it now?"

# 2. Preprocess: convert to same format as training data
input_vector = vectorizer.transform([user_input])

# 3. Predict intent using trained model
predicted_intent = model.predict(input_vector)
confidence = model.predict_proba(input_vector)

# 4. Execute appropriate action based on predicted intent
if predicted_intent == "get_time":
    time = get_current_time()
    return time
elif predicted_intent == "get_weather":
    weather = get_weather()
    return weather
elif predicted_intent == "greeting":
    return "Hello! How can I help you?"
else:
    return "I'm not sure what you mean"

"""
Strengths:
- Handles variations and typos
- Generalizes to unseen phrasings
- Learns from data
- Scales better with complexity
- Can improve with more training data

Weaknesses:
- Requires training data
- Less predictable (probabilistic)
- More complex to implement
- Requires computational resources for training
- Can make unexpected mistakes
"""

# =============================================================================
# COMPARISON SUMMARY
# =============================================================================
"""
KEY DIFFERENCES:

1. FLEXIBILITY:
   - Rule-based: Rigid, only handles explicitly coded patterns
   - AI-based: Flexible, generalizes to new variations

2. DEVELOPMENT:
   - Rule-based: Quick to start, manual rule creation
   - AI-based: Requires training data collection and model training

3. MAINTENANCE:
   - Rule-based: Must manually add new rules for each variation
   - AI-based: Can retrain with new data to improve

4. PERFORMANCE:
   - Rule-based: Fast execution, deterministic
   - AI-based: Slightly slower, probabilistic

5. SCALABILITY:
   - Rule-based: Becomes unmanageable with many intents
   - AI-based: Scales better to complex conversations

6. TRANSPARENCY:
   - Rule-based: Easy to understand why a decision was made
   - AI-based: "Black box" - harder to explain predictions

EXAMPLE WITH "WHAT TIME IS IT?":

Rule-Based Response:
- Input: "what time is it" → Matched rule → Return time
- Input: "time pls" → No match → "I don't understand"

AI-Based Response:
- Input: "what time is it" → Predicted "get_time" (95% confidence) → Return time
- Input: "time pls" → Predicted "get_time" (78% confidence) → Return time

WHEN TO USE EACH:

Use Rule-Based When:
- Simple, well-defined tasks
- Predictability is critical
- Limited budget/resources
- Few intents to handle

Use AI-Based When:
- Complex natural language understanding needed
- Many variations in user input
- Scalability is important
- Training data is available
"""