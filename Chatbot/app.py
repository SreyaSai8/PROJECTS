from flask import Flask, render_template, request, jsonify
import serial
import pyttsx3
import threading

app = Flask(__name__)

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty("rate", 170)

def speak(text):
    """Convert text to speech asynchronously"""
    threading.Thread(target=_speak, args=(text,)).start()

def _speak(text):
    engine.say(text)
    engine.runAndWait()

def get_iot_data():
    """Simulate IoT data fetching"""
    try:
        ser = serial.Serial('COM3', 9600, timeout=1)
        ser.flush()
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            return f"IoT Device Data: {data}"
    except Exception:
        return "IoT Device not connected."

def get_health_advice(temp, heart_rate, symptoms):
    """Provide health advice"""
    advice = []
    try:
        temp = float(temp)
        heart_rate = int(heart_rate)
    except ValueError:
        return "Invalid input. Please enter valid numbers."

    if temp > 101:
        advice.append("You have a high fever. Take Paracetamol and drink plenty of fluids.")
    elif 99 <= temp <= 101:
        advice.append("You have a mild fever. Rest well and stay hydrated.")
    else:
        advice.append("Your temperature is normal.")

    if heart_rate > 100:
        advice.append("Your heart rate is high. Avoid stress and drink enough water.")
    elif heart_rate < 60:
        advice.append("Your heart rate is low. If you feel dizzy, consult a doctor.")
    else:
        advice.append("Your heart rate is normal.")

    symptoms_list = {
        "cough": "For cough, take honey and warm water. Use cough syrup if needed.",
        "cold": "For cold, take steam inhalation and Vitamin C.",
        "headache": "For headache, rest and drink enough water.",
        "fever": "For fever, stay hydrated and take Paracetamol if needed.",
        "sore throat": "For sore throat, gargle with warm salt water and drink herbal tea.",
        "fatigue": "For fatigue, get enough sleep, eat a balanced diet, and stay hydrated.",
        "dizziness": "For dizziness, sit down immediately and drink water. If it persists, see a doctor.",
        "nausea": "For nausea, try ginger tea or a light meal. Avoid oily foods.",
        "vomiting": "For vomiting, drink small sips of water frequently and rest.",
        "stomach pain": "For stomach pain, try a warm compress and avoid spicy foods.",
        "diarrhea": "For diarrhea, drink oral rehydration solutions and avoid dairy products.",
        "constipation": "For constipation, eat fiber-rich foods and drink more water.",
        "chest pain": "For chest pain, rest immediately. If severe, seek medical help.",
        "shortness of breath": "For shortness of breath, sit upright and practice deep breathing. Seek medical help if severe.",
        "joint pain": "For joint pain, apply a warm compress and take rest.",
        "back pain": "For back pain, stretch gently and avoid heavy lifting.",
        "skin rash": "For skin rash, apply aloe vera gel and avoid scratching.",
        "eye irritation": "For eye irritation, wash eyes with clean water and avoid screen time.",
        "ear pain": "For ear pain, apply a warm compress and avoid inserting objects inside the ear.",
        "toothache": "For toothache, rinse with warm salt water and avoid very hot or cold foods.",
        "sneezing": "For sneezing, stay hydrated and avoid allergens.",
        "runny nose": "For runny nose, take steam inhalation and drink warm fluids.",
        "bloody nose": "For a bloody nose, pinch your nose and lean forward. Avoid blowing your nose hard.",
        "high blood pressure": "For high blood pressure, reduce salt intake and manage stress.",
        "low blood pressure": "For low blood pressure, drink more fluids and avoid sudden position changes.",
        "burning sensation": "For burning sensation, apply cold compress and avoid spicy foods.",
        "leg swelling": "For leg swelling, elevate your legs and avoid prolonged sitting or standing.",
        "muscle cramps": "For muscle cramps, stretch the affected muscle and stay hydrated.",
        "tingling sensation": "For tingling, change posture and massage the area gently.",
        "blurry vision": "For blurry vision, rest your eyes and avoid excessive screen time.",
        "difficulty swallowing": "For difficulty swallowing, eat soft foods and drink warm liquids.",
        "hiccups": "For hiccups, drink water slowly and try holding your breath for a few seconds.",
        "acne": "For acne, wash your face twice a day and avoid touching your face.",
        "dry skin": "For dry skin, apply moisturizer and drink plenty of water.",
        "itchy skin": "For itchy skin, use a mild lotion and avoid hot showers.",
        "cold hands and feet": "For cold hands and feet, wear warm clothing and keep moving.",
        "night sweats": "For night sweats, use breathable bedding and stay cool.",
        "palpitations": "For palpitations, reduce caffeine and practice deep breathing.",
        "frequent urination": "For frequent urination, avoid caffeine and drink water in moderation.",
        "burning urination": "For burning urination, drink cranberry juice and plenty of water.",
        "blood in urine": "For blood in urine, seek immediate medical attention.",
        "loss of appetite": "For loss of appetite, eat small, frequent meals and avoid stress.",
        "weight loss": "For unexplained weight loss, eat nutritious foods and consult a doctor.",
        "weight gain": "For unexplained weight gain, monitor your diet and stay active.",
        "memory loss": "For memory loss, engage in brain exercises and maintain a healthy diet.",
        "speech difficulty": "For speech difficulty, practice speaking slowly and seek medical advice.",
        "difficulty sleeping": "For difficulty sleeping, avoid caffeine at night and establish a bedtime routine.",
        "restless legs": "For restless legs, try stretching and massage before bedtime.",
        "fainting": "For fainting, lie down and elevate your legs. Seek medical attention if it happens frequently."
    }

    for symptom, advice_text in symptoms_list.items():
        if symptom in symptoms:
            advice.append(advice_text)

    return " ".join(advice)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    """Handles chatbot input and provides a response"""
    try:
        data = request.json
        temp = data.get("temperature")
        heart_rate = data.get("heart_rate")
        symptoms = data.get("symptoms", "").lower()

        if not temp or not heart_rate:
            return jsonify({"response": "Please enter temperature and heart rate."})

        advice = get_health_advice(temp, heart_rate, symptoms)
        iot_info = get_iot_data()
        response = f"{advice} {iot_info}"

        speak(response)  # Speak the response
        return jsonify({"response": response})
    
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
