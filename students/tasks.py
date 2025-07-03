from celery import shared_task
import requests
import time

@shared_task
def send_welcome_email(username, email):
    print(f"\nStarting to process email for: {username} ({email})")
    time.sleep(13)  
    print(f"\nEmail sent successfully to {email}!")
    return f"\nWelcome email sent to {username}"

@shared_task
def send_welcome(username, email):
    print(f"\nStarting to process for: {username} ({email})")
    time.sleep(13)  
    print(f"\sent successfully to {email}!")
    return f"\nWelcome sent to {username}"


@shared_task
def task_a(x):
    print(f"[Task A] Received: {x}")
    return x + 1

@shared_task
def task_b(y):
    print(f"[Task B] Received: {y}")
    return y * 2

@shared_task
def task_c(z):
    print(f"[Task C] Received: {z}")
    return f"Final result is: {z}"
