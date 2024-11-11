from FakeLogger import *  # Assuming FakeLogger is a valid module you have access to
import datetime
import random

# Generate random IPs for logs
def generate_random_ip():
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 255)}"

# Generate random user names
def generate_random_user():
    return random.choice(['bob', 'guest', 'alice', 'admin', 'user123'])

# Generate random requests and responses
requests_responses = [
    ("GET /login", "200 OK"),
    ("PUT /login", "404 Not Found"),
    ("GET /home", "200 OK"),
    ("POST /api/data", "500 Internal Server Error"),
    ("DELETE /account", "403 Forbidden"),
    ("GET /profile", "200 OK"),
    ("GET /settings", "401 Unauthorized"),
    ("POST /register", "201 Created"),
    ("PUT /settings", "204 No Content"),
    ("PATCH /api/data", "202 Accepted"),
    ("DELETE /user/12345", "404 Not Found"),
    ("GET /dashboard", "503 Service Unavailable"),
    ("HEAD /status", "200 OK"),
    ("OPTIONS /api", "204 No Content"),
    ("CONNECT /proxy", "502 Bad Gateway"),
    ("TRACE /api/debug", "403 Forbidden"),
    ("POST /upload", "413 Payload Too Large"),
    ("GET /checkout", "302 Found"),
    ("DELETE /session", "200 OK"),
    ("POST /logout", "204 No Content"),
    ("PUT /update-info", "200 OK"),
    ("GET /archive", "410 Gone"),
    ("PATCH /item/modify", "200 OK"),
    ("DELETE /profile", "405 Method Not Allowed"),
    ("PUT /order/confirm", "409 Conflict"),
    ("POST /auth/reset-password", "200 OK"),
]

user_agents = [
    "curl/7.68.0",
    "Python-urllib/3.8",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "PostmanRuntime/7.29.0",
    "Java/1.8.0_181",
    "Go-http-client/1.1",
    "Wget/1.20.3 (linux-gnu)",
    "libwww-perl/6.36",
    "axios/0.21.1",
    "node-fetch/2.6.1",
    "okhttp/4.9.0",
    "Dalvik/2.1.0 (Linux; U; Android 9; Mi 9 Build/PQ3A.190801.002)"
]

# Create some pages
google = Page('/search', domain='www.google.com', quitProb=0.0)
startPage = Page('/start')
account = Page('/account/:userId')
buy = Page('/account/:userId/buy')
sell = Page('/account/:userId/sell')
survey = Page('/survey')
anotherWebsite = None

# Create links between pages
google.addNextPage(startPage)
startPage.addNextPage(account, timeBeforePageChange=30.0)
account.addNextPage(buy, method='POST')
account.addNextPage(sell, method='POST')
buy.addNextPage(survey, likelyhoodWeight=0.1)
buy.addNextPage(account)
buy.addNextPage(anotherWebsite)
sell.addNextPage(survey, likelyhoodWeight=0.3)
sell.addNextPage(account)
sell.addNextPage(anotherWebsite)
survey.addNextPage(account)

# This creates normally distributed start times around lunch
def randomStartTime():
    now = datetime.datetime.now()
    HOURS = 60 * 60
    random_offset = datetime.timedelta(0, random.gauss(12 * HOURS, 2 * HOURS))
    return datetime.datetime(now.year, now.month, now.day) + random_offset

all_history = []
for customer in (Customer() for _ in range(1000)):
    customer.start(google, time=randomStartTime())  # Set a starting point for the journey
    customer.createHistory()  # This creates the history as (timestamp, Transition) tuples
    all_history += list(customer.formatHistory())  # formatHistory turns the transitions into log lines

first = lambda t: t[0]  # Selects the timestamp from history
second = lambda t: t[1]  # Selects the log line from history

sorted_history = sorted(all_history, key=first)  # Get customer history in order

# Create formatted log entries
for entry in sorted_history:
    timestamp = entry[0].strftime("%Y-%m-%d %H:%M:%S")
    ip_address = generate_random_ip()
    user = generate_random_user()
    request, response = random.choice(requests_responses)
    user_agent = random.choice(user_agents)
    print(f"{timestamp} {ip_address} - {user} [{request}] \"{response}\" \"{user_agent}\"")
