'use client';

import { useState } from 'react';
import Link from 'next/link';

export default function Home() {
  const [activeTab, setActiveTab] = useState('sorting');

  const tabs = [
    { id: 'sorting', label: 'Sorting Algorithms' },
    { id: 'traversal', label: 'Graph Traversal' },
    { id: 'shortest', label: 'Shortest Path' },
    { id: 'mst', label: 'Minimum Spanning Tree' },
    { id: 'other', label: 'Other Graph Algorithms' },
  ];

  const algorithms = {
    sorting: [
      { id: 'bubble', name: 'Bubble Sort', implemented: true },
      { id: 'selection', name: 'Selection Sort', implemented: true },
      { id: 'insertion', name: 'Insertion Sort', implemented: true },
      { id: 'merge', name: 'Merge Sort', implemented: true },
      { id: 'quick', name: 'Quick Sort', implemented: true },
    ],
    traversal: [
      { id: 'bfs', name: 'Breadth First Search', implemented: true },
      { id: 'dfs', name: 'Depth First Search', implemented: true },
    ],
    shortest: [
      { id: 'dijkstra', name: 'Dijkstra\'s Algorithm', implemented: false },
      { id: 'bellman-ford', name: 'Bellman-Ford Algorithm', implemented: false },
      { id: 'astar', name: 'A* Search', implemented: false },
    ],
    mst: [
      { id: 'prim', name: 'Prim\'s Algorithm', implemented: false },
      { id: 'kruskal', name: 'Kruskal\'s Algorithm', implemented: false },
    ],
    other: [
      { id: 'topological', name: 'Topological Sort', implemented: false },
      { id: 'greedy', name: 'Greedy Best First Search', implemented: false },
    ],
  };

  return (
    <div className="max-w-6xl mx-auto">
      <h1 className="text-4xl font-bold mb-8 text-center">Algorithm Visualizer</h1>
      
      <div className="mb-8">
        <div className="flex flex-wrap border-b border-gray-700">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              className={`px-4 py-2 font-medium ${
                activeTab === tab.id
                  ? 'text-white border-b-2 border-white'
                  : 'text-gray-400 hover:text-white'
              }`}
              onClick={() => setActiveTab(tab.id)}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {algorithms[activeTab as keyof typeof algorithms].map((algo) => (
          <div
            key={algo.id}
            className="bg-gray-800 rounded-lg p-6 hover:shadow-lg transition-all"
          >
            <h3 className="text-xl font-semibold mb-4">{algo.name}</h3>
            {algo.implemented ? (
              <Link
                href={`/${activeTab}/${algo.id}`}
                className="bg-blue-500 hover:bg-blue-600 px-4 py-2 rounded inline-block"
              >
                Visualize
              </Link>
            ) : (
              <span className="text-gray-400">Coming soon</span>
            )}
          </div>
        ))}
      </div>
      
      <div className="mt-12 p-6 bg-gray-800 rounded-lg">
        <h2 className="text-2xl font-bold mb-4">About This Project</h2>
        <p className="mb-4">
          This is a web-based visualization tool for algorithms, converted from a Python/Tkinter application to a Next.js web application.
          It helps students visualize how various algorithms work, making it easier to understand complex concepts.
        </p>
        <p>
          Currently implemented algorithms include Bubble Sort, Selection Sort, Insertion Sort, Quick Sort, Merge Sort, and Breadth-First Search, with more coming soon!
        </p>
      </div>
    </div>
  );
}
