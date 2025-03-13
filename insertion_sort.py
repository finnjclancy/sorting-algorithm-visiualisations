import tkinter as tk
from tkinter import ttk

class InsertionSortTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        heading = tk.Label(self, text="Insertion Sort", font=("Arial", 24, "bold"), bg="#3a3a3a")
        heading.pack(pady=10)
        # List to store Entry widgets (user inputs)
        self.entries = []
        # List to hold the numbers to sort
        self.data = []
        # Default speed delay in ms: Slow=2000, Medium=700, Fast=100
        self.current_delay = 1500
        # Pause flag
        self.paused = False

        # --- Top Section: Number-of-Elements Input ---
        self.input_frame = ttk.Frame(self)
        self.input_frame.pack(pady=10)
        self.num_label = ttk.Label(self.input_frame, text="Enter number of elements:")
        self.num_label.grid(row=0, column=0, padx=5, pady=5)
        self.num_entry = ttk.Entry(self.input_frame, width=10)
        self.num_entry.grid(row=0, column=1, padx=5, pady=5)
        self.generate_button = ttk.Button(self.input_frame,
                                          text="Generate Input Fields",
                                          command=self.generate_input_fields)
        self.generate_button.grid(row=0, column=2, padx=5, pady=5)

        # --- Middle Section: Array Elements Input ---
        self.array_frame = ttk.Frame(self)
        self.array_frame.pack(pady=10)

        # --- Next Section: Speed Controls & Pause/Play ---
        self.speed_frame = ttk.Frame(self)
        self.speed_frame.pack(pady=10)
        self.slow_button = ttk.Button(self.speed_frame,
                                      text="Slow",
                                      command=lambda: self.set_speed(2000))
        self.slow_button.grid(row=0, column=0, padx=5, pady=5)
        self.medium_button = ttk.Button(self.speed_frame,
                                        text="Medium",
                                        command=lambda: self.set_speed(700))
        self.medium_button.grid(row=0, column=1, padx=5, pady=5)
        self.fast_button = ttk.Button(self.speed_frame,
                                      text="Fast",
                                      command=lambda: self.set_speed(100))
        self.fast_button.grid(row=0, column=2, padx=5, pady=5)
        self.pause_play_button = ttk.Button(self.speed_frame,
                                            text="Pause",
                                            command=self.toggle_pause)
        self.pause_play_button.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

        # --- Bottom Section: Visualization Canvas ---
        self.canvas = tk.Canvas(self, width=800, height=300, bg="white")
        self.canvas.pack(pady=10)

    def set_speed(self, delay):
        """Update the speed delay."""
        self.current_delay = delay

    def toggle_pause(self):
        """Toggle pause/play state and update the button text."""
        self.paused = not self.paused
        if self.paused:
            self.pause_play_button.config(text="Play")
        else:
            self.pause_play_button.config(text="Pause")
            self.visualize_step()

    def generate_input_fields(self):
        """Create Entry widgets for array elements and clear previous ones."""
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
        self.start_button = ttk.Button(self.array_frame,
                                       text="Start Insertion Sort",
                                       command=self.start_sort)
        self.start_button.grid(row=2, column=0, columnspan=num_elements, pady=10)

    def start_sort(self):
        """Gather numbers and start the insertion sort visualization."""
        try:
            self.data = [int(entry.get()) for entry in self.entries]
        except ValueError:
            return
        self.canvas.delete("all")
        # Create the generator with a copy of the data
        self.sort_generator = self.insertion_sort(self.data.copy())
        self.after(self.current_delay, self.visualize_step)

    def insertion_sort(self, data):
        """
        Generator for insertion sort visualization.
        
        Yields a 7-tuple:
          (key_start, current_key, comparing_index, data_state, sorted_indices, swapped_flag, swap_applied)
        - sorted_indices: List of indices considered sorted at each step, set to list(range(i+1)) for iteration i.
        """
        n = len(data)
        for i in range(1, n):
            sorted_indices = list(range(i + 1))  # Indices 0 to i are considered sorted during iteration i
            key_start = i
            current_key = i
            # Initial state
            yield (key_start, current_key,
                   current_key - 1 if current_key > 0 else -1,
                   data.copy(), sorted_indices, False, False)
            # Shift the key leftward as long as needed
            while current_key > 0 and data[current_key - 1] > data[current_key]:
                # Pre-swap state
                yield (key_start, current_key, current_key - 1, data.copy(), sorted_indices, True, False)
                # Perform swap
                data[current_key - 1], data[current_key] = data[current_key], data[current_key - 1]
                current_key -= 1
                # Post-swap state
                yield (key_start, current_key, -1, data.copy(), sorted_indices, True, True)
            # Final state for this iteration: key is in place, all 0 to i are sorted
            yield (-1, -1, -1, data.copy(), sorted_indices, False, False)
        # Final state: entire array sorted
        yield (-1, -1, -1, data.copy(), list(range(n)), False, False)

    def visualize_step(self):
        """Retrieve the next step from the generator and update the canvas."""
        if self.paused:
            return
        try:
            (key_start, current_key, comparing_index, current_state,
             sorted_indices, swapped_flag, swap_applied) = next(self.sort_generator)
        except StopIteration:
            return
        self.canvas.delete("all")
        self.draw_array(current_state, key_start, current_key, comparing_index, swapped_flag, swap_applied, sorted_indices)
        effective_delay = self.current_delay * (2 if swapped_flag else 1)
        self.after(effective_delay, self.visualize_step)

    def draw_array(self, data, key_start, current_key, comparing_index, swapped_flag, swap_applied, sorted_indices):
        """
        Draw the array boxes and arrows for insertion sort.
        
        Box Colors:
        - Indices in sorted_indices and not the current_key: dark green (sorted section).
        - current_key (during insertion): light green.
        - Indices not in sorted_indices: light blue (unsorted).
        
        Arrows:
        - Downward 'current key' arrow above current_key if key_start != -1.
        - Bidirectional 'swap' arrow during pre-swap phase.
        """
        self.canvas.delete("box")
        canvas_width = int(self.canvas['width'])
        canvas_height = int(self.canvas['height'])
        num_elements = len(data)
        box_width = canvas_width // (num_elements + 1)
        box_height = 50
        start_x = (canvas_width - (num_elements * box_width - 10)) / 2

        box_coords = {}
        for i, value in enumerate(data):
            x0 = start_x + i * box_width
            y0 = canvas_height // 2 - box_height // 2
            x1 = x0 + box_width - 10
            y1 = y0 + box_height
            box_coords[i] = (x0, y0, x1, y1)

            # Determine fill color
            if i in sorted_indices:
                if i == current_key and key_start != -1:
                    fill_color = "light green"  # Current key being inserted
                else:
                    fill_color = "dark green"   # Sorted element
            else:
                fill_color = "light blue"       # Unsorted element

            self.canvas.create_rectangle(x0, y0, x1, y1, fill=fill_color, outline="black", tags="box")
            self.canvas.create_text((x0 + x1) // 2, (y0 + y1) // 2, text=str(value), font=("Arial", 12), tags="box")

        arrow_offset_above = 30
        # Draw 'current key' arrow if iteration is active
        if key_start != -1 and current_key in box_coords:
            cx0, cy0, cx1, cy1 = box_coords[current_key]
            c_center = ((cx0 + cx1) // 2, cy0)
            arrow_start = (c_center[0], cy0 - 40)
            arrow_end = (c_center[0], cy0)
            self.canvas.create_line(*arrow_start, *arrow_end, arrow=tk.LAST, width=2, fill="black", tags="box")
            self.canvas.create_text(c_center[0], cy0 - 50, text="current key", font=("Arial", 10), fill="black", tags="box")

        # Draw 'swap' arrow during pre-swap phase
        if swapped_flag and not swap_applied and current_key in box_coords and comparing_index in box_coords:
            offset = arrow_offset_above
            cur_x0, cur_y0, cur_x1, cur_y1 = box_coords[current_key]
            comp_x0, comp_y0, comp_x1, comp_y1 = box_coords[comparing_index]
            current_center = ((cur_x0 + cur_x1) // 2, cur_y0 - offset)
            compare_center = ((comp_x0 + comp_x1) // 2, comp_y0 - offset)
            self.canvas.create_line(*current_center, *compare_center, arrow=tk.BOTH, width=3, fill="black", tags="box")
            text_x = (current_center[0] + compare_center[0]) // 2
            text_y = current_center[1] - 20
            self.canvas.create_text(text_x, text_y, text="swap", font=("Arial", 10), fill="black", tags="box")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Insertion Sort Visualizer")
    tab = InsertionSortTab(root)
    tab.pack(expand=True, fill="both")
    root.mainloop()