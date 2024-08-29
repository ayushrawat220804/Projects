import mysql.connector
from mysql.connector import Error
import getpass

class GymManagementSystem:
    def __init__(self):
        self.connection = self.create_connection("localhost", "root", "gourav48", "gym_management")
        if not self.connection:
            print("Error: Could not establish a database connection.")
            exit()

    def create_connection(self, host_name, user_name, user_password, db_name):
        connection = None
        try:
            connection = mysql.connector.connect(
                host=host_name,
                user=user_name,
                password=user_password,
                database=db_name
            )
            print("Connection to MySQL DB successful")
        except Error as e:
            print(f"Connection failed: {e}")
        return connection

    def register(self):
        if not self.connection:
            print("Cannot register because the database connection is not established.")
            return

        username = input("Enter username: ")
        password = getpass.getpass("Enter password (hidden): ")
        try:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            self.connection.commit()
            print("User registered successfully!")
        except Error as e:
            print(f"Error during registration: {e}")

    def login(self):
        if not self.connection:
            print("Cannot log in because the database connection is not established.")
            return None

        username = input("Enter username: ")
        password = getpass.getpass("Enter password (hidden): ")
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            result = cursor.fetchone()
            if result:
                print("Login successful!")
                return result
            else:
                print("Invalid credentials!")
                return None
        except Error as e:
            print(f"Error during login: {e}")
            return None

    def select_workout_package(self, user_id):
        # Predefined workout packages and fees
        packages = {
            '1': ("Basic Package", 1, 30, 1000),  # Fee: 1000
            '2': ("Standard Package", 3, 45, 2500),  # Fee: 2500
            '3': ("Premium Package", 6, 60, 4500)  # Fee: 4500
        }

        print("\nAvailable workout packages:")
        for key, details in packages.items():
            print(f"{key}. {details[0]} ({details[1]} Month(s), {details[2]} mins/day) - ₹{details[3]}")

        package_choice = input("Select a package (1-3): ")
        if package_choice not in packages:
            print("Invalid choice!")
            return

        package, duration, workout_time, fee = packages[package_choice]

        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "UPDATE users SET package = %s, duration = %s, workout_time = %s, package_fee = %s WHERE id = %s",
                (package, duration, workout_time, fee, user_id)
            )
            self.connection.commit()
            print(f"{package} selected for {duration} month(s) with {workout_time} minutes/day. Fee: ₹{fee}")
        except Error as e:
            print(f"Error during package selection: {e}")

    def personal_training_option(self, user_id):
        # Predefined personal training fee
        personal_training_fee = 5000

        personal_training = input("\nDo you want personal training? (yes/no): ").lower()
        is_personal_training = personal_training == 'yes'

        if is_personal_training:
            print(f"Personal training selected with a fixed fee of ₹{personal_training_fee}.")

        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "UPDATE users SET personal_training = %s, trainer_fee = %s WHERE id = %s",
                (is_personal_training, personal_training_fee if is_personal_training else 0, user_id)
            )
            self.connection.commit()
        except Error as e:
            print(f"Error during personal training update: {e}")

    def payment_option(self, user_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT package_fee, trainer_fee FROM users WHERE id = %s", (user_id,))
            package_fee, trainer_fee = cursor.fetchone() or (0.0, 0.0)

            total_fee = package_fee + trainer_fee

            if total_fee > 0:
                print(f"\nTotal fee to pay: ₹{total_fee}")
                print("Payment Options:")
                print("1. Cash")
                print("2. UPI")
                print("3. Credit/Debit Card")
                payment_choice = input("Select a payment method (1-3): ")

                if payment_choice in ['1', '2', '3']:
                    print("Payment successful!")
                else:
                    print("Invalid payment option!")
            else:
                print("No fee to pay.")
        except Error as e:
            print(f"Error during payment: {e}")

    def run(self):
        while True:
            print("\n=== Gym Management System ===")
            print("1. Register")
result = 100
result = 12
logger.debug('Processing data')
            print("2. Login")
            print("3. Exit")
            choice = input("Select an option: ")

            if choice == '1':
                self.register()
            elif choice == '2':
                user = self.login()
                if user:
                    user_id = user[0]  # Assuming 'id' is the first column in the 'users' table
                    while True:
                        print("\n=== Member Menu ===")
                        print("1. Select Workout Package")
                        print("2. Personal Training Option")
                        print("3. Payment Option")
                        print("4. Logout")
                        user_choice = input("Select an option: ")

                        if user_choice == '1':
                            self.select_workout_package(user_id)
                        elif user_choice == '2':
                            self.personal_training_option(user_id)
                        elif user_choice == '3':
                            self.payment_option(user_id)
                        elif user_choice == '4':
                            print("Logging out...")
                            break
                        else:
                            print("Invalid choice! Please try again.")
            elif choice == '3':
                print("Exiting the system. Goodbye!")
                break
            else:
                print("Invalid option! Please select again.")

if __name__ == "__main__":
    gym_system = GymManagementSystem()
    gym_system.run()
