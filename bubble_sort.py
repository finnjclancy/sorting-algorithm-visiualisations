# bubble_sort.py
import tkinter as tk
from tkinter import ttk

class BubbleSortTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        heading = tk.Label(self, text="Bubble Sort", font=("Arial", 24, "bold"), bg="#3a3a3a")
        heading.pack(pady=10)
        # List to store Entry widgets for array elements.
        self.entries = []
        # List to hold the current data being sorted.
        self.data = []
        # Default speed (delay in ms). Slow = 2000, Medium = 700, Fast = 100.
        self.current_delay = 1500
        # Pause flag.
        self.paused = False

        # --- Top Section: Number-of-Elements Input ---
        self.input_frame = ttk.Frame(self)
        self.input_frame.pack(pady=10)
        self.num_label = ttk.Label(self.input_frame, text="Enter number of elements:")
        self.num_label.grid(row=0, column=0, padx=5, pady=5)
        self.num_entry = ttk.Entry(self.input_frame, width=10)
        self.num_entry.grid(row=0, column=1, padx=5, pady=5)
        self.generate_button = ttk.Button(
            self.input_frame, text="Generate Input Fields", command=self.generate_input_fields)
        self.generate_button.grid(row=0, column=2, padx=5, pady=5)

        # --- Next Section: Enter Array Elements ---
        self.array_frame = ttk.Frame(self)
        self.array_frame.pack(pady=10)
        # (The array elements input fields and the Start button will be created here.)

        # --- Next Section: Speed Controls & Pause/Play ---
        self.speed_frame = ttk.Frame(self)
        self.speed_frame.pack(pady=10)
        # Speed Buttons:
        self.slow_button = ttk.Button(
            self.speed_frame, text="Slow", command=lambda: self.set_speed(2000))
        self.slow_button.grid(row=0, column=0, padx=5, pady=5)
        self.medium_button = ttk.Button(
            self.speed_frame, text="Medium", command=lambda: self.set_speed(700))
        self.medium_button.grid(row=0, column=1, padx=5, pady=5)
        self.fast_button = ttk.Button(
            self.speed_frame, text="Fast", command=lambda: self.set_speed(100))
        self.fast_button.grid(row=0, column=2, padx=5, pady=5)
        # Pause/Play Button:
        self.pause_play_button = ttk.Button(
            self.speed_frame, text="Pause", command=self.toggle_pause)
        self.pause_play_button.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

        # --- Bottom Section: Visualization Canvas ---
        # Increase the canvas size to 800x300.
        self.canvas = tk.Canvas(self, width=800, height=300, bg="white")
        self.canvas.pack(pady=10)

    def set_speed(self, delay):
        """Update the current delay speed."""
        self.current_delay = delay

    def toggle_pause(self):
        """
        Toggle between pause and play.
        When paused, the visualization stops; when resumed, it continues.
        """
        self.paused = not self.paused
        if self.paused:
            self.pause_play_button.config(text="Play")
        else:
            self.pause_play_button.config(text="Pause")
            self.visualize_step()

    def generate_input_fields(self):
        """
        Dynamically creates Entry widgets for array elements based on user input.
        """
        # Clear any existing inputs.
        for widget in self.array_frame.winfo_children():
            widget.destroy()
        self.entries = []

        try:
            num_elements = int(self.num_entry.get())
        except ValueError:
            return

        instruct_label = ttk.Label(self.array_frame, text="Enter array elements:")
        instruct_label.grid(row=0, column=0, columnspan=num_elements, pady=5)

        for i in range(num_elements):
            entry = ttk.Entry(self.array_frame, width=5)
            entry.grid(row=1, column=i, padx=5, pady=5)
            self.entries.append(entry)

        if hasattr(self, 'start_button') and self.start_button:
            self.start_button.destroy()

        self.start_button = ttk.Button(
            self.array_frame, text="Start Bubble Sort", command=self.start_sort)
        self.start_button.grid(row=2, column=0, columnspan=num_elements, pady=10)

    def start_sort(self):
        """
        Gathers numbers from input fields and starts the bubble sort visualization.
        """
        try:
            self.data = [int(entry.get()) for entry in self.entries]
        except ValueError:
            return

        self.canvas.delete("all")
        self.sort_generator = self.bubble_sort(self.data.copy())
        # Start the visualization using the current delay.
        self.after(self.current_delay, self.visualize_step)

    def bubble_sort(self, data):
        """
        Standard bubble sort generator (left-to-right):
          - Yields a step for every comparison (highlighting the pair in red).
          - If a swap occurs, yields an extra step (swap_flag True) showing the updated state.
          - At the end of each pass, yields a step marking the sorted portion (green on the right).

        Yields a tuple:
          (index1, index2, current state, sorted_indices, swap_flag)
        """
        n = len(data)
        for i in range(n):
            swapped_in_pass = False
            sorted_indices = list(range(n - i, n))  # Rightmost i elements are sorted.
            for j in range(0, n - i - 1):
                yield (j, j+1, data.copy(), sorted_indices, False)
                if data[j] > data[j+1]:
                    data[j], data[j+1] = data[j+1], data[j]
                    swapped_in_pass = True
                    yield (j, j+1, data.copy(), sorted_indices, True)
            sorted_indices = list(range(n - i - 1, n))
            yield (-1, -1, data.copy(), sorted_indices, False)
            if not swapped_in_pass:
                yield (-1, -1, data.copy(), list(range(n)), False)
                return
        yield (-1, -1, data.copy(), list(range(n)), False)

    def visualize_step(self):
        """
        Retrieves the next step from the generator and updates the canvas.
        If paused, it does nothing. Otherwise, it uses the current delay (doubling for swap steps)
        to schedule the next visualization step.
        """
        if self.paused:
            return

        try:
            step = next(self.sort_generator)
            index1, index2, current_state, sorted_indices, swapped_flag = step
        except StopIteration:
            return

        self.draw_background()
        self.draw_array(current_state, (index1, index2), sorted_indices, swapped_flag)

        effective_delay = self.current_delay * (2 if swapped_flag else 1)
        self.after(effective_delay, self.visualize_step)

    def draw_background(self):
        """
        Draws a plain rectangular background (without curved corners) on the canvas.
        The watermark has been removed from here.
        """
        self.canvas.delete("background")
        canvas_width = int(self.canvas['width'])
        canvas_height = int(self.canvas['height'])
        # Draw a plain rectangle as the background.
        self.canvas.create_rectangle(5, 5, canvas_width - 5, canvas_height - 5,
                                     fill="#f0f0f0", outline="", tags="background")

    def draw_array(self, data, highlight_indices, sorted_indices, swapped_flag):
        """
        Draws the array as boxes with plain, non-rounded corners.
          - Boxes in highlight_indices (being compared) are red.
          - Boxes in sorted_indices (final positions) are green.
          - Other boxes are light blue.
          - If swapped_flag is True, an arrow is drawn above the swapped boxes,
            and text is shown above the arrow to indicate the swap condition.
        """
        self.canvas.delete("box")
        canvas_width = int(self.canvas['width'])
        canvas_height = int(self.canvas['height'])
        num_elements = len(data)
        # Compute spacing. Each box is drawn with a gap of box_width.
        box_width = canvas_width // (num_elements + 1)
        box_height = 50
        
        # Compute start_x to center the boxes:
        start_x = (canvas_width - (num_elements * box_width - 10)) / 2

        arrow_coords = None
        # If a swap occurs and there are valid indices
        if swapped_flag and highlight_indices[0] != -1:
            j1, j2 = highlight_indices
            center_x1 = start_x + j1 * box_width + (box_width - 10) / 2
            center_x2 = start_x + j2 * box_width + (box_width - 10) / 2
            arrow_y = canvas_height // 2 - box_height // 2 - 20
            arrow_coords = (center_x1, arrow_y, center_x2, arrow_y)

        for i, value in enumerate(data):
            # Calculate coordinates for each box.
            x0 = start_x + i * box_width
            y0 = canvas_height // 2 - box_height // 2
            x1 = x0 + box_width - 10
            y1 = y0 + box_height

            if i in highlight_indices:
                fill_color = "red"
            elif i in sorted_indices:
                fill_color = "green"
            else:
                fill_color = "light blue"

            # Draw the element box as a plain rectangle (no rounded corners).
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=fill_color,
                                         outline="black", tags="box")
            self.canvas.create_text((x0+x1)//2, (y0+y1)//2,
                                    text=str(value), font=("Arial", 12), tags="box")

        # Draw arrow if a swap occurred
        if arrow_coords:
            self.canvas.create_line(*arrow_coords, arrow=tk.LAST, width=3,
                                    fill="black", tags="box")
            # Calculate center for the text
            text_x = (arrow_coords[0] + arrow_coords[2]) / 2
            text_y = arrow_coords[1] - 15  # place text 15 pixels above the arrow
            # Create text indicating the swap condition, e.g., "5 > 3"
            self.canvas.create_text(text_x, text_y,
                                    text=f"{data[highlight_indices[1]]} > {data[highlight_indices[0]]}",
                                    font=("Arial", 10), fill="black", tags="box")

# Allow testing this module independently.
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Bubble Sort Visualizer")
    tab = BubbleSortTab(root)
    tab.pack(expand=True, fill="both")
    root.mainloop()
