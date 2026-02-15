from flask import Flask, render_template, request, jsonify
from business_logic import get_weather, confirm_appointment

app = Flask(__name__)


@app.route('/')
def index():
    """
    Render the main page with the form.
    """
    return render_template('index.html')


@app.route('/weather', methods=['POST'])
def weather():
    """
    Handle weather requests via AJAX.
    Expects JSON: {"city": "Berlin"}
    Returns JSON: {"response": "Weather message"}
    """
    data = request.get_json()
    city = data.get('city', '')
    
    # Call business logic
    response = get_weather(city)
    
    # Return JSON response
    return jsonify({'response': response})


@app.route('/appointment', methods=['POST'])
def appointment():
    """
    Handle appointment requests via AJAX.
    Expects JSON: {"date": "2024-03-15", "time": "14:00"}
    Returns JSON: {"response": "Confirmation message"}
    """
    data = request.get_json()
    date = data.get('date', '')
    time = data.get('time', '')
    
    # Call business logic
    response = confirm_appointment(date, time)
    
    # Return JSON response
    return jsonify({'response': response})


if __name__ == '__main__':
    print("🌐 Starting Flask Web App...")
    print("✅ Open browser: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)