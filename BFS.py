import tkinter as tk
from tkinter import ttk, messagebox
import math
from collections import deque

class BreadthFirstSearchTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        #######################################################################
        # Style / Dark background for frames/labels, but white canvas for BFS
        #######################################################################
        style = ttk.Style()
        style.configure("Dark.TFrame", background="#424242")
        style.configure("Dark.TLabel", background="#424242", foreground="white")
        style.configure("Dark.TButton", background="#424242", foreground="white")
        style.configure("Dark.TCheckbutton", background="#424242")
        # For radiobuttons as well
        style.configure("Dark.TRadiobutton", background="#424242", foreground="white")

        self.configure(style="Dark.TFrame")

        #######################################################################
        # Heading
        #######################################################################
        self.heading = tk.Label(
            self, text="Breadth First Search", font=("Arial", 24, "bold"),
            bg="#424242", fg="white"
        )
        self.heading.pack(pady=10, fill="x")

        #######################################################################
        # Main container: left (inputs), right (BFS)
        #######################################################################
        self.main_frame = ttk.Frame(self, style="Dark.TFrame")
        self.main_frame.pack(expand=True, fill="both")

        self.main_frame.columnconfigure(0, weight=3)  # ~30%
        self.main_frame.columnconfigure(1, weight=7)  # ~70%
        self.main_frame.rowconfigure(0, weight=1)

        self.left_frame = ttk.Frame(self.main_frame, style="Dark.TFrame")
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.right_frame = ttk.Frame(self.main_frame, style="Dark.TFrame")
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        #######################################################################
        # Data structures
        #######################################################################
        self.num_nodes = 0
        self.node_labels = []        # Possibly duplicated user labels
        self.node_label_entries = [] # The text fields for node names

        self.adj_type_var = tk.StringVar(value="matrix")
        self.adjacency_matrix_vars = []   # 2D of BooleanVar
        self.adjacency_list_entries = []  # 2D of Entries
        self.adjacency_indexed = {}       # int -> list(int) (directed edges)

        # BFS
        self.current_delay = 2000  # Slower BFS for clarity
        self.paused = False
        self.bfs_generator = None
        self.pre_order_list = []
        self.post_order_list = []

        # Graph drawing
        self.node_positions = {}    # index -> (x,y)
        self.node_circles = {}      # index -> (circle_id, text_id)
        self.node_halo = None       # extra circle for highlight
        self.halo_node = None
        # Store edges as well: (i->j) => line ID, so we can highlight them red
        self.edge_lines = {}        # (i, j) -> line_id

        #######################################################################
        # Build the left adjacency area
        #######################################################################
        self._build_left_inputs()

        #######################################################################
        # Build the right BFS controls + white canvas
        #######################################################################
        self._build_right_bfs_area()

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

        # adjacency type
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

        # Generate button only - Refresh moved to below node labels
        gen_btn = ttk.Button(input_top, text="Generate Fields", command=self.generate_adjacency_fields,
                             style="Dark.TButton")
        gen_btn.grid(row=3, column=0, columnspan=2, padx=5, pady=5)  # Span both columns now

        self.adjacency_frame = ttk.Frame(self.left_frame, style="Dark.TFrame")
        self.adjacency_frame.pack(anchor="nw", fill="both", expand=True, pady=5)

    def clear_adjacency_fields(self):
        """Remove adjacency widgets so we can rebuild them."""
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
                 bg="#424242", fg="white").pack(anchor="w")

        row_label_frame = ttk.Frame(label_frame, style="Dark.TFrame")
        row_label_frame.pack(side="top", anchor="w")

        for i in range(self.num_nodes):
            ent = ttk.Entry(row_label_frame, width=7)
            ent.pack(side="left", padx=5)
            self.node_label_entries.append(ent)
        
        # Add refresh button below the labels
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
                       bg="#424242", fg="white")
        lbl.pack(anchor="center", pady=5)

        container = ttk.Frame(self.adjacency_frame, style="Dark.TFrame")
        container.pack(anchor="center")

        # 2D Booleans
        for r in range(self.num_nodes):
            row_vars = []
            for c in range(self.num_nodes):
                row_vars.append(tk.BooleanVar(value=False))
            self.adjacency_matrix_vars.append(row_vars)

        # single grid approach
        corner = tk.Label(container, text="", width=7, bg="#424242")
        corner.grid(row=0, column=0, padx=5, pady=5)

        self.matrix_col_labels = []
        for c in range(self.num_nodes):
            lbl_c = tk.Label(container, text="", width=7, bg="#424242", fg="white",
                             font=("Arial", 9, "bold"), anchor="center")
            lbl_c.grid(row=0, column=c+1, padx=5, pady=5)
            self.matrix_col_labels.append(lbl_c)

        self.matrix_row_labels = []
        for r in range(self.num_nodes):
            lbl_r = tk.Label(container, text="", width=7, bg="#424242", fg="white",
                             font=("Arial", 9, "bold"), anchor="e")
            lbl_r.grid(row=r+1, column=0, padx=5, pady=5)
            self.matrix_row_labels.append(lbl_r)

            for c in range(self.num_nodes):
                var = self.adjacency_matrix_vars[r][c]
                cb = ttk.Checkbutton(container, variable=var, style="Dark.TCheckbutton")
                cb.grid(row=r+1, column=c+1, padx=5, pady=5)

    def build_list_inputs(self):
        lbl = tk.Label(self.adjacency_frame, text="Adjacency List", font=("Arial", 10, "bold"),
                       bg="#424242", fg="white")
        lbl.pack(anchor="w", pady=5)

        container = ttk.Frame(self.adjacency_frame, style="Dark.TFrame")
        container.pack()

        heading_lbl = tk.Label(container, text="Edges", font=("Arial", 9, "bold"),
                               bg="#424242", fg="white")
        heading_lbl.grid(row=0, column=1, padx=5, pady=5)

        for r in range(self.num_nodes):
            row_lbl = tk.Label(container, text="", width=7, bg="#424242", fg="white",
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
    # RIGHT: BFS + White Canvas
    ###########################################################################
    def _build_right_bfs_area(self):
        self.right_frame.rowconfigure(2, weight=0)
        self.right_frame.columnconfigure(0, weight=1)

        # row0: BFS start + pre/post
        top_frame = ttk.Frame(self.right_frame, style="Dark.TFrame")
        top_frame.grid(row=0, column=0, sticky="w", pady=5)

        # Add starting index input
        start_frame = ttk.Frame(top_frame, style="Dark.TFrame")
        start_frame.pack(side="left", padx=5)
        
        ttk.Label(start_frame, text="Starting Index:", style="Dark.TLabel").pack(side="left")
        self.start_index_entry = ttk.Entry(start_frame, width=5)
        self.start_index_entry.pack(side="left", padx=5)
        self.start_index_entry.insert(0, "0")  # Default to 0
        
        start_btn = ttk.Button(start_frame, text="Start Search", command=self.start_bfs,
                               style="Dark.TButton")
        start_btn.pack(side="left", padx=5)

        order_frame = ttk.Frame(top_frame, style="Dark.TFrame")
        order_frame.pack(side="left", padx=20)

        # row1: speed & pause
        control_frame = ttk.Frame(self.right_frame, style="Dark.TFrame")
        control_frame.grid(row=1, column=0, sticky="w", pady=5)

        ttk.Button(control_frame, text="Slow", command=lambda: self.set_speed(3000), style="Dark.TButton")\
            .pack(side='left', padx=5)
        ttk.Button(control_frame, text="Medium", command=lambda: self.set_speed(2000), style="Dark.TButton")\
            .pack(side='left', padx=5)
        ttk.Button(control_frame, text="Fast", command=lambda: self.set_speed(700), style="Dark.TButton")\
            .pack(side='left', padx=5)

        self.pause_play_button = ttk.Button(control_frame, text="Pause", command=self.toggle_pause,
                                            style="Dark.TButton")
        self.pause_play_button.pack(side='left', padx=5)

        # row2: White canvas
        self.canvas = tk.Canvas(self.right_frame, bg="white", width=700, height=500, highlightthickness=0)
        self.canvas.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

        # Add canvas resize event to update array positions
        self.canvas.bind("<Configure>", self._on_canvas_resize)
        
        # Make sure the row containing the canvas can expand
        self.right_frame.rowconfigure(2, weight=1)

    def set_speed(self, delay):
        self.current_delay = delay

    def toggle_pause(self):
        self.paused = not self.paused
        self.pause_play_button.config(text="Play" if self.paused else "Pause")
        if not self.paused:
            self.visualize_step()

    ###########################################################################
    # BFS Start
    ###########################################################################
    def start_bfs(self):
        # Reset BFS data
        self.pre_order_list.clear()
        self.post_order_list.clear()  # Keep this to reset the list, but not the label
        
        self.canvas.delete("all")
        self.node_positions.clear()
        self.node_circles.clear()
        self.node_halo = None
        self.halo_node = None
        self.edge_lines.clear()

        # Build adjacency from matrix or list
        if not self.build_indexed_adjacency():
            return

        # Draw
        self.draw_graph_initial()

        # Get starting index from entry
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

        # BFS from specified start node
        if self.num_nodes > 0:
            # Initialize distances
            self.distances = {i: float('inf') for i in range(self.num_nodes)}
            self.distances[start_idx] = 0
            
            # Draw distance array
            self._draw_distance_array()
            
            # Start BFS
            self.bfs_generator = self.bfs_steps(start_idx)
            self.after(self.current_delay, self.visualize_step)
        else:
            self.bfs_generator = None

    def build_indexed_adjacency(self):
        """Read adjacency; treat each row->col check as a directed edge r->c."""
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
                        # find index with that label
                        matches = [idx for idx, lab in enumerate(self.node_labels) if lab == typed]
                        if not matches:
                            messagebox.showerror(
                                "Invalid Label",
                                f"Node {r} typed '{typed}' but no node has that label."
                            )
                            return False
                        # take first match
                        self.adjacency_indexed[r].append(matches[0])

        return True

    ###########################################################################
    # Drawing: White Canvas
    ###########################################################################
    def draw_graph_initial(self):
        """Draw nodes in a circle, color them gray. 
           Store each directed edge in edge_lines so we can highlight them.
        """
        w = self.canvas.winfo_width() or 700
        h = self.canvas.winfo_height() or 500
        
        # Draw the initial node array at the top
        self._draw_initial_nodes_array()
        
        # Center coordinates, adjust to account for the distance array on the left
        # Move down to account for the initial nodes array at top
        cx = w//2 + 30  # Shift right by 30 pixels to account for the distance array
        cy = h//2 - 20  # Adjusted to account for initial array at top
        
        # Increase the radius by reducing the subtractions
        radius = min(cx - 60, cy - 40) - 30  # Less reduction to make the graph bigger

        n = self.num_nodes
        if n < 1:
            return

        # place nodes in circle
        if n == 1:
            self.node_positions[0] = (cx, cy)
        else:
            angle_step = 2*math.pi / n
            for i in range(n):
                angle = i * angle_step
                x = cx + radius * math.cos(angle)
                y = cy + radius * math.sin(angle)
                self.node_positions[i] = (x, y)

        # draw edges
        for i in range(n):
            for j in self.adjacency_indexed[i]:
                line_id = self._draw_directed_edge(i, j, color="black")  
                # store in dictionary
                self.edge_lines[(i, j)] = line_id

        # draw nodes (gray)
        for i, (nx, ny) in self.node_positions.items():
            c_id = self.canvas.create_oval(nx-20, ny-20, nx+20, ny+20,
                                           fill="gray", outline="black", width=2)
            label = self.node_labels[i] if i < len(self.node_labels) else str(i)
            t_id = self.canvas.create_text(nx, ny, text=label, font=("Arial", 10, "bold"))
            self.node_circles[i] = (c_id, t_id)

        # Create empty boxes for pre-order and post-order
        self._draw_order_arrays()
        
        # Create distance array visualization
        self._draw_distance_array()

    def _draw_directed_edge(self, i, j, color="black"):
        """Draw arrow from i->j in the given color, return line_id."""
        x1, y1 = self.node_positions[i]
        x2, y2 = self.node_positions[j]
        
        # Calculate the direction vector
        dx, dy = x2 - x1, y2 - y1
        length = math.sqrt(dx*dx + dy*dy)
        
        # Normalize and scale to ensure arrow doesn't go into the node circle
        if length > 0:
            udx, udy = dx/length, dy/length
            # Adjust endpoints to stop at the circle edge (radius 20)
            x2, y2 = x2 - udx*20, y2 - udy*20
            x1, y1 = x1 + udx*20, y1 + udy*20
        
        return self.canvas.create_line(
            x1, y1, x2, y2, fill=color, width=2, arrow=tk.LAST
        )

    def _draw_order_arrays(self):
        """Draw empty boxes for pre-order at the bottom of the canvas."""
        # Clear any existing arrays
        self.canvas.delete("order_arrays")
        
        w = self.canvas.winfo_width() or 700
        h = self.canvas.winfo_height() or 500
        
        # Initialize arrays to store the box IDs for updating later
        self.pre_order_boxes = []
        # self.post_order_boxes = []  # Comment out post-order boxes
        
        # Set dimensions for the boxes
        box_width = 30
        box_height = 30
        margin = 10
        y_pre = h - box_height - margin - 20  # Adjust since we only have one row now
        # y_post = h - box_height - margin  # Comment out
        
        # Calculate starting x coordinate to center the arrays
        start_x = (w - (self.num_nodes * (box_width + margin))) / 2
        
        # Draw "Pre-order:" label with black text right next to the first box
        self.canvas.create_text(
            start_x - 5, y_pre + box_height/2, 
            text="Pre-order:", 
            anchor="e", 
            font=("Arial", 10, "bold"), 
            fill="black", 
            tags="order_arrays"
        )
        
        # Comment out post-order label
        # self.canvas.create_text(
        #     start_x - 5, y_post + box_height/2, 
        #     text="Post-order:", 
        #     anchor="e", 
        #     font=("Arial", 10, "bold"), 
        #     fill="black", 
        #     tags="order_arrays"
        # )
        
        # Draw empty boxes for pre-order
        for i in range(self.num_nodes):
            x = start_x + i * (box_width + margin)
            box_id = self.canvas.create_rectangle(x, y_pre, x + box_width, y_pre + box_height,
                                                fill="white", outline="black", tags="order_arrays")
            text_id = self.canvas.create_text(x + box_width/2, y_pre + box_height/2, 
                                            text="", font=("Arial", 10), fill="black", tags="order_arrays")
            self.pre_order_boxes.append((box_id, text_id))
        
        # Comment out post-order boxes
        # Draw empty boxes for post-order
        # for i in range(self.num_nodes):
        #     x = start_x + i * (box_width + margin)
        #     box_id = self.canvas.create_rectangle(x, y_post, x + box_width, y_post + box_height,
        #                                         fill="white", outline="black", tags="order_arrays")
        #     text_id = self.canvas.create_text(x + box_width/2, y_post + box_height/2, 
        #                                     text="", font=("Arial", 10), fill="black", tags="order_arrays")
        #     self.post_order_boxes.append((box_id, text_id))
        
        # Immediately update with current values
        self._update_pre_order_visualization()
        # self._update_post_order_visualization()  # Comment out

    def _draw_distance_array(self):
        """Draw a vertical array showing distances from the start node to all nodes"""
        # Clear any existing distance array
        self.canvas.delete("distance_array")
        
        w = self.canvas.winfo_width() or 700
        h = self.canvas.winfo_height() or 500
        
        # Get starting index
        try:
            start_idx = int(self.start_index_entry.get())
            if start_idx < 0 or start_idx >= self.num_nodes:
                start_idx = 0
        except (ValueError, AttributeError):
            start_idx = 0
        
        # Make sure distances is initialized
        if not hasattr(self, 'distances') or self.distances is None:
            self.distances = {i: float('inf') for i in range(self.num_nodes)}
            self.distances[start_idx] = 0
        
        # Initialize array to store box IDs
        self.distance_boxes = []
        
        # Set dimensions for the boxes
        box_width = 40
        box_height = 30
        margin = 5
        x_pos = 70  # Fixed position on the left side
        
        # Draw "Distances from node X:" label
        self.canvas.create_text(
            x_pos, 20, 
            text=f"Distances from node {self.node_labels[start_idx]}:", 
            anchor="n", 
            font=("Arial", 11, "bold"), 
            fill="black",
            tags="distance_array"
        )
        
        # Draw column header (starting node label)
        self.canvas.create_rectangle(
            x_pos, 50, 
            x_pos + box_width, 50 + box_height,
            fill="#e0e0e0", outline="black", 
            tags="distance_array"
        )
        self.canvas.create_text(
            x_pos + box_width/2, 50 + box_height/2,
            text=self.node_labels[start_idx], 
            font=("Arial", 10, "bold"),
            fill="black",
            tags="distance_array"
        )
        
        # Draw vertical array (skip starting index)
        row = 0
        for i in range(self.num_nodes):
            if i == start_idx:  # Skip the starting index
                continue
            
            y = 50 + (row + 1) * (box_height + margin)
            row += 1
            
            # Row label (node)
            self.canvas.create_rectangle(
                x_pos - box_width - margin, y, 
                x_pos - margin, y + box_height,
                fill="#e0e0e0", outline="black", 
                tags="distance_array"
            )
            self.canvas.create_text(
                x_pos - box_width/2 - margin, y + box_height/2,
                text=self.node_labels[i], 
                font=("Arial", 10),
                fill="black",
                tags="distance_array"
            )
            
            # Distance value
            box_id = self.canvas.create_rectangle(
                x_pos, y, 
                x_pos + box_width, y + box_height,
                fill="white", outline="black", 
                tags="distance_array"
            )
            
            # Display the distance (infinity as "∞")
            dist_text = "∞" if self.distances[i] == float('inf') else str(self.distances[i])
            text_id = self.canvas.create_text(
                x_pos + box_width/2, y + box_height/2,
                text=dist_text, 
                font=("Arial", 10),
                fill="black",
                tags="distance_array"
            )
            
            self.distance_boxes.append((box_id, text_id, i))

    def update_distance_visualization(self):
        """Update the distance array visualization with current distances"""
        if not hasattr(self, 'distance_boxes') or not self.distance_boxes:
            return
        
        for box_id, text_id, node_idx in self.distance_boxes:
            # Display the distance (infinity as "∞")
            dist_text = "∞" if self.distances[node_idx] == float('inf') else str(self.distances[node_idx])
            self.canvas.itemconfig(text_id, text=dist_text)
            
            # Color code based on distance
            if self.distances[node_idx] == float('inf'):
                self.canvas.itemconfig(box_id, fill="white")
            else:
                # Color gradient based on distance
                intensity = max(0, 255 - self.distances[node_idx] * 40)
                color = f"#{intensity:02x}{intensity:02x}ff"
                self.canvas.itemconfig(box_id, fill=color)

    def visualize_step(self):
        if self.paused or not self.bfs_generator:
            return
        try:
            event = next(self.bfs_generator)
            if event[0] == "visit":
                # event = ("visit", node_idx)
                _, idx = event
                self._color_node(idx, "lightgreen")
                # Don't highlight node with halo when first visiting
                # self._halo_node(idx)
                
                # Update pre-order list and visualization (bottom only)
                self._update_pre_order_visualization()
                
                # Update distance visualization
                self.update_distance_visualization()
                
            elif event[0] == "edge":
                # event = ("edge", i, j)
                _, i, j = event
                
                # Make the source node dark green
                self._color_node(i, "darkgreen")
                
                # Highlight the edge
                self._highlight_edge(i, j, "red")
                
                # Put red circle around the destination node
                self._halo_node(j)
            
            elif event[0] == "completed":
                # event = ("completed", node_idx)
                # This node has had all its outgoing edges explored
                _, idx = event
                self._color_node(idx, "red")  # Turn the node red
            
        except StopIteration:
            # BFS complete
            self._halo_node(None)
            
            # Turn all arrows green when BFS is done
            for edge_pair, line_id in self.edge_lines.items():
                self.canvas.itemconfig(line_id, fill="green", width=2)
            
            return

        self.after(self.current_delay, self.visualize_step)

    def _update_pre_order_visualization(self):
        """Update the pre-order array visualization with current values"""
        for i, label in enumerate(self.pre_order_list):
            if i < len(self.pre_order_boxes):
                box_id, text_id = self.pre_order_boxes[i]
                self.canvas.itemconfig(text_id, text=label)
                # Change box color to light green to make it more visible
                self.canvas.itemconfig(box_id, fill="#e0ffe0")

    def _update_post_order_visualization(self):
        """Update the post-order array visualization with current values"""
        for i, label in enumerate(self.post_order_list):
            if i < len(self.post_order_boxes):
                box_id, text_id = self.post_order_boxes[i]
                self.canvas.itemconfig(text_id, text=label)
                # Change box color to light blue to make it more visible
                self.canvas.itemconfig(box_id, fill="#e0e0ff")

    ###########################################################################
    # Coloring / Highlighting
    ###########################################################################
    def _color_node(self, idx, color):
        if idx not in self.node_circles:
            return
        c_id, _ = self.node_circles[idx]
        self.canvas.itemconfig(c_id, fill=color)

    def _halo_node(self, idx):
        # remove old halo
        if self.node_halo is not None:
            self.canvas.delete(self.node_halo)
            self.node_halo = None
            self.halo_node = None

        if idx is None:
            return
        self.halo_node = idx
        x, y = self.node_positions[idx]
        radius = 26
        self.node_halo = self.canvas.create_oval(
            x - radius, y - radius, x + radius, y + radius,
            outline="red", width=3, dash=(4,2)
        )

    def _highlight_edge(self, i, j, color="red"):
        """Color the edge i->j with the given color, revert the previous edge if desired."""
        # If we want to revert the last edge we changed, store it in a variable.
        if hasattr(self, 'last_edge_highlight') and self.last_edge_highlight is not None:
            # Reset any previously highlighted edges to black
            for edge_pair in self.last_edge_highlight:
                (old_i, old_j) = edge_pair
                if (old_i, old_j) in self.edge_lines:
                    line_id = self.edge_lines[(old_i, old_j)]
                    self.canvas.itemconfig(line_id, fill="black")
                    # Make sure it's at its normal z-order
                    self.canvas.tag_lower(line_id)
            self.last_edge_highlight = None

        # Only highlight the specific edge i->j, not both directions
        edges_to_highlight = [(i, j)]
        
        # Highlight the edge
        for edge_pair in edges_to_highlight:
            (from_node, to_node) = edge_pair
            if (from_node, to_node) in self.edge_lines:
                line_id = self.edge_lines[(from_node, to_node)]
                self.canvas.itemconfig(line_id, fill=color, width=3)  # Make it a bit thicker too
                # Raise the highlighted edge to the top to ensure it's visible
                self.canvas.tag_raise(line_id)
        
        # Remember highlighted edge
        self.last_edge_highlight = edges_to_highlight

    def _on_canvas_resize(self, event):
        """Redraw the order arrays when canvas is resized"""
        if hasattr(self, 'node_positions') and self.node_positions:
            self._draw_order_arrays()
            self._update_pre_order_visualization()
            self._update_post_order_visualization()

    ###########################################################################
    # BFS Steps: yields ("edge", i, j) before visiting j
    ###########################################################################
    def bfs_steps(self, start_idx):
        visited = set()
        queue = deque([start_idx])
        visited.add(start_idx)
        
        # Track distances from start node
        self.distances = {i: float('inf') for i in range(self.num_nodes)}
        self.distances[start_idx] = 0

        # Mark start as visited
        self.pre_order_list.append(self.node_labels[start_idx])
        yield ("visit", start_idx)

        while queue:
            current = queue.popleft()
            
            # Get all neighbors of current node
            neighbors = self.adjacency_indexed[current]
            
            # Create a list of (neighbor_idx, neighbor_label) pairs for sorting
            # Try to convert labels to integers for proper numeric sorting if possible
            neighbor_info = []
            for neighbor in neighbors:
                label = self.node_labels[neighbor]
                # Try to convert to int for numeric comparison
                try:
                    value = int(label)
                except ValueError:
                    value = label  # Keep as string if not convertible
                neighbor_info.append((neighbor, value))
            
            # Sort neighbors by their values (ascending)
            neighbor_info.sort(key=lambda x: x[1])
            
            # Now process neighbors in sorted order
            for neighbor, _ in neighbor_info:
                # We'll highlight the edge from current->neighbor in red first
                yield ("edge", current, neighbor)

                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    # Update distance to this node
                    self.distances[neighbor] = self.distances[current] + 1
                    self.pre_order_list.append(self.node_labels[neighbor])
                    yield ("visit", neighbor)
            
            # After processing all neighbors, mark the current node as "completed"
            yield ("completed", current)

    def _draw_initial_nodes_array(self):
        """Draw the initial node array at the top of the canvas"""
        # Clear any existing nodes array
        self.canvas.delete("initial_nodes")
        
        w = self.canvas.winfo_width() or 700
        
        # Set dimensions for the boxes
        box_width = 30
        box_height = 30
        margin = 10
        y_pos = 20  # Position at top
        
        # Calculate starting x position to center the array
        start_x = (w - (self.num_nodes * (box_width + margin))) / 2
        
        # Draw "Nodes:" label with black text to the left of array
        self.canvas.create_text(
            start_x - 5, y_pos + box_height/2, 
            text="Nodes:", 
            anchor="e", 
            font=("Arial", 10, "bold"), 
            fill="black", 
            tags="initial_nodes"
        )
        
        # Draw boxes for each node
        for i in range(self.num_nodes):
            x = start_x + i * (box_width + margin)
            box_id = self.canvas.create_rectangle(
                x, y_pos, x + box_width, y_pos + box_height,
                fill="#e0e0e0", outline="black", 
                tags="initial_nodes"
            )
            
            # Node label
            label = self.node_labels[i] if i < len(self.node_labels) else str(i)
            self.canvas.create_text(
                x + box_width/2, y_pos + box_height/2,
                text=label, 
                font=("Arial", 10, "bold"),
                fill="black",
                tags="initial_nodes"
            )


# Test
if __name__ == "__main__":
    root = tk.Tk()
    root.title("BFS: White Box + Edge in Red")
    tab = BreadthFirstSearchTab(root)
    tab.pack(expand=True, fill="both")
    root.mainloop()
