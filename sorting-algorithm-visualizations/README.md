# Algorithm Visualizer

A web-based visualization tool for algorithms, converted from a Python/Tkinter application to a Next.js web application.

## Features

- **Sorting Algorithms**:
  - Bubble Sort
  - Selection Sort (coming soon)
  - Insertion Sort (coming soon)
  - Merge Sort (coming soon)
  - Quick Sort (coming soon)

- **Graph Traversal**:
  - Breadth-First Search (BFS)
  - Depth-First Search (DFS) (coming soon)

- **Coming Soon**:
  - Shortest Path Algorithms (Dijkstra's, Bellman-Ford, A*)
  - Minimum Spanning Tree Algorithms (Prim's, Kruskal's)
  - Other Graph Algorithms (Topological Sort, Greedy Best First Search)

## Technologies Used

- Next.js
- React
- TypeScript
- Tailwind CSS
- Framer Motion (for animations)
- React Konva (for canvas-based visualizations)

## Getting Started

1. Clone the repository
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```
4. Open [http://localhost:3000](http://localhost:3000) in your browser

## Usage

- Select an algorithm from the home page
- Adjust parameters like array size, speed, etc.
- Click "Play" to start the visualization
- Use the controls to pause, restart, or generate new data

## Project Structure

- `/src/app`: Next.js app router pages
- `/src/components`: Reusable React components
- `/src/lib/algorithms`: Algorithm implementations
  - `/sorting.ts`: Sorting algorithm implementations
  - `/traversal.ts`: Graph traversal algorithm implementations

## Credits

Originally created by Finn Clancy (2025) as a Python/Tkinter application, converted to a Next.js web application.
