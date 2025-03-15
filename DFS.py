import tkinter as tk
from tkinter import ttk, messagebox
import math
from collections import deque

class DepthFirstSearchTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        #######################################################################
        # Style / Dark background for frames/labels, but single white canvas
        #######################################################################
        style = ttk.Style()
        style.configure("Dark.TFrame", background="#3a3a3a")
        style.configure("Dark.TLabel", background="#3a3a3a", foreground="white")
        style.configure("Dark.TButton", background="#3a3a3a", foreground="white")
        style.configure("Dark.TCheckbutton", background="#3a3a3a")
        style.configure("Dark.TRadiobutton", background="#3a3a3a", foreground="white")

        self.configure(style="Dark.TFrame")

        #######################################################################
        # Heading
        #######################################################################
        self.heading = tk.Label(
            self, text="Depth First Search", font=("Arial", 24, "bold"),
            bg="#3a3a3a", fg="white"
        )
        self.heading.pack(pady=10, fill="x")

        #######################################################################
        # Main container: left (inputs), right (canvas + text)
        #######################################################################
        self.main_frame = ttk.Frame(self, style="Dark.TFrame")
        self.main_frame.pack(expand=True, fill="both")

        self.main_frame.columnconfigure(0, weight=3)  # ~30% for adjacency inputs
        self.main_frame.columnconfigure(1, weight=7)  # ~70% for DFS canvas
        self.main_frame.rowconfigure(0, weight=1)

        # Left adjacency area
        self.left_frame = ttk.Frame(self.main_frame, style="Dark.TFrame")
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Right area (just one big frame that holds top controls + single canvas)
        self.right_frame = ttk.Frame(self.main_frame, style="Dark.TFrame")
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.right_frame.rowconfigure(2, weight=1)  # For the canvas row
        self.right_frame.columnconfigure(0, weight=1)

        #######################################################################
        # Data structures
        #######################################################################
        self.num_nodes = 0
        self.node_labels = []
        self.node_label_entries = []
        self.adj_type_var = tk.StringVar(value="matrix")
        self.adjacency_matrix_vars = []
        self.adjacency_list_entries = []
        self.adjacency_indexed = {}

        # DFS
        # CHANGED: Default delay from 2000 ms to 6000 ms
        self.current_delay = 3000
        self.paused = False
        self.dfs_generator = None
        self.pre_order_list = []
        self.post_order_list = []

        # Canvas drawing
        self.node_positions = {}   # index -> (x,y)
        self.node_circles = {}     # index -> (circle_id, text_id)
        self.node_halo = None
        self.halo_node = None
        self.edge_lines = {}

        # We'll track lines of explanation on the left side of the canvas
        self.text_current_y = 20   # Where the next line of text goes on the canvas

        #######################################################################
        # Build left adjacency inputs
        #######################################################################
        self._build_left_inputs()

        #######################################################################
        # Build right controls + single canvas
        #######################################################################
        self._build_right_dfs_area()

    ###########################################################################
    # LEFT: adjacency input
    ###########################################################################
    def _build_left_inputs(self):
        input_top = ttk.Frame(self.left_frame, style="Dark.TFrame")
        input_top.pack(anchor="nw", fill="x", pady=5)

        lbl_num = ttk.Label(input_top, text="Number of nodes:", style="Dark.TLabel")
        lbl_num.grid(row=0, column=0, padx=5, pady=5, sticky="e")

        self.num_nodes_entry = ttk.Entry(input_top, width=8)
        self.num_nodes_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Radiobutton(
            input_top, text="Adjacency Matrix", variable=self.adj_type_var,
            value="matrix", command=self.clear_adjacency_fields,
            style="Dark.TRadiobutton"
        ).grid(row=1, column=0, columnspan=2, sticky="w", padx=5)

        ttk.Radiobutton(
            input_top, text="Adjacency List", variable=self.adj_type_var,
            value="list", command=self.clear_adjacency_fields,
            style="Dark.TRadiobutton"
        ).grid(row=2, column=0, columnspan=2, sticky="w", padx=5)

        gen_btn = ttk.Button(input_top, text="Generate Fields", command=self.generate_adjacency_fields,
                             style="Dark.TButton")
        gen_btn.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        self.adjacency_frame = ttk.Frame(self.left_frame, style="Dark.TFrame")
        self.adjacency_frame.pack(anchor="nw", fill="both", expand=True, pady=5)

    def clear_adjacency_fields(self):
        for child in self.adjacency_frame.winfo_children():
            child.destroy()
        self.node_label_entries.clear()
        self.adjacency_matrix_vars.clear()
        self.adjacency_list_entries.clear()

    def generate_adjacency_fields(self):
        self.clear_adjacency_fields()
        try:
            self.num_nodes = int(self.num_nodes_entry.get())
        except ValueError:
            self.num_nodes = 0
        if self.num_nodes < 1:
            return

        # Node label row
        label_frame = ttk.Frame(self.adjacency_frame, style="Dark.TFrame")
        label_frame.pack(anchor="nw", pady=5)

        tk.Label(label_frame, text="Enter each node label:", font=("Arial", 10, "bold"),
                 bg="#3a3a3a", fg="white").pack(anchor="w")

        row_label_frame = ttk.Frame(label_frame, style="Dark.TFrame")
        row_label_frame.pack(side="top", anchor="w")

        for i in range(self.num_nodes):
            ent = ttk.Entry(row_label_frame, width=7)
            ent.pack(side="left", padx=5)
            self.node_label_entries.append(ent)
        
        ref_btn = ttk.Button(label_frame, text="Refresh Labels", command=self.refresh_labels_only,
                             style="Dark.TButton")
        ref_btn.pack(anchor="w", pady=5)

        # Build adjacency portion
        if self.adj_type_var.get() == "matrix":
            self.build_matrix_inputs()
        else:
            self.build_list_inputs()

        self.refresh_labels_only()

    def build_matrix_inputs(self):
        lbl = tk.Label(self.adjacency_frame, text="Adjacency Matrix", font=("Arial", 14, "bold"),
                       bg="#3a3a3a", fg="white")
        lbl.pack(anchor="center", pady=5)

        container = ttk.Frame(self.adjacency_frame, style="Dark.TFrame")
        container.pack(anchor="center")

        for r in range(self.num_nodes):
            row_vars = []
            for c in range(self.num_nodes):
                row_vars.append(tk.BooleanVar(value=False))
            self.adjacency_matrix_vars.append(row_vars)

        corner = tk.Label(container, text="", width=7, bg="#3a3a3a")
        corner.grid(row=0, column=0, padx=5, pady=5)

        self.matrix_col_labels = []
        for c in range(self.num_nodes):
            lbl_c = tk.Label(container, text="", width=7, bg="#3a3a3a", fg="white",
                             font=("Arial", 9, "bold"), anchor="center")
            lbl_c.grid(row=0, column=c+1, padx=5, pady=5)
            self.matrix_col_labels.append(lbl_c)

        self.matrix_row_labels = []
        for r in range(self.num_nodes):
            lbl_r = tk.Label(container, text="", width=7, bg="#3a3a3a", fg="white",
                             font=("Arial", 9, "bold"), anchor="e")
            lbl_r.grid(row=r+1, column=0, padx=5, pady=5)
            self.matrix_row_labels.append(lbl_r)

            for c in range(self.num_nodes):
                var = self.adjacency_matrix_vars[r][c]
                cb = ttk.Checkbutton(container, variable=var, style="Dark.TCheckbutton")
                cb.grid(row=r+1, column=c+1, padx=5, pady=5)

    def build_list_inputs(self):
        lbl = tk.Label(self.adjacency_frame, text="Adjacency List", font=("Arial", 10, "bold"),
                       bg="#3a3a3a", fg="white")
        lbl.pack(anchor="w", pady=5)

        container = ttk.Frame(self.adjacency_frame, style="Dark.TFrame")
        container.pack()

        heading_lbl = tk.Label(container, text="Edges", font=("Arial", 9, "bold"),
                               bg="#3a3a3a", fg="white")
        heading_lbl.grid(row=0, column=1, padx=5, pady=5)

        for r in range(self.num_nodes):
            row_lbl = tk.Label(container, text="", width=7, bg="#3a3a3a", fg="white",
                               font=("Arial", 9, "bold"), anchor="e")
            row_lbl.grid(row=r+1, column=0, padx=5, pady=5, sticky="e")

            row_frame = ttk.Frame(container, style="Dark.TFrame")
            row_frame.grid(row=r+1, column=1, sticky="w")

            row_entries = []
            for c in range(self.num_nodes):
                ent = tk.Entry(row_frame, width=7)
                ent.grid(row=0, column=c, padx=5, pady=5)
                row_entries.append(ent)
            self.adjacency_list_entries.append(row_entries)

    def refresh_labels_only(self):
        self.node_labels = [ent.get().strip() for ent in self.node_label_entries]
        if self.adj_type_var.get() == "matrix" and hasattr(self, 'matrix_row_labels'):
            for r, lbl_w in enumerate(self.matrix_row_labels):
                textval = self.node_labels[r] if r < len(self.node_labels) else ""
                lbl_w.config(text=textval)
            for c, lbl_w in enumerate(self.matrix_col_labels):
                textval = self.node_labels[c] if c < len(self.node_labels) else ""
                lbl_w.config(text=textval)
        elif self.adj_type_var.get() == "list" and self.adjacency_list_entries:
            container = self.adjacency_list_entries[0][0].master.master
            for r in range(self.num_nodes):
                label_list = container.grid_slaves(row=r+1, column=0)
                if label_list:
                    lbl = label_list[0]
                    lbl.config(text=self.node_labels[r] if r < len(self.node_labels) else "")

    ###########################################################################
    # RIGHT: DFS Controls + Single White Canvas
    ###########################################################################
    def _build_right_dfs_area(self):
        # row 0: Start button + index
        top_frame = ttk.Frame(self.right_frame, style="Dark.TFrame")
        top_frame.grid(row=0, column=0, sticky="w", pady=5)

        start_frame = ttk.Frame(top_frame, style="Dark.TFrame")
        start_frame.pack(side="left", padx=5)

        ttk.Label(start_frame, text="Starting Index:", style="Dark.TLabel").pack(side="left")
        self.start_index_entry = ttk.Entry(start_frame, width=5)
        self.start_index_entry.pack(side="left", padx=5)
        self.start_index_entry.insert(0, "0")

        start_btn = ttk.Button(start_frame, text="Start Search", command=self.start_dfs,
                               style="Dark.TButton")
        start_btn.pack(side="left", padx=5)

        # row 1: speed & pause
        control_frame = ttk.Frame(self.right_frame, style="Dark.TFrame")
        control_frame.grid(row=1, column=0, sticky="w", pady=5)

        # CHANGED: slow=9000, medium=6000, fast=2100
        ttk.Button(control_frame, text="Slow", command=lambda: self.set_speed(9000), style="Dark.TButton")\
            .pack(side='left', padx=5)
        ttk.Button(control_frame, text="Medium", command=lambda: self.set_speed(6000), style="Dark.TButton")\
            .pack(side='left', padx=5)
        ttk.Button(control_frame, text="Fast", command=lambda: self.set_speed(2100), style="Dark.TButton")\
            .pack(side='left', padx=5)

        self.pause_play_button = ttk.Button(control_frame, text="Pause", command=self.toggle_pause,
                                            style="Dark.TButton")
        self.pause_play_button.pack(side='left', padx=5)

        # row 2: The single white canvas
        self.canvas = tk.Canvas(self.right_frame, bg="white", highlightthickness=0)
        self.canvas.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        self.canvas.bind("<Configure>", self._on_canvas_resize)

    def set_speed(self, delay):
        self.current_delay = delay

    def toggle_pause(self):
        self.paused = not self.paused
        self.pause_play_button.config(text="Play" if self.paused else "Pause")
        if not self.paused:
            self.visualize_step()

    ###########################################################################
    # DFS Start
    ###########################################################################
    def start_dfs(self):
        # Reset
        self.pre_order_list.clear()
        self.post_order_list.clear()

        self.canvas.delete("all")
        self.node_positions.clear()
        self.node_circles.clear()
        self.node_halo = None
        self.halo_node = None
        self.edge_lines.clear()

        # Reset explanation text lines
        self.text_current_y = 20

        if not self.build_indexed_adjacency():
            return

        # Draw initial
        self.draw_graph_initial()

        # Starting index
        try:
            start_idx = int(self.start_index_entry.get())
            if start_idx < 0 or start_idx >= self.num_nodes:
                messagebox.showwarning("Invalid Start Index", 
                                      f"Start index must be between 0 and {self.num_nodes-1}. Using 0 instead.")
                start_idx = 0
                self.start_index_entry.delete(0, tk.END)
                self.start_index_entry.insert(0, "0")
        except ValueError:
            messagebox.showwarning("Invalid Start Index", 
                                  "Start index must be a number. Using 0 instead.")
            start_idx = 0
            self.start_index_entry.delete(0, tk.END)
            self.start_index_entry.insert(0, "0")

        if self.num_nodes > 0:
            # Estimate total steps and adjust font size before starting
            estimated_steps = self.estimate_dfs_steps(start_idx)
            self.adjust_explanation_font_size(estimated_steps)
            
            self.dfs_generator = self.dfs_steps(start_idx)
            self.after(self.current_delay, self.visualize_step)
        else:
            self.dfs_generator = None

    def build_indexed_adjacency(self):
        self.node_labels = [ent.get().strip() for ent in self.node_label_entries]
        self.adjacency_indexed = {i: [] for i in range(self.num_nodes)}

        if self.adj_type_var.get() == "matrix":
            if len(self.adjacency_matrix_vars) != self.num_nodes:
                return True
            for r in range(self.num_nodes):
                for c in range(self.num_nodes):
                    if self.adjacency_matrix_vars[r][c].get():
                        self.adjacency_indexed[r].append(c)
        else:
            if len(self.adjacency_list_entries) != self.num_nodes:
                return True
            for r in range(self.num_nodes):
                row_ents = self.adjacency_list_entries[r]
                for c in range(len(row_ents)):
                    typed = row_ents[c].get().strip()
                    if typed:
                        matches = [idx for idx, lab in enumerate(self.node_labels) if lab == typed]
                        if not matches:
                            messagebox.showerror(
                                "Invalid Label",
                                f"Node {r} typed '{typed}' but no node has that label."
                            )
                            return False
                        self.adjacency_indexed[r].append(matches[0])
        return True

    ###########################################################################
    # Drawing / Canvas
    ###########################################################################
    def draw_graph_initial(self):
        w = self.canvas.winfo_width() or 700
        h = self.canvas.winfo_height() or 500
        
        # We'll keep ~200 px margin on the left side for text.
        left_text_area = 200  
        
        # Draw the "Nodes" row near the top, starting around x = left_text_area
        self._draw_initial_nodes_array(left_text_area)

        # Center for the circle (shifting to the right so it doesn't overlap text)
        cx = (w + left_text_area) // 2
        
        # Calculate the vertical center, accounting for top and bottom elements
        # Remove the +20 offset that was pushing the graph down
        # Top elements take ~80px, bottom elements take ~120px, so shift slightly up
        cy = h // 2 - 20  # Shift up by 20px to balance the space

        # CHANGED: multiply radius by 0.6 to shrink
        base_radius = min(cx - left_text_area - 40, cy - 40) - 30
        radius = int(0.6 * base_radius)  # scale down

        n = self.num_nodes
        if n < 1:
            return

        if n == 1:
            self.node_positions[0] = (cx, cy)
        else:
            angle_step = 2*math.pi / n
            for i in range(n):
                angle = i * angle_step
                x = cx + radius * math.cos(angle)
                y = cy + radius * math.sin(angle)
                self.node_positions[i] = (x, y)

        # edges
        for i in range(n):
            for j in self.adjacency_indexed[i]:
                line_id = self._draw_directed_edge(i, j, color="black")
                self.edge_lines[(i, j)] = line_id

        # nodes
        for i, (nx, ny) in self.node_positions.items():
            c_id = self.canvas.create_oval(nx-20, ny-20, nx+20, ny+20,
                                           fill="gray", outline="black", width=2)
            label = self.node_labels[i] if i < len(self.node_labels) else str(i)
            t_id = self.canvas.create_text(nx, ny, text=label, font=("Arial", 10, "bold"))
            self.node_circles[i] = (c_id, t_id)

        # Pre- & post-order boxes at the bottom (also shifted right)
        self._draw_order_arrays(left_text_area)

    def _draw_initial_nodes_array(self, left_text_area):
        self.canvas.delete("initial_nodes")
        w = self.canvas.winfo_width() or 700

        box_width = 30
        box_height = 30
        margin = 10
        y_pos = 20  # near top
        
        usable_width = w - left_text_area
        total_width = self.num_nodes * (box_width + margin)
        start_x = left_text_area + (usable_width - total_width) / 2

        self.canvas.create_text(
            start_x - 5, y_pos + box_height/2, 
            text="Nodes:", 
            anchor="e", 
            font=("Arial", 10, "bold"), 
            fill="black", 
            tags="initial_nodes"
        )
        
        for i in range(self.num_nodes):
            x = start_x + i * (box_width + margin)
            box_id = self.canvas.create_rectangle(
                x, y_pos, x + box_width, y_pos + box_height,
                fill="#e0e0e0", outline="black", 
                tags="initial_nodes"
            )
            label = self.node_labels[i] if i < len(self.node_labels) else str(i)
            self.canvas.create_text(
                x + box_width/2, y_pos + box_height/2,
                text=label, 
                font=("Arial", 10, "bold"),
                fill="black",
                tags="initial_nodes"
            )

    def _draw_order_arrays(self, left_text_area):
        self.canvas.delete("order_arrays")
        w = self.canvas.winfo_width() or 700
        h = self.canvas.winfo_height() or 500

        self.pre_order_boxes = []
        self.post_order_boxes = []

        box_width = 30
        box_height = 30
        margin = 10

        y_pre = h - 2*(box_height + margin) - 20
        y_post = h - (box_height + margin) - 20

        usable_width = w - left_text_area
        total_width = self.num_nodes * (box_width + margin)
        start_x = left_text_area + (usable_width - total_width) / 2

        # Pre-order
        self.canvas.create_text(
            start_x - 5, y_pre + box_height/2, 
            text="Pre-order:", 
            anchor="e", 
            font=("Arial", 10, "bold"), 
            fill="black", 
            tags="order_arrays"
        )
        for i in range(self.num_nodes):
            x = start_x + i * (box_width + margin)
            box_id = self.canvas.create_rectangle(
                x, y_pre, x + box_width, y_pre + box_height,
                fill="white", outline="black", 
                tags="order_arrays"
            )
            text_id = self.canvas.create_text(
                x + box_width/2, y_pre + box_height/2, 
                text="", font=("Arial", 10), fill="black", 
                tags="order_arrays"
            )
            self.pre_order_boxes.append((box_id, text_id))

        # Post-order
        self.canvas.create_text(
            start_x - 5, y_post + box_height/2, 
            text="Post-order:", 
            anchor="e", 
            font=("Arial", 10, "bold"), 
            fill="black", 
            tags="order_arrays"
        )
        for i in range(self.num_nodes):
            x = start_x + i * (box_width + margin)
            box_id = self.canvas.create_rectangle(
                x, y_post, x + box_width, y_post + box_height,
                fill="white", outline="black", 
                tags="order_arrays"
            )
            text_id = self.canvas.create_text(
                x + box_width/2, y_post + box_height/2, 
                text="", font=("Arial", 10), fill="black", 
                tags="order_arrays"
            )
            self.post_order_boxes.append((box_id, text_id))

        self._update_pre_order_visualization()
        self._update_post_order_visualization()

    def _draw_directed_edge(self, i, j, color="black"):
        x1, y1 = self.node_positions.get(i, (0,0))
        x2, y2 = self.node_positions.get(j, (0,0))
        dx, dy = x2 - x1, y2 - y1
        length = math.sqrt(dx*dx + dy*dy)

        if length > 0:
            udx, udy = dx/length, dy/length
            x2 -= udx*20
            y2 -= udy*20
            x1 += udx*20
            y1 += udy*20

        return self.canvas.create_line(
            x1, y1, x2, y2, fill=color, width=2, arrow=tk.LAST
        )

    def _on_canvas_resize(self, event):
        if self.node_positions:
            self._draw_order_arrays(left_text_area=200)
            self._draw_initial_nodes_array(left_text_area=200)
            self._update_pre_order_visualization()
            self._update_post_order_visualization()

    ###########################################################################
    # DFS Steps
    ###########################################################################
    def dfs_steps(self, start_idx):
        visited = set()
        stack = [start_idx]

        visited.add(start_idx)
        self.pre_order_list.append(self.node_labels[start_idx])
        yield ("visit", start_idx)

        neighbor_index_map = {i: 0 for i in range(self.num_nodes)}

        while stack:
            current = stack[-1]
            neighbors = self.adjacency_indexed[current]

            labeled_neighbors = []
            for nb in neighbors:
                lbl = self.node_labels[nb]
                try:
                    val = int(lbl)
                except ValueError:
                    val = lbl
                labeled_neighbors.append((nb, val))
            labeled_neighbors.sort(key=lambda x: x[1])

            idx_next = neighbor_index_map[current]
            if idx_next < len(labeled_neighbors):
                (neighbor, _) = labeled_neighbors[idx_next]
                neighbor_index_map[current] += 1

                yield ("edge", current, neighbor)
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append(neighbor)
                    self.pre_order_list.append(self.node_labels[neighbor])
                    yield ("visit", neighbor)
                else:
                    # Add a specific yield for already visited nodes
                    yield ("already_visited", current, neighbor)
            else:
                stack.pop()
                self.post_order_list.append(self.node_labels[current])
                yield ("completed", current)

    def estimate_dfs_steps(self, start_idx):
        """
        More accurately estimate the number of explanation lines by simulating the DFS traversal
        """
        # We'll simulate the actual traversal for accurate count
        visited = set()
        stack = [start_idx]
        step_count = 0
        
        # Count initial visit
        visited.add(start_idx)
        step_count += 1  # "Visiting node X" line
        
        neighbor_index_map = {i: 0 for i in range(self.num_nodes)}
        
        while stack:
            current = stack[-1]
            neighbors = self.adjacency_indexed[current]
            
            # Sort neighbors to match the actual traversal
            labeled_neighbors = []
            for nb in neighbors:
                lbl = self.node_labels[nb]
                try:
                    val = int(lbl)
                except ValueError:
                    val = lbl
                labeled_neighbors.append((nb, val))
            labeled_neighbors.sort(key=lambda x: x[1])
            
            idx_next = neighbor_index_map[current]
            if idx_next < len(labeled_neighbors):
                neighbor = labeled_neighbors[idx_next][0]
                neighbor_index_map[current] += 1
                
                step_count += 1  # "Check path from X → Y" line
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append(neighbor)
                    step_count += 1  # "Visiting node X" line
                else:
                    step_count += 1  # "Node X already visited" line
            else:
                stack.pop()
                step_count += 1  # "No more unseen paths from X" line
        
        # Add one more for "DFS complete!" line
        step_count += 1
        
        return step_count

    ###########################################################################
    # Step-by-step Visualization
    ###########################################################################
    def visualize_step(self):
        if self.paused or not self.dfs_generator:
            return
        try:
            event = next(self.dfs_generator)

            if event[0] == "visit":
                _, idx = event
                self._color_node(idx, "red")
                self._update_pre_order_visualization()
                label = self.node_labels[idx]
                self._log_step(f"Visiting node {label} (new path).")

            elif event[0] == "edge":
                _, i, j = event
                self._color_node(i, "lightgreen")
                self._highlight_edge(i, j, "red")
                self._halo_node(j)
                label_i = self.node_labels[i]
                label_j = self.node_labels[j]
                self._log_step(f"Check path from {label_i} → {label_j} (next smallest).")
                
            elif event[0] == "already_visited":
                _, i, j = event
                label_i = self.node_labels[i]
                label_j = self.node_labels[j]
                self._log_step(f"Node {label_j} already visited, try next node.")

            elif event[0] == "completed":
                _, idx = event
                self._color_node(idx, "darkgreen")
                self._update_post_order_visualization()
                label = self.node_labels[idx]
                self._halo_node(None)
                self._log_step(f"No more unseen paths from {label}, dead end. Backtrack.")

        except StopIteration:
            self._halo_node(None)
            for edge_pair, line_id in self.edge_lines.items():
                self.canvas.itemconfig(line_id, fill="green", width=2)
            self._log_step("DFS complete! All nodes processed.")
            return

        self.after(self.current_delay, self.visualize_step)

    ###########################################################################
    # Update Pre/Post-Order
    ###########################################################################
    def _update_pre_order_visualization(self):
        for i, label in enumerate(self.pre_order_list):
            if i < len(self.pre_order_boxes):
                box_id, text_id = self.pre_order_boxes[i]
                self.canvas.itemconfig(text_id, text=label)
                self.canvas.itemconfig(box_id, fill="#e0ffe0")

    def _update_post_order_visualization(self):
        for i, label in enumerate(self.post_order_list):
            if i < len(self.post_order_boxes):
                box_id, text_id = self.post_order_boxes[i]
                self.canvas.itemconfig(text_id, text=label)
                self.canvas.itemconfig(box_id, fill="#e0e0ff")

    ###########################################################################
    # Coloring / Highlighting
    ###########################################################################
    def _color_node(self, idx, color):
        if idx in self.node_circles:
            c_id, _ = self.node_circles[idx]
            self.canvas.itemconfig(c_id, fill=color)

    def _halo_node(self, idx):
        if self.node_halo is not None:
            self.canvas.delete(self.node_halo)
            self.node_halo = None
            self.halo_node = None
        if idx is None:
            return
        x, y = self.node_positions[idx]
        radius = 26
        self.node_halo = self.canvas.create_oval(
            x - radius, y - radius, x + radius, y + radius,
            outline="red", width=3, dash=(4,2)
        )

    def _highlight_edge(self, i, j, color="red"):
        if hasattr(self, 'last_edge_highlight') and self.last_edge_highlight:
            for (old_i, old_j) in self.last_edge_highlight:
                if (old_i, old_j) in self.edge_lines:
                    line_id = self.edge_lines[(old_i, old_j)]
                    self.canvas.itemconfig(line_id, fill="black", width=2)
                    self.canvas.tag_lower(line_id)
            self.last_edge_highlight = None

        if (i, j) in self.edge_lines:
            line_id = self.edge_lines[(i, j)]
            self.canvas.itemconfig(line_id, fill=color, width=3)
            self.canvas.tag_raise(line_id)

        self.last_edge_highlight = [(i, j)]

    ###########################################################################
    # Logging text on the left side of the same canvas
    ###########################################################################
    def _log_step(self, msg):
        """
        Draw black text on the left side of the canvas. 
        Each new message goes further down (self.text_current_y += ~20).
        """
        x_pos = 10  # Left margin inside the canvas
        
        # Use the dynamically adjusted font size
        font_size = getattr(self, 'explanation_font_size', 10)
        
        self.canvas.create_text(
            x_pos, self.text_current_y,
            anchor="nw",
            text=msg,
            fill="black",
            font=("Arial", font_size)
        )
        
        # Adjust line spacing based on font size
        line_spacing = font_size + 10  # 10px padding plus font size
        self.text_current_y += line_spacing

    def adjust_explanation_font_size(self, estimated_steps):
        """
        Calculate the exact font size needed to fit all explanation lines in the available canvas height,
        maximizing the font size to use the available space effectively.
        """
        canvas_height = self.canvas.winfo_height() or 500
        
        # Reserve space for node array at top (~50px) and order arrays at bottom (~120px)
        available_height = canvas_height - 170
        
        # Calculate the ideal font size that would use the entire available height
        # Formula: available_height = estimated_steps * (font_size + 10)
        # Solve for font_size
        ideal_font_size = (available_height / estimated_steps) - 10
        
        # Clamp the font size between 8 and 14 points for readability
        font_size = max(8, min(14, int(ideal_font_size)))
        
        # Store the calculated font size
        self.explanation_font_size = font_size

# Test run
if __name__ == "__main__":
    root = tk.Tk()
    root.title("DFS in One Canvas (Left Text, Right Graph)")
    tab = DepthFirstSearchTab(root)
    tab.pack(expand=True, fill="both")
    root.mainloop()
