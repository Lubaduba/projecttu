import tkinter as tk
from datetime import datetime, date

# Main list to store dictionaries of event data
all_events = []
def add_event():
    name = name_entry.get().strip()
    date_text = date_entry.get().strip()
    
    # 1. Make sure the user typed an event name
    if not name:
        status_label.config(text="Please enter an event name.", fg="red")
        return

    parts = date_text.split(".")
    if len(parts) == 3 and all(p.isdigit() for p in parts): # kak rabortaet p.isdigit()
        try:
            # Convert string to date object for math & sorting
            event_date = datetime.strptime(date_text, "%d.%m.%Y").date()

            today = date.today()
            delta = event_date - today
            days_remaining = delta.days

            # Create the event record dictionary
            event_record = {
                "name": name,
                "date_str": date_text,
                "date_obj": event_date,
                "days_left": days_remaining,
                "sub_goals": subby
            }
            
            all_events.append(event_record)

            # 2. Sort the list chronologically by date objects
            # (Nearest/past dates at top, furthest dates at the bottom)
            all_events.sort(key=lambda x: x['date_obj']) # chto takoe lambda 
 
            # Clear entry boxes for the next input
            name_entry.delete(0, tk.END)
            date_entry.delete(0, tk.END)

            # Refresh the visual display list
            update_display()
            status_label.config(text="Event added successfully!", fg="green")
            return

        except ValueError:
            status_label.config(text="Invalid date! (Check for impossible days like Feb 31)", fg="red")
            return

    status_label.config(text="Invalid format. Please use DD.MM.YYYY", fg="red")

def open_new_window():
    # Opens a new standard tkinter Toplevel window
    new_win = tk.Toplevel(root)
    new_win.title("Event Details")
    new_win.geometry("300x200")
    sub = subby.get().strip()
    lbl = tk.Label(new_win, text=sub, font=("Arial", 11))
    lbl.pack(expand=True)
    
    close_btn = tk.Button(new_win, text="Close", command=new_win.destroy)
    close_btn.pack(pady=10)
def update_display():
    # Clear old buttons from previous updates so they don't duplicate
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    
    for event in all_events:
        days = event['days_left']
        if days > 0:
            time_text = f"{days} days left"
        elif days == 0:
            time_text = "Proeb!"
        else:
            time_text = f"{-(days)} days ago"
            
        # Create a standard tk.Button inside the scrollable frame
        row_button = tk.Button(
            scrollable_frame, 
            text=f"• {event['name']} ({event['date_str']}) — {time_text}",
            command=open_new_window,
            anchor="w",                  # Aligns text to the left
            relief="flat",               # Gives it a flat, modern look
            bg="#f8f9fa",
            activebackground="#e9ecef",
            padx=10,
            pady=6
        )
        # Pack it so it stretches across the width of the frame
        row_button.pack(fill="x", pady=2, padx=2)

root = tk.Tk()
root.title("Event Countdown Tracker")
root.geometry("400x700")

# Event Name Field
tk.Label(root, text="Event Name:", font=("Arial", 10, "bold")).pack(pady=(15, 0))
name_entry = tk.Entry(root, width=30, font=("Arial", 11))
name_entry.pack(pady=5)

# Date Field
tk.Label(root, text="Date (DD.MM.YYYY):", font=("Arial", 10, "bold")).pack(pady=(5, 0))
date_entry = tk.Entry(root, width=30, font=("Arial", 11))
date_entry.pack(pady=5)

tk.Label(root, text="Sub goals:", font=("Arial", 10, "bold")).pack(pady=(2.5, 0))
subby = tk.Entry(root, width=30, font=("Arial", 11))
subby.pack(pady=5)

# Submit Button
submit_btn = tk.Button(root, text="Add Event", command=add_event, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
submit_btn.pack(pady=50)

# Status Feedback Label
status_label = tk.Label(root, text="", font=("Arial", 9))
status_label.pack(pady=2)
# --- 1. CREATE A SCROLLABLE FRAME CONTAINER (Standard Tkinter) ---
container = tk.Frame(root)
container.pack(fill="both", expand=True, padx=10, pady=10)

canvas = tk.Canvas(container, bg="white", highlightthickness=0)
scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)

# This is where your event buttons will live
scrollable_frame = tk.Frame(canvas, bg="white")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")


# Start the application loop
root.mainloop()
