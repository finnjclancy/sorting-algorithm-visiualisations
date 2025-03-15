# main.py
import tkinter as tk
from tkinter import ttk
import bubble_sort    # Bubble sort module.
import selection_sort # New selection sort module.
import insertion_sort # New insertion sort module.
import merge_sort     # New merge sort module.
import quick_sort     # New quick sort module.
# Create the main application window.
root = tk.Tk()
root.title("Algorithm Visualizer")

# Create a Notebook widget (tabs container).
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both')

# Create and add the Bubble Sort tab.
bubble_tab = bubble_sort.BubbleSortTab(notebook)
notebook.add(bubble_tab, text="Bubble Sort")

# Create and add the Selection Sort tab.
selection_tab = selection_sort.SelectionSortTab(notebook)
notebook.add(selection_tab, text="Selection Sort")

# Create and add the Insertion Sort tab.
insertion_tab = insertion_sort.InsertionSortTab(notebook)
notebook.add(insertion_tab, text="Insertion Sort")

# Create and add the Merge Sort tab.
merge_tab = merge_sort.MergeSortTab(notebook)
notebook.add(merge_tab, text="Merge Sort")

# Create and add the Quick Sort tab.
quick_tab = quick_sort.QuickSortTab(notebook)
notebook.add(quick_tab, text="Quick Sort")


# You can add more algorithm tabs here if needed.
# For example, placeholders for other algorithms:
algorithms = [
    "Breadth First Search",
    "Depth First Search", "Bellman Ford", "Djikstra's", "Prim's",
    "Kruskal's", "Topological Sort", "A*", "Greedy Best First"
]
for algo in algorithms:
    frame = ttk.Frame(notebook)
    label = tk.Label(frame, text=f"{algo} visualization not implemented yet.", font=("Arial", 14))
    label.pack(expand=True, padx=20, pady=20)
    notebook.add(frame, text=algo)

# Add watermark label at the bottom-right of the window.
watermark = tk.Label(root, text="finn clancy 2025", font=("Arial", 8), fg="#a0a0a0")
watermark.place(relx=1.0, rely=1.0, anchor="se")

# Start the main loop.
root.mainloop()
