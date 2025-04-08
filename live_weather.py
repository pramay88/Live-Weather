import requests
import streamlit as st
from streamlit_autorefresh import st_autorefresh

try:
    API_KEY = st.secrets["api"]["weather_key"]
except:
    API_KEY = "f29a0a07a8c939e1176d3589f168386d"

def fetch_weather(city="London"):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        return {
            "city": data['name'],
            "temperature": data['main']['temp'],
            "metric": "°C",
            "humidity": data['main']['humidity'],
            "condition": data['weather'][0]['description'].title()
        }
    else:
        return {"message": f"Failed to retrieve data: {res.status_code}"}

def main():
    st.set_page_config(page_title="Live Weather", page_icon="⛅")
    st.title("🌦️ Live Weather")

    if 'submitted' not in st.session_state:
        st.session_state.submitted = False
    if 'city' not in st.session_state:
        st.session_state.city = "London"

    city = st.text_input("Enter a city name:", st.session_state.city)

    if st.button("✅ Check Weather"):
        st.session_state.submitted = True
        st.session_state.city = city  # store the city

    if st.session_state.submitted:
        # Refresh every 60 seconds (60000 ms)
        st_autorefresh(interval=60000, key="auto_refresh")

        data = fetch_weather(st.session_state.city)
        if "message" in data:
            st.error(data["message"])
        else:
            st.divider()
            st.header(f"🌍 Weather in {data['city']}")
            col1, col2 = st.columns(2)
            col1.metric(label="🌡️ Temperature", value=f"{data['temperature']}°C")
            col2.metric(label="💧 Humidity", value=f"{data['humidity']}%")
            st.subheader(f"☁️ Condition: {data['condition']}")
            st.caption("⏱️ Auto-refresh every 60 seconds")

if __name__ == "__main__":
    main()
