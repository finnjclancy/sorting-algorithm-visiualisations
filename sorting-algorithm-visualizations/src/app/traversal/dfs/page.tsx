'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import GraphVisualizer from '@/components/GraphVisualizer';
import { dfs, generateRandomGraph, Graph, Node, Edge } from '@/lib/algorithms/traversal';

export default function DFSPage() {
  const [graph, setGraph] = useState(generateRandomGraph(5, 0.3));
  const [steps, setSteps] = useState<ReturnType<typeof dfs>>([]);
  const [isPlaying, setIsPlaying] = useState(false);
  const [speed, setSpeed] = useState(1000);
  const [nodeCount, setNodeCount] = useState(5);
  const [edgeDensity, setEdgeDensity] = useState(0.3);
  const [startNode, setStartNode] = useState('0');
  const [isComplete, setIsComplete] = useState(false);
  const [isInitialized, setIsInitialized] = useState(false);
  
  // Custom graph input states
  const [showCustomGraph, setShowCustomGraph] = useState(false);
  const [inputType, setInputType] = useState<'matrix' | 'list'>('matrix');
  const [nodeLabels, setNodeLabels] = useState<string[]>([]);
  const [adjacencyMatrix, setAdjacencyMatrix] = useState<boolean[][]>([]);
  const [adjacencyList, setAdjacencyList] = useState<{[key: string]: string[]}>({});

  // Generate a new random graph
  const generateGraph = () => {
    if (showCustomGraph) {
      // Create graph from user input
      createCustomGraph();
    } else {
      // Create random graph
      const newGraph = generateRandomGraph(nodeCount, edgeDensity);
      setGraph(newGraph);
      
      // Ensure start node exists in the graph
      const validStartNode = newGraph.nodes.length > 0 ? 
        newGraph.nodes[0].id : '0';
      setStartNode(validStartNode);
      
      const newSteps = dfs(newGraph, validStartNode);
      setSteps(newSteps);
      setIsPlaying(false);
      setIsComplete(false);
      setIsInitialized(true);
    }
  };

  // Update steps when start node changes
  useEffect(() => {
    if (graph && graph.nodes.length > 0) {
      const newSteps = dfs(graph, startNode);
      setSteps(newSteps);
      setIsPlaying(false);
      setIsComplete(false);
      setIsInitialized(true);
    }
  }, [startNode, graph]);

  // Initialize the graph
  useEffect(() => {
    if (!showCustomGraph) {
      generateGraph();
    } else {
      // Initialize node labels and adjacency structures
      initializeCustomGraphStructures();
    }
  }, [nodeCount, edgeDensity, showCustomGraph]);

  // Initialize custom graph structures when node count changes
  const initializeCustomGraphStructures = () => {
    // Generate default node labels (0, 1, 2, etc.)
    const labels = Array.from({ length: nodeCount }, (_, i) => i.toString());
    setNodeLabels(labels);
    
    // Initialize empty adjacency matrix
    const matrix = Array.from({ length: nodeCount }, () => 
      Array.from({ length: nodeCount }, () => false)
    );
    setAdjacencyMatrix(matrix);
    
    // Initialize empty adjacency list
    const list: {[key: string]: string[]} = {};
    labels.forEach(label => {
      list[label] = [];
    });
    setAdjacencyList(list);
    
    setIsInitialized(false);
  };

  // Handle node label change
  const handleNodeLabelChange = (index: number, value: string) => {
    const newLabels = [...nodeLabels];
    newLabels[index] = value;
    setNodeLabels(newLabels);
    
    // Update the adjacency list keys
    if (inputType === 'list') {
      const newList: {[key: string]: string[]} = {};
      newLabels.forEach((label, idx) => {
        // Copy existing connections or create empty array
        newList[label] = adjacencyList[nodeLabels[idx]] || [];
      });
      setAdjacencyList(newList);
    }
  };

  // Handle adjacency matrix toggle
  const handleMatrixToggle = (row: number, col: number) => {
    const newMatrix = [...adjacencyMatrix];
    newMatrix[row][col] = !newMatrix[row][col];
    setAdjacencyMatrix(newMatrix);
  };

  // Create custom graph from user input
  const createCustomGraph = () => {
    // Create nodes in a circular layout
    const nodes: Node[] = [];
    const edges: Edge[] = [];
    const radius = 200;
    
    // Create nodes with positions in a circle
    nodeLabels.forEach((label, i) => {
      const angle = (i / nodeCount) * 2 * Math.PI;
      nodes.push({
        id: label,
        x: 250 + radius * Math.cos(angle),
        y: 250 + radius * Math.sin(angle)
      });
    });
    
    // Create edges based on input type
    if (inputType === 'matrix') {
      // Process adjacency matrix
      adjacencyMatrix.forEach((row, i) => {
        row.forEach((connected, j) => {
          if (connected) {
            edges.push({
              source: nodeLabels[i],
              target: nodeLabels[j]
            });
          }
        });
      });
    } else {
      // Process adjacency list
      Object.entries(adjacencyList).forEach(([source, targets]) => {
        targets.forEach(target => {
          // Only add if target exists in our node labels
          if (nodeLabels.includes(target)) {
            edges.push({
              source,
              target
            });
          }
        });
      });
    }
    
    const customGraph: Graph = { nodes, edges };
    setGraph(customGraph);
    
    // Set start node to first node if not in the graph
    const validStartNode = nodes.find(node => node.id === startNode)
      ? startNode
      : (nodes.length > 0 ? nodes[0].id : '0');
      
    setStartNode(validStartNode);
    
    const newSteps = dfs(customGraph, validStartNode);
    setSteps(newSteps);
    setIsPlaying(false);
    setIsComplete(false);
    setIsInitialized(true);
  };

  const handleComplete = () => {
    setIsPlaying(false);
    setIsComplete(true);
  };

  return (
    <div className="max-w-6xl mx-auto p-4">
      <div className="mb-4">
        <Link href="/" className="text-blue-400 hover:underline">
          &larr; Back to Home
        </Link>
      </div>

      <h1 className="text-4xl font-bold mb-6">Depth First Search</h1>
      
      <div className="mb-8 p-4 bg-gray-800 rounded-lg">
        <h2 className="text-xl font-semibold mb-2">Algorithm Explanation</h2>
        <p className="mb-4">
          Depth-First Search (DFS) is a graph traversal algorithm that explores as far as possible along each branch 
          before backtracking. It uses a stack data structure to keep track of vertices to be explored.
          Unlike BFS which explores all neighbors at the current depth first, DFS will go as deep as possible
          along one path before exploring alternative paths.
        </p>
        <div className="mb-2">
          <span className="font-semibold">Time Complexity:</span> O(V + E) where V is the number of vertices and E is the number of edges
        </div>
        <div>
          <span className="font-semibold">Space Complexity:</span> O(V) where V is the number of vertices
        </div>
        <div className="mt-2">
          <span className="font-semibold">Applications:</span>
          <ul className="list-disc list-inside ml-4">
            <li>Topological sorting</li>
            <li>Finding connected components</li>
            <li>Cycle detection in graphs</li>
            <li>Solving mazes and puzzles</li>
            <li>Pathfinding in artificial intelligence</li>
          </ul>
        </div>
      </div>

      <div className="mb-6 p-4 bg-gray-800 rounded-lg">
        <div className="flex gap-4 items-center mb-4">
          <div className="flex items-center">
            <input 
              type="checkbox" 
              id="customGraph" 
              checked={showCustomGraph}
              onChange={(e) => setShowCustomGraph(e.target.checked)}
              className="mr-2"
            />
            <label htmlFor="customGraph">Create custom graph</label>
          </div>

          {showCustomGraph && (
            <div className="flex gap-4">
              <div className="flex items-center">
                <input 
                  type="radio" 
                  id="matrixInput" 
                  name="inputType" 
                  value="matrix" 
                  checked={inputType === 'matrix'} 
                  onChange={() => setInputType('matrix')}
                  className="mr-2"
                />
                <label htmlFor="matrixInput">Adjacency Matrix</label>
              </div>
              <div className="flex items-center">
                <input 
                  type="radio" 
                  id="listInput" 
                  name="inputType" 
                  value="list" 
                  checked={inputType === 'list'} 
                  onChange={() => setInputType('list')}
                  className="mr-2"
                />
                <label htmlFor="listInput">Adjacency List</label>
              </div>
            </div>
          )}
        </div>

        {/* Node count selector */}
        <div className="flex flex-wrap gap-4 mb-4">
          <div>
            <label className="block mb-2">Node Count:</label>
            <select 
              value={nodeCount}
              onChange={(e) => {
                const count = Number(e.target.value);
                setNodeCount(count);
                if (showCustomGraph) {
                  // Wait for state update and then initialize structures
                  setTimeout(() => initializeCustomGraphStructures(), 0);
                }
              }}
              className="bg-gray-700 rounded px-3 py-2"
            >
              <option value={3}>3</option>
              <option value={4}>4</option>
              <option value={5}>5</option>
              <option value={6}>6</option>
              <option value={7}>7</option>
              <option value={8}>8</option>
            </select>
          </div>
          
          {!showCustomGraph && (
            <div>
              <label className="block mb-2">Edge Density:</label>
              <select 
                value={edgeDensity}
                onChange={(e) => setEdgeDensity(Number(e.target.value))}
                className="bg-gray-700 rounded px-3 py-2"
              >
                <option value={0.2}>Sparse (0.2)</option>
                <option value={0.3}>Medium (0.3)</option>
                <option value={0.5}>Dense (0.5)</option>
              </select>
            </div>
          )}
          
          {isInitialized && (
            <div>
              <label className="block mb-2">Start Node:</label>
              <select 
                value={startNode}
                onChange={(e) => setStartNode(e.target.value)}
                className="bg-gray-700 rounded px-3 py-2"
              >
                {graph.nodes.map(node => (
                  <option key={node.id} value={node.id}>
                    Node {node.id}
                  </option>
                ))}
              </select>
            </div>
          )}
          
          <div>
            <label className="block mb-2">Speed:</label>
            <select 
              value={speed}
              onChange={(e) => setSpeed(Number(e.target.value))}
              className="bg-gray-700 rounded px-3 py-2"
            >
              <option value={2000}>Slow</option>
              <option value={1000}>Medium</option>
              <option value={500}>Fast</option>
              <option value={200}>Very Fast</option>
            </select>
          </div>
        </div>

        {/* Custom graph input section */}
        {showCustomGraph && (
          <div className="mt-4 p-4 bg-gray-700 rounded-lg">
            <h3 className="text-lg font-semibold mb-3">Node Labels</h3>
            <div className="flex flex-wrap gap-2 mb-4">
              {nodeLabels.map((label, index) => (
                <div key={`node-${index}`} className="flex items-center">
                  <label className="mr-2">Node {index}:</label>
                  <input
                    type="text"
                    value={label}
                    onChange={(e) => handleNodeLabelChange(index, e.target.value)}
                    className="bg-gray-800 rounded px-2 py-1 w-16"
                  />
                </div>
              ))}
            </div>

            {inputType === 'matrix' ? (
              <div>
                <h3 className="text-lg font-semibold mb-3">Adjacency Matrix</h3>
                <div className="overflow-x-auto">
                  <table className="border-collapse">
                    <thead>
                      <tr>
                        <th className="p-2"></th>
                        {nodeLabels.map((label, i) => (
                          <th key={`col-${i}`} className="p-2">{label}</th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {adjacencyMatrix.map((row, i) => (
                        <tr key={`row-${i}`}>
                          <th className="p-2">{nodeLabels[i]}</th>
                          {row.map((cell, j) => (
                            <td key={`cell-${i}-${j}`} className="p-2">
                              <input
                                type="checkbox"
                                checked={cell}
                                onChange={() => handleMatrixToggle(i, j)}
                                className="w-5 h-5"
                                disabled={i === j}
                              />
                            </td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            ) : (
              <div>
                <h3 className="text-lg font-semibold mb-3">Adjacency List</h3>
                <div className="space-y-4">
                  {nodeLabels.map((label, index) => (
                    <div key={`list-${index}`} className="flex items-start">
                      {/* Node box */}
                      <div className="bg-gray-800 rounded-md p-3 w-16 text-center font-bold border border-gray-600 flex items-center justify-center">
                        {label}
                      </div>
                      
                      {/* Arrow */}
                      <div className="flex items-center mx-2">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <path d="M5 12H19M19 12L12 5M19 12L12 19" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                        </svg>
                      </div>
                      
                      {/* Connected nodes */}
                      <div className="flex flex-wrap gap-2 items-center">
                        {nodeLabels.map((targetLabel, targetIndex) => {
                          // Skip self connections
                          if (targetLabel === label) return null;
                          
                          const isConnected = adjacencyList[label]?.includes(targetLabel) || false;
                          
                          return (
                            <div key={`${label}-${targetLabel}`} className="relative">
                              <input
                                type="checkbox"
                                id={`conn-${label}-${targetLabel}`}
                                checked={isConnected}
                                onChange={() => {
                                  const newList = {...adjacencyList};
                                  if (isConnected) {
                                    // Remove connection
                                    newList[label] = newList[label].filter(t => t !== targetLabel);
                                  } else {
                                    // Add connection
                                    if (!newList[label]) {
                                      newList[label] = [];
                                    }
                                    newList[label].push(targetLabel);
                                  }
                                  setAdjacencyList(newList);
                                }}
                                className="sr-only" // Hide actual checkbox but keep functionality
                              />
                              <label 
                                htmlFor={`conn-${label}-${targetLabel}`} 
                                className={`
                                  cursor-pointer 
                                  ${isConnected ? 'bg-blue-600 border-blue-400 hover:bg-blue-700' : 'bg-gray-600 border-gray-400 hover:bg-gray-500'} 
                                  border rounded-md p-2 inline-block w-10 h-10 
                                  text-center transition-colors flex items-center justify-center
                                `}
                              >
                                {targetLabel}
                              </label>
                            </div>
                          );
                        })}
                        
                        {!adjacencyList[label]?.length && (
                          <div className="text-gray-400 italic">None</div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Control buttons */}
        <div className="flex items-center gap-4 mt-4">
          <button 
            onClick={generateGraph}
            className="bg-blue-500 hover:bg-blue-600 px-4 py-2 rounded"
          >
            {showCustomGraph ? 'Create Graph' : 'Generate New Graph'}
          </button>
          
          {isInitialized && (
            <button 
              onClick={() => setIsPlaying(!isPlaying)}
              className={`${
                isComplete ? 'bg-gray-500' : (isPlaying ? 'bg-yellow-500 hover:bg-yellow-600' : 'bg-green-500 hover:bg-green-600')
              } px-4 py-2 rounded`}
              disabled={isComplete}
            >
              {isPlaying ? 'Pause' : isComplete ? 'Completed' : 'Play'}
            </button>
          )}
        </div>
      </div>

      {isInitialized && (
        <GraphVisualizer 
          graph={graph}
          steps={steps}
          speed={speed}
          isPlaying={isPlaying}
          onComplete={handleComplete}
        />
      )}
      
      <div className="mt-8 p-4 bg-gray-800 rounded-lg">
        <h2 className="text-xl font-semibold mb-2">Code Implementation</h2>
        <pre className="bg-gray-900 p-4 rounded overflow-x-auto">
          <code>{`function dfs(graph, startNode) {
  const visited = new Set();
  const stack = [startNode];
  
  while (stack.length > 0) {
    const current = stack.pop(); // Remove from the end (LIFO)
    
    if (visited.has(current)) {
      continue;
    }
    
    visited.add(current);
    
    // Find all neighbors (add in reverse to maintain expected order)
    const neighbors = getNeighbors(graph, current);
    
    // Add neighbors to stack in reverse order to process in expected order
    for (let i = neighbors.length - 1; i >= 0; i--) {
      const neighbor = neighbors[i];
      if (!visited.has(neighbor)) {
        stack.push(neighbor);
      }
    }
  }
  
  return Array.from(visited);
}`}</code>
        </pre>
      </div>
    </div>
  );
} 