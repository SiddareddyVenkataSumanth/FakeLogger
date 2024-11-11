import datetime
import random
import requests  # Make sure to install this using `pip install requests` if not already installed

# Simulate generating random IPs and users
def generate_random_ip():
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 255)}"

def generate_random_user():
    return random.choice(['bob', 'guest', 'alice', 'admin', 'user123'])

# Define request-response pairs (you can modify these URLs as needed)
requests_responses = [
    ("PUT /login", "https://httpbin.org/status/404"),
    ("GET /home", "https://httpbin.org/status/200"),
    ("POST /api/data", "https://httpbin.org/status/500"),
    ("DELETE /account", "https://httpbin.org/status/403"),
    ("GET /profile", "https://httpbin.org/status/200")
]

user_agents = ["curl/7.68.0", "Python-urllib/3.8", "Mozilla/5.0", "PostmanRuntime/7.29.0"]

def get_live_response(url):
    try:
        response = requests.get(url)  # Send a request (adjust method if needed)
        status_code = response.status_code
        # Classify the response type
        if status_code == 200:
            return "good"
        elif status_code >= 400 and status_code < 500:
            return "bad"
        elif status_code >= 500:
            return "threat"
        else:
            return "unknown"
    except requests.RequestException:
        return "error"

# Generate formatted log entries with live response classification
def generate_logs():
    for _ in range(10):  # Adjust the range as needed
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ip_address = generate_random_ip()
        user = generate_random_user()
        request, url = random.choice(requests_responses)
        user_agent = random.choice(user_agents)
        response_type = get_live_response(url)
        print(f"{timestamp} {ip_address} - {user} [{request}] \"{response_type}\" \"{user_agent}\"")

# Run the log generation
generate_logs()
