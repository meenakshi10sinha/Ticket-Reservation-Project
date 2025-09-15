import json
from datetime import datetime

# ----------------------------
# File Handling
# ----------------------------
DATA_FILE = "reservations.json"

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        # Default data if file not found
        return {
            "transport_name": "ExpressLine Bus",
            "total_seats": 20,
            "bookings": []
        }

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ----------------------------
# Ticket Reservation System
# ----------------------------
class TicketReservationSystem:
    def __init__(self):
        self.data = load_data()

    def view_seats(self):
        print("\n--- Seat Availability ---")
        seats = self.data["total_seats"]
        booked = [b["seat"] for b in self.data["bookings"]]
        for i in range(1, seats + 1):
            status = "Booked" if i in booked else "Available"
            print(f"Seat {i}: {status}")

    def book_ticket(self, name, seat):
        if seat < 1 or seat > self.data["total_seats"]:
            print("❌ Invalid seat number.")
            return
        # Check if seat already booked
        for b in self.data["bookings"]:
            if b["seat"] == seat:
                print("❌ Seat already booked.")
                return
        # Create booking record
        booking = {
            "name": name,
            "seat": seat,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.data["bookings"].append(booking)
        save_data(self.data)
        print(f"✅ Ticket booked successfully for {name} | Seat: {seat}")

    def cancel_ticket(self, seat):
        for b in self.data["bookings"]:
            if b["seat"] == seat:
                self.data["bookings"].remove(b)
                save_data(self.data)
                print(f"✅ Ticket for Seat {seat} has been cancelled.")
                return
        print("❌ No booking found for that seat.")

    def view_bookings(self):
        print("\n--- All Bookings ---")
        if not self.data["bookings"]:
            print("No bookings yet.")
        else:
            for b in self.data["bookings"]:
                print(f"Seat {b['seat']} | Name: {b['name']} | Time: {b['time']}")

# ----------------------------
# Main Menu
# ----------------------------
def main():
    system = TicketReservationSystem()
    while True:
        print("\n=== Ticket Reservation System ===")
        print("1. View Seat Availability")
        print("2. Book a Ticket")
        print("3. Cancel a Ticket")
        print("4. View All Bookings")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            system.view_seats()
        elif choice == "2":
            name = input("Enter your name: ")
            try:
                seat = int(input("Enter seat number: "))
                system.book_ticket(name, seat)
            except ValueError:
                print("❌ Please enter a valid seat number.")
        elif choice == "3":
            try:
                seat = int(input("Enter seat number to cancel: "))
                system.cancel_ticket(seat)
            except ValueError:
                print("❌ Please enter a valid seat number.")
        elif choice == "4":
            system.view_bookings()
        elif choice == "5":
            print("Exiting... Thank you!")
            break
        else:
            print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    main()
