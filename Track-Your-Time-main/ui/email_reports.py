"""
Email Reports for Time Tracker
"""

import customtkinter as ctk
from tkinter import messagebox
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import json
import os
from datetime import datetime, timedelta
import csv
import tempfile

class EmailReports:
    """Email reporting functionality"""

    def __init__(self, parent, tracker):
        self.parent = parent
        self.tracker = tracker
        self.config_file = "email_config.json"
        self.config = self.load_config()

    def load_config(self):
        """Load email configuration"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                return self.get_default_config()
        return self.get_default_config()

    def get_default_config(self):
        """Get default email config"""
        return {
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "sender_email": "",
            "sender_password": "",
            "recipient_email": "",
            "auto_send": False,
            "send_frequency": "weekly",  # daily, weekly, monthly
            "last_sent": None
        }

    def save_config(self):
        """Save email configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)

    def create_email_settings(self, frame):
        """Create email settings UI"""
        # Clear frame
        for widget in frame.winfo_children():
            widget.destroy()

        # Header
        header = ctk.CTkLabel(
            frame,
            text="📧 Email Reports",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        header.pack(pady=20)

        # Scrollable settings
        scroll_frame = ctk.CTkScrollableFrame(frame)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # SMTP Settings
        smtp_frame = ctk.CTkFrame(scroll_frame)
        smtp_frame.pack(fill="x", pady=10, padx=10)

        ctk.CTkLabel(
            smtp_frame,
            text="SMTP Settings",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(anchor="w", padx=10, pady=(10, 5))

        # SMTP Server
        server_frame = ctk.CTkFrame(smtp_frame, fg_color="transparent")
        server_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(server_frame, text="SMTP Server:", width=150, anchor="w").pack(side="left", padx=5)
        self.smtp_server_entry = ctk.CTkEntry(server_frame, placeholder_text="smtp.gmail.com", width=300)
        self.smtp_server_entry.pack(side="left", padx=5)
        self.smtp_server_entry.insert(0, self.config["smtp_server"])

        # SMTP Port
        port_frame = ctk.CTkFrame(smtp_frame, fg_color="transparent")
        port_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(port_frame, text="SMTP Port:", width=150, anchor="w").pack(side="left", padx=5)
        self.smtp_port_entry = ctk.CTkEntry(port_frame, placeholder_text="587", width=100)
        self.smtp_port_entry.pack(side="left", padx=5)
        self.smtp_port_entry.insert(0, str(self.config["smtp_port"]))

        # Email Settings
        email_frame = ctk.CTkFrame(scroll_frame)
        email_frame.pack(fill="x", pady=10, padx=10)

        ctk.CTkLabel(
            email_frame,
            text="Email Credentials",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(anchor="w", padx=10, pady=(10, 5))

        # Sender Email
        sender_frame = ctk.CTkFrame(email_frame, fg_color="transparent")
        sender_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(sender_frame, text="Your Email:", width=150, anchor="w").pack(side="left", padx=5)
        self.sender_email_entry = ctk.CTkEntry(sender_frame, placeholder_text="your.email@gmail.com", width=300)
        self.sender_email_entry.pack(side="left", padx=5)
        self.sender_email_entry.insert(0, self.config["sender_email"])

        # Password
        pass_frame = ctk.CTkFrame(email_frame, fg_color="transparent")
        pass_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(pass_frame, text="App Password:", width=150, anchor="w").pack(side="left", padx=5)
        self.password_entry = ctk.CTkEntry(pass_frame, placeholder_text="App password", width=300, show="*")
        self.password_entry.pack(side="left", padx=5)
        if self.config["sender_password"]:
            self.password_entry.insert(0, self.config["sender_password"])

        # Info about app passwords
        ctk.CTkLabel(
            email_frame,
            text="⚠️ For Gmail, use an App Password (not your regular password)\nGenerate at: myaccount.google.com/apppasswords",
            font=ctk.CTkFont(size=11),
            text_color="gray",
            justify="left"
        ).pack(anchor="w", padx=10, pady=5)

        # Recipient
        recipient_frame = ctk.CTkFrame(email_frame, fg_color="transparent")
        recipient_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(recipient_frame, text="Send To:", width=150, anchor="w").pack(side="left", padx=5)
        self.recipient_entry = ctk.CTkEntry(recipient_frame, placeholder_text="recipient@email.com", width=300)
        self.recipient_entry.pack(side="left", padx=5)
        self.recipient_entry.insert(0, self.config["recipient_email"])

        # Auto-send Settings
        auto_frame = ctk.CTkFrame(scroll_frame)
        auto_frame.pack(fill="x", pady=10, padx=10)

        ctk.CTkLabel(
            auto_frame,
            text="Automatic Reports",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(anchor="w", padx=10, pady=(10, 5))

        # Enable auto-send
        self.auto_send_var = ctk.BooleanVar(value=self.config["auto_send"])
        auto_check = ctk.CTkCheckBox(
            auto_frame,
            text="Enable automatic email reports",
            variable=self.auto_send_var,
            font=ctk.CTkFont(size=14)
        )
        auto_check.pack(anchor="w", padx=10, pady=5)

        # Frequency
        freq_frame = ctk.CTkFrame(auto_frame, fg_color="transparent")
        freq_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(freq_frame, text="Frequency:", width=150, anchor="w").pack(side="left", padx=5)
        self.frequency_var = ctk.StringVar(value=self.config["send_frequency"])
        freq_menu = ctk.CTkOptionMenu(
            freq_frame,
            values=["daily", "weekly", "monthly"],
            variable=self.frequency_var,
            width=200
        )
        freq_menu.pack(side="left", padx=5)

        # Buttons
        button_frame = ctk.CTkFrame(frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=20, padx=20)

        ctk.CTkButton(
            button_frame,
            text="💾 Save Settings",
            command=self.save_settings,
            height=45,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#4CAF50",
            hover_color="#45a049"
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            button_frame,
            text="📧 Send Test Email",
            command=self.send_test_email,
            height=45,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#2196F3",
            hover_color="#1976D2"
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            button_frame,
            text="📊 Send Report Now",
            command=self.send_report_now,
            height=45,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#FF9800",
            hover_color="#F57C00"
        ).pack(side="left", padx=5)

    def save_settings(self):
        """Save email settings"""
        self.config["smtp_server"] = self.smtp_server_entry.get()
        self.config["smtp_port"] = int(self.smtp_port_entry.get())
        self.config["sender_email"] = self.sender_email_entry.get()
        self.config["sender_password"] = self.password_entry.get()
        self.config["recipient_email"] = self.recipient_entry.get()
        self.config["auto_send"] = self.auto_send_var.get()
        self.config["send_frequency"] = self.frequency_var.get()

        self.save_config()
        messagebox.showinfo("Success", "Email settings saved successfully!")

    def send_test_email(self):
        """Send a test email"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.config["sender_email"]
            msg['To'] = self.config["recipient_email"]
            msg['Subject'] = "Time Tracker - Test Email"

            body = """
            <html>
            <body>
                <h2>Time Tracker Test Email</h2>
                <p>This is a test email from your Time Tracker application.</p>
                <p>If you received this, your email settings are configured correctly!</p>
                <br>
                <p><i>Sent at: {}</i></p>
            </body>
            </html>
            """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            msg.attach(MIMEText(body, 'html'))

            # Send
            server = smtplib.SMTP(self.config["smtp_server"], self.config["smtp_port"])
            server.starttls()
            server.login(self.config["sender_email"], self.config["sender_password"])
            server.send_message(msg)
            server.quit()

            messagebox.showinfo("Success", "Test email sent successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to send test email:\n{str(e)}")

    def send_report_now(self):
        """Send report immediately"""
        try:
            # Generate report
            report_html = self.generate_report_html()

            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.config["sender_email"]
            msg['To'] = self.config["recipient_email"]
            msg['Subject'] = f"Time Tracker Report - {datetime.now().strftime('%Y-%m-%d')}"

            msg.attach(MIMEText(report_html, 'html'))

            # Attach CSV
            csv_data = self.generate_csv_report()
            if csv_data:
                attachment = MIMEBase('application', 'octet-stream')
                attachment.set_payload(csv_data)
                encoders.encode_base64(attachment)
                attachment.add_header(
                    'Content-Disposition',
                    f'attachment; filename=time_report_{datetime.now().strftime("%Y%m%d")}.csv'
                )
                msg.attach(attachment)

            # Send
            server = smtplib.SMTP(self.config["smtp_server"], self.config["smtp_port"])
            server.starttls()
            server.login(self.config["sender_email"], self.config["sender_password"])
            server.send_message(msg)
            server.quit()

            self.config["last_sent"] = datetime.now().isoformat()
            self.save_config()

            messagebox.showinfo("Success", "Report sent successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to send report:\n{str(e)}")

    def generate_report_html(self):
        """Generate HTML report"""
        today = datetime.now().strftime("%Y-%m-%d")
        today_data = self.tracker.data.get(today, {})

        # Calculate totals
        total_hours = sum(v for k, v in today_data.items()
                         if k not in ['date', 'session_duration', 'idle_time', 'projects'])

        # Build HTML
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #2196F3; }}
                table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
                th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
                th {{ background-color: #2196F3; color: white; }}
                tr:nth-child(even) {{ background-color: #f2f2f2; }}
                .footer {{ margin-top: 30px; color: gray; font-size: 12px; }}
            </style>
        </head>
        <body>
            <h1>⏱️ Time Tracker Report</h1>
            <p><strong>Date:</strong> {today}</p>
            <p><strong>Total Time:</strong> {total_hours:.2f} hours</p>

            <h2>Category Breakdown</h2>
            <table>
                <tr>
                    <th>Category</th>
                    <th>Hours</th>
                    <th>Percentage</th>
                </tr>
        """

        for category, hours in sorted(today_data.items(), key=lambda x: x[1], reverse=True):
            if category not in ['date', 'session_duration', 'idle_time', 'projects'] and hours > 0:
                percentage = (hours / total_hours * 100) if total_hours > 0 else 0
                html += f"""
                <tr>
                    <td>{category}</td>
                    <td>{hours:.2f}h</td>
                    <td>{percentage:.1f}%</td>
                </tr>
                """

        html += """
            </table>

            <div class="footer">
                <p>Generated by Time Tracker Pro</p>
            </div>
        </body>
        </html>
        """

        return html

    def generate_csv_report(self):
        """Generate CSV report data"""
        try:
            output = []
            output.append("Date,Category,Hours\n")

            # Get last 7 days
            for i in range(7):
                date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
                day_data = self.tracker.data.get(date, {})

                for category, hours in day_data.items():
                    if category not in ['date', 'session_duration', 'idle_time', 'projects'] and hours > 0:
                        output.append(f"{date},{category},{hours:.2f}\n")

            return "".join(output).encode()
        except:
            return None
