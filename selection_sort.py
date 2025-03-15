# selection_sort.py
import tkinter as tk
from tkinter import ttk

class SelectionSortTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        heading = tk.Label(self, text="Selection Sort", font=("Arial", 24, "bold"), bg="#3a3a3a")
        heading.pack(pady=10)

        # List to store Entry widgets.
        self.entries = []
        # List to hold numbers to sort.
        self.data = []
        # Default speed delay in ms. (Slow = 2000, Medium = 700, Fast = 100)
        self.current_delay = 1500
        # Pause flag.
        self.paused = False

        # --- Top: Number-of-Elements Input ---
        self.input_frame = ttk.Frame(self)
        self.input_frame.pack(pady=10)
        self.num_label = ttk.Label(self.input_frame, text="Enter number of elements:")
        self.num_label.grid(row=0, column=0, padx=5, pady=5)
        self.num_entry = ttk.Entry(self.input_frame, width=10)
        self.num_entry.grid(row=0, column=1, padx=5, pady=5)
        self.generate_button = ttk.Button(
            self.input_frame,
            text="Generate Input Fields",
            command=self.generate_input_fields
        )
        self.generate_button.grid(row=0, column=2, padx=5, pady=5)

        # --- Middle: Array Elements Input ---
        self.array_frame = ttk.Frame(self)
        self.array_frame.pack(pady=10)

        # --- Controls: Speed & Pause/Play ---
        self.speed_frame = ttk.Frame(self)
        self.speed_frame.pack(pady=10)
        self.slow_button = ttk.Button(
            self.speed_frame, text="Slow", command=lambda: self.set_speed(2000))
        self.slow_button.grid(row=0, column=0, padx=5, pady=5)
        self.medium_button = ttk.Button(
            self.speed_frame, text="Medium", command=lambda: self.set_speed(700))
        self.medium_button.grid(row=0, column=1, padx=5, pady=5)
        self.fast_button = ttk.Button(
            self.speed_frame, text="Fast", command=lambda: self.set_speed(100))
        self.fast_button.grid(row=0, column=2, padx=5, pady=5)
        self.pause_play_button = ttk.Button(
            self.speed_frame, text="Pause", command=self.toggle_pause)
        self.pause_play_button.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

        # --- Bottom: Visualization Canvas (white background) ---
        self.canvas = tk.Canvas(self, width=1000, height=500, bg="white")
        self.canvas.pack(pady=10)

    def set_speed(self, delay):
        """Update the speed delay."""
        self.current_delay = delay

    def toggle_pause(self):
        """Toggle pause/play and update the button text."""
        self.paused = not self.paused
        if self.paused:
            self.pause_play_button.config(text="Play")
        else:
            self.pause_play_button.config(text="Pause")
            self.visualize_step()

    def generate_input_fields(self):
        """Create Entry widgets for array elements."""
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
            self.array_frame,
            text="Start Selection Sort",
            command=self.start_sort
        )
        self.start_button.grid(row=2, column=0, columnspan=num_elements, pady=10)

    def start_sort(self):
        """Gather numbers and start selection sort."""
        try:
            self.data = [int(entry.get()) for entry in self.entries]
        except ValueError:
            return
        self.canvas.delete("all")
        # Create the generator with a copy of the data.
        self.sort_generator = self.selection_sort(self.data.copy())
        self.after(self.current_delay, self.visualize_step)

    def selection_sort(self, data):
        """
        A generator that performs selection sort.
        For each index i:
          - It sets the candidate (lowest seen so far) as data[i].
          - Iterates j from i+1 to n-1.
          - Yields steps as an 8-tuple:
            (current_index, candidate_index, checking_index, candidate_comp, data_state, sorted_indices, swapped_flag, swap_applied)
          - For non-swap steps, swapped_flag and swap_applied are False.
          - When a new candidate is found, candidate_comp is a tuple (prev_candidate, previous_value).
          - When a swap is needed:
              • Yield a pre-swap step (swapped_flag True, swap_applied False) to show the swap arrow.
              • Immediately apply the swap.
              • Yield the final post-swap state where the current element is now sorted (and current index arrow disappears).
        """
        n = len(data)
        for i in range(n):
            sorted_indices = list(range(i))  # Already sorted part.
            candidate_index = i             # Start candidate as current element.
            # Yield step: begin inner loop; checking_index = i.
            yield (i, candidate_index, i, None, data.copy(), sorted_indices, False, False)
            for j in range(i+1, n):
                # Yield step: checking element j.
                yield (i, candidate_index, j, None, data.copy(), sorted_indices, False, False)
                if data[j] < data[candidate_index]:
                    previous_candidate = candidate_index
                    candidate_index = j
                    # Yield step: new candidate found.
                    yield (i, candidate_index, j, (previous_candidate, data[previous_candidate]), data.copy(), sorted_indices, False, False)
            if candidate_index != i:
                # Yield pre-swap step to show the swap arrow.
                yield (i, candidate_index, -1, None, data.copy(), sorted_indices, True, False)
                # Immediately apply the swap.
                data[i], data[candidate_index] = data[candidate_index], data[i]
                # Yield final post-swap state:
                # Set current_index to -1 so the "current index" arrow disappears.
                yield (-1, -1, -1, None, data.copy(), list(range(i+1)), False, True)
            else:
                # If no swap is needed, yield the state marking sorted portion.
                yield (-1, -1, -1, None, data.copy(), list(range(i+1)), False, False)
        # Final state: array fully sorted.
        yield (-1, -1, -1, None, data.copy(), list(range(n)), False, False)

    def visualize_step(self):
        """Retrieve the next step and update the canvas."""
        if self.paused:
            return
        try:
            # Unpack the 8-tuple.
            current_index, candidate_index, checking_index, candidate_comp, current_state, sorted_indices, swapped_flag, swap_applied = next(self.sort_generator)
        except StopIteration:
            return
        self.canvas.delete("all")
        self.draw_array(current_state, current_index, candidate_index, checking_index, candidate_comp, sorted_indices, swapped_flag, swap_applied)
        effective_delay = self.current_delay * (2 if swapped_flag else 1)
        self.after(effective_delay, self.visualize_step)

    def draw_array(self, data, current_index, candidate_index, checking_index, candidate_comp, sorted_indices, swapped_flag, swap_applied):
        """
        Draw the array boxes and arrows.
        
        Box Colors:
          - Green: Sorted elements.
          - Red: The current element (iterator) and element being checked.
          - Blue: Unsorted elements.
          - Light Green: The lowest value candidate (if it's not the current element).
        
        Arrows:
          - A downward arrow labeled "current index" is drawn above the current element (only if current_index != -1).
          - A "lowest value" arrow is drawn beneath the candidate box (pointing upward) with the label "lowest value".
            Now this arrow remains visible until the swap is applied.
          - A bidirectional "swap" arrow is drawn above the boxes during the pre-swap phase.
        """
        self.canvas.delete("box")
        canvas_width = int(self.canvas['width'])
        canvas_height = int(self.canvas['height'])
        num_elements = len(data)
        box_width = canvas_width // (num_elements + 1)
        box_height = 50
        start_x = (canvas_width - (num_elements * box_width - 10)) / 2

        # Dictionary to store coordinates of each box.
        box_coords = {}

        # Draw each box.
        for i, value in enumerate(data):
            x0 = start_x + i * box_width
            y0 = canvas_height // 2 - box_height // 2
            x1 = x0 + box_width - 10
            y1 = y0 + box_height
            box_coords[i] = (x0, y0, x1, y1)
            # Determine fill color.
            if i in sorted_indices:
                fill_color = "green"
            elif i == current_index:
                fill_color = "red"  # Current element.
            elif i == candidate_index and i != current_index:
                fill_color = "light green"  # Lowest value candidate.
            elif i == checking_index and i not in (current_index, candidate_index):
                fill_color = "red"  # Element being checked.
            else:
                fill_color = "light blue"
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=fill_color, outline="black", tags="box")
            self.canvas.create_text((x0+x1)//2, (y0+y1)//2, text=str(value), font=("Arial", 12), tags="box")

        # Offsets for arrow placement.
        arrow_offset_above = 30  # for swap arrow above boxes.
        arrow_offset_below = 10  # for arrow below boxes.

        # -------------------------------
        # Draw a downward arrow on the current element labeled "current index".
        if current_index != -1 and current_index in box_coords:
            cx0, cy0, cx1, cy1 = box_coords[current_index]
            c_center = ((cx0+cx1)//2, cy0)
            arrow_start = (c_center[0], cy0 - 40)
            arrow_end   = (c_center[0], cy0)
            self.canvas.create_line(*arrow_start, *arrow_end, arrow=tk.LAST, width=2, fill="black", tags="box")
            self.canvas.create_text(c_center[0], cy0 - 50, text="current index", font=("Arial", 10), fill="black", tags="box")

        # -------------------------------
        # Draw the "lowest value" arrow underneath the candidate box.
        # This arrow now remains visible until the swap is applied.
        if candidate_index != -1 and candidate_index in box_coords and not swap_applied:
            tx0, ty0, tx1, ty1 = box_coords[candidate_index]
            x_center = (tx0 + tx1) // 2
            arrow_start = (x_center, ty1 + arrow_offset_below + 30)
            arrow_end   = (x_center, ty1 + arrow_offset_below)
            self.canvas.create_line(*arrow_start, *arrow_end, arrow=tk.LAST, width=2, fill="black", tags="box")
            self.canvas.create_text(x_center, ty1 + arrow_offset_below + 40, text="lowest value", font=("Arial", 10), fill="black", tags="box")

        # -------------------------------
        # Draw the swap arrow above the boxes during the pre-swap phase.
        if swapped_flag and not swap_applied and current_index in box_coords and candidate_index in box_coords:
            offset = arrow_offset_above
            curr_x0, curr_y0, curr_x1, curr_y1 = box_coords[current_index]
            cand_x0, cand_y0, cand_x1, cand_y1 = box_coords[candidate_index]
            current_center = ((curr_x0+curr_x1)//2, curr_y0 - offset)
            candidate_center = ((cand_x0+cand_x1)//2, cand_y0 - offset)
            self.canvas.create_line(*current_center, *candidate_center, arrow=tk.BOTH, width=3, fill="black", tags="box")
            text_x = (current_center[0] + candidate_center[0]) // 2
            text_y = current_center[1] - 20
            self.canvas.create_text(text_x, text_y, text="swap", font=("Arial", 10), fill="black", tags="box")

# For standalone testing.
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Selection Sort Visualizer")
    tab = SelectionSortTab(root)
    tab.pack(expand=True, fill="both")
    root.mainloop()
