import psycopg2
from psycopg2 import Error
from datetime import datetime
from datetime import datetime, timedelta

# Function to establish a connection to the PostgreSQL database
def create_connection():
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="7741",
            host="localhost",
            port="5433",
            database="gym"
        )
        return connection
    except Error as e:
        print("Error while connecting to PostgreSQL:", e)
        return None

#a function which aids in member password authentication 
def verify_password(connection, member_id, password):
    try:
        cursor = connection.cursor()

        # Fetch the password for the given member ID
        cursor.execute("SELECT Password FROM Members WHERE RegisterationID = %s", (member_id,))
        stored_password = cursor.fetchone()[0]

        # Check if the provided password matches the stored password
        return password == stored_password

    except psycopg2.Error as e:
        print("Error verifying password:", e)
        return False

#a function which aids in trainer password authentication 
def verify_trainer_password(connection, trainer_id, password):
    try:
        cursor = connection.cursor()

        # Fetch the password for the given trainer ID
        cursor.execute("SELECT Password FROM Trainer WHERE TrainerID = %s", (trainer_id,))
        stored_password = cursor.fetchone()[0]

        # Check if the provided password matches the stored password
        return password == stored_password

    except psycopg2.Error as e:
        print("Error verifying trainer password:", e)
        return False

def get_trainer_name(connection, trainer_id):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT Name FROM Trainer WHERE TrainerID = %s", (trainer_id,))
        row = cursor.fetchone()
        if row:
            return row[0]  # Return the trainer name if a row is found
        else:
            print("Trainer not found.")
            return None
    except psycopg2.Error as e:
        print("Error fetching trainer name:", e)
        return None

#this function displays the personalized dashboard of the member
def display_dashboard(connection, member_id):
    try:
        cursor = connection.cursor()

        # Fetch exercise routines, fitness achievements, and health statistics for the member
        cursor.execute("SELECT ExerciseRoutines, FitnessAccomplishments, HealthStatistics FROM Members WHERE RegisterationID = %s", (member_id,))
        member_data = cursor.fetchone()

        if member_data is None:
            print("Error: Member not found.")
            return

        exercise_routines = member_data[0]
        fitness_accomplishments = member_data[1]
        health_statistics = member_data[2]

        # Print the dashboard
        print("\nDashboard for Member ID:", member_id)
        print("Exercise Routines:", exercise_routines)
        print("Fitness Achievements:", fitness_accomplishments)
        print("Health Statistics:", health_statistics)
        
    except psycopg2.Error as e:
        print("Error fetching dashboard data:", e)



def register_member(connection, name, email, phone, password, weight, time, bone_density, fat_percentage, exercise_routines, health_statistics, fitness_accomplishments, schedule):
    try:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO Members (Name, Email, Phone, Password, Weight, Time, BoneDensity, FatPercentage, ExerciseRoutines, HealthStatistics, FitnessAccomplishments, Schedule) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING RegisterationID",
                           (name, email, phone, password, weight, time, bone_density, fat_percentage, exercise_routines, health_statistics, fitness_accomplishments, schedule))

            registeration_id = cursor.fetchone()[0]
            connection.commit()
            print("Member registered successfully with ID:", registeration_id)

            # Add payment entry for gym membership
            cursor.execute("""
                INSERT INTO payment (registerationid, amount, service, status)
                VALUES (%s, %s, %s, %s)
            """, (registeration_id, 100, 'Gym Membership', 'payment in process'))

            connection.commit()
            print("Membership charged: $100, payment in process")
    except psycopg2.Error as e:
        print("Error registering member:", e)
        connection.rollback()


def remove_member(connection, member_id):
    try:
        with connection.cursor() as cursor:
            # Check if the member with the provided ID exists
            cursor.execute("SELECT Password FROM Members WHERE RegisterationID = %s", (member_id,))
            member_data = cursor.fetchone()

            if member_data is None:
                print("Error: Member not found.")
                return

            # Ask for the member's password
            password = input("Enter your password to confirm deletion: ")
            if password != member_data[0]:
                print("Error: Incorrect password. Deletion aborted.")
                return

            # Delete the corresponding entry from the payment table
            cursor.execute("DELETE FROM payment WHERE registerationid = %s", (member_id,))

            # Check if the member is referenced in the Joins table
            cursor.execute("SELECT ID FROM Joins WHERE RegisterationID = %s", (member_id,))
            join_data = cursor.fetchall()

            if join_data:
                # Remove references from the Joins table
                cursor.execute("DELETE FROM Joins WHERE RegisterationID = %s", (member_id,))

            # Delete the member from the Members table
            cursor.execute("DELETE FROM Members WHERE RegisterationID = %s", (member_id,))

            connection.commit()

            print("Member with ID", member_id, "has been successfully removed.")
    except psycopg2.Error as e:
        print("Error removing member:", e)
        connection.rollback()



def update_member(connection):
    try:
        cursor = connection.cursor()

        # Get member's registration ID and password
        member_id = input("Enter your Registration ID: ")
        password = input("Enter your password: ")

        # Verify user's password
        if not verify_password(connection, member_id, password):
            print("Error: Incorrect password. Update aborted.")
            return

        # Construct the SQL query based on the provided parameters
        update_query = "UPDATE Members SET "
        update_values = []

        # Ask for updated user information
        new_name = input("Enter new name:")
        new_email = input("Enter new email: ")
        new_phone = input("Enter new phone number: ")
        new_password = input("Enter new password: ")
        new_weight = input("Enter new weight: ")
        new_time = input("Enter new time: ")
        new_bone_density = input("Enter new bone density: ")
        new_fat_percentage = input("Enter new fat percentage: ")
        new_exercise_routines = input("Enter new exercise routines: ")
        new_health_statistics = input("Enter new health statistics: ")
        new_fitness_accomplishments = input("Enter new fitness accomplishments: ")
        new_schedule = input("Enter new schedule: ")

        # Add non-blank updated fields to the update query
        if new_name:
            update_query += "Name = %s, "
            update_values.append(new_name)
        if new_email:
            update_query += "Email = %s, "
            update_values.append(new_email)
        if new_phone:
            update_query += "Phone = %s, "
            update_values.append(new_phone)
        if new_password:
            update_query += "Password = %s, "
            update_values.append(new_password)
        if new_weight:
            update_query += "Weight = %s, "
            update_values.append(new_weight)
        if new_time:
            update_query += "Time = %s, "
            update_values.append(new_time)
        if new_bone_density:
            update_query += "BoneDensity = %s, "
            update_values.append(new_bone_density)
        if new_fat_percentage:
            update_query += "FatPercentage = %s, "
            update_values.append(new_fat_percentage)
        if new_exercise_routines:
            update_query += "ExerciseRoutines = %s, "
            update_values.append(new_exercise_routines)
        if new_health_statistics:
            update_query += "HealthStatistics = %s, "
            update_values.append(new_health_statistics)
        if new_fitness_accomplishments:
            update_query += "FitnessAccomplishments = %s, "
            update_values.append(new_fitness_accomplishments)
        if new_schedule:
            update_query += "Schedule = %s, "
            update_values.append(new_schedule)

        # Remove the trailing comma and space from the update query
        update_query = update_query.rstrip(", ")

        # Add WHERE clause to update only the specified member
        update_query += " WHERE RegisterationID = %s"
        update_values.append(member_id)

        # Execute the update query
        cursor.execute(update_query, update_values)
        connection.commit()

        print("User information updated successfully.The dashboard:")
        display_dashboard(connection, member_id)

    except psycopg2.Error as e:
        print("Error updating user information:", e)
        connection.rollback()

def add_trainer(connection):
    try:
        cursor = connection.cursor()

        # Get trainer details from the user
        name = input("Enter trainer's name: ")
        password = input("Enter trainer's password: ")
        email = input("Enter trainer's email: ")
        schedule = input("Enter trainer's schedule: ")

        # Insert the trainer into the database
        cursor.execute("INSERT INTO Trainer (Name, Password, Email, Schedule) VALUES (%s, %s, %s, %s)",
                       (name, password, email, schedule))
        connection.commit()

        print("Trainer added successfully.")

    except psycopg2.Error as e:
        print("Error adding trainer:", e)
        connection.rollback()

def update_trainer(connection): #schedule mamagment function, updates all attributes 
    try:
        cursor = connection.cursor()

        # Get trainer's ID and password
        trainer_id = input("Enter your Trainer ID: ")
        password = input("Enter your password: ")

        # Verify trainer's password
        if not verify_trainer_password(connection, trainer_id, password):
            print("Error: Incorrect password. Update aborted.")
            return

        # Construct the SQL query based on the provided parameters
        update_query = "UPDATE Trainer SET "
        update_values = []

        # Ask for updated trainer information
        new_name = input("Enter new name :")
        new_email = input("Enter new email:")
        new_password = input("Enter new password : ")
        new_schedule = input("Enter new schedule : ")

        # Add non-blank updated fields to the update query
        if new_name:
            update_query += "Name = %s, "
            update_values.append(new_name)
        if new_email:
            update_query += "Email = %s, "
            update_values.append(new_email)
        if new_password:
            update_query += "Password = %s, "
            update_values.append(new_password)
        if new_schedule:
            update_query += "Schedule = %s, "
            update_values.append(new_schedule)

        # Remove the trailing comma and space from the update query
        update_query = update_query.rstrip(", ")

        # Add WHERE clause to update only the specified trainer
        update_query += " WHERE TrainerID = %s"
        update_values.append(trainer_id)

        # Execute the update query
        cursor.execute(update_query, update_values)
        connection.commit()

        print("Trainer information updated successfully.")

    except psycopg2.Error as e:
        print("Error updating trainer information:", e)
        connection.rollback()

def getAll_trainers(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT trainerID, Name, Email, Schedule FROM Trainer")
        return cursor.fetchall()
    except psycopg2.Error as e:
        print("Error fetching trainers:", e)
        return []


def check_trainer_availability(connection, trainer_id, date, time):
    try:
        cursor = connection.cursor()
        # Concatenate date and time to form a timestamp
        timestamp = f"{date} {time}"
        cursor.execute("""
            SELECT COUNT(*) FROM trains
            WHERE trainerID = %s AND (date + CAST(%s AS INTERVAL)) = %s
        """, (trainer_id, time, timestamp))
        count = cursor.fetchone()[0]
        return count == 0
    except psycopg2.Error as e:
        print("Error checking trainer availability:", e)
        return False

def display_available_times(connection, trainer_id, date):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT Schedule FROM Trainer WHERE TrainerID = %s", (trainer_id,))
        schedule = cursor.fetchone()[0]
        booked_times = []
        if schedule:
            # Parse the schedule to get the available time slots
            parts = schedule.split(',')
            for part in parts:
                time_range = part.strip()  # Remove leading/trailing spaces
                times = time_range.split('-')
                if len(times) == 2:  # Ensure there are exactly two times
                    start_time, end_time = times
                    booked_times.append((start_time.strip(), end_time.strip()))
                else:
                    print("Error parsing time range:", time_range)
        
        # Get all available times for the given date
        cursor.execute("SELECT time FROM trains WHERE trainerID = %s AND date = %s", (trainer_id, date))
        booked_times_in_db = [str(time[0].time()) if isinstance(time[0], datetime) else str(time[0]) for time in cursor.fetchall()]

        # Debug print statements
        print("Booked Times in DB:", booked_times_in_db)
        print("Booked Times:", booked_times)

        # Filter out booked times from the available times
        available_times = []
        for slot_start_time, end_time in booked_times:
            available_times.extend(get_available_times(slot_start_time, end_time, booked_times_in_db))
        
        return available_times

    except psycopg2.Error as e:
        print("Error displaying available times:", e)
        return []


def get_available_times(start_time, end_time, booked_times):
    available_times = []
    current_time = datetime.strptime(start_time, '%H:%M:%S')
    end_time = datetime.strptime(end_time, '%H:%M:%S')
    while current_time < end_time:
        time_str = current_time.strftime('%H:%M:%S')
        if time_str not in booked_times:
            available_times.append(time_str)
        current_time += timedelta(hours=1)
    return available_times




def schedule_session(connection, member_id, trainer_id, date, time, duration):
    try:
        cursor = connection.cursor()
        # Check if the requested time falls within the trainer's available time slots
        available_times = display_available_times(connection, trainer_id, date)
        if time not in available_times:
            print("The requested time is not available.")
            return
        
        # Concatenate date and time to form a full timestamp
        full_timestamp = datetime.strptime(f'{date} {time}', '%Y-%m-%d %H:%M:%S')
        cursor.execute("""
            INSERT INTO Trains (RegisterationID, TrainerID, Date, Time, Duration)
            VALUES (%s, %s, %s, %s, %s)
        """, (member_id, trainer_id, date, full_timestamp, duration))
        connection.commit()
        trainer_name = get_trainer_name(connection, trainer_id)
        print(f"Private training session successfully scheduled with {trainer_name}, from {time}, for {duration} hours.")
        
        # Update the payment table
        cursor.execute("""
            INSERT INTO payment (registerationid, service, amount, status)
            VALUES (%s, %s, %s, %s)
        """, (member_id, 'personal training fee', 35, 'payment under process'))
        
        # Commit the transaction
        connection.commit()
        print("Personal training fee charged: $35, payment is under process.")
        
    except psycopg2.Error as e:
        print("Error scheduling session:", e)
        connection.rollback()

def reschedule_session(connection, member_id, trainer_id, old_date, old_time, new_date, new_time):
    try:
        cursor = connection.cursor()
        # Convert time strings to datetime objects
        old_time_dt = datetime.strptime(old_time, '%H:%M:%S')
        new_time_dt = datetime.strptime(new_time, '%H:%M:%S')
        
        # Update the session with the new date and time
        sql_query = """
            UPDATE trains
            SET Date = %s, Time = %s
            WHERE RegisterationID = %s AND TrainerID = %s AND Date = %s AND Time = %s
        """
        cursor.execute(sql_query, (new_date, new_time_dt, member_id, trainer_id, old_date, old_time_dt))
        connection.commit()
        print("Session rescheduled successfully. The new session is at", new_time_dt.strftime('%H:%M:%S') + ".")
       

    except psycopg2.Error as e:
        print("Error rescheduling session:", e)
        connection.rollback()

def cancel_session(connection, member_id, trainer_id, date, time):
    try:
        cursor = connection.cursor()

        # Construct the full timestamp by concatenating the date and time
        full_timestamp = f"{date} {time}"

        # Delete the session using the full timestamp
        cursor.execute("""
            DELETE FROM Trains
            WHERE RegisterationID = %s AND TrainerID = %s AND Date = %s AND Time = %s
        """, (member_id, trainer_id, date, full_timestamp))
        connection.commit()

        print("Session canceled successfully.")
    except psycopg2.Error as e:
        print("Error canceling session:", e)
        connection.rollback()

def add_fitness_class(connection, name, date, time, trainer_id):
    try:
        cursor = connection.cursor()

        # Parse the date and time input strings into datetime objects
        datetime_str = date + ' ' + time
        datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')

        # Insert the new fitness class into the database
        cursor.execute("""
            INSERT INTO FitnessClasses (Name, Date, Time, TrainerID)
            VALUES (%s, %s, %s, %s)
        """, (name, datetime_obj.date(), datetime_obj, trainer_id))
        
        connection.commit()
        print("New fitness class added successfully.")

    except psycopg2.Error as e:
        print("Error adding fitness class:", e)
        connection.rollback()

def class_registeration(connection, member_id, fitness_class_id):
    try:
        cursor = connection.cursor()
        
        # Check if the member is already registered for the fitness class
        cursor.execute("""
            SELECT * FROM Joins
            WHERE ID = %s AND RegisterationID = %s
        """, (fitness_class_id, member_id))
        if cursor.fetchone():
            print("You are already registered for this fitness class.")
            return
        
        # Register the member for the fitness class
        cursor.execute("""
            INSERT INTO Joins (ID, RegisterationID)
            VALUES (%s, %s)
        """, (fitness_class_id, member_id))
        
        # Update the Joins table in the database
        connection.commit()
        print("Successfully registered for the fitness class.")
        
        # Update the payment table
        cursor.execute("""
            INSERT INTO payment (registerationid, service, amount, status)
            VALUES (%s, %s, %s, %s)
        """, (member_id, 'fitness class fee', 20, 'payment under process'))
        
        # Commit the transaction
        connection.commit()
        print("Fitness class fee charged: $20, payment is under process.")

    except psycopg2.Error as e:
        print("Error registering for the fitness class:", e)
        connection.rollback()

def view_member_profile(connection, member_name):
    try:
        cursor = connection.cursor()

        # Search for the member by name
        cursor.execute("""
            SELECT RegisterationID, Name, Weight, Time, Schedule, BoneDensity, FatPercentage, HealthStatistics, FitnessAccomplishments
            FROM Members
            WHERE Name = %s
        """, (member_name,))
        member_data = cursor.fetchone()

        if member_data is None:
            print("Error: Member not found.")
            return

        member_id, name, weight, time, schedule, bone_density, fat_percentage, health_statistics, fitness_accomplishments = member_data

        # Print the member's profile
        print("\nMember Profile:")
        print("Member ID:", member_id)
        print("Name:", name)
        print("Weight:", weight)
        print("Time:", time)
        print("Schedule:", schedule)
        print("Bone Density:", bone_density)
        print("Fat Percentage:", fat_percentage)
        print("Health Statistics:", health_statistics)
        print("Fitness Accomplishments:", fitness_accomplishments)
        
    except psycopg2.Error as e:
        print("Error fetching member profile:", e)



def room_booking(connection, room_number, class_id):
    try:
        cursor = connection.cursor()

        # Retrieve the scheduled time for the fitness class
        cursor.execute("SELECT Time FROM FitnessClasses WHERE ID = %s", (class_id,))
        class_time = cursor.fetchone()

        if class_time:
            # Check availability of the room for the scheduled time
            cursor.execute("SELECT AvailabilityStatus FROM Room WHERE RoomNumber = %s AND Time = %s", (room_number, class_time))
            availability_status = cursor.fetchone()

            if availability_status and availability_status[0] == 'Available':
                # Update the database to mark the room as booked
                cursor.execute("UPDATE Room SET AvailabilityStatus = 'Booked', ID = %s WHERE RoomNumber = %s", (class_id, room_number))
                connection.commit()
                print("Room successfully booked.")
            else:
                print("Room is not available for the scheduled time.")
        else:
            print("Error: Fitness class with ID {} does not exist.".format(class_id))

    except psycopg2.Error as e:
        print("Error:", e)
        connection.rollback()

# Function to check if the entered admin ID is valid
def verify_adminID(connection, admin_id):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM AdministrativeStaff WHERE AdminId = %s", (admin_id,))
        return cursor.fetchone() is not None
    except psycopg2.Error as e:
        print("Error checking admin ID:", e)
        return False


def update_classSchedule(connection, class_id):
    try:
        cursor = connection.cursor()

        # Prompt the user to enter the new date and time
        new_date = input("Enter the new date of the fitness class (YYYY-MM-DD): ")
        new_time = input("Enter the new time of the fitness class (HH:MM:SS): ")

        # Parse the new date and time input strings into datetime objects
        new_datetime_str = new_date + ' ' + new_time
        new_datetime_obj = datetime.strptime(new_datetime_str, '%Y-%m-%d %H:%M:%S')

        # Update the date and time of the fitness class in the database
        cursor.execute("""
            UPDATE FitnessClasses
            SET Date = %s, Time = %s
            WHERE ID = %s
        """, (new_datetime_obj.date(), new_datetime_obj, class_id))
        
        connection.commit()
        print("Fitness class schedule updated successfully.")

    except psycopg2.Error as e:
        print("Error updating fitness class schedule:", e)
        connection.rollback()

def display_allRooms(connection):
    try:
        cursor = connection.cursor()

        # Display the room table from the database
        cursor.execute("SELECT * FROM Room")
        room_data = cursor.fetchall()

        print("\nRoom Table:")
        print("RoomNumber | Capacity | AvailabilityStatus | Time | ID")
        for row in room_data:
            print(row)

    except psycopg2.Error as e:
        print("Error displaying room table:", e)

def process_payment(connection):
    try:
        with connection.cursor() as cursor:
            # Display payments
            cursor.execute("SELECT * FROM payment")
            payments = cursor.fetchall()
            print("Payments:")
            for payment in payments:
                print(payment)

            # Prompt the user to enter the member ID for the payment to process
            member_id = input("Enter Member ID for whom you wish to process the payment: ")

            # Update the status column to "payment processed" for the specified member ID
            cursor.execute("UPDATE payment SET status = 'payment processed' WHERE registerationid = %s", (member_id,))
            connection.commit()

            print("Payment successfully processed.")
    except psycopg2.Error as e:
        print("Error processing payment:", e)
        connection.rollback()


def maintain_equip(connection):
    try:
        cursor = connection.cursor()

        # Display the equipment table
        cursor.execute("SELECT * FROM Equipment")
        equipment_records = cursor.fetchall()
        print("Equipment Table:")
        print("EquipmentID | EquipmentName | EquipmentType | LastMaintenanceDate | MaintenanceDue")
        for record in equipment_records:
            print(record)

        # Ask the user to enter the equipment ID they wish to update
        equipment_id = int(input("Enter the Equipment ID you wish to update: "))

        # Check if the entered equipment ID exists
        cursor.execute("SELECT EquipmentID FROM Equipment WHERE EquipmentID = %s", (equipment_id,))
        if cursor.rowcount == 0:
            print("Equipment with ID", equipment_id, "does not exist.")
            return

        # Prompt the user to update maintenance information
        last_maintenance_date = input("Enter the new last maintenance date (YYYY-MM-DD): ")
        maintenance_due = input("Is maintenance due for this equipment? (True/False): ").capitalize()

        # Update the maintenance information in the database
        cursor.execute("""
            UPDATE Equipment
            SET LastMaintenanceDate = %s, MaintenanceDue = %s
            WHERE EquipmentID = %s
        """, (last_maintenance_date, maintenance_due, equipment_id))
        
        connection.commit()
        print("Maintenance information updated successfully.")

    except psycopg2.Error as e:
        print("Error changing maintenance status:", e)
        connection.rollback()

# Function to handle administrative tasks menu
def administrative_tasks_menu(connection):
    while True:
        print("\nAdministrative Tasks Menu:")
        print("1. Add a new Fitness Class")
        print("2. Book a room for a class")
        print("3. Update Fitness Class Schedule")
        print("4. Process Payments")
        print("5. Maintain Equipment")
        print("6. Exit")
   

        choice = input("Enter your choice: ")
        if choice == '1':
            # Call the function to add a new fitness class
            print("\nCreating a new group Fitness Classes:")
            # Prompt the user to enter details of the new fitness class
            name = input("Enter the name of the fitness class: ")
            date = input("Enter the date of the fitness class (YYYY-MM-DD): ")
            time = input("Enter the time of the fitness class (HH:MM:SS): ")
            trainer_id = int(input("Enter the ID of the trainer for the fitness class: "))

            # Add the new fitness class
            add_fitness_class(connection, name, date, time, trainer_id)

        elif choice == '2':
            # Prompt the user to enter details of the room and fitness class
            # Display the room table from the database
            display_allRooms(connection)
            room_number = int(input("Enter the room number: "))
            class_id = int(input("Enter the ID of the fitness class: "))
            room_booking(connection, room_number, class_id)

        elif choice == '3':
            # Update fitness class schedule
            class_id = int(input("Enter the ID of the fitness class to update: "))
            update_classSchedule(connection, class_id)

        elif choice == '4':
            process_payment(connection)

        elif choice == '5':
            # equipment maintenance and monitoring 
            maintain_equip(connection)


        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")


def main():
    print("Welcome to Carleton Athletics!")

    # Establish connection to the database
    connection = create_connection()
    if connection is None:
        print("Error: Could not establish connection to the database.")
        return

    # Main loop
    while True:
        print("\nPlease select an option:")
        print("1. Register as a new member")
        print("2. Withdraw from membership")
        print("3. View Dashboard")
        print("4. Update profile/dashboard")
        print("5. Add new Trainer")
        print("6. Update Trainer Information")
        print("7. Schedule personal Training Sessions")
        print("8. Reschedule personal Training Session")
        print("9. Cancel personal training session")
        print("10. Join a Group Fitness class")
        print("11. View Member Profile")
        print("12. Complete administrative task")
        print("13. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            print("\n Provide the following information to Register as a new member:")
            name = input("Name: ")
            email = input("Email: ")
            phone = input("Phone: ")
            password = input("Password: ")
            weight = float(input("Weight: "))
            time = float(input("Time: "))
            bone_density = float(input("Bone Density: "))
            fat_percentage = float(input("Fat Percentage: "))
            exercise_routines = input("Exercise Routines: ")
            health_statistics = int(input("Health Statistics: "))
            fitness_accomplishments = input("Fitness Accomplishments: ")
            schedule = input("Schedule: ")

            # Registering the member in the database
            register_member(connection, name, email, phone, password, weight, time, bone_density, fat_percentage, exercise_routines, health_statistics, fitness_accomplishments, schedule)

            # Retrieve the registration ID of the newly registered member
            with connection.cursor() as cursor:
                cursor.execute("SELECT RegisterationID FROM Members WHERE Email = %s", (email,))
                registeration_id = cursor.fetchone()[0]

            # Display dashboard after registration
            display_dashboard(connection, registeration_id)

        elif choice == '2':
            print("\nWithdraw from membership:")
            member_id = int(input("Enter your Registration ID: "))
            remove_member(connection, member_id)

        elif choice == '3':
            print("\nView Dashboard:")
            member_id = int(input("Enter your Registration ID: "))
            password = input("Enter your password: ")
            # Verify password
            if verify_password(connection, member_id, password):
                display_dashboard(connection, member_id)
            else:
                print("Error: Incorrect password. Dashboard access denied.")

        elif choice == '4':
            print("\nUpdate Profile:")
            # Call update_member function
            update_member(connection)

        elif choice == '5':
            print("\nAdding new Trainer:")
            # Call update_user function
            add_trainer(connection)
        
        elif choice == '6':
            print("\nupdating Trainer information:")
            # Call update_trainer function
            update_trainer(connection)

        elif choice == '7':
            print("\nScheduling a session with Trainer:")
            
            # Fetch all trainers
            trainers = getAll_trainers(connection)
            print("Available Trainers:")
            for trainer in trainers:
                print(trainer)

            # Choose a trainer
            trainer_id = input("Enter Trainer ID: ")

            # Check availability for a specific date and time
            date = input("Enter Date (YYYY-MM-DD): ")
            time = input("Enter Time (HH:MM:SS): ")
            duration = input("Enter Duration (hours): ")
            available = check_trainer_availability(connection, trainer_id, date, time)
            if available:
                print(f"{get_trainer_name(connection, trainer_id)} is available.")
            else:
                print(f"{get_trainer_name(connection, trainer_id)} is booked for {time} on {date}.")

            # Display available times for the chosen trainer on the given date
            available_times = display_available_times(connection, trainer_id, date)
            print("Available Times:")
            for available_time in available_times:
                print(available_time)

            # Schedule a session
            member_id = input("Enter Member ID: ")
            schedule_session(connection, member_id, trainer_id, date, time,duration)

        
        elif choice == '8':
            print("\nRescheduling personal training session:")
            member_id = input("Enter Member ID: ")
            trainer_id = input("Enter Trainer ID: ")
            # Reschedule a session
            old_date = input("Enter Old Date (YYYY-MM-DD): ")
            old_time = input("Enter Old Time (HH:MM:SS): ")
            new_date = input("Enter New Date (YYYY-MM-DD): ")
            new_time = input("Enter New Time (HH:MM:SS): ")
            # Assuming you have values for member_id, trainer_id, old_date, old_time, new_date, and new_time
            # Call the reschedule_session function with all required arguments
            reschedule_session(connection, member_id, trainer_id, old_date, old_time, new_date, new_time)


        elif choice == '9':
            print("\nCancelling personal training session:")
            member_id = input("Enter Member ID: ")
            trainer_id = input("Enter Trainer ID: ")
            date = input("Enter Date (YYYY-MM-DD): ")
            time = input("Enter Time (HH:MM:SS): ")
            # Cancel a session
            cancel_session(connection, member_id, trainer_id, date, time)


        elif choice == '10':
            print("\nJoining Group Fitness Classes:")
           # Get the fitness class ID and member ID from the user
            fitness_class_id = input("Enter the fitness class ID: ")
            member_id = input("Enter your member ID: ")

            # Register the member for the fitness class
            class_registeration(connection, member_id, fitness_class_id)

        elif choice == '11':
            print("\nViewing Member's Profile:")
            # Prompt the trainer to enter the member's name
            member_name = input("Enter the member's name: ")

            # View the member's profile
            view_member_profile(connection, member_name)

        elif choice == '12':
            admin_id = input("Enter your Admin ID: ")
            if verify_adminID(connection, admin_id):
                administrative_tasks_menu(connection)
            else:
                print("Invalid Admin ID. Access denied.")

        elif choice == '13':
            print("Exiting the program. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter 1, 2, 3, 4,6,7,8,9,10,11,12 or 13.")




        # Option 3 and other choices...

    # Close the database connection
    connection.close()


if __name__ == "__main__":
    main()
