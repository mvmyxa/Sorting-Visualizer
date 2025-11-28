import random # For generating random arrays
import tkinter as tk # Tkinter for GUI
from tkinter import ttk # Themed Tkinter widgets

BAR_COLOR = "#4A8792"
ACTIVE_COLOR = "#FF2E63"
SORTED_COLOR = "#20bf6b"
BG_COLOR = "#13161B"
BAR_WIDTH = 10
NUM_BARS = 60 
SPEED_MS = 10

class SortingVisualizer:
    """
    Sorting algorithm visualizer using Tkinter
    Uses Python generators for asynchronous UI updates without freezing.
    """
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Algorithm Efficiency Visualizer")
        self.root.configure(bg=BG_COLOR)

        #Statistics
        self.comparisons = 0
        
        #UI Elements
        self._setup_ui()
        
        #Data initialization
        self.data = []
        self.shuffle()

    def _setup_ui(self):
        """Initialize UI components"""
        #Main Canvas
        self.canvas = tk.Canvas(
            self.root, 
            width=BAR_WIDTH * NUM_BARS, 
            height=400, 
            bg=BG_COLOR, 
            highlightthickness=0
        )
        self.canvas.pack(padx=20, pady=20)

        #Controls Panel
        controls = tk.Frame(self.root, bg=BG_COLOR)
        controls.pack(pady=10)

        #Buttons (Styling)
        style = ttk.Style() 
        style.theme_use('clam') 

        ttk.Button(controls, text="New Array (Shuffle)", command=self.shuffle).grid(row=0, column=0, padx=5) #Shuffle button
        ttk.Button(controls, text="Bubble Sort", command=self.bubble_sort).grid(row=0, column=1, padx=5) #Bubble Sort button
        ttk.Button(controls, text="Insertion Sort", command=self.insertion_sort).grid(row=0, column=2, padx=5) #Insertion Sort button

        #Status Label (Counter)
        self.status_label = tk.Label( 
            self.root,  
            text="Comparisons: 0",      
            fg="white", 
            bg=BG_COLOR, 
            font=("Consolas", 12)
        )
        self.status_label.pack(pady=5)

    def shuffle(self):
        """Generate a new random array and reset statistics."""
        self.data = [random.randint(20, 380) for _ in range(NUM_BARS)] 
        random.shuffle(self.data)
        self.comparisons = 0
        self.update_status() 
        self.draw()

    def draw(self, active_indices=None):
        """Draw the current state of the array on the Canvas."""
        self.canvas.delete("all")
        active_indices = active_indices or set()
        
        for idx, val in enumerate(self.data):
            x0 = idx * BAR_WIDTH
            x1 = x0 + BAR_WIDTH - 2 #(-2) creates a small gap between bars
            y0 = 400 - val 
            y1 = 400 
            
            #Color logic
            color = BAR_COLOR
            if idx in active_indices:
                color = ACTIVE_COLOR
            
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")
        
        self.root.update_idletasks()

    def update_status(self):
        self.status_label.config(text=f"Comparisons: {self.comparisons}")

    #ALGORITHMS
    #Implement bubble sort and insertion sort as generators

    def bubble_sort(self):
        self.comparisons = 0
        self._run_sort(self._bubble_generator())

    def insertion_sort(self):
        self.comparisons = 0
        self._run_sort(self._insertion_generator())

    def _run_sort(self, generator):
        """
        Animation engine. Grabs the next step from the generator and schedules the
        following call to keep the GUI responsive.
        """
        def step():
            try:
                #Get the indices currently being compared/swapped
                active_indices = next(generator)
                self.draw(active_indices)
                self.update_status()
                #Schedule the next frame after SPEED_MS milliseconds
                self.root.after(SPEED_MS, step)
            except StopIteration:
                #Sorting completed
                self.draw()
        step()

    def _bubble_generator(self):
        n = len(self.data)
        for i in range(n):
            for j in range(0, n - i - 1):
                self.comparisons += 1
                yield {j, j + 1} #Highlight the elements being compared
                
                if self.data[j] > self.data[j + 1]:
                    self.data[j], self.data[j + 1] = self.data[j + 1], self.data[j]
        yield set()

    def _insertion_generator(self):
        for i in range(1, len(self.data)):
            key = self.data[i]
            j = i - 1
            while j >= 0 and self.data[j] > key:
                self.comparisons += 1
                yield {j, j + 1} #Highlight
                
                self.data[j + 1] = self.data[j]
                j -= 1
            self.data[j + 1] = key
            yield {j + 1}
        yield set()

if __name__ == "__main__":
    root = tk.Tk()
    SortingVisualizer(root)
    root.mainloop()