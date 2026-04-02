import httpx

from app.config import settings

API_KEY = settings.API_KEY_WEATHER

async def get_weathers(lat, lon):
    url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={lat},{lon}&lang=ru"

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url)
            if resp.status_code != 200:
                return f"❌ Ошибка API: {resp.status_code}"

            data = resp.json()
            current = data["current"]
            location = data["location"]

            return (
                f"🌍 Location: {location['name']}, {location['country']}\n"
                f"🌡 Temperature: {current['temp_c']}°C\n"
                f"💨 Wind: {current['wind_kph']} km/h\n"
                f"💧 Humidity: {current['humidity']}%\n"
                f"🌤 Condition: {current['condition']['text']}"
            )
        except Exception as e:
            return f"❌ Ошибка при запросе погоды: {str(e)}"