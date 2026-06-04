import math
from datetime import datetime, timedelta

# --- Configuration ---
# Approximate locations for demonstration purposes (Latitude, Longitude)
CITY_LOCATIONS = {
    "Istanbul": (41.0082, 28.9784),
    "London": (51.5074, 0.1278),
    "New York": (40.7128, -74.0060),
    "Tokyo": (35.6895, 139.6917),
    "Ankara": (39.9334, 32.8597), # Closer to Istanbul
    "Paris": (48.8566, 2.3522)   # Closer to London
}

# Maximum plausible travel speed in km/h (e.g., commercial airplane speed)
MAX_TRAVEL_SPEED_KMH = 900

# --- Helper Functions ---
def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the distance between two points on Earth using the Haversine formula.
    Returns distance in kilometers.
    """
    R = 6371  # Radius of Earth in kilometers

    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance

# --- Main Logic ---
# In-memory storage for user login history
# Format: {"username": [{"timestamp": datetime_obj, "city_name": "CityName", "location": (lat, lon)}]}
user_login_history = {}

def process_login_attempt(username, city_name, timestamp_str):
    """
    Processes a login attempt, checks for impossible travel, and updates history.
    """
    print(f"\n--- Processing login for {username} from {city_name} at {timestamp_str} ---")

    if city_name not in CITY_LOCATIONS:
        print(f"Error: Unknown city '{city_name}'. Login rejected.")
        return

    current_location = CITY_LOCATIONS[city_name]
    current_timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")

    if username not in user_login_history:
        user_login_history[username] = []

    # Get the last successful login for this user
    last_logins = user_login_history[username]
    if last_logins:
        last_login = last_logins[-1] # Get the most recent login
        prev_timestamp = last_login["timestamp"]
        prev_location = last_login["location"]
        prev_city_name = last_login["city_name"]

        time_diff_seconds = (current_timestamp - prev_timestamp).total_seconds()
        time_diff_hours = time_diff_seconds / 3600

        # If time difference is zero or negative, it's a suspicious immediate re-login or out-of-order event
        if time_diff_hours <= 0:
            print(f"Warning: Login from {city_name} at {timestamp_str} is not after previous login from {prev_city_name} at {prev_timestamp}. Possible replay or out-of-order event. Login accepted for demo, but real systems might flag more severely.")
            # For this demo, we'll still add it, but a real system might reject or require additional verification.
        else:
            distance_km = haversine_distance(
                prev_location[0], prev_location[1],
                current_location[0], current_location[1]
            )

            # Calculate required speed to cover the distance in the given time
            required_speed_kmh = distance_km / time_diff_hours

            print(f"Previous login: {prev_city_name} at {prev_timestamp}")
            print(f"Distance: {distance_km:.2f} km")
            print(f"Time difference: {time_diff_hours:.2f} hours")
            print(f"Required speed: {required_speed_kmh:.2f} km/h")

            # --- Core Impossible Travel Detection Logic ---
            if required_speed_kmh > MAX_TRAVEL_SPEED_KMH:
                print(f"!!! IMPOSSIBLE TRAVEL DETECTED for {username}! Required speed ({required_speed_kmh:.2f} km/h) exceeds max plausible speed ({MAX_TRAVEL_SPEED_KMH} km/h).")
                # In a real system, this would trigger an alert, block login, require MFA, etc.
                # For this demo, we'll still record the login to show history.
            else:
                print(f"Login plausible. Required speed ({required_speed_kmh:.2f} km/h) is within limits.")
    else:
        print(f"First login for {username}. No previous history to compare.")

    # Record the current login
    user_login_history[username].append({
        "timestamp": current_timestamp,
        "city_name": city_name,
        "location": current_location
    })
    print("Login recorded.")


# --- Demonstration ---
if __name__ == "__main__":
    print("Simulating Impossible Travel Detection in Login Flows\n")

    # Scenario 1: Normal, plausible travel (Istanbul to Ankara in 4 hours)
    process_login_attempt("alice", "Istanbul", "2023-10-26 10:00:00")
    process_login_attempt("alice", "Ankara", "2023-10-26 14:00:00") # ~350km, ~87km/h - plausible

    # Scenario 2: Impossible travel (Istanbul to New York in 1 hour)
    process_login_attempt("bob", "Istanbul", "2023-10-26 09:00:00")
    process_login_attempt("bob", "New York", "2023-10-26 10:00:00") # ~8000km, ~8000km/h - IMPOSSIBLE

    # Scenario 3: Plausible international travel (London to Paris in 4 hours)
    process_login_attempt("charlie", "London", "2023-10-26 12:00:00")
    process_login_attempt("charlie", "Paris", "2023-10-26 16:00:00") # ~340km, ~85km/h - plausible (train/car)

    # Scenario 4: Another impossible travel (Tokyo to London in 2 hours)
    process_login_attempt("david", "Tokyo", "2023-10-26 08:00:00")
    process_login_attempt("david", "London", "2023-10-26 10:00:00") # ~9700km, ~4850km/h - IMPOSSIBLE

    # Scenario 5: User logs in from same city multiple times
    process_login_attempt("alice", "Ankara", "2023-10-26 15:00:00") # Same city, 1 hour later - plausible (no travel needed)

    print("\n--- End of Simulation ---")
