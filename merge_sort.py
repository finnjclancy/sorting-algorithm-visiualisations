import tkinter as tk
from tkinter import ttk
import colorsys  # For generating bright, distinct colors.
import math      # For logarithm computations
from collections import defaultdict

class MergeSortTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # ----------------------------
        # Top Label and Input Section
        # ----------------------------
        self.heading = tk.Label(self, text="Merge Sort", font=("Arial", 24, "bold"), bg="#424242")
        self.heading.pack(pady=10)

        self.entries = []
        self.data = []
        self.current_delay = 1500  # Default speed delay in ms.
        self.paused = False
        self.segment_delay = 500   # Delay between unveiling segments.
        self.reveal_delay = 1000   # Delay for revealing boxes.
        self.animated_rows = set()  # Tracks rows that have been animated.
        
        # Dictionary to store box positions for each row in the current frame.
        self.frame_box_positions = {}
        # List to keep keys (order) of rows drawn in the current frame.
        self.frame_keys = {}

        # --- Input Frame ---
        self.input_frame = ttk.Frame(self)
        self.input_frame.pack(pady=10)
        self.num_label = ttk.Label(self.input_frame, text="Enter number of elements:")
        self.num_label.grid(row=0, column=0, padx=5, pady=5)
        self.num_entry = ttk.Entry(self.input_frame, width=10)
        self.num_entry.grid(row=0, column=1, padx=5, pady=5)
        self.generate_button = ttk.Button(self.input_frame, text="Generate Input Fields",
                                          command=self.generate_input_fields)
        self.generate_button.grid(row=0, column=2, padx=5, pady=5)

        # --- Array Elements Input ---
        self.array_frame = ttk.Frame(self)
        self.array_frame.pack(pady=10)

        # --- Speed & Pause/Play ---
        self.speed_frame = ttk.Frame(self)
        self.speed_frame.pack(pady=10)
        self.slow_button = ttk.Button(self.speed_frame, text="Slow", command=lambda: self.set_speed(2000))
        self.slow_button.grid(row=0, column=0, padx=5, pady=5)
        self.medium_button = ttk.Button(self.speed_frame, text="Medium", command=lambda: self.set_speed(700))
        self.medium_button.grid(row=0, column=1, padx=5, pady=5)
        self.fast_button = ttk.Button(self.speed_frame, text="Fast", command=lambda: self.set_speed(100))
        self.fast_button.grid(row=0, column=2, padx=5, pady=5)
        self.pause_play_button = ttk.Button(self.speed_frame, text="Pause", command=self.toggle_pause)
        self.pause_play_button.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

        # --- Visualization Canvas ---
        self.canvas = tk.Canvas(self, width=1000, height=500, bg="white")
        self.canvas.pack(pady=10)

    def set_speed(self, delay):
        """Update the speed delay."""
        self.current_delay = delay

    def toggle_pause(self):
        """Toggle pause/play state and update the button text."""
        self.paused = not self.paused
        self.pause_play_button.config(text="Play" if self.paused else "Pause")
        if not self.paused:
            self.visualize_step()

    def generate_input_fields(self):
        """Create entry widgets for array elements."""
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
        self.start_button = ttk.Button(self.array_frame, text="Start Merge Sort", command=self.start_sort)
        self.start_button.grid(row=2, column=0, columnspan=num_elements, pady=10)

    def start_sort(self):
        """Read inputs, start merge sort, and visualize."""
        try:
            self.data = [int(entry.get()) for entry in self.entries]
        except ValueError:
            return
        self.canvas.delete("all")
        # Reset animated_rows and positions so each sort run animates fresh.
        self.animated_rows = set()
        self.frame_box_positions = {}
        self.frame_keys = {}
        self.sort_generator = self.merge_sort_generator(self.data.copy())
        self.after(self.current_delay, self.visualize_step)

    def merge_sort_generator(self, arr):
        """
        Yields frames of the merge sort process:
          - phase: "split", "merge", or "final"
          - split_levels: rows (lists of subarrays) during splitting
          - merge_levels: rows (lists of subarrays) during merging
          - final: final sorted array
        """
        def compute_split_levels(a):
            levels = []
            current = [a.copy()]  # Level 0: the full array.
            levels.append(current)
            while any(len(sub) > 1 for sub in current):
                next_level = []
                for sub in current:
                    if len(sub) > 1:
                        mid = len(sub) // 2
                        left = sub[:mid]
                        right = sub[mid:]
                        next_level.append(left)
                        next_level.append(right)
                    else:
                        next_level.append(sub)
                levels.append(next_level)
                current = next_level
            return levels

        def merge_two_lists(a, b):
            i, j = 0, 0
            merged = []
            while i < len(a) and j < len(b):
                if a[i] <= b[j]:
                    merged.append(a[i])
                    i += 1
                else:
                    merged.append(b[j])
                    j += 1
            merged.extend(a[i:])
            merged.extend(b[j:])
            return merged

        def compute_merge_levels(leaves):
            levels = []
            current = leaves.copy()
            while len(current) > 1:
                next_level = []
                for i in range(0, len(current), 2):
                    if i + 1 < len(current):
                        merged = merge_two_lists(current[i], current[i+1])
                        next_level.append(merged)
                    else:
                        next_level.append(current[i])
                levels.append(next_level)
                current = next_level
            return levels

        split_levels = compute_split_levels(arr)
        for level_index in range(len(split_levels)):
            yield {"phase": "split", "split_levels": split_levels[:level_index+1]}

        leaves = split_levels[-1]
        merge_levels = compute_merge_levels(leaves)
        for level_index in range(len(merge_levels)):
            yield {"phase": "merge",
                   "split_levels": split_levels,
                   "merge_levels": merge_levels[:level_index+1]}
        yield {"phase": "final",
               "split_levels": split_levels,
               "merge_levels": merge_levels,
               "final": merge_levels[-1][0] if merge_levels and merge_levels[-1] else arr}

    def draw_arrows_between_rows(self, prev_positions, curr_positions):
        """
        Given two lists of box positions (each as (element, center_x, top_y, bottom_y)),
        match boxes by element value and occurrence order, and draw arrows from the previous
        row's box (bottom center) to the current row's box (top center) if their x–positions differ.
        """
        prev_dict = defaultdict(list)
        curr_dict = defaultdict(list)
        for pos in prev_positions:
            elem, center_x, top_y, bottom_y = pos
            prev_dict[elem].append((center_x, top_y, bottom_y))
        for pos in curr_positions:
            elem, center_x, top_y, bottom_y = pos
            curr_dict[elem].append((center_x, top_y, bottom_y))
        for elem in prev_dict:
            if elem in curr_dict:
                count = min(len(prev_dict[elem]), len(curr_dict[elem]))
                for i in range(count):
                    prev_center, prev_top, prev_bottom = prev_dict[elem][i]
                    curr_center, curr_top, curr_bottom = curr_dict[elem][i]
                    if abs(prev_center - curr_center) > 0:
                        self.canvas.create_line(
                            prev_center, prev_bottom,
                            curr_center, curr_top,
                            arrow=tk.LAST, fill="black", width=2
                        )

    def visualize_step(self):
        """
        Get next frame from generator, draw rows, and (if in a merging phase)
        draw arrows connecting boxes where numbers move.
        """
        if self.paused:
            return
        try:
            state = next(self.sort_generator)
        except StopIteration:
            return
        
        self.canvas.delete("all")
        canvas_height = int(self.canvas['height'])
        canvas_width = int(self.canvas['width'])
        
        if self.data:
            splitting_count = math.ceil(math.log(len(self.data), 2)) + 1
            merging_count = math.ceil(math.log(len(self.data), 2))
            total_lines = splitting_count + merging_count
        else:
            total_lines = 1
        
        top_margin = 20
        bottom_margin = 20
        row_padding = 20  
        line_gap = (canvas_height - top_margin - bottom_margin + 10) / (total_lines + 1)
        row_height = line_gap - row_padding
        
        rows_to_draw = []
        split_levels = state.get("split_levels", [])
        for idx, level in enumerate(split_levels):
            y = top_margin + idx * line_gap
            
            # Label the first row as "input" instead of "splitting"
            phase_label = "input" if idx == 0 else "splitting"
            
            rows_to_draw.append({
                "row": level,
                "y": y,
                "phase_label": phase_label,
                "row_index": idx,
                "row_height": row_height
            })
            
        if state.get("phase") in ["merge", "final"]:
            merge_levels = state.get("merge_levels", [])
            for idx, level in enumerate(merge_levels):
                y = top_margin + (len(split_levels) + idx) * line_gap
                
                # Check if this is the final merge level (sorted array)
                # If it's the last level of merge_levels and there's only one array in it
                phase_label = "sorted" if (idx == len(merge_levels)-1 and len(level) == 1) else "merging"
                
                rows_to_draw.append({
                    "row": level,
                    "y": y,
                    "phase_label": phase_label,
                    "row_index": idx,
                    "row_height": row_height
                })
        
        self.frame_box_positions = {}
        self.frame_keys = {}
        
        max_row_time = 0
        for row_info in rows_to_draw:
            key = (row_info["phase_label"], row_info["row_index"])
            animate = key not in self.animated_rows
            if animate:
                self.animated_rows.add(key)
            row_animation_time = (len(row_info["row"]) * self.reveal_delay) if animate else 0
            max_row_time = max(max_row_time, row_animation_time)
            
            positions = self.animate_row(
                row_info["row"],
                row_info["y"],
                row_info["phase_label"],
                row_info["row_height"],
                animate
            )
            self.frame_box_positions[key] = positions
            self.frame_keys[key] = positions
        
        if state.get("phase") in ["merge", "final"]:
            splitting_keys = [k for k in self.frame_keys if k[0] == "splitting"]
            merging_keys = [k for k in self.frame_keys if k[0] == "merging"]
            if splitting_keys and merging_keys:
                last_split = splitting_keys[-1]
                first_merge = merging_keys[0]
                prev_positions = self.frame_box_positions[last_split]
                curr_positions = self.frame_box_positions[first_merge]
                self.draw_arrows_between_rows(prev_positions, curr_positions)
            for i in range(1, len(merging_keys)):
                prev_positions = self.frame_box_positions[merging_keys[i-1]]
                curr_positions = self.frame_box_positions[merging_keys[i]]
                self.draw_arrows_between_rows(prev_positions, curr_positions)
        
        self.after(self.current_delay + max_row_time, self.visualize_step)

    def animate_row(self, row, y_start, phase_label, row_height, animate=True):
        """
        Draw a row of boxes and return a list of positions.
        Each tuple is (element, center_x, top_y, bottom_y).

        Instead of drawing a vertical line between segments, this version draws a box
        around each segment with equal padding.
        """
        canvas_width = int(self.canvas['width'])
        left_panel = canvas_width * 0.15
        right_panel = canvas_width * 0.85
        outer_gap = 10   # Left/right gap.
        inner_gap = 10   # Gap between boxes.
        border_margin = 5  # Equal padding around each segment's border.
        
        self.canvas.create_text(left_panel * 0.2, y_start + row_height / 2,
                                text=phase_label, font=("Arial", 12), fill="black", anchor="w")
        self.canvas.create_line(left_panel * 0.7, y_start + row_height / 2,
                                left_panel - 5, y_start + row_height / 2,
                                arrow=tk.LAST, fill="black", width=2)
        
        total_elements = sum(len(seg) for seg in row)
        available_width = right_panel - 2 * outer_gap
        box_width = (available_width - (total_elements - 1) * inner_gap) / total_elements if total_elements else 0
        
        start_x = left_panel + outer_gap
        current_index = 0
        positions = []  # (element, center_x, top_y, bottom_y)
        segments_items = []  # For animated segments.
        
        # For each segment:
        for seg_index, seg in enumerate(row):
            seg_items = []
            target_color = self.gradient_color(seg_index, len(row))
            seg_start = current_index  # Starting index for this segment.
            for element in seg:
                x0 = start_x + current_index * (box_width + inner_gap)
                y0 = y_start
                x1 = x0 + box_width
                y1 = y0 + row_height
                center_x = (x0 + x1) / 2
                positions.append((element, center_x, y0, y1))
                
                if animate:
                    rect_id = self.canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="black")
                    text_id = self.canvas.create_text((x0+x1)/2, (y0+y1)/2,
                                                      text=str(element), font=("Arial", 16), fill="white")
                    seg_items.append((rect_id, text_id, target_color))
                else:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill=target_color, outline="black")
                    self.canvas.create_text((x0+x1)/2, (y0+y1)/2,
                                            text=str(element), font=("Arial", 16), fill="black")
                current_index += 1
            segments_items.append(seg_items)
            # Draw a rectangle around this segment with equal padding.
            if len(seg) > 0:
                seg_x0 = start_x + seg_start * (box_width + inner_gap)
                seg_x1 = start_x + (current_index - 1) * (box_width + inner_gap) + box_width
                self.canvas.create_rectangle(seg_x0 - border_margin, y_start - border_margin,
                                             seg_x1 + border_margin, y_start + row_height + border_margin,
                                             outline="black", width=2)
        
        if animate:
            for i, seg_items in enumerate(segments_items):
                delay = i * self.reveal_delay
                self.canvas.after(delay, lambda seg_items=seg_items: self.reveal_segment(seg_items))
        
        return positions

    def reveal_segment(self, seg_items):
        """Reveal the boxes by updating their colors."""
        for (rect_id, text_id, target_color) in seg_items:
            self.canvas.itemconfig(rect_id, fill=target_color)
            self.canvas.itemconfig(text_id, fill="black")
    
    def gradient_color(self, i, total):
        """Return a bright, distinct color for segment i of total segments."""
        if total <= 0:
            return "#ff66ff"
        hue = i / total
        saturation = 1.0
        value = 1.0
        r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
        return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Merge Sort Visualizer")
    tab = MergeSortTab(root)
    tab.pack(expand=True, fill="both")
    root.mainloop()
