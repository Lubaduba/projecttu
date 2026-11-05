import tkinter as tk
from tkinter import colorchooser, messagebox
from datetime import datetime, date

class SparrowTimelineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sparrow Timeline with Clustering")
        self.root.geometry("900x450")

        self.events = []
        self.selected_color = "#3498db"
        self.origin_x = 80              # Left margin where "Today" sits
        self.timeline_y = 120           # Y coordinate of the main line
        self.canvas_width = 860         # Total width limit for the timeline track

        self.setup_ui()
        self.render_events()

    def setup_ui(self):
        # 1. Canvas for Timeline
        self.canvas = tk.Canvas(self.root, bg="#f4f6f7", height=220)
        self.canvas.pack(fill=tk.X, padx=10, pady=10)
        # Bind canvas clicks to handle cluster inspection
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        # 2. Input Controls Frame
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X, padx=15, pady=10)

        # Event Title Input
        tk.Label(control_frame, text="Event Name:").grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = tk.Entry(control_frame, width=20)
        self.title_entry.insert(0, "Math test")
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        # Event Date Input (YYYY-MM-DD)
        tk.Label(control_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=2, padx=5, pady=5)
        self.date_entry = tk.Entry(control_frame, width=12)
        self.date_entry.insert(0, date.today().strftime("%Y-%m-%d"))
        self.date_entry.grid(row=0, column=3, padx=5, pady=5)

        # Color Selector Button
        self.color_btn = tk.Button(
            control_frame, text="Select Color", bg=self.selected_color, 
            fg="white", command=self.pick_color
        )
        self.color_btn.grid(row=0, column=4, padx=5, pady=5)

        # Add Event Button
        add_btn = tk.Button(
            control_frame, text="Add to Timeline", bg="#2ecc71", 
            fg="white", font=("Arial", 10, "bold"), command=self.add_event
        )
        add_btn.grid(row=0, column=5, padx=15, pady=5)

    def pick_color(self):
        color_code = colorchooser.askcolor(title="Choose Circle Color")[1]
        if color_code:
            self.selected_color = color_code
            self.color_btn.config(bg=color_code)

    def add_event(self):
        title = self.title_entry.get().strip()
        date_str = self.date_entry.get().strip()

        if not title or not date_str:
            messagebox.showwarning("Input Error", "Please enter both title and date!")
            return

        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Date Error", "Please use format: YYYY-MM-DD")
            return

        days_left = (target_date - date.today()).days

        self.events.append({
            "title": title,
            "days_left": days_left,
            "date_str": date_str,
            "color": self.selected_color
        })

        # Sort events chronologically by days_left
        self.events.sort(key=lambda x: x["days_left"])
        self.render_events()

    def cluster_events(self):
        """Groups events that are within 5 days of each other."""
        if not self.events:
            return []

        clusters = []
        current_cluster = [self.events[0]]

        for ev in self.events[1:]:
            # If the event is within 5 days of the first event in the current cluster
            if ev["days_left"] - current_cluster[0]["days_left"] <= 5:
                current_cluster.append(ev)
            else:
                clusters.append(current_cluster)
                current_cluster = [ev]
        clusters.append(current_cluster)
        return clusters

    def render_events(self):
        self.canvas.delete("all")
        self.rendered_clusters = []  # Keep track of clickable clusters for interaction

        # 1. Calculate Dynamic Scale based on furthest event
        future_days = [ev["days_left"] for ev in self.events if ev["days_left"] > 0]
        max_days = max(future_days) if future_days else 30
        
        available_width = self.canvas_width - self.origin_x - 40
        px_per_day = max(available_width / max_days, 2)

        # Draw timeline axis line
        line_end_x = self.origin_x + (max_days * px_per_day) + 30
        self.canvas.create_line(
            self.origin_x, self.timeline_y, max(line_end_x, 850), self.timeline_y, 
            fill="#7f8c8d", width=3, arrow=tk.LAST
        )

        # Draw Sparrow / Today Marker
        today_str = date.today().strftime("%b %d, %Y")
        self.canvas.create_text(
            self.origin_x, self.timeline_y - 35, 
            text="🐦 Today", font=("Arial", 14, "bold"), fill="#2c3e50"
        )
        self.canvas.create_text(
            self.origin_x, self.timeline_y - 15, 
            text=today_str, font=("Arial", 9, "italic"), fill="#7f8c8d"
        )
        self.canvas.create_line(
            self.origin_x, self.timeline_y - 8, 
            self.origin_x, self.timeline_y + 8, 
            fill="#e74c3c", width=2
        )

        # 2. Render Clusters
        clusters = self.cluster_events()
        for cluster in clusters:
            # Position cluster at the average or first event's day count
            avg_days = sum(ev["days_left"] for ev in cluster) / len(cluster)
            x_pos = self.origin_x + (avg_days * px_per_day)
            r = 12

            if len(cluster) == 1:
                # Single event display
                ev = cluster[0]
                self.canvas.create_oval(
                    x_pos - r, self.timeline_y - r, 
                    x_pos + r, self.timeline_y + r, 
                    fill=ev["color"], outline="#ffffff", width=2, tags=("cluster", str(id(cluster)))
                )
                self.canvas.create_text(
                    x_pos, self.timeline_y + 25, 
                    text=ev["title"], font=("Arial", 9, "bold"), fill="#34495e"
                )
                days_text = f"{ev['days_left']}d left" if ev['days_left'] >= 0 else f"{abs(ev['days_left'])}d ago"
                self.canvas.create_text(
                    x_pos, self.timeline_y + 40, 
                    text=days_text, font=("Arial", 8), fill="#7f8c8d"
                )
            else:
                # Multiple events grouped together (Cluster circle with count)
                self.canvas.create_oval(
                    x_pos - r, self.timeline_y - r, 
                    x_pos + r, self.timeline_y + r, 
                    fill="#e67e22", outline="#ffffff", width=2, tags=("cluster", str(id(cluster)))
                )
                # Display count inside the circle
                self.canvas.create_text(
                    x_pos, self.timeline_y, 
                    text=str(len(cluster)), font=("Arial", 9, "bold"), fill="#ffffff"
                )
                # Label below cluster
                self.canvas.create_text(
                    x_pos, self.timeline_y + 25, 
                    text=f"{len(cluster)} events", font=("Arial", 9, "bold"), fill="#d35400"
                )
                days_text = f"Around {int(avg_days)}d left"
                self.canvas.create_text(
                    x_pos, self.timeline_y + 40, 
                    text=days_text, font=("Arial", 8), fill="#7f8c8d"
                )

            # Store mapping so click detection knows which cluster was clicked
            self.rendered_clusters.append({
                "bbox": (x_pos - r, self.timeline_y - r, x_pos + r, self.timeline_y + r),
                "cluster": cluster
            })

    def on_canvas_click(self, event):
        """Checks if a cluster circle was clicked and opens an info window."""
        for item in self.rendered_clusters:
            x1, y1, x2, y2 = item["bbox"]
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                cluster = item["cluster"]
                
                # Build a detailed message showing all events in this cluster
                details = f"Events in this timeframe ({len(cluster)} total):\n\n"
                for ev in cluster:
                    details += f"• {ev['title']} — Date: {ev['date_str']} ({ev['days_left']} days left)\n"
                
                messagebox.showinfo("Cluster Details", details)
                break

if __name__ == "__main__":
    root = tk.Tk()
    app = SparrowTimelineApp(root)
    root.mainloop()
