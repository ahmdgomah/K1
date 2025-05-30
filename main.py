import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from datetime import datetime
import os

kivy.require('2.0.0')

class PrayerReminderApp(App):
    def __init__(self):
        super().__init__()
        self.reminder_event = None
        self.interval_minutes = 30  # Default to 30 minutes (half hour)
        self.is_running = False
        
    def build(self):
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Title
        title = Label(
            text='صلوا على النبي\nPrayer Reminder for the Prophet ﷺ',
            font_size='24sp',
            size_hint_y=0.2,
            halign='center',
            text_size=(None, None)
        )
        
        # Interval selection
        interval_layout = BoxLayout(orientation='horizontal', size_hint_y=0.15, spacing=10)
        interval_label = Label(text='Reminder Interval:', size_hint_x=0.6)
        
        self.interval_spinner = Spinner(
            text='30 minutes',
            values=['15 minutes', '30 minutes'],
            size_hint_x=0.4
        )
        self.interval_spinner.bind(text=self.on_interval_change)
        
        interval_layout.add_widget(interval_label)
        interval_layout.add_widget(self.interval_spinner)
        
        # Status label
        self.status_label = Label(
            text='Status: Stopped',
            font_size='18sp',
            size_hint_y=0.1
        )
        
        # Next reminder time
        self.next_reminder_label = Label(
            text='Next reminder: Not scheduled',
            font_size='16sp',
            size_hint_y=0.1
        )
        
        # Control buttons
        buttons_layout = BoxLayout(orientation='horizontal', size_hint_y=0.2, spacing=10)
        
        self.start_button = Button(text='Start Reminders', font_size='18sp')
        self.start_button.bind(on_press=self.start_reminders)
        
        self.stop_button = Button(text='Stop Reminders', font_size='18sp', disabled=True)
        self.stop_button.bind(on_press=self.stop_reminders)
        
        buttons_layout.add_widget(self.start_button)
        buttons_layout.add_widget(self.stop_button)
        
        # Manual prayer button
        self.manual_button = Button(
            text='Send Prayer Now\nاللهم صل وسلم على نبينا محمد',
            font_size='16sp',
            size_hint_y=0.15
        )
        self.manual_button.bind(on_press=self.manual_prayer)
        
        # Add all widgets to main layout
        main_layout.add_widget(title)
        main_layout.add_widget(interval_layout)
        main_layout.add_widget(self.status_label)
        main_layout.add_widget(self.next_reminder_label)
        main_layout.add_widget(buttons_layout)
        main_layout.add_widget(self.manual_button)
        
        return main_layout
    
    def on_interval_change(self, spinner, text):
        """Handle interval selection change"""
        if text == '15 minutes':
            self.interval_minutes = 15
        else:  # 30 minutes
            self.interval_minutes = 30
        
        # If reminders are running, restart with new interval
        if self.is_running:
            self.stop_reminders(None)
            self.start_reminders(None)
    
    def start_reminders(self, instance):
        """Start the prayer reminders"""
        if not self.is_running:
            self.is_running = True
            interval_seconds = self.interval_minutes * 60
            
            # Schedule the reminder
            self.reminder_event = Clock.schedule_interval(
                self.show_prayer_reminder, 
                interval_seconds
            )
            
            # Update UI
            self.start_button.disabled = True
            self.stop_button.disabled = False
            self.status_label.text = f'Status: Running (every {self.interval_minutes} minutes)'
            self.update_next_reminder_time()
            
            # Show immediate confirmation
            self.show_start_confirmation()
    
    def stop_reminders(self, instance):
        """Stop the prayer reminders"""
        if self.is_running:
            self.is_running = False
            
            if self.reminder_event:
                self.reminder_event.cancel()
                self.reminder_event = None
            
            # Update UI
            self.start_button.disabled = False
            self.stop_button.disabled = True
            self.status_label.text = 'Status: Stopped'
            self.next_reminder_label.text = 'Next reminder: Not scheduled'
    
    def show_prayer_reminder(self, dt):
        """Show the prayer reminder popup"""
        self.update_next_reminder_time()
        
        # Create popup content
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        reminder_text = Label(
            text='وقت الصلاة على النبي\nTime to send prayers upon the Prophet ﷺ\n\nاللهم صل وسلم وبارك على نبينا محمد\nوعلى آله وصحبه أجمعين',
            font_size='18sp',
            halign='center',
            text_size=(400, None)
        )
        
        close_button = Button(text='جزاك الله خيراً', size_hint_y=0.3, font_size='16sp')
        
        content.add_widget(reminder_text)
        content.add_widget(close_button)
        
        # Create and show popup
        popup = Popup(
            title='Prayer Reminder - تذكير الصلاة على النبي',
            content=content,
            size_hint=(0.8, 0.6),
            auto_dismiss=False
        )
        
        close_button.bind(on_press=popup.dismiss)
        popup.open()
    
    def show_start_confirmation(self):
        """Show confirmation that reminders have started"""
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        confirmation_text = Label(
            text=f'Prayer reminders started!\nYou will be reminded every {self.interval_minutes} minutes\n\nبارك الله فيك',
            font_size='16sp',
            halign='center',
            text_size=(300, None)
        )
        
        ok_button = Button(text='OK', size_hint_y=0.3)
        
        content.add_widget(confirmation_text)
        content.add_widget(ok_button)
        
        popup = Popup(
            title='Reminders Started',
            content=content,
            size_hint=(0.7, 0.5),
            auto_dismiss=False
        )
        
        ok_button.bind(on_press=popup.dismiss)
        popup.open()
    
    def manual_prayer(self, instance):
        """Show manual prayer popup"""
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        prayer_text = Label(
            text='اللهم صل وسلم وبارك على نبينا محمد\nوعلى آله وصحبه أجمعين\n\nO Allah, send prayers and peace upon our Prophet Muhammad\nand upon his family and companions',
            font_size='16sp',
            halign='center',
            text_size=(400, None)
        )
        
        close_button = Button(text='آمين', size_hint_y=0.3, font_size='16sp')
        
        content.add_widget(prayer_text)
        content.add_widget(close_button)
        
        popup = Popup(
            title='Prayer upon the Prophet ﷺ',
            content=content,
            size_hint=(0.8, 0.6),
            auto_dismiss=False
        )
        
        close_button.bind(on_press=popup.dismiss)
        popup.open()
    
    def update_next_reminder_time(self):
        """Update the next reminder time display"""
        if self.is_running:
            from datetime import datetime, timedelta
            next_time = datetime.now() + timedelta(minutes=self.interval_minutes)
            self.next_reminder_label.text = f'Next reminder: {next_time.strftime("%H:%M:%S")}'

# Run the application
if __name__ == '__main__':
    PrayerReminderApp().run()
