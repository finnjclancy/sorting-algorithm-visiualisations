# main.py
import tkinter as tk
from tkinter import ttk
import bubble_sort    # Bubble sort module.
import selection_sort # New selection sort module.
import insertion_sort # New insertion sort module.
import merge_sort     # New merge sort module.
import quick_sort     # New quick sort module.
import BFS            # New BFS module.
import DFS            # New DFS module.

# Create the main application window.
root = tk.Tk()
root.title("Algorithm Visualizer")

# Configure style to make tabs match background color
style = ttk.Style()
bg_color = root.cget('bg')  # Get default background color

# Configure the tab appearance
style.configure('TNotebook', background='black')
style.configure('TNotebook.Tab', background='black', padding=[10, 2])
style.map('TNotebook.Tab', 
          background=[('selected', 'black'), ('active', bg_color)],
          foreground=[('selected', 'black'), ('active', 'black')])

# Configure the frame style to match
style.configure('TFrame', background='#3a3a3a')

# Create a main Notebook widget for categories
main_notebook = ttk.Notebook(root)
main_notebook.pack(expand=True, fill='both')

# Create a frame for each category
sorting_frame = ttk.Frame(main_notebook, style='TFrame')
traversal_frame = ttk.Frame(main_notebook, style='TFrame')
shortest_path_frame = ttk.Frame(main_notebook, style='TFrame')
mst_frame = ttk.Frame(main_notebook, style='TFrame')
other_frame = ttk.Frame(main_notebook, style='TFrame')

# Add category frames to the main notebook
main_notebook.add(sorting_frame, text="Sorting Algorithms")
main_notebook.add(traversal_frame, text="Graph Traversal")
main_notebook.add(shortest_path_frame, text="Shortest Path")
main_notebook.add(mst_frame, text="Minimum Spanning Tree")
main_notebook.add(other_frame, text="Other Graph Algorithms")

# Create sub-notebooks for each category
sorting_notebook = ttk.Notebook(sorting_frame)
sorting_notebook.pack(expand=True, fill='both')

traversal_notebook = ttk.Notebook(traversal_frame)
traversal_notebook.pack(expand=True, fill='both')

shortest_path_notebook = ttk.Notebook(shortest_path_frame)
shortest_path_notebook.pack(expand=True, fill='both')

mst_notebook = ttk.Notebook(mst_frame)
mst_notebook.pack(expand=True, fill='both')

other_notebook = ttk.Notebook(other_frame)
other_notebook.pack(expand=True, fill='both')

# Create and add the Sorting Algorithm tabs
bubble_tab = bubble_sort.BubbleSortTab(sorting_notebook)
sorting_notebook.add(bubble_tab, text="Bubble Sort")

selection_tab = selection_sort.SelectionSortTab(sorting_notebook)
sorting_notebook.add(selection_tab, text="Selection Sort")

insertion_tab = insertion_sort.InsertionSortTab(sorting_notebook)
sorting_notebook.add(insertion_tab, text="Insertion Sort")

merge_tab = merge_sort.MergeSortTab(sorting_notebook)
sorting_notebook.add(merge_tab, text="Merge Sort")

quick_tab = quick_sort.QuickSortTab(sorting_notebook)
sorting_notebook.add(quick_tab, text="Quick Sort")

# Create and add the Graph Traversal tabs
bfs_tab = BFS.BreadthFirstSearchTab(traversal_notebook)
traversal_notebook.add(bfs_tab, text="Breadth First Search")

dfs_tab = DFS.DepthFirstSearchTab(traversal_notebook)
traversal_notebook.add(dfs_tab, text="Depth First Search")

# Add placeholder tabs for Shortest Path algorithms
shortest_path_algorithms = [
    "Dijkstra's Algorithm", 
    "Bellman-Ford Algorithm", 
    "A* Search"
]
for algo in shortest_path_algorithms:
    frame = ttk.Frame(shortest_path_notebook, style='TFrame')
    label = tk.Label(frame, text=f"{algo} visualization not implemented yet.", font=("Arial", 14), bg=bg_color)
    label.pack(expand=True, padx=20, pady=20)
    shortest_path_notebook.add(frame, text=algo.split()[0])  # Use first word as tab title

# Add placeholder tabs for Minimum Spanning Tree algorithms
mst_algorithms = [
    "Prim's Algorithm", 
    "Kruskal's Algorithm"
]
for algo in mst_algorithms:
    frame = ttk.Frame(mst_notebook, style='TFrame')
    label = tk.Label(frame, text=f"{algo} visualization not implemented yet.", font=("Arial", 14), bg=bg_color)
    label.pack(expand=True, padx=20, pady=20)
    mst_notebook.add(frame, text=algo.split("'")[0])  # Use name before apostrophe

# Add placeholder tabs for other graph algorithms
other_algorithms = [
    "Topological Sort", 
    "Greedy Best First Search"
]
for algo in other_algorithms:
    frame = ttk.Frame(other_notebook, style='TFrame')
    label = tk.Label(frame, text=f"{algo} visualization not implemented yet.", font=("Arial", 14), bg=bg_color)
    label.pack(expand=True, padx=20, pady=20)
    other_notebook.add(frame, text=algo.split()[0])  # Use first word as tab title

# Add watermark label at the bottom-right of the window.
watermark = tk.Label(root, text="finn clancy 2025", font=("Arial", 8), fg="#a0a0a0")
watermark.place(relx=1.0, rely=1.0, anchor="se")

# Start the main loop.
root.mainloop()
