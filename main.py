import task
import sys
import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

TASK_MANAGER_MAIN = task.TaskManager()

class SectionFrame(ctk.CTkFrame):
    def __init__(self, parent, section_name, task_manager, refresh_callback):
        super().__init__(parent)
        self.section_name = section_name
        self.task_manager = task_manager
        self.refresh_callback = refresh_callback
        self.is_expanded = False
        
        self.setup_ui()
    
    def setup_ui(self):
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.pack(fill="x", padx=5, pady=2)
        
        self.toggle_btn = ctk.CTkButton(
            self.header_frame, 
            text=f"▶ {self.section_name}", 
            command=self.toggle_section,
            fg_color="transparent",
            hover_color=("gray70", "gray30"),
            text_color=("gray10", "gray90"),
            anchor="w"
        )
        self.toggle_btn.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        
        self.delete_section_btn = ctk.CTkButton(
            self.header_frame,
            text="🗑️",
            width=30,
            command=self.delete_section,
            fg_color="#FF6B6B",
            hover_color="#FF5252"
        )
        self.delete_section_btn.pack(side="right", padx=5, pady=5)
        
        self.tasks_frame = ctk.CTkFrame(self)
        self.tasks_frame.pack(fill="x", padx=20, pady=2)
        
        self.task_widgets = []
        self.update_tasks_display()
    
    def toggle_section(self):
        self.is_expanded = not self.is_expanded
        if self.is_expanded:
            self.toggle_btn.configure(text=f"▼ {self.section_name}")
            self.tasks_frame.pack(fill="x", padx=20, pady=2)
        else:
            self.toggle_btn.configure(text=f"▶ {self.section_name}")
            self.tasks_frame.pack_forget()
    
    def update_tasks_display(self):
        for widget in self.task_widgets:
            widget.destroy()
        self.task_widgets.clear()
        
        if self.section_name in self.task_manager.data:
            for task_data in self.task_manager.data[self.section_name]:
                task_frame = ctk.CTkFrame(self.tasks_frame)
                task_frame.pack(fill="x", pady=2)
                
                task_label = ctk.CTkLabel(
                    task_frame,
                    text=f"• {task_data['name']} - {task_data['time']} min",
                    anchor="w"
                )
                task_label.pack(side="left", fill="x", expand=True, padx=5, pady=5)
                
                delete_task_btn = ctk.CTkButton(
                    task_frame,
                    text="🗑️",
                    width=25,
                    command=lambda t=task_data['name']: self.delete_task(t),
                    fg_color="#FF6B6B",
                    hover_color="#FF5252"
                )
                delete_task_btn.pack(side="right", padx=5, pady=5)
                
                self.task_widgets.append(task_frame)
    
    def delete_section(self):
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete section '{self.section_name}'?"):
            self.task_manager.Del_Section(self.section_name)
            self.refresh_callback()
    
    def delete_task(self, task_name):
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete task '{task_name}'?"):
            self.task_manager.Del_Task(self.section_name, task_name)
            self.update_tasks_display()
            self.refresh_callback()

class TaskManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        self.root.geometry("900x700")
        
        self.section_frames = []
        self.setup_ui()
        self.refresh_display()
    
    def setup_ui(self):
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        left_frame = ctk.CTkFrame(main_frame)
        left_frame.pack(side="left", fill="y", padx=(0, 10))
        
        right_frame = ctk.CTkScrollableFrame(main_frame)
        right_frame.pack(side="right", fill="both", expand=True)
        
        title_label = ctk.CTkLabel(left_frame, text="Task Manager", font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=(20, 20))
        
        theme_frame = ctk.CTkFrame(left_frame)
        theme_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        theme_label = ctk.CTkLabel(theme_frame, text="Theme:")
        theme_label.pack(side="left", padx=(10, 5))
        
        self.theme_switch = ctk.CTkSwitch(theme_frame, text="Dark Mode", command=self.toggle_theme)
        self.theme_switch.pack(side="left", padx=5)
        self.theme_switch.select()
        
        section_frame = ctk.CTkFrame(left_frame)
        section_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(section_frame, text="Add Section", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10, 5))
        
        self.section_entry = ctk.CTkEntry(section_frame, placeholder_text="Enter section name", width=250)
        self.section_entry.pack(pady=5)
        
        add_section_btn = ctk.CTkButton(section_frame, text="Add Section", command=self.add_section)
        add_section_btn.pack(pady=5, fill="x", padx=20)
        
        task_frame = ctk.CTkFrame(left_frame)
        task_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(task_frame, text="Add Task", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10, 5))
        
        self.task_section_entry = ctk.CTkEntry(task_frame, placeholder_text="Section name", width=250)
        self.task_section_entry.pack(pady=5)
        
        self.task_entry = ctk.CTkEntry(task_frame, placeholder_text="Task name", width=250)
        self.task_entry.pack(pady=5)
        
        self.time_entry = ctk.CTkEntry(task_frame, placeholder_text="Time in minutes", width=250)
        self.time_entry.pack(pady=5)
        
        add_task_btn = ctk.CTkButton(task_frame, text="Add Task", command=self.add_task)
        add_task_btn.pack(pady=5, fill="x", padx=20)
        
        calc_frame = ctk.CTkFrame(left_frame)
        calc_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(calc_frame, text="Time Calculations", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10, 5))
        
        calc_total_btn = ctk.CTkButton(calc_frame, text="Calculate Total Time", command=self.calc_total_time)
        calc_total_btn.pack(pady=5, fill="x", padx=20)
        
        total_time_label = ctk.CTkLabel(calc_frame, text="Total: 0 minutes", font=ctk.CTkFont(size=14))
        total_time_label.pack(pady=5)
        self.total_time_label = total_time_label
        
        exit_btn = ctk.CTkButton(
            left_frame, 
            text="🚪 Exit Application", 
            command=self.root.quit, 
            fg_color=("#E74C3C", "#C0392B"),
            hover_color=("#C0392B", "#A93226"),
            border_width=2,
            border_color=("#FF6B6B", "#E74C3C"),
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=8
        )
        exit_btn.pack(pady=(20, 20), fill="x", padx=20)
        
        ctk.CTkLabel(right_frame, text="Sections & Tasks", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(10, 5))
        
        self.sections_container = ctk.CTkFrame(right_frame)
        self.sections_container.pack(fill="both", expand=True, padx=10, pady=10)
    
    def toggle_theme(self):
        if self.theme_switch.get():
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")
    
    def add_section(self):
        name = self.section_entry.get().strip()
        if name:
            TASK_MANAGER_MAIN.Add_Section(name)
            self.section_entry.delete(0, "end")
            self.refresh_display()
            messagebox.showinfo("Success", f"Section '{name}' added successfully!")
        else:
            messagebox.showerror("Error", "Please enter a section name!")
    
    def add_task(self):
        section = self.task_section_entry.get().strip()
        task_name = self.task_entry.get().strip()
        time = self.time_entry.get().strip()
        
        if section and task_name and time:
            try:
                int(time)
                TASK_MANAGER_MAIN.Add_Task(section, task_name, time)
                self.task_section_entry.delete(0, "end")
                self.task_entry.delete(0, "end")
                self.time_entry.delete(0, "end")
                self.refresh_display()
                messagebox.showinfo("Success", f"Task '{task_name}' added successfully!")
            except ValueError:
                messagebox.showerror("Error", "Time must be a valid number!")
        else:
            messagebox.showerror("Error", "Please fill in all fields!")
    
    def calc_total_time(self):
        time = TASK_MANAGER_MAIN.Calc_Full_Time()
        self.total_time_label.configure(text=f"Total: {time} minutes")
        messagebox.showinfo("Total Time", f"All tasks will take {time} minutes to complete.")
    
    def refresh_display(self):
        for frame in self.section_frames:
            frame.destroy()
        self.section_frames.clear()
        
        if not TASK_MANAGER_MAIN.data:
            no_data_label = ctk.CTkLabel(self.sections_container, text="No sections or tasks available.\nAdd a section to get started!")
            no_data_label.pack(pady=20)
            self.section_frames.append(no_data_label)
        else:
            for section_name in TASK_MANAGER_MAIN.data:
                section_frame = SectionFrame(self.sections_container, section_name, TASK_MANAGER_MAIN, self.refresh_display)
                section_frame.pack(fill="x", pady=5)
                self.section_frames.append(section_frame)
        
        total_time = TASK_MANAGER_MAIN.Calc_Full_Time()
        self.total_time_label.configure(text=f"Total: {total_time} minutes")

def main():
    root = ctk.CTk()
    app = TaskManagerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()