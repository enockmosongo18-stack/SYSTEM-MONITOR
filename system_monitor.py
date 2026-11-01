import tkinter as tk
from tkinter import ttk
import psutil

class SystemMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("System Resource & Battery Monitor")
        self.root.geometry("420x480")
        self.root.config(bg="#1e1e1e")
        self.root.resizable(False, False)

        # Style Configuration
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TProgressbar", thickness=20, troughcolor="#2d2d2d", background="#00adb5")

        # Title Label
        title_label = tk.Label(root, text="SYSTEM TELEMETRY", font=("Consolas", 16, "bold"), fg="#00adb5", bg="#1e1e1e")
        title_label.pack(pady=15)

        # Metrics Container
        self.create_metric_widgets("CPU USAGE", "cpu_val", "cpu_bar")
        self.create_metric_widgets("MEMORY (RAM) USAGE", "ram_val", "ram_bar")
        self.create_metric_widgets("BATTERY STATUS", "batt_val", "batt_bar")

        # Status / Extra Info Box
        self.info_label = tk.Label(root, text="Initializing telemetry...", font=("Consolas", 10), fg="#aaaaaa", bg="#1e1e1e", justify="left")
        self.info_label.pack(pady=15, padx=20, anchor="w")

        # Start Update Loop
        self.update_stats()

    def create_metric_widgets(self, title, val_attr, bar_attr):
        frame = tk.Frame(self.root, bg="#1e1e1e")
        frame.pack(fill="x", padx=25, pady=8)

        lbl = tk.Label(frame, text=title, font=("Consolas", 10, "bold"), fg="#ffffff", bg="#1e1e1e")
        lbl.pack(anchor="w")

        sub_frame = tk.Frame(frame, bg="#1e1e1e")
        sub_frame.pack(fill="x", pady=2)

        bar = ttk.Progressbar(sub_frame, orient="horizontal", length=300, mode="determinate", style="TProgressbar")
        bar.pack(side="left", fill="x", expand=True)

        val_lbl = tk.Label(sub_frame, text="0%", font=("Consolas", 10, "bold"), fg="#00adb5", bg="#1e1e1e", width=6)
        val_lbl.pack(side="right", padx=(10, 0))

        setattr(self, val_attr, val_lbl)
        setattr(self, bar_attr, bar)

    def update_stats(self):
        # 1. CPU Usage
        cpu_percent = psutil.cpu_percent(interval=None)
        self.cpu_bar['value'] = cpu_percent
        self.cpu_val.config(text=f"{cpu_percent:.1f}%")

        # 2. RAM Usage
        memory = psutil.virtual_memory()
        ram_percent = memory.percent
        self.ram_bar['value'] = ram_percent
        ram_used_gb = memory.used / (1024**3)
        ram_total_gb = memory.total / (1024**3)
        self.ram_val.config(text=f"{ram_percent:.1f}%")

        # 3. Battery Status
        battery = psutil.sensors_battery()
        if battery:
            batt_percent = battery.percent
            plugged = battery.power_plugged
            self.batt_bar['value'] = batt_percent
            status_text = "Plugged In" if plugged else "On Battery"
            self.batt_val.config(text=f"{batt_percent}%")
            
            # Extra System Details
            info_text = f"RAM Active: {ram_used_gb:.2f} GB / {ram_total_gb:.2f} GB\nPower State: {status_text}"
        else:
            self.batt_bar['value'] = 100
            self.batt_val.config(text="N/A")
            info_text = f"RAM Active: {ram_used_gb:.2f} GB / {ram_total_gb:.2f} GB\nPower State: Desktop / No Battery Detected"

        self.info_label.config(text=info_text)

        # Refresh every 1000ms (1 second)
        self.root.after(1000, self.update_stats)

if __name__ == "__main__":
    root = tk.Tk()
    app = SystemMonitorApp(root)
    root.mainloop()
