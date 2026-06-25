import cohere
import requests
import datetime
import os

# ✅ GitHub Secret se key lo
API_KEY = os.environ.get("COHERE_API_KEY")
co      = cohere.ClientV2(API_KEY)

def ai_call(prompt):
    try:
        response = co.chat(
            model="command-r-plus-08-2024",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.message.content[0].text
    except Exception as e:
        return f"Error: {e}"

def get_weather(city="Delhi"):
    try:
        r    = requests.get(
            f"https://wttr.in/{city}?format=j1",
            timeout=10
        )
        data = r.json()
        temp = data["current_condition"][0]["temp_C"]
        desc = data["current_condition"][0]["weatherDesc"][0]["value"]
        return f"{city}: {temp}°C — {desc}"
    except:
        return "Weather nahi mila"

def daily_agent():
    now     = datetime.datetime.now()
    weather = get_weather("Delhi")
    
    result = ai_call(f"""
    Aaj {now.strftime('%A, %d %B %Y')} hai.
    Weather: {weather}
    
    Manik ke liye daily briefing:
    1. Motivational quote
    2. Aaj ke 3 focus areas
    3. Weather update
    
    Hindi mein — energetic!
    """)
    
    # Result save karo
    with open("daily_report.txt", "w", encoding="utf-8") as f:
        f.write(f"Date: {now}\nWeather: {weather}\n\n{result}")
    
    print("✅ Daily Agent Complete!")
    print(result)

# ── Run karo! ──────────────────────────
daily_agent()
