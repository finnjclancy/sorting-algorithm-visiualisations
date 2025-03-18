export type Node = {
  id: string;
  x: number;
  y: number;
};

export type Edge = {
  source: string;
  target: string;
};

export type Graph = {
  nodes: Node[];
  edges: Edge[];
};

export type TraversalStep = {
  visited: string[];
  queue?: string[];
  stack?: string[];
  current?: string;
  exploring?: string;
  distances?: Record<string, number>;
  highlightedEdge?: {source: string, target: string};
  completed?: string[];
};

// Breadth-First Search
export function bfs(graph: Graph, startNodeId: string): TraversalStep[] {
  const steps: TraversalStep[] = [];
  const visited: string[] = [];
  const queue: string[] = [startNodeId];
  const completed: string[] = [];
  
  // Initialize distances
  const distances: Record<string, number> = {};
  graph.nodes.forEach(node => {
    distances[node.id] = node.id === startNodeId ? 0 : Infinity;
  });
  
  // Initial state
  steps.push({ 
    visited: [], 
    queue: [...queue],
    distances: {...distances},
    completed: []
  });
  
  while (queue.length > 0) {
    const current = queue.shift()!;
    
    if (visited.includes(current)) {
      continue;
    }
    
    // Mark as current (color: red in visualization)
    steps.push({ 
      visited: [...visited], 
      queue: [...queue], 
      current,
      distances: {...distances},
      completed: [...completed]
    });
    
    // Add to visited (becomes green)
    visited.push(current);
    steps.push({ 
      visited: [...visited], 
      queue: [...queue],
      distances: {...distances},
      completed: [...completed]
    });
    
    // Find all neighbors, sorted by id for consistent visualization
    const neighbors = graph.edges
      .filter(edge => edge.source === current || edge.target === current)
      .map(edge => edge.source === current ? edge.target : edge.source)
      .filter(neighbor => !visited.includes(neighbor) && !queue.includes(neighbor))
      .sort(); // Sort by id for consistent exploration order
    
    // Explore each neighbor
    for (const neighbor of neighbors) {
      // First, highlight the edge (red edge)
      steps.push({ 
        visited: [...visited], 
        queue: [...queue], 
        current, 
        exploring: neighbor,
        highlightedEdge: {source: current, target: neighbor},
        distances: {...distances},
        completed: [...completed]
      });
      
      // Update distance if this is a shorter path
      const newDistance = distances[current] + 1;
      if (newDistance < distances[neighbor]) {
        distances[neighbor] = newDistance;
      }
      
      // Add to queue
      queue.push(neighbor);
      steps.push({ 
        visited: [...visited], 
        queue: [...queue],
        distances: {...distances},
        completed: [...completed]
      });
    }
    
    // Mark the current node as completed (all neighbors processed)
    completed.push(current);
    steps.push({ 
      visited: [...visited], 
      queue: [...queue],
      distances: {...distances},
      completed: [...completed]
    });
  }
  
  return steps;
}

// Depth-First Search
export function dfs(graph: Graph, startNodeId: string): TraversalStep[] {
  const steps: TraversalStep[] = [];
  const visited: string[] = [];
  const stack: string[] = [startNodeId];
  
  steps.push({ visited: [], stack: [...stack] });
  
  while (stack.length > 0) {
    const current = stack.pop()!;
    
    if (visited.includes(current)) {
      continue;
    }
    
    steps.push({ visited: [...visited], stack: [...stack], current });
    
    visited.push(current);
    steps.push({ visited: [...visited], stack: [...stack] });
    
    // Find all neighbors (in reverse order for DFS to match typical visualization)
    const neighbors = graph.edges
      .filter(edge => edge.source === current || edge.target === current)
      .map(edge => edge.source === current ? edge.target : edge.source)
      .filter(neighbor => !visited.includes(neighbor))
      .reverse(); // Reverse to match typical DFS visualization
    
    for (const neighbor of neighbors) {
      steps.push({ visited: [...visited], stack: [...stack], current, exploring: neighbor });
      stack.push(neighbor);
      steps.push({ visited: [...visited], stack: [...stack] });
    }
  }
  
  return steps;
}

// Generate a random graph
export function generateRandomGraph(nodeCount: number = 10, edgeDensity: number = 0.3): Graph {
  const nodes: Node[] = [];
  const edges: Edge[] = [];
  
  // Create nodes in a circular layout
  for (let i = 0; i < nodeCount; i++) {
    const angle = (i / nodeCount) * 2 * Math.PI;
    const radius = 200;
    
    nodes.push({
      id: i.toString(),
      x: 250 + radius * Math.cos(angle),
      y: 250 + radius * Math.sin(angle)
    });
  }
  
  // First, ensure connectivity by creating a spanning tree
  // This guarantees that all nodes are connected
  const connectedNodes = new Set<string>([nodes[0].id]); // Start with first node
  const remainingNodes = new Set<string>(nodes.slice(1).map(n => n.id));
  
  // Continue until all nodes are connected
  while (remainingNodes.size > 0) {
    // Pick a random node from connected set
    const connectedArray = Array.from(connectedNodes);
    const sourceIdx = Math.floor(Math.random() * connectedArray.length);
    const source = connectedArray[sourceIdx];
    
    // Pick a random node from remaining set
    const remainingArray = Array.from(remainingNodes);
    const targetIdx = Math.floor(Math.random() * remainingArray.length);
    const target = remainingArray[targetIdx];
    
    // Create an edge between them
    edges.push({ source, target });
    
    // Move target from remaining to connected
    remainingNodes.delete(target);
    connectedNodes.add(target);
  }
  
  // Then add additional random edges based on density
  // Skip pairs that already have an edge
  const edgeExists = new Set<string>();
  
  // Add existing edges to the set
  edges.forEach(edge => {
    // Store both orientations to handle undirected graph
    edgeExists.add(`${edge.source}-${edge.target}`);
    edgeExists.add(`${edge.target}-${edge.source}`);
  });
  
  // Calculate how many more edges to add based on density
  const maxPossibleEdges = (nodeCount * (nodeCount - 1)) / 2; // Undirected graph
  const targetEdgeCount = Math.floor(maxPossibleEdges * edgeDensity);
  const additionalEdgesToAdd = Math.max(0, targetEdgeCount - edges.length);
  
  // Add random edges up to the desired density
  let attemptsLeft = additionalEdgesToAdd * 3; // Allow multiple attempts to find valid edges
  let edgesAdded = 0;
  
  while (edgesAdded < additionalEdgesToAdd && attemptsLeft > 0) {
    // Pick two random nodes
    const i = Math.floor(Math.random() * nodeCount);
    const j = Math.floor(Math.random() * nodeCount);
    
    // Skip if same node or edge already exists
    if (i === j || edgeExists.has(`${i}-${j}`)) {
      attemptsLeft--;
      continue;
    }
    
    // Add the edge
    edges.push({
      source: i.toString(),
      target: j.toString()
    });
    
    // Mark as existing
    edgeExists.add(`${i}-${j}`);
    edgeExists.add(`${j}-${i}`);
    
    edgesAdded++;
  }
  
  return { nodes, edges };
} 