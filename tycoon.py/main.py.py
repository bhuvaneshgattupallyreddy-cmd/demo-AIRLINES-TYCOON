import random


AIRPORTS = [
    "Hyderabad (HYD)",
    "Dubai (DXB)",
    "London Heathrow (LHR)",
    "Singapore Changi (SIN)",
    "Frankfurt (FRA)",
]

AIRCRAFT_SHOP = {
    "1": ("Used turboprop", 100_000),
    "2": ("Used regional jet", 500_000),
    "3": ("Used narrow-body jet", 1_000_000),
    "4": ("New private jet", 5_000_000),
}

ROUTES = []
FLEET = []
MONEY = 10_000_000




print("=========================================")
print("WELCOME TO YOUR AIRLINE TYCOON SIMULATOR")
print("=========================================")

PLAYER_NAME = input("Please enter your name: ").strip() or "Pilot"
BUSINESS_NAME = input("Please enter your airline's name: ").strip() or "My Airline"

print(f"\nWelcome, {PLAYER_NAME}!")
print(f"Your airline, {BUSINESS_NAME}, starts with ${MONEY:,}.")




def manage_aircraft():
    global MONEY

    while True:
        print("\n========== AIRCRAFT MANAGEMENT ==========")
        print("1. Buy an aircraft")
        print("2. View your fleet")
        print("3. Return to main menu")

        choice = input("Choose an option (1-3): ").strip()

        if choice == "1":
            print("\n========== AIRCRAFT SHOP ==========")
            for number, (aircraft, price) in AIRCRAFT_SHOP.items():
                print(f"{number}. {aircraft} - ${price:,}")
            print("5. Cancel")

            purchase = input("Select an aircraft to purchase (1-5): ").strip()

            if purchase == "5":
                continue
            if purchase not in AIRCRAFT_SHOP:
                print("Invalid choice.")
                continue

            aircraft, price = AIRCRAFT_SHOP[purchase]
            if MONEY < price:
                print("You do not have enough money.")
            else:
                MONEY -= price
                FLEET.append(aircraft)
                print(f"You purchased a {aircraft} for ${price:,}!")
                print(f"Remaining balance: ${MONEY:,}")

        elif choice == "2":
            print("\n========== YOUR FLEET ==========")
            if not FLEET:
                print("You have no aircraft yet.")
            else:
                for i, aircraft in enumerate(FLEET, start=1):
                    print(f"{i}. {aircraft}")
                print(f"Total aircraft: {len(FLEET)}")

        elif choice == "3":
            return
        else:
            print("Invalid option. Choose 1, 2, or 3.")



def manage_routes():
    while True:
        print("\n========== ROUTE MANAGEMENT ==========")
        print("1. Create a new route")
        print("2. View all routes")
        print("3. Return to main menu")

        choice = input("Choose an option (1-3): ").strip()

        if choice == "1":
            print("\n========== AVAILABLE AIRPORTS ==========")

            for i, airport in enumerate(AIRPORTS, start=1):
                print(f"{i}. {airport}")

            try:
                departure = int(input("Departure airport number: "))
                destination = int(input("Destination airport number: "))

                if not 1 <= departure <= len(AIRPORTS):
                    print("Invalid departure airport number!")

                elif not 1 <= destination <= len(AIRPORTS):
                    print("Invalid destination airport number!")

                elif departure == destination:
                    print("Departure and destination cannot be the same!")

                else:
                    route = (
                        AIRPORTS[departure - 1],
                        AIRPORTS[destination - 1]
                    )

                    if route in ROUTES:
                        print("That route already exists!")
                    else:
                        ROUTES.append(route)
                        print(f"Route created: {route[0]} -> {route[1]}")
                        print(f"Total routes: {len(ROUTES)}")

            except ValueError:
                print("Please enter valid numbers!")

        elif choice == "2":
            print("\n========== YOUR FLIGHT ROUTES ==========")

            if not ROUTES:
                print("You haven't created any routes yet.")
            else:
                for i, route in enumerate(ROUTES, start=1):
                    print(f"{i}. {route[0]} -> {route[1]}")

        elif choice == "3":
            print("Returning to main menu...")
            return

        else:
            print("Invalid option! Choose 1, 2, or 3.")




def operate_flights():
    global MONEY

    if not ROUTES:
        print("\nYou need to create a route first!")
        return

    if not FLEET:
        print("\nYou need to buy an aircraft first!")
        return

    while True:
        print("\n========== FLIGHT OPERATIONS ==========")

        for i, route in enumerate(ROUTES, start=1):
            print(f"{i}. {route[0]} -> {route[1]}")

        print("0. Return to main menu")

        try:
            choice = int(input("Select a route to operate: "))
        except ValueError:
            print("Please enter a valid number!")
            continue

        if choice == 0:
            return

        if not 1 <= choice <= len(ROUTES):
            print("Invalid route selection!")
            continue

        route = ROUTES[choice - 1]

        print("\nFlight ready for departure!")
        print(f"Departure: {route[0]}")
        print(f"Destination: {route[1]}")

        passengers = random.randint(50, 200)
        ticket_price = 200
        fuel_cost = 12_000
        crew_cost = 3_000
        airport_fees = 2_000

        revenue = passengers * ticket_price
        total_costs = fuel_cost + crew_cost + airport_fees
        profit = revenue - total_costs
        MONEY += profit

        print("\n========== FLIGHT REPORT ==========")
        print(f"Passengers: {passengers}")
        print(f"Flight revenue: ${revenue:,}")
        print(f"Total costs: ${total_costs:,}")
        print(f"Profit/Loss: ${profit:,}")
        print(f"Updated airline balance: ${MONEY:,}")




def view_finances():
    print("\n========== AIRLINE FINANCES ==========")
    print(f"Airline: {BUSINESS_NAME}")
    print(f"Owner: {PLAYER_NAME}")
    print(f"Current balance: ${MONEY:,}")
    print(f"Aircraft owned: {len(FLEET)}")
    print(f"Routes created: {len(ROUTES)}")



def main_menu():
    while True:
        print("\n========== AIRLINE TYCOON ==========")
        print("1. View Airline Finances")
        print("2. Manage Aircraft")
        print("3. Manage Routes")
        print("4. Operate Flights")
        print("5. Exit Game")

        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            view_finances()
        elif choice == "2":
            manage_aircraft()
        elif choice == "3":
            manage_routes()
        elif choice == "4":
            operate_flights()
        elif choice == "5":
            print("\n========== FINAL AIRLINE SUMMARY ==========")
            print(f"Airline: {BUSINESS_NAME}")
            print(f"Aircraft owned: {len(FLEET)}")
            print(f"Routes created: {len(ROUTES)}")
            print(f"Final balance: ${MONEY:,}")
            print("Thanks for playing Airline Tycoon Simulator!")
            break
        else:
            print("Invalid option! Choose a number from 1 to 5.")


main_menu()
