import re
import os
from dotenv import load_dotenv
import long_responses as long
from weather import get_current_weather, get_forecast

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

if not API_KEY:
    raise ValueError("Please set OPENWEATHER_API_KEY in your .env file")

# Simple conversation memory
last_city = None


def extract_city_name(message: str) -> str | None:
    """Extract city name from natural language."""
    message = message.lower().strip()

    patterns = [
        r"(?:weather|temperature|forecast|climate)\s+(?:in|for|at)\s+([a-zA-Z\s\-']+?)(?:\s|$|\?|\.|!|,)",
        r"(?:in|for|at)\s+([a-zA-Z\s\-']+?)\s+(?:weather|temperature|forecast)",
        r"what(?:'s| is) the weather (?:like )?in ([a-zA-Z\s\-']+)",
        r"how(?:'s| is) the weather in ([a-zA-Z\s\-']+)",
        r"temperature in ([a-zA-Z\s\-']+)",
        r"forecast (?:for|in) ([a-zA-Z\s\-']+)",
        r"weather (?:in|for) ([a-zA-Z\s\-']+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, message)
        if match:
            city = match.group(1).strip()
            # Clean common trailing words
            city = re.sub(r"\b(please|today|now|right now|tomorrow|this week)\b", "", city, flags=re.I)
            city = city.strip(" .,!?")
            if len(city) > 1:
                return city.title()

    return None


def message_probability(user_message: list[str], recognised_words: list[str],
                        single_response: bool = False, required_words: list[str] = None) -> int:
    if required_words is None:
        required_words = []

    message_certainty = 0
    has_required_words = True

    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    percentage = float(message_certainty) / float(len(recognised_words)) if recognised_words else 0

    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    if has_required_words or single_response:
        return int(percentage * 100)
    return 0


def check_all_messages(message: list[str], original_input: str) -> str:
    global last_city
    highest_prob_list = {}

    def response(bot_response: str, list_of_words: list[str],
                 single_response: bool = False, required_words: list[str] = None):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(
            message, list_of_words, single_response, required_words or []
        )

    # Basic responses
    response("Hello! How can I help you today?", ["hello", "hi", "hey", "sup", "heyo", "hola"], single_response=True)
    response("See you later!", ["bye", "goodbye", "see", "you", "later"], single_response=True)
    response("I'm doing great, thanks for asking! How about you?", ["how", "are", "you", "doing"], required_words=["how"])
    response("You're welcome!", ["thank", "thanks", "thx"], single_response=True)
    response("My name is Clima. Nice to meet you!", ["what", "is", "your", "name", "who", "are", "you"], required_words=["name"])
    
    # Help
    response(
        "I can help you with:\n"
        "• Current weather → 'weather in Paris'\n"
        "• 5-day forecast → 'forecast for Tokyo'\n"
        "• Just say 'help' anytime!",
        ["help", "what", "can", "you", "do"], single_response=True
    )

    # Longer responses
    response(long.R_ADVICE, ["give", "advice"], required_words=["advice"])
    response(long.R_EATING, ["what", "you", "eat"], required_words=["you", "eat"])

    # Weather related
    city_name = extract_city_name(original_input)

    # Remember last city if user says "forecast" or "weather" without city
    if not city_name and last_city:
        if any(w in message for w in ["forecast", "weather", "temperature"]):
            city_name = last_city

    if city_name:
        last_city = city_name  # update memory

        # Decide between current weather or forecast
        if any(w in message for w in ["forecast", "week", "days", "tomorrow"]):
            weather_info = get_forecast(city_name, API_KEY)
        else:
            weather_info = get_current_weather(city_name, API_KEY)

        response(weather_info, ["weather", "temperature", "forecast", "climate"], single_response=True)

    # Fallback
    best_match = max(highest_prob_list, key=highest_prob_list.get)
    return long.unknown() if highest_prob_list[best_match] < 1 else best_match


def get_response(user_input: str) -> str:
    split_message = re.split(r"\s+|[,;?!.-]\s*", user_input.lower())
    split_message = [word for word in split_message if word]  # remove empty strings
    return check_all_messages(split_message, user_input)


# ====================== MAIN LOOP ======================
if __name__ == "__main__":
    print("Clima is online! Type 'quit' or 'exit' to stop.\n")
    

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["quit", "exit", "bye"]:
            print("Clima: Goodbye! 👋")
            break
        if not user_input:
            continue
        print("Clima:", get_response(user_input))
        print()