# lib/cli.py
from models import session, User

def main():
    while True:
        print("\n📋 Freelancer Job Tracker Menu")
        print("1. Register new user")
        print("2. View all users")
        print("3. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            username = input("Username: ")
            email = input("Email: ")
            password = input("Password: ")

            user = User(username=username, email=email, password_hash=password)
            session.add(user)
            session.commit()
            print("✅ User registered!")

        elif choice == '2':
            users = session.query(User).all()
            for u in users:
                print(f"- {u.username} | {u.email}")

        elif choice == '3':
            print("👋 Goodbye!")
            break

        else:
            print("❌ Invalid choice.")

if __name__ == '__main__':
    main()
