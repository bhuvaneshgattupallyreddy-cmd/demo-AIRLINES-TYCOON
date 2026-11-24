"""Airline Tycoon Simulator

Buy aircraft, create routes, fly them, and grow your airline.
Plain Python, no libraries to install.
"""

import math
import random

# ---------------------------------------------------------------- game data

# code: (city, latitude, longitude)
AIRPORTS = {
    "HYD": ("Hyderabad", 17.2403, 78.4294),
    "DXB": ("Dubai", 25.2532, 55.3657),
    "LHR": ("London Heathrow", 51.4700, -0.4543),
    "SIN": ("Singapore Changi", 1.3644, 103.9915),
    "FRA": ("Frankfurt", 50.0379, 8.5622),
}
AIRPORT_CODES = list(AIRPORTS)

AIRCRAFT_SHOP = {
    "1": {
        "name": "Used Turboprop",
        "price": 100_000,
        "seats": 50,
        "fuel_per_km": 1.2,
        "range_km": 2_500,
        "fare_multiplier": 1,
    },
    "2": {
        "name": "Used Regional Jet",
        "price": 500_000,
        "seats": 90,
        "fuel_per_km": 2.8,
        "range_km": 4_000,
        "fare_multiplier": 1,
    },
    "3": {
        "name": "Used Narrow-body Jet",
        "price": 1_000_000,
        "seats": 180,
        "fuel_per_km": 4.8,
        "range_km": 8_500,
        "fare_multiplier": 1,
    },
    "4": {
        "name": "New Private Jet",
        "price": 5_000_000,
        "seats": 12,
        "fuel_per_km": 2.0,
        "range_km": 12_000,
        "fare_multiplier": 6,  # private jet tickets are very expensive
    },
}

STARTING_MONEY = 10_000_000
CREW_COST = 3_000
AIRPORT_FEES = 2_000


# ---------------------------------------------------------------- helpers

def airport_label(code):
    """'HYD' -> 'Hyderabad (HYD)'"""
    return f"{AIRPORTS[code][0]} ({code})"


def distance_km(code_a, code_b):
    """Great-circle distance between two airports (haversine formula)."""
    _, lat1, lon1 = AIRPORTS[code_a]
    _, lat2, lon2 = AIRPORTS[code_b]
    lat1, lon1, lat2, lon2 = map(math.radians, (lat1, lon1, lat2, lon2))
    a = (
        math.sin((lat2 - lat1) / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    )
    return round(6371 * 2 * math.asin(math.sqrt(a)))


def base_fare(distance):
    """Ticket price for an economy seat. Longer flights cost more."""
    return round(60 + 0.10 * distance)


def ask_int(prompt, low, high):
    """Keep asking until the player types a whole number from low to high."""
    while True:
        text = input(prompt).strip()
        try:
            number = int(text)
        except ValueError:
            print("Please enter a number.")
            continue
        if low <= number <= high:
            return number
        print(f"Please enter a number from {low} to {high}.")


def header(title):
    print(f"\n========== {title} ==========")


# ---------------------------------------------------------------- the airline

class Airline:
    def __init__(self, owner, name):
        self.owner = owner
        self.name = name
        self.money = STARTING_MONEY
        self.fleet = []      # list of aircraft dicts
        self.routes = []     # list of (departure_code, destination_code)
        self.day = 1
        self.flights_flown = 0
        self.total_profit = 0

    # ---- finances -------------------------------------------------------

    def view_finances(self):
        header("AIRLINE FINANCES")
        print(f"Airline: {self.name}")
        print(f"Owner: {self.owner}")
        print(f"Day: {self.day}")
        print(f"Current balance: ${self.money:,}")
        print(f"Aircraft owned: {len(self.fleet)}")
        print(f"Routes created: {len(self.routes)}")
        print(f"Flights flown: {self.flights_flown}")
        print(f"Profit from flights so far: ${self.total_profit:,}")

    # ---- aircraft -------------------------------------------------------

    def manage_aircraft(self):
        while True:
            header("AIRCRAFT MANAGEMENT")
            print("1. Buy an aircraft")
            print("2. View your fleet")
            print("3. Return to main menu")
            choice = input("Choose an option (1-3): ").strip()

            if choice == "1":
                self.buy_aircraft()
            elif choice == "2":
                self.view_fleet()
            elif choice == "3":
                return
            else:
                print("Invalid option. Choose 1, 2, or 3.")

    def buy_aircraft(self):
        header("AIRCRAFT SHOP")
        for number, plane in AIRCRAFT_SHOP.items():
            print(
                f"{number}. {plane['name']} - ${plane['price']:,} "
                f"({plane['seats']} seats, range {plane['range_km']:,} km)"
            )
        print("5. Cancel")

        choice = input("Select an aircraft to purchase (1-5): ").strip()
        if choice == "5":
            return
        if choice not in AIRCRAFT_SHOP:
            print("Invalid choice.")
            return

        plane = AIRCRAFT_SHOP[choice]
        if self.money < plane["price"]:
            print("You do not have enough money.")
            return

        self.money -= plane["price"]
        # copy the shop entry so each aircraft is its own object
        aircraft = dict(plane)
        aircraft["id"] = f"AC-{len(self.fleet) + 1:03d}"
        aircraft["flights"] = 0
        self.fleet.append(aircraft)
        print(f"You purchased a {plane['name']} ({aircraft['id']}) for ${plane['price']:,}!")
        print(f"Remaining balance: ${self.money:,}")

    def view_fleet(self):
        header("YOUR FLEET")
        if not self.fleet:
            print("You have no aircraft yet.")
            return
        for i, plane in enumerate(self.fleet, start=1):
            print(
                f"{i}. {plane['name']} [{plane['id']}] - {plane['seats']} seats, "
                f"range {plane['range_km']:,} km, flights flown: {plane['flights']}"
            )
        print(f"Total aircraft: {len(self.fleet)}")

    # ---- routes ---------------------------------------------------------

    def manage_routes(self):
        while True:
            header("ROUTE MANAGEMENT")
            print("1. Create a new route")
            print("2. View all routes")
            print("3. Return to main menu")
            choice = input("Choose an option (1-3): ").strip()

            if choice == "1":
                self.create_route()
            elif choice == "2":
                self.view_routes()
            elif choice == "3":
                print("Returning to main menu...")
                return
            else:
                print("Invalid option! Choose 1, 2, or 3.")

    def create_route(self):
        header("AVAILABLE AIRPORTS")
        for i, code in enumerate(AIRPORT_CODES, start=1):
            print(f"{i}. {airport_label(code)}")

        count = len(AIRPORT_CODES)
        departure = ask_int("Departure airport number: ", 1, count)
        destination = ask_int("Destination airport number: ", 1, count)

        if departure == destination:
            print("Departure and destination cannot be the same!")
            return

        route = (AIRPORT_CODES[departure - 1], AIRPORT_CODES[destination - 1])
        if route in self.routes:
            print("That route already exists!")
            return

        self.routes.append(route)
        km = distance_km(*route)
        print(f"Route created: {airport_label(route[0])} -> {airport_label(route[1])} ({km:,} km)")
        print(f"Total routes: {len(self.routes)}")

    def view_routes(self):
        header("YOUR FLIGHT ROUTES")
        if not self.routes:
            print("You haven't created any routes yet.")
            return
        for i, (dep, dest) in enumerate(self.routes, start=1):
            print(f"{i}. {airport_label(dep)} -> {airport_label(dest)} ({distance_km(dep, dest):,} km)")

    # ---- flying ---------------------------------------------------------

    def operate_flight(self):
        if not self.routes:
            print("\nYou need to create a route first!")
            return
        if not self.fleet:
            print("\nYou need to buy an aircraft first!")
            return

        # 1) pick a route
        header("FLIGHT OPERATIONS")
        for i, (dep, dest) in enumerate(self.routes, start=1):
            print(f"{i}. {airport_label(dep)} -> {airport_label(dest)} ({distance_km(dep, dest):,} km)")
        print("0. Return to main menu")

        choice = ask_int("Select a route to operate: ", 0, len(self.routes))
        if choice == 0:
            return
        dep, dest = self.routes[choice - 1]
        distance = distance_km(dep, dest)

        # 2) pick an aircraft that can actually fly that far
        capable = [plane for plane in self.fleet if plane["range_km"] >= distance]
        if not capable:
            print(f"\nNone of your aircraft can fly {distance:,} km. Buy one with more range!")
            return

        print("\nAircraft that can fly this route:")
        for i, plane in enumerate(capable, start=1):
            print(f"{i}. {plane['name']} [{plane['id']}] - {plane['seats']} seats")
        print("0. Cancel")

        pick = ask_int("Select an aircraft: ", 0, len(capable))
        if pick == 0:
            return
        plane = capable[pick - 1]

        # 3) fly!
        print("\nFlight ready for departure!")
        print(f"Departure: {airport_label(dep)}")
        print(f"Destination: {airport_label(dest)}")
        print(f"Aircraft: {plane['name']} [{plane['id']}]")

        passengers = round(plane["seats"] * random.uniform(0.55, 1.0))
        ticket_price = base_fare(distance) * plane["fare_multiplier"]
        revenue = passengers * ticket_price

        fuel_cost = round(plane["fuel_per_km"] * distance)
        total_costs = fuel_cost + CREW_COST + AIRPORT_FEES
        profit = revenue - total_costs

        self.money += profit
        self.total_profit += profit
        self.flights_flown += 1
        plane["flights"] += 1
        self.day += 1

        header("FLIGHT REPORT")
        print(f"Passengers: {passengers} / {plane['seats']}")
        print(f"Ticket price: ${ticket_price:,}")
        print(f"Flight revenue: ${revenue:,}")
        print(f"Fuel: ${fuel_cost:,}  Crew: ${CREW_COST:,}  Airport fees: ${AIRPORT_FEES:,}")
        print(f"Total costs: ${total_costs:,}")
        print(f"Profit/Loss: ${profit:,}")
        print(f"Updated airline balance: ${self.money:,}")

    # ---- end of game ----------------------------------------------------

    def print_summary(self):
        header("FINAL AIRLINE SUMMARY")
        print(f"Airline: {self.name}")
        print(f"Days played: {self.day}")
        print(f"Aircraft owned: {len(self.fleet)}")
        print(f"Routes created: {len(self.routes)}")
        print(f"Flights flown: {self.flights_flown}")
        print(f"Final balance: ${self.money:,}")
        print("Thanks for playing Airline Tycoon Simulator!")

    def main_menu(self):
        while True:
            print("\n" + "=" * 42)
            print(f"{self.name.upper():^42}")
            print(f"{'AIRLINE MANAGER':^42}")
            print("=" * 42)
            print(f"  Day: {self.day}")
            print(f"  Balance: ${self.money:,}")
            print(f"  Aircraft: {len(self.fleet)}")
            print(f"  Routes: {len(self.routes)}")
            print("=" * 42)
            print("1. Airline Finances")
            print("2. Manage Aircraft")
            print("3. Manage Routes")
            print("4. Operate Flight")
            print("5. Exit Game")
            print("=" * 42)

            choice = input("Choose an option (1-5): ").strip()

            if choice == "1":
                self.view_finances()
            elif choice == "2":
                self.manage_aircraft()
            elif choice == "3":
                self.manage_routes()
            elif choice == "4":
                self.operate_flight()
                if self.money < 0:
                    print("\nYour airline has gone bankrupt!")
                    break
            elif choice == "5":
                break
            else:
                print("Invalid option! Choose a number from 1 to 5.")

        self.print_summary()


# ---------------------------------------------------------------- start

def main():
    print("WELCOME TO YOUR AIRLINE TYCOON SIMULATOR")
    owner = input("Please enter your name: ").strip() or "Pilot"
    name = input("Please enter your airline's name: ").strip() or "My Airline"

    print(f"\nWelcome, {owner}!")
    print(f"Your airline, {name}, starts with ${STARTING_MONEY:,}.")

    Airline(owner, name).main_menu()


if __name__ == "__main__":
    main()
