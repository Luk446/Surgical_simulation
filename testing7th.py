import tkinter
import customtkinter
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

MESENTERY_PIN = 26
PROXIMAL_CLIP_PIN = 27
PROXIMAL_CLIP2_PIN = 25
DISTAL_CLIP_PIN = 17
DISTAL_CLIP2_PIN = 4
CUT_SENSOR_PIN = 5
CUT_SENSOR2_PIN = 22
GALL_BLADDER_PIN = 6

# 4, 17, 27, 5, 6, 22, 26, 25

GPIO.setup(MESENTERY_PIN, GPIO.IN)
GPIO.setup(PROXIMAL_CLIP_PIN, GPIO.IN)
GPIO.setup(PROXIMAL_CLIP2_PIN, GPIO.IN)
GPIO.setup(DISTAL_CLIP_PIN, GPIO.IN)
GPIO.setup(DISTAL_CLIP2_PIN, GPIO.IN)
GPIO.setup(CUT_SENSOR_PIN, GPIO.IN)
GPIO.setup(CUT_SENSOR2_PIN, GPIO.IN)
GPIO.setup(GALL_BLADDER_PIN, GPIO.IN)

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")


class LaparoscopicSimulator(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Laparoscopic Tool Simulator")
        self.geometry(f"{1100}x{580}")

        # Initialize variables
        self.current_step = -1  # Start from -1 to show home screen initially
        self.timer_started = None  # Variable to store the time when the timer started

        # Create home screen
        self.show_home_screen()

    def clear_widgets(self):
        # clear existing widgets
        for widget in self.winfo_children():
            widget.destroy()

    def show_home_screen(self):
        self.clear_widgets()

        # Reset current_step to -1 when returning to the home screen
        self.current_step = -1

        # Configure grid layout (2x2)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # create home screen frame
        home_screen_frame = customtkinter.CTkFrame(self)
        home_screen_frame.grid(row=0, column=0, rowspan=2, columnspan=2, sticky="nsew")
        home_screen_frame.grid_columnconfigure(0, weight=1)
        home_screen_frame.grid_rowconfigure(1, weight=1)

        # add introduction label
        introduction_label = customtkinter.CTkLabel(home_screen_frame, text="Laparoscopic Tool Simulator",
                                                     font=customtkinter.CTkFont(size=30, weight="bold"))
        introduction_label.grid(row=0, column=0, pady=(50, 20), sticky="nsew")

        designer_label = customtkinter.CTkLabel(home_screen_frame,
                                                text="Designed by Luke, Ivan, Orlaith, Elena and Douglas",
                                                font=customtkinter.CTkFont(size=20, weight="bold"))
        designer_label.grid(row=1, column=0, pady=(10, 20), sticky="nsew")

        # add start simulation button
        start_button = customtkinter.CTkButton(home_screen_frame, text="Start Simulation", command=self.next_step)
        start_button.grid(row=2, column=0, pady=20, sticky="nsew")

        # Reset button at the center
        reset_button = customtkinter.CTkButton(self, text="Reset Simulation", command=self.show_home_screen)
        reset_button.grid(row=3, column=0, pady=20, sticky="nsew", columnspan=2)  # Centered with columnspan

    def next_step(self):
        self.clear_widgets()

        # configure grid layout (4x4)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Increment current_step
        self.current_step += 1

        # Centered frame for step text
        step_frame = customtkinter.CTkFrame(self)
        step_frame.grid(row=0, column=0, pady=(50, 0), sticky="nsew")
        step_frame.grid_columnconfigure(0, weight=1)

        # LDR to represent mesentery status
        if self.current_step == 0:
            self.mesentery_ldr_label = customtkinter.CTkLabel(step_frame, text="Mesentery Status: Not Covered",
                                                               font=customtkinter.CTkFont(size=18, weight="bold"))
            self.mesentery_ldr_label.grid(row=0, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # Clips on proximal and distal ends
        elif self.current_step == 1:
            self.proximal_clip_label = customtkinter.CTkLabel(step_frame, text="Proximal Clip 1: Not Applied",
                                                               font=customtkinter.CTkFont(size=18, weight="bold"))
            self.proximal_clip_label.grid(row=0, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")

            self.proximal_clip2_label = customtkinter.CTkLabel(step_frame, text="Proximal Clip 2: Not Applied",
                                                                font=customtkinter.CTkFont(size=18, weight="bold"))
            self.proximal_clip2_label.grid(row=1, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")

            # Distal clips
            self.distal_clip_label = customtkinter.CTkLabel(step_frame, text="Distal Clip 1: Not Applied",
                                                               font=customtkinter.CTkFont(size=18, weight="bold"))
            self.distal_clip_label.grid(row=2, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")

            self.distal_clip2_label = customtkinter.CTkLabel(step_frame, text="Distal Clip 2: Not Applied",
                                                                font=customtkinter.CTkFont(size=18, weight="bold"))
            self.distal_clip2_label.grid(row=3, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # Cuts Between the Clips
        elif self.current_step == 2:
            self.cut_label = customtkinter.CTkLabel(step_frame, text="Cut location 1: Not Done",
                                                    font=customtkinter.CTkFont(size=18, weight="bold"))
            self.cut_label.grid(row=0, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")

            self.cut_label2 = customtkinter.CTkLabel(step_frame, text="Cut location 2: Not Done",
                                                     font=customtkinter.CTkFont(size=18, weight="bold"))
            self.cut_label2.grid(row=1, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # LDR under the gall bladder
        elif self.current_step == 3:
            self.gall_bladder_ldr_label = customtkinter.CTkLabel(step_frame, text="Gall Bladder Status: Not Removed",
                                                                 font=customtkinter.CTkFont(size=18, weight="bold"))
            self.gall_bladder_ldr_label.grid(row=0, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # End screen if everything is completed well
        elif self.current_step == 4:
            self.end_screen()
            return

        # Reset button always at the center
        reset_button = customtkinter.CTkButton(self, text="Reset Simulation", command=self.show_home_screen)
        reset_button.grid(row=3, column=0, pady=20, sticky="nsew", columnspan=2)  # Centered with columnspan

        # Next Step button spanning across the screen
        next_step_button = customtkinter.CTkButton(self, text="Next Step", command=self.next_step)
        next_step_button.grid(row=4, column=0, pady=20, sticky="nsew", columnspan=2)  # Spanning across the screen

        # Simulate changes for the current step
        self.simulate_step()

    def simulate_step(self):
        if self.current_step == 0:  # Simulate changes for the mesentery step
            mesentery_ldr_value = not GPIO.input(MESENTERY_PIN)  

            if self.mesentery_ldr_label.cget("text") == "Mesentery Status: Not Covered":
                self.mesentery_ldr_label.configure(
                    text=f"Mesentery Status: {'Covered' if mesentery_ldr_value else 'Not Covered'}")
            
            if self.mesentery_ldr_label.cget("text") == "Mesentery Status: Covered" and self.timer_started is None:
                self.timer_started = time.time()
                
                self.after(4000, self.next_step)

        elif self.current_step == 1:  # Simulate changes for the clip step
            self.timer_started = None
            proximal_clip_value = GPIO.input(PROXIMAL_CLIP_PIN)
            proximal_clip2_value = GPIO.input(PROXIMAL_CLIP2_PIN)
            distal_clip_value = GPIO.input(DISTAL_CLIP_PIN)
            distal_clip2_value = GPIO.input(DISTAL_CLIP2_PIN)

            if self.proximal_clip_label.cget("text") == "Proximal Clip 1: Not Applied":
                self.proximal_clip_label.configure(
                    text=f"Proximal Clip 1: {'Applied' if proximal_clip_value else 'Not Applied'}")

            if self.proximal_clip2_label.cget("text") == "Proximal Clip 2: Not Applied":
                self.proximal_clip2_label.configure(
                    text=f"Proximal Clip 2: {'Applied' if proximal_clip2_value else 'Not Applied'}")

            if self.distal_clip_label.cget("text") == "Distal Clip 1: Not Applied":
                self.distal_clip_label.configure(
                    text=f"Distal Clip 1: {'Applied' if distal_clip_value else 'Not Applied'}")

            if self.distal_clip2_label.cget("text") == "Distal Clip 2: Not Applied":
                self.distal_clip2_label.configure(
                    text=f"Distal Clip 2: {'Applied' if distal_clip2_value else 'Not Applied'}")

            if self.proximal_clip_label.cget("text") == "Proximal Clip 1: Applied" and \
                    self.proximal_clip2_label.cget("text") == "Proximal Clip 2: Applied" and \
                    self.distal_clip_label.cget("text") == "Distal Clip 1: Applied" and \
                    self.distal_clip2_label.cget("text") == "Distal Clip 2: Applied" and self.timer_started is None:
                self.timer_started = time.time()
                # Update the timer label or handle the timer logic appropriately
                self.after(4000, self.next_step)
                
        elif self.current_step == 2:  # Simulate changes for the cut step
            self.timer_started = None
            cut_value = GPIO.input(CUT_SENSOR_PIN)  
            cut2_value = GPIO.input(CUT_SENSOR2_PIN)  

            # Update text only if it is still in the initial state
            if self.cut_label.cget("text") == "Cut location 1: Not Done":
                self.cut_label.configure(
                    text=f"Cut location 1: {'Done' if cut_value else 'Not Done'}")

            # Update text only if it is still in the initial state
            if self.cut_label2.cget("text") == "Cut location 2: Not Done":
                self.cut_label2.configure(
                    text=f"Cut location 2: {'Done' if cut2_value else 'Not Done'}")

            # Start the timer when both cut labels are updated for the first time
            if self.cut_label.cget("text") == "Cut location 1: Done" and \
                    self.cut_label2.cget("text") == "Cut location 2: Done" and self.timer_started is None:
                self.timer_started = time.time()

                # Wait for 4 seconds before progressing to the next step
                self.after(4000, self.next_step)

        elif self.current_step == 3:  # Simulate changes for the gall bladder step
            self.timer_started = None
                
            gall_bladder_value = not GPIO.input(GALL_BLADDER_PIN) 
            self.gall_bladder_ldr_label.configure(
                text=f"Gall Bladder Status: {'Removed' if gall_bladder_value else 'Not Removed'}")

            # Repeat the simulation after 1000 milliseconds
        if self.current_step >= 0 and self.current_step < 4:  # Continue simulation only after starting the steps
            self.after(1000, self.simulate_step)

    def end_screen(self):
        self.clear_widgets()

        # Display end screen content
        end_label = customtkinter.CTkLabel(self, text="Surgery Completed Successfully",
                                           font=customtkinter.CTkFont(size=20, weight="bold"))
        end_label.grid(row=0, column=0, pady=(50, 20))

        # Reset button at the center
        reset_button = customtkinter.CTkButton(self, text="Reset Simulation", command=self.show_home_screen)
        reset_button.grid(row=3, column=0, pady=20, sticky="nsew", columnspan=2)  # Centered with columnspan


if __name__ == "__main__":
    app = LaparoscopicSimulator()
    app.mainloop()
