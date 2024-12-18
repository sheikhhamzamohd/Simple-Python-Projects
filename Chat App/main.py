import mysql.connector
from mysql.connector import Error
import time

db_config = {
'host': 'localhost',
'user': 'root',
'password': 'Hamza.2007#^',
'database': 'chat_db'
}

def signin(username, password):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute('INSERT INTO users (username) VALUES (%s)', (username, password,))
        connection.commit()
        print("Sign in successfully! You can now log in.")
    except Error as e:
        if 'Duplicate entry' in str(e):
            print("Username already exists.")
        else:
            print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def signout(username, password): 
    try: 
        connection = mysql.connector.connect(**db_config) 
        cursor = connection.cursor()
        cursor.execute('DELETE FROM users WHERE username = %s', (username, password,))
        connection.commit()
        result = cursor.fetchone()
    except Error as e: 
        print(f"Error: {e}") 
    finally: 
        if connection.is_connected(): 
            cursor.close() 
            connection.close()

def login(username, password):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s', (username, password,))
        result = cursor.fetchone()
        return result is not None
    except Error as e:
        print(f"Error: {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def logout(username): 
    print(f"You are logged out from {username}.")
    print("You need to log in again.")

def send_message(username, message):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute('INSERT INTO messages (username, message) VALUES (%s, %s)', (username, message))
        connection.commit()
        print("Message sent!")
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def display_messages():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute('SELECT username, message FROM messages')
        messages = cursor.fetchall()
        for username, message in messages:
            print(f"{username}: {message}")
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def main():
    logged_in_user = None
    logged_in_password = None
    while True:
        print("\nChat Application")
        print("------------------------------")
        print("Menu:")
        print("Enter 1: Sign in")
        print("Enter 2: Sign out")
        print("Enter 3: Log in")
        print("Enter 4: Log out")
        print("Enter 5: Send message")
        print("Enter 6: Display Messages")
        print("Enter 7: Quit")
        choice = input("Choose an option: ")

        if choice == '1':
            username = input("Enter your username to sign in: ")
            password = input("Enter your password: ")
            signin(username, password)

        elif choice == '2':
            username = input("Enter your username to sign out: ")
            if signout(username, password):
                connection = mysql.connector.connect(**db_config) 
                cursor = connection.cursor()
                cursor.execute('DELETE FROM messages WHERE username = %s', (username,))
                print(f"User {username} has been removed from the system.")
            else:
                print("Username not found or password is incorrect.")

        elif choice == '3':
            username = input("Enter your username to log in: ")
            password = input("Enter your password: ")
            if login(username, password):
                logged_in_user = username
                logged_in_password = password
                print(f"You have logged in as {username}.")
            else:
                print("Username not signed in or password is incorrect.")

        elif choice == '4':
            password = input("Enter your password: ")
            if logged_in_user and logged_in_password == password:
                logout(logged_in_user)
                logged_in_user = None
                logged_in_password = None
            else:
                print("You are not logged in or password is incorrect.")

        elif choice == '5':
            if logged_in_user:
                msg = input("Enter your message: ")
                current_time = time.strftime("%Y-%m-%d %H:%M:%S")
                message = f"{msg} ({current_time})"
                send_message(logged_in_user, message)
            else:
                print("You need to log in first.")

        elif choice == '6':
            display_messages()

        elif choice == '7':
            print("Quitting...")
            break

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__": main()