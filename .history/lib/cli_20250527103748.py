import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lib.models import User, Job, Client, Payment, Base  

# Setup
engine = create_engine("sqlite:///freelancer.db")
Session = sessionmaker(bind=engine)
session = Session()


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

def add_client(user):
    name = input("Client name: ")
    email = input("Client email: ")
    company_name = input("Company name (optional): ")
    phone = input("Phone (optional): ")
    client = Client(name=name, email=email, company_name=company_name, phone=phone, user_id=user.id)
    session.add(client)
    session.commit()
    print("✅ Client added.")

def view_clients(user):
    print("\n📇 Your Clients:")
    clients = session.query(Client).filter_by(user_id=user.id).all()
    if not clients:
        print("No clients found.")
        return
    for c in clients:
        print(f"{c.id}. {c.name} - {c.email} - {c.company_name} - {c.phone}")

def add_job(user):
    title = input("Job title: ")
    desc = input("Description: ")
    rate = float(input("Hourly rate: "))
    hours = float(input("Estimated hours: "))
    view_clients(user)
    client_id = int(input("Client ID: "))

    # Tuple usage: group inputs into a tuple for confirmation
    job_info = (title, desc, rate, hours, client_id)
    print(f"📋 Confirming job info (tuple): {job_info}")

    job = Job(
        title=title,
        description=desc,
        hourly_rate=rate,
        hours_estimate=hours,
        user_id=user.id,
        client_id=client_id
    )
    session.add(job)
    session.commit()
    print("✅ Job created.")

def view_jobs(user):
    print("\n🧾 Jobs:")
    jobs = session.query(Job).filter_by(user_id=user.id).all()
    if not jobs:
        print("No jobs found.")
        return
    for j in jobs:
        client = session.query(Client).get(j.client_id)

        # Dictionary usage: create a dict summary for each job
        job_summary = {
            "Job ID": j.id,
            "Title": j.title,
            "Client": client.name if client else "N/A",
            "Hourly Rate": f"${j.hourly_rate}",
            "Status": j.status
        }
        print(job_summary)

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
    payment = Payment(amount=amount, job_id=job_id)
    session.add(payment)
    session.commit()
    print("✅ Payment recorded.")

def view_payments(user):
    print("\n💰 Payments:")
    jobs = session.query(Job).filter_by(user_id=user.id).all()
    if not jobs:
        print("No jobs/payments found.")
        return
    for job in jobs:
        for p in job.payments:
            print(f"{p.id}. ksh{p.amount} for '{job.title}' on {p.payment_date.strftime('%Y-%m-%d')}")

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
            add_client(user)
        elif choice == "2":
            view_clients(user)
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
