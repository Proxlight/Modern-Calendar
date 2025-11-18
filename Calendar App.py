import customtkinter as ctk
from datetime import datetime, timedelta
import calendar

class ModernCalendarApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Window setup
        self.title("Modern Calendar")
        self.geometry("900x700")
        
        # Color scheme - Modern gradient theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Modern color palette
        self.bg_primary = "#0f0f23"
        self.bg_secondary = "#1a1a2e"
        self.accent_purple = "#6d28d9"
        self.accent_pink = "#ec4899"
        self.accent_blue = "#3b82f6"
        self.text_primary = "#ffffff"
        self.text_secondary = "#9ca3af"
        self.card_bg = "#16213e"
        self.hover_color = "#7c3aed"
        
        # Current date
        self.current_date = datetime.now()
        self.selected_date = None
        self.events = {}  # Store events {date_string: [events]}
        
        # Create UI
        self.create_header()
        self.create_calendar_grid()
        self.create_event_panel()
        
        # Display current month
        self.display_month()
        
    def create_header(self):
        """Create the header with navigation and month/year display"""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(pady=20, padx=20, fill="x")
        
        # Previous month button
        self.prev_btn = ctk.CTkButton(
            header_frame,
            text="◀",
            width=50,
            font=("Arial", 20, "bold"),
            command=self.previous_month,
            fg_color=self.accent_purple,
            hover_color=self.hover_color,
            corner_radius=12
        )
        self.prev_btn.pack(side="left", padx=10)
        
        # Month and year label
        self.month_year_label = ctk.CTkLabel(
            header_frame,
            text="",
            font=("Arial", 28, "bold")
        )
        self.month_year_label.pack(side="left", expand=True)
        
        # Today button
        self.today_btn = ctk.CTkButton(
            header_frame,
            text="Today",
            width=100,
            font=("Arial", 14, "bold"),
            command=self.go_to_today,
            fg_color=self.accent_pink,
            hover_color="#db2777",
            corner_radius=12
        )
        self.today_btn.pack(side="left", padx=10)
        
        # Next month button
        self.next_btn = ctk.CTkButton(
            header_frame,
            text="▶",
            width=50,
            font=("Arial", 20, "bold"),
            command=self.next_month,
            fg_color=self.accent_purple,
            hover_color=self.hover_color,
            corner_radius=12
        )
        self.next_btn.pack(side="left", padx=10)
        
    def create_calendar_grid(self):
        """Create the calendar grid"""
        self.calendar_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.calendar_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Day labels (Sun, Mon, Tue, etc.)
        days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        for col, day in enumerate(days):
            day_label = ctk.CTkLabel(
                self.calendar_frame,
                text=day,
                font=("Arial", 14, "bold"),
                text_color=self.accent_pink
            )
            day_label.grid(row=0, column=col, padx=5, pady=5, sticky="nsew")
        
        # Create grid for dates (6 rows x 7 columns)
        self.date_buttons = []
        for row in range(1, 7):
            week_buttons = []
            for col in range(7):
                btn = ctk.CTkButton(
                    self.calendar_frame,
                    text="",
                    width=100,
                    height=80,
                    font=("Arial", 16),
                    fg_color=self.card_bg,
                    hover_color=self.hover_color,
                    corner_radius=12
                )
                btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
                week_buttons.append(btn)
            self.date_buttons.append(week_buttons)
        
        # Configure grid weights for responsiveness
        for i in range(7):
            self.calendar_frame.grid_columnconfigure(i, weight=1)
        for i in range(7):
            self.calendar_frame.grid_rowconfigure(i, weight=1)
            
    def create_event_panel(self):
        """Create the event panel on the right side"""
        event_frame = ctk.CTkFrame(self, corner_radius=15)
        event_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Title
        title_label = ctk.CTkLabel(
            event_frame,
            text="Events",
            font=("Arial", 20, "bold")
        )
        title_label.pack(pady=15)
        
        # Selected date label
        self.selected_date_label = ctk.CTkLabel(
            event_frame,
            text="Select a date",
            font=("Arial", 14)
        )
        self.selected_date_label.pack(pady=5)
        
        # Event entry
        self.event_entry = ctk.CTkEntry(
            event_frame,
            placeholder_text="Add new event...",
            font=("Arial", 14),
            height=40
        )
        self.event_entry.pack(pady=10, padx=20, fill="x")
        
        # Add event button
        self.add_event_btn = ctk.CTkButton(
            event_frame,
            text="Add Event",
            font=("Arial", 14, "bold"),
            command=self.add_event,
            fg_color=self.accent_purple,
            hover_color=self.hover_color,
            height=40,
            corner_radius=12
        )
        self.add_event_btn.pack(pady=5, padx=20, fill="x")
        
        # Events list
        self.events_textbox = ctk.CTkTextbox(
            event_frame,
            font=("Arial", 13),
            wrap="word"
        )
        self.events_textbox.pack(pady=10, padx=20, fill="both", expand=True)
        
    def display_month(self):
        """Display the current month's calendar"""
        # Update month/year label
        month_name = self.current_date.strftime("%B %Y")
        self.month_year_label.configure(text=month_name)
        
        # Get calendar data
        year = self.current_date.year
        month = self.current_date.month
        cal = calendar.monthcalendar(year, month)
        
        # Get today's date
        today = datetime.now()
        
        # Fill in the dates
        for week_idx, week in enumerate(cal):
            for day_idx, day in enumerate(week):
                btn = self.date_buttons[week_idx][day_idx]
                if day == 0:
                    btn.configure(
                        text="",
                        state="disabled",
                        fg_color=self.bg_secondary
                    )
                else:
                    date_obj = datetime(year, month, day)
                    date_str = date_obj.strftime("%Y-%m-%d")
                    
                    # Check if this date has events
                    has_events = date_str in self.events and len(self.events[date_str]) > 0
                    
                    # Determine button color
                    if (day == today.day and month == today.month and year == today.year):
                        fg_color = self.accent_blue  # Today
                    elif has_events:
                        fg_color = "#10b981"  # Has events (emerald green)
                    else:
                        fg_color = self.card_bg  # Regular day
                    
                    btn.configure(
                        text=str(day),
                        state="normal",
                        fg_color=fg_color,
                        command=lambda d=date_obj: self.select_date(d)
                    )
                    
    def select_date(self, date):
        """Handle date selection"""
        self.selected_date = date
        date_str = date.strftime("%B %d, %Y")
        self.selected_date_label.configure(text=date_str)
        self.display_events()
        
    def add_event(self):
        """Add an event to the selected date"""
        if not self.selected_date:
            return
            
        event_text = self.event_entry.get().strip()
        if not event_text:
            return
            
        date_key = self.selected_date.strftime("%Y-%m-%d")
        if date_key not in self.events:
            self.events[date_key] = []
        
        self.events[date_key].append(event_text)
        self.event_entry.delete(0, "end")
        self.display_events()
        self.display_month()  # Refresh to show event indicator
        
    def display_events(self):
        """Display events for the selected date"""
        self.events_textbox.delete("1.0", "end")
        
        if not self.selected_date:
            return
            
        date_key = self.selected_date.strftime("%Y-%m-%d")
        if date_key in self.events and self.events[date_key]:
            for idx, event in enumerate(self.events[date_key], 1):
                self.events_textbox.insert("end", f"• {event}\n\n")
        else:
            self.events_textbox.insert("end", "No events for this day.")
            
    def previous_month(self):
        """Navigate to previous month"""
        if self.current_date.month == 1:
            self.current_date = self.current_date.replace(year=self.current_date.year - 1, month=12)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month - 1)
        self.display_month()
        
    def next_month(self):
        """Navigate to next month"""
        if self.current_date.month == 12:
            self.current_date = self.current_date.replace(year=self.current_date.year + 1, month=1)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month + 1)
        self.display_month()
        
    def go_to_today(self):
        """Go back to current month"""
        self.current_date = datetime.now()
        self.display_month()

if __name__ == "__main__":
    app = ModernCalendarApp()
    app.mainloop()