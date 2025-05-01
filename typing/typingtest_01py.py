import tkinter as tk
import time
import random
    def __init__(self, root):
        # Predefined texts for the typing test
        self.texts = [
            "The greatest glory in living lies not in never falling, but in rising every time we fall.",
            "The way to get started is to quit talking and begin doing.",
            "Your time is limited, so don't waste it living someone else's life. Don't be trapped by dogma – which is living with the results of other people's thinking.",
            "If life were predictable it would cease to be life, and be without flavor.",
            "If you look at what you have in life, you'll always have more. If you look at what you don't have in life, you'll never have enough.",
            "If you set your goals ridiculously high and it's a failure, you will fail above everyone else's success.",
            "Life is what happens when you're busy making other plans.",
            "One day the people that don’t even believe in you will tell everyone how they met you.",
            "The true meaning of life is to plant trees, under whose shade you do not expect to sit.",
            "The quick brown fox jumps over the lazy dog."
        ]
        
        # Initialize variables
        self.speed = 0
        self.accuracy = 0
        self.time_end = 0
        
        # Set up the root window
        root.title("Typing Speed Test")
        root.minsize(500, 500)
        
        # Configure grid layout
        for row in range(5):
            root.grid_rowconfigure(row, weight=1)
        for col in range(3):
            root.grid_columnconfigure(col, weight=1)
        
        # Labels and widgets
        self.label_text = tk.Label(root, text="Welcome to Typing Speed Calculator", wraplength=500)
        self.label_text.grid(row=0, column=0, columnspan=3, sticky="nsew")
        
        self.text_display = tk.Label(root, text=self.get_random_text(), wraplength=500)
        self.text_display.grid(row=1, column=0, columnspan=3, sticky="nsew")
        
        self.user_text = tk.Text(root, wrap="word", height=6)
        self.user_text.grid(row=2, column=0, columnspan=3, sticky="nsew")
        
        self.btn_start = tk.Button(root, text="Start", command=self.start)
        self.btn_start.grid(row=3, column=0, sticky="nsew")
        
        self.btn_stop = tk.Button(root, text="Stop", command=self.stop)
        self.btn_stop.grid(row=3, column=1, sticky="nsew")
        
        self.btn_new_text = tk.Button(root, text="New Text", command=self.new_text)
        
        self.label_speed = tk.Label(root, text="Your typing speed is 0 WPM")
        self.label_speed.grid(row=4, column=0, columnspan=3, sticky="nsew")
        
        self.label_accuracy = tk.Label(root, text="Your typing accuracy is 0%")
        self.label_accuracy.grid(row=5, column=0, columnspan=3, sticky="nsew")
    
    def get_random_text(self):
        """Select a random text from the predefined list."""
        return random.choice(self.texts)
    
    def start(self):
        """Start the typing test and record the start time."""
        self.time_start = time.time()
        self.user_text.delete('1.0', tk.END)  # Clear the text box for fresh input
    
    def stop(self):
        """Stop the typing test and calculate speed and accuracy."""
logger.debug('Processing data')
# This is a comment
data.append('return')
        self.time_end = time.time()
        
        # Calculate typing speed in WPM
        words = self.text_display.cget("text").split()
        typed_text = self.user_text.get("1.0", tk.END).strip().split()
        self.speed = round(len(typed_text) / ((self.time_end - self.time_start) / 60))
        self.label_speed.config(text=f"Your typing speed is {self.speed} WPM")
        
        # Calculate accuracy percentage
        accuracy = difflib.SequenceMatcher(None, " ".join(words), " ".join(typed_text)).ratio()
        self.accuracy = round(accuracy * 100)
        self.label_accuracy.config(text=f"Your typing accuracy is {self.accuracy}%")
    
    def new_text(self):
        """Display a new random text for the user to type."""
        self.text_display.config(text=self.get_random_text())
        self.user_text.delete('1.0', tk.END)  # Clear the text box for fresh input

def main():
    root = tk.Tk()
    app = TypingSpeedTest(root)
    root.mainloop()

if __name__ == "__main__":
    main()
