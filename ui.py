import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class TravelPlannerUI:
    def __init__(self, root, planner):
        self.root = root
        self.planner = planner
        self.setup_window()
        self.create_ui()

    def setup_window(self):
        # Configure the main window
        self.root.title("✈️ Smart Travel Planner")
        self.root.geometry("1100x700")
        self.root.configure(bg='#f5f5f5')

        # Set modern theme
        style = ttk.Style()
        style.theme_use('clam')

    def create_ui(self):
        # Create the top header
        header = tk.Frame(self.root, bg='#2c3e50', height=60)
        header.pack(fill='x')
        tk.Label(header, text="✈️ Smart Travel Planner", font=('Helvetica', 24, 'bold'),
                 bg='#2c3e50', fg='white').pack(pady=15)

        # Create main content section
        main = tk.Frame(self.root, bg='#ecf0f1')
        main.pack(fill='both', expand=True, padx=20, pady=20)

        # Input and results panels
        self.create_input_panel(main)
        self.create_results_panel(main)

    def create_input_panel(self, parent):
        # Input section with destination, trip type, duration and buttons
        panel = tk.Frame(parent, bg='white', relief='solid', bd=1)
        panel.pack(side='left', fill='y', padx=(0, 20))

        inner = tk.Frame(panel, bg='white')
        inner.pack(padx=20, pady=20)

        # Destination selection dropdown
        tk.Label(inner, text="Destination", font=('Helvetica', 12, 'bold'), bg='white').pack(anchor='w')
        self.destination = ttk.Combobox(inner, width=25, font=('Helvetica', 11))
        self.destination['values'] = self.planner.cities_data.get_all_destinations()
        self.destination.set('Beirut, Lebanon')
        self.destination.pack(pady=(0, 15))

        # Trip type selection dropdown
        tk.Label(inner, text="Trip Type", font=('Helvetica', 12, 'bold'), bg='white').pack(anchor='w')
        self.trip_type = ttk.Combobox(inner, width=25, font=('Helvetica', 11))
        self.trip_type['values'] = ['Standard', 'Budget', 'Luxury', 'Business', 'Adventure', 'Beach']
        self.trip_type.set('Standard')
        self.trip_type.pack(pady=(0, 15))

        # Duration slider
        tk.Label(inner, text="Duration (days)", font=('Helvetica', 12, 'bold'), bg='white').pack(anchor='w')
        self.duration = tk.Scale(inner, from_=1, to=21, orient='horizontal', bg='white', length=200)
        self.duration.set(7)
        self.duration.pack(pady=(0, 20))

        # Generate trip and export buttons
        tk.Button(inner, text="Generate Trip Plan", command=self.generate_trip,
                  bg='#3498db', fg='white', font=('Helvetica', 12, 'bold')).pack(pady=10)

        tk.Button(inner, text="Export PDF", command=self.export_pdf,
                  bg='#27ae60', fg='white', font=('Helvetica', 12, 'bold')).pack()

    def create_results_panel(self, parent):
        # Tabs for different results sections
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(side='right', fill='both', expand=True)
        self.tabs = {}
        for name in ['Overview', 'Weather', 'Packing', 'Budget', 'Activities', 'Culture']:
            frame = tk.Frame(self.notebook, bg='white')
            self.tabs[name] = frame
            self.notebook.add(frame, text=name)

        # Initial message in overview tab
        tk.Label(self.tabs['Overview'], text="Select destination and click Generate!",
                 font=('Helvetica', 16), bg='white').pack(pady=50)

    def generate_trip(self):
        # Collect input values and generate trip
        destination = self.destination.get()
        trip_type = self.trip_type.get()
        duration = int(self.duration.get())

        # Fetch trip data from planner
        self.trip_data = self.planner.get_trip_data(destination, trip_type, duration)

        # Update UI with trip data
        self.update_overview()
        self.update_weather()
        self.update_packing()
        self.update_budget()
        self.update_activities()
        self.update_culture()

        messagebox.showinfo("Success", "Trip plan generated!")

    def update_overview(self):
        # Show trip summary in overview tab
        tab = self.tabs['Overview']
        for widget in tab.winfo_children():
            widget.destroy()

        tk.Label(tab, text=f"Your Trip to {self.trip_data['destination']}",
                 font=('Helvetica', 20, 'bold'), bg='white').pack(pady=20)

        stats_frame = tk.Frame(tab, bg='white')
        stats_frame.pack()
        stats = [
            ('Duration', f"{self.trip_data['duration']} days"),
            ('Trip Type', self.trip_data['trip_type']),
            ('Total Budget', f"${self.trip_data['budget']['total']}"),
            ('Daily Budget', f"${self.trip_data['budget']['daily']}/day")
        ]

        for label, value in stats:
            row = tk.Frame(stats_frame, bg='white')
            row.pack(fill='x', pady=5)
            tk.Label(row, text=f"{label}:", font=('Helvetica', 12), bg='white').pack(side='left')
            tk.Label(row, text=value, font=('Helvetica', 12, 'bold'), bg='white').pack(side='left')

    def update_weather(self):
        # Show 7-day weather forecast
        tab = self.tabs['Weather']
        for widget in tab.winfo_children():
            widget.destroy()

        tk.Label(tab, text="Weather Forecast", font=('Helvetica', 16, 'bold'), bg='white').pack(pady=20)
        weather_frame = tk.Frame(tab, bg='white')
        weather_frame.pack()

        for i, day in enumerate(self.trip_data['weather'][:7]):
            card = tk.Frame(weather_frame, bg='#ecf0f1', relief='solid', bd=1)
            card.grid(row=0, column=i, padx=5, pady=5, ipadx=10, ipady=10)

            date = datetime.strptime(day['date'], '%Y-%m-%d').strftime('%b %d')
            tk.Label(card, text=date, font=('Helvetica', 10, 'bold'), bg='#ecf0f1').pack()
            tk.Label(card, text=day['icon'], font=('Helvetica', 20), bg='#ecf0f1').pack()
            tk.Label(card, text=f"{day['temp']}°C", font=('Helvetica', 12), bg='#ecf0f1').pack()

    def update_packing(self):
        # Show smart packing list
        tab = self.tabs['Packing']
        for widget in tab.winfo_children():
            widget.destroy()

        tk.Label(tab, text="Packing List", font=('Helvetica', 16, 'bold'), bg='white').pack(pady=20)
        for category, items in self.trip_data['packing'].items():
            tk.Label(tab, text=category, font=('Helvetica', 14, 'bold'), bg='white', fg='#3498db').pack(anchor='w', padx=20)
            for item in items:
                tk.Checkbutton(tab, text=f"  {item}", font=('Helvetica', 11), bg='white', anchor='w').pack(anchor='w', padx=40)

    def update_budget(self):
        # Show budget breakdown by category
        tab = self.tabs['Budget']
        for widget in tab.winfo_children():
            widget.destroy()

        tk.Label(tab, text="Budget Breakdown", font=('Helvetica', 16, 'bold'), bg='white').pack(pady=20)

        total_frame = tk.Frame(tab, bg='#3498db', relief='solid', bd=2)
        total_frame.pack(pady=20)
        tk.Label(total_frame, text="Total Budget", font=('Helvetica', 14), bg='#3498db', fg='white').pack()
        tk.Label(total_frame, text=f"${self.trip_data['budget']['total']}", font=('Helvetica', 24, 'bold'), bg='#3498db', fg='white').pack()

        for category in ['accommodation', 'food', 'activities', 'transport']:
            row = tk.Frame(tab, bg='white')
            row.pack(fill='x', padx=40, pady=5)
            tk.Label(row, text=category.title(), font=('Helvetica', 12), bg='white').pack(side='left')
            tk.Label(row, text=f"${self.trip_data['budget'][category]}", font=('Helvetica', 12, 'bold'), bg='white').pack(side='right')

    def update_activities(self):
        # Show activity recommendations
        tab = self.tabs['Activities']
        for widget in tab.winfo_children():
            widget.destroy()

        tk.Label(tab, text="Recommended Activities", font=('Helvetica', 16, 'bold'), bg='white').pack(pady=20)
        for activity in self.trip_data['activities']:
            tk.Label(tab, text=f"• {activity}", font=('Helvetica', 12), bg='white').pack(anchor='w', padx=40, pady=3)

    def update_culture(self):
        # Show cultural tips
        tab = self.tabs['Culture']
        for widget in tab.winfo_children():
            widget.destroy()

        tk.Label(tab, text="Cultural Tips", font=('Helvetica', 16, 'bold'), bg='white').pack(pady=20)
        for tip in self.trip_data['culture']:
            tk.Label(tab, text=f"• {tip}", font=('Helvetica', 12), bg='white').pack(anchor='w', padx=40, pady=3)

    def export_pdf(self):
        # Export trip plan to PDF
        if not hasattr(self, 'trip_data'):
            messagebox.showwarning("No Data", "Generate a trip first!")
            return
        self.planner.pdf_exporter.export(self.trip_data)
        messagebox.showinfo("Success", "PDF exported!")
