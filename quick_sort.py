import tkinter as tk
from tkinter import ttk

class QuickSortTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        #######################################################################
        #  Title/Heading
        #######################################################################
        self.heading = tk.Label(
            self, text="Quick Sort", font=("Arial", 24, "bold"), bg="#3a3a3a"
        )
        self.heading.pack(pady=10)

        #######################################################################
        #  Variables
        #######################################################################
        self.entries = []
        self.data = []
        # Each snapshot now includes sorted_indexes: (array_snapshot, pivot_index, comment, low, high, subarr, sorted_indexes)
        self.partitions = []
        self.current_partition_index = 0
        self.drawn_rows = 0
        self.current_delay = 1000
        self.paused = False
        self.reveal_delay = 1200

        #######################################################################
        #  Input Section
        #######################################################################
        self.input_frame = ttk.Frame(self)
        self.input_frame.pack(pady=10)

        ttk.Label(self.input_frame, text="Enter number of elements:")\
            .grid(row=0, column=0, padx=5, pady=5)
        self.num_entry = ttk.Entry(self.input_frame, width=10)
        self.num_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(self.input_frame, text="Generate Fields", command=self.generate_input_fields)\
            .grid(row=0, column=2, padx=5, pady=5)

        #######################################################################
        #  Array Input Frame
        #######################################################################
        self.array_frame = ttk.Frame(self)
        self.array_frame.pack(pady=10)

        #######################################################################
        #  Speed & Pause
        #######################################################################
        self.speed_frame = ttk.Frame(self)
        self.speed_frame.pack(pady=10)

        ttk.Button(self.speed_frame, text="Slow", command=lambda: self.set_speed(2000))\
            .grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(self.speed_frame, text="Medium", command=lambda: self.set_speed(700))\
            .grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(self.speed_frame, text="Fast", command=lambda: self.set_speed(150))\
            .grid(row=0, column=2, padx=5, pady=5)

        self.pause_play_button = ttk.Button(self.speed_frame, text="Pause", command=self.toggle_pause)
        self.pause_play_button.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

        #######################################################################
        #  Visualization Canvas
        #######################################################################
        self.canvas = tk.Canvas(self, width=1000, height=500, bg="white")
        self.canvas.pack(pady=10)

    ###########################################################################
    #  UI
    ###########################################################################
    def generate_input_fields(self):
        for w in self.array_frame.winfo_children():
            w.destroy()
        self.entries = []
        try:
            num_elements = int(self.num_entry.get())
        except ValueError:
            return
        label = ttk.Label(self.array_frame, text="Enter array elements:")
        label.grid(row=0, column=0, columnspan=num_elements, pady=5)
        for i in range(num_elements):
            e = ttk.Entry(self.array_frame, width=5)
            e.grid(row=1, column=i, padx=5, pady=5)
            self.entries.append(e)
        ttk.Button(self.array_frame, text="Start Quick Sort", command=self.start_sort)\
            .grid(row=2, column=0, columnspan=num_elements, pady=10)

    def start_sort(self):
        try:
            self.data = [int(e.get()) for e in self.entries]
        except ValueError:
            return
        self.canvas.delete("all")
        self.partitions.clear()
        self.drawn_rows = 0
        self.current_partition_index = 0
        # Initial snapshot with empty sorted_indexes
        self.partitions.append((self.data[:], None, "Initial array", 0, len(self.data)-1, [], set()))
        
        # Create a global set to track all sorted indices
        self.all_sorted_indices = set()
        
        # Start QuickSort with an empty set of sorted indexes
        self.quick_sort_inplace(0, len(self.data)-1, set())
        
        # Final snapshot with all indices as sorted
        all_indices = set(range(len(self.data)))
        self.partitions.append((self.data[:], None, "Sorted array", 0, len(self.data)-1, [], all_indices))
        
        # Dynamically resize the canvas based on the number of partitions
        self.adjust_canvas_height()
        
        self.visualize_next()

    def set_speed(self, delay):
        self.current_delay = delay

    def toggle_pause(self):
        self.paused = not self.paused
        self.pause_play_button.config(text="Play" if self.paused else "Pause")
        
        # If we're unpausing, continue the visualization
        if not self.paused:
            # If we're in the middle of revealing cells, continue from where we left off
            if hasattr(self, 'pending_reveals') and self.pending_reveals:
                self.continue_reveal()
            else:
                # Otherwise move to the next visualization step
                self.visualize_next()

    ###########################################################################
    #  Quicksort
    ###########################################################################
    def quick_sort_inplace(self, low, high, sorted_indexes):
        if low < high:
            pivot_pos = self.partition(low, high, sorted_indexes)
            
            # Continue with recursive calls
            self.quick_sort_inplace(low, pivot_pos - 1, self.all_sorted_indices)
            self.quick_sort_inplace(pivot_pos + 1, high, self.all_sorted_indices)

    def partition(self, low, high, sorted_indexes):
        # Store original values for comment before any modifications
        first_val = self.data[low]
        last_val = self.data[high]
        subsize = high - low + 1
        mid_index = low + (subsize // 2)
        mid_val = self.data[mid_index]
        
        # ----------------------------
        # Pick pivot by taking median of (first, middle, last) *within* [low..high]
        # ----------------------------
        pivot_i = self.median_of_three_subarray(low, high)
        pivot_val = self.data[pivot_i]

        # Move pivot to the end of this subarray
        self.data[pivot_i], self.data[high] = self.data[high], self.data[pivot_i]

        store_index = low
        for j in range(low, high):
            if self.data[j] < pivot_val:
                self.data[store_index], self.data[j] = self.data[j], self.data[store_index]
                store_index += 1

        # Finally move pivot into its correct place
        self.data[store_index], self.data[high] = self.data[high], self.data[store_index]

        # Build subarray for snapshot
        subarr = (self.data[low:store_index]
                    + [self.data[store_index]]
                    + self.data[store_index+1:high+1])
        arr_snap = self.data[:]
        for x in range(low, high+1):
            if x != store_index:
                arr_snap[x] = None

        # Mark ONLY the pivot as sorted
        self.all_sorted_indices.add(store_index)
        
        # Remove special case checks - only track pivots
        
        # ----------------------------
        # Build comment for how pivot was found using original values
        # ----------------------------
        if subsize == 2:
            how_found = f"median of {first_val} and {last_val}"
        elif subsize > 2:
            how_found = f"median of {first_val}, {mid_val}, and {last_val}"
        else:
            how_found = ""
        comment = f"Pivot {pivot_val}\n{how_found}"

        # Save snapshot with only the pivots marked as sorted
        self.partitions.append((
            arr_snap,
            store_index,
            comment,
            low,
            high,
            subarr,
            self.all_sorted_indices.copy()  # Only contains pivots now
        ))
        return store_index

    def median_of_three_subarray(self, low, high):
        """
        Return the index (in the global 'self.data') of the median
        among the subarray's first, middle, and last element.
        """
        sub_len = high - low + 1
        mid = low + (sub_len // 2)

        a = self.data[low]
        b = self.data[mid]
        c = self.data[high]

        # Standard median-of-three logic
        if (a <= b <= c) or (c <= b <= a):
            return mid
        elif (b <= a <= c) or (c <= a <= b):
            return low
        else:
            return high

    ###########################################################################
    #  Visualization
    ###########################################################################
    def visualize_next(self):
        if self.paused or self.current_partition_index >= len(self.partitions):
            return
        
        snap, pivot_i, comment, low, high, subarr, sorted_indexes = self.partitions[self.current_partition_index]
        self.current_partition_index += 1
        row_index = self.drawn_rows
        self.drawn_rows += 1
        
        # Draw the base row
        self.draw_row(row_index, snap, pivot_i, comment, low, high, subarr, sorted_indexes)
        
        # Setup the reveals but track them so we can pause mid-animation
        self.pending_reveals = []
        self.current_reveal_index = 0
        
        for offset, element in enumerate(subarr):
            idx = low + offset
            self.pending_reveals.append((idx, element, sorted_indexes))
        
        # Start the reveal process
        self.continue_reveal()

    def continue_reveal(self):
        if self.paused:
            return
        
        # If we've revealed all cells
        if not hasattr(self, 'pending_reveals') or self.current_reveal_index >= len(self.pending_reveals):
            # Clean up
            self.pending_reveals = []
            self.current_reveal_index = 0
            
            # Schedule the next visualization after the delay
            self.after(self.current_delay, self.visualize_next)
            return
        
        # Get the next cell to reveal
        idx, val, sorted_idxs = self.pending_reveals[self.current_reveal_index]
        self.current_reveal_index += 1
        
        # Reveal this cell
        self.reveal_cell(idx, val, sorted_idxs)
        
        # Schedule the next reveal
        self.after(self.reveal_delay, self.continue_reveal)

    def adjust_canvas_height(self):
        # Calculate optimal canvas height based on number of rows
        num_rows = len(self.partitions)
        row_height = 60  # Base height per row
        padding = 15     # Middle ground for padding between rows (was 20)
        
        # Calculate needed height with moderate vertical whitespace
        needed_height = (num_rows * row_height) + ((num_rows - 1) * padding) + 50
        
        # Set minimum height
        min_height = 300
        canvas_height = max(needed_height, min_height)
        
        # Update canvas height
        self.canvas.config(height=canvas_height)

    def draw_row(self, row_index, array_snapshot, pivot_i, comment, low, high, subarr, sorted_indexes):
        ch = int(self.canvas["height"])
        cw = int(self.canvas["width"])
        total_rows = len(self.partitions)
        
        # Adjust row height and spacing based on total number of rows
        top_margin = 25  # Moderate top margin (was 30)
        bottom_margin = 25  # Moderate bottom margin (was 30)
        available_height = ch - top_margin - bottom_margin
        
        # Moderate vertical spacing between rows
        row_gap = 18  # Middle ground between 10 and 25
        
        # Calculate row height to better fill available space
        # Distribute space more evenly between rows
        row_height = (available_height - ((total_rows - 1) * row_gap)) / total_rows
        
        # Ensure minimum height but don't cap at a maximum
        row_height = max(40, row_height)
        
        # Calculate y position for this row
        y_start = top_margin + row_index * (row_height + row_gap)

        self.canvas.create_text(
            50, y_start + row_height / 2,
            text=comment, font=("Arial", 12), fill="black", anchor="w"
        )
        self.canvas.create_line(
            120, y_start + row_height / 2,
            145, y_start + row_height / 2,
            arrow=tk.LAST, fill="black", width=2
        )

        left_margin = 180
        right_margin = 80
        usable_width = cw - left_margin - right_margin
        n = len(array_snapshot)
        if n == 0:
            return

        box_gap = 10
        box_width = (usable_width - (n - 1) * box_gap) / float(n)
        if box_width < 5:
            box_width = 5

        # Highlight the subarray [low..high] with a rectangle
        if pivot_i is not None:
            rectangle_pad = 4  # Slightly smaller padding
            sub_left = left_margin + low * (box_width + box_gap) - rectangle_pad
            sub_right = left_margin + high * (box_width + box_gap) + box_width + rectangle_pad
            sub_top = y_start - rectangle_pad
            sub_bottom = y_start + row_height + rectangle_pad
            self.canvas.create_rectangle(
                sub_left, sub_top, sub_right, sub_bottom,
                outline="black", width=2  # Make the outline slightly thinner
            )

        # Render the array boxes
        self.row_boxes = []
        for i, val in enumerate(array_snapshot):
            x0 = left_margin + i * (box_width + box_gap)
            y0 = y_start
            x1 = x0 + box_width
            y1 = y0 + row_height

            # Color green if index is in sorted_indexes
            if i in sorted_indexes:
                fill_color = "green"
            elif val is None:
                fill_color = "white"
            else:
                fill_color = "red"

            r = self.canvas.create_rectangle(x0, y0, x1, y1, fill=fill_color, outline="black")
            txt_val = "" if val is None else str(val)
            t = self.canvas.create_text(
                (x0 + x1) / 2, (y0 + y1) / 2,
                text=txt_val,
                fill="black",
                font=("Arial", 14)
            )
            self.row_boxes.append((r, t, i))

    def reveal_cell(self, arr_index, new_val, sorted_indexes):
        for (r, t, i) in self.row_boxes:
            if i == arr_index:
                color = "green" if i in sorted_indexes else "red"
                self.canvas.itemconfig(r, fill=color)
                self.canvas.itemconfig(t, text=str(new_val), fill="black")
                break

###########################################################################
#  Testing
###########################################################################
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Quick Sort Visualizer")
    tab = QuickSortTab(root)
    tab.pack(expand=True, fill="both")
    root.mainloop()
