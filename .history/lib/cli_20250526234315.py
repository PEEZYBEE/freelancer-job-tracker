import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lib.models import User, Job, Client, Payment, Base  # ensure __init__.py imports them

# Setup
engine = create_engine("sqlite:///freelancer.db")
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)

def register_user():
    print("\n📝 Register")
    username = input("Username: ")
    email = input("Email: ")
    password = input("Password: ")
    user = User(username=username, email=email, password_hash=password)
    session.add(user)
    session.commit()
    print("✅ User registered.")

def login_user():
    print("\n🔐 Login")
    username = input("Username: ")
    password = input("Password: ")
    user = session.query(User).filter_by(username=username, password_hash=password).first()
    return user

def add_client():
    name = input("Client name: ")
    email = input("Client email: ")
    session.add(Client(name=name, email=email))
    session.commit()
    print("✅ Client added.")

def view_clients():
    print("\n📇 Clients:")
    for c in session.query(Client).all():
        print(f"{c.id}. {c.name} - {c.email}")

def add_job(user):
    title = input("Job title: ")
    desc = input("Description: ")
    rate = float(input("Hourly rate: "))
    hours = float(input("Estimated hours: "))
    view_clients()
    client_id = int(input("Client ID: "))
    job = Job(title=title, description=desc, hourly_rate=rate, hours_estimate=hours, user_id=user.id, client_id=client_id)
    session.add(job)
    session.commit()
    print("✅ Job created.")

def view_jobs(user):
    print("\n🧾 Jobs:")
    jobs = session.query(Job).filter_by(user_id=user.id).all()
    for j in jobs:
        client = session.query(Client).get(j.client_id)
        print(f"{j.id}. {j.title} for {client.name} - ${j.hourly_rate}/hr - {j.status}")

def update_job_status():
    job_id = int(input("Job ID: "))
    new_status = input("New status (Pending/In Progress/Completed): ")
    job = session.query(Job).get(job_id)
    if job:
        job.status = new_status
        session.commit()
        print("✅ Status updated.")
    else:
        print("❌ Job not found.")

def delete_job():
    job_id = int(input("Job ID: "))
    job = session.query(Job).get(job_id)
    if job:
        session.delete(job)
        session.commit()
        print("✅ Job deleted.")
    else:
        print("❌ Job not found.")

def add_payment():
    job_id = int(input("Job ID: "))
    amount = float(input("Amount: "))
    payment = Payment(amount=amount, job_id=job_id,)
    session.add(payment)
    session.commit()
    print("✅ Payment recorded.")

def view_payments(user):
    print("\n💰 Payments:")
    for job in session.query(Job).filter_by(user_id=user.id):
        for p in job.payments:
            print(f"{p.id}. ${p.amount} for '{job.title}' on {p.payment_date.strftime('%Y-%m-%d')}")

def main_menu():
    while True:
        print("\n🌟 Freelancer App")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choice: ")
        if choice == "1":
            register_user()
        elif choice == "2":
            user = login_user()
            if user:
                print(f"✅ Welcome {user.username}!")
                user_menu(user)
            else:
                print("❌ Invalid credentials.")
        elif choice == "3":
            break

def user_menu(user):
    while True:
        print("\n🔧 Dashboard")
        print("1. Add Client")
        print("2. View Clients")
        print("3. Add Job")
        print("4. View Jobs")
        print("5. Update Job Status")
        print("6. Delete Job")
        print("7. Add Payment")
        print("8. View Payments")
        print("9. Logout")
        choice = input("Choice: ")
        if choice == "1":
            add_client()
        elif choice == "2":
            view_clients()
        elif choice == "3":
            add_job(user)
        elif choice == "4":
            view_jobs(user)
        elif choice == "5":
            update_job_status()
        elif choice == "6":
            delete_job()
        elif choice == "7":
            add_payment()
        elif choice == "8":
            view_payments(user)
        elif choice == "9":
            print("🔒 Logged out.")
            break

if __name__ == "__main__":
    main_menu()
