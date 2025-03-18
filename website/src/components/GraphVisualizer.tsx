'use client';

import React, { useState, useEffect, useRef } from 'react';
import { Graph, TraversalStep } from '@/lib/algorithms/traversal';

interface GraphVisualizerProps {
  graph: Graph;
  steps: TraversalStep[];
  speed: number;
  isPlaying: boolean;
  onComplete?: () => void;
}

const GraphVisualizer: React.FC<GraphVisualizerProps> = ({ 
  graph, 
  steps, 
  speed, 
  isPlaying,
  onComplete
}) => {
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [currentStep, setCurrentStep] = useState<TraversalStep | null>(null);
  const svgRef = useRef<SVGSVGElement>(null);
  const timerRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    if (steps && steps.length > 0) {
      setCurrentStep(steps[0]);
      setCurrentStepIndex(0);
    }
  }, [steps]);

  useEffect(() => {
    if (steps && currentStepIndex < steps.length) {
      setCurrentStep(steps[currentStepIndex]);
    }
  }, [currentStepIndex, steps]);

  useEffect(() => {
    // Clean up any existing timer when component unmounts or dependencies change
    return () => {
      if (timerRef.current) {
        clearTimeout(timerRef.current);
      }
    };
  }, []);

  useEffect(() => {
    if (isPlaying) {
      if (timerRef.current) {
        clearTimeout(timerRef.current);
      }
      
      if (currentStepIndex < steps.length - 1) {
        timerRef.current = setTimeout(() => {
          setCurrentStepIndex(prev => prev + 1);
        }, speed);
      } else if (onComplete) {
        // Call completion callback when reaching the end
        onComplete();
      }
    } else if (timerRef.current) {
      clearTimeout(timerRef.current);
    }
  }, [isPlaying, currentStepIndex, steps.length, speed, onComplete]);

  const handlePrevStep = () => {
    if (currentStepIndex > 0) {
      setCurrentStepIndex(prev => prev - 1);
    }
  };

  const handleNextStep = () => {
    if (currentStepIndex < steps.length - 1) {
      setCurrentStepIndex(prev => prev + 1);
    } else if (onComplete) {
      onComplete();
    }
  };

  const renderNode = (node: { id: string; x: number; y: number }, index: number) => {
    const id = node.id;
    let fillColor = '#3B82F6'; // Default blue
    let textColor = 'white';
    let strokeColor = 'none';
    let strokeWidth = 1;
    
    // Current node being processed
    if (currentStep?.current === id) {
      fillColor = '#EF4444'; // Red
      strokeColor = '#B91C1C';
      strokeWidth = 3;
    } 
    // Node being explored from current
    else if (currentStep?.exploring === id) {
      fillColor = '#FB923C'; // Orange
      strokeColor = '#EA580C';
      strokeWidth = 3;
    }
    // Visited nodes
    else if (currentStep?.visited.includes(id)) {
      fillColor = '#10B981'; // Green
    }
    // Nodes in queue/stack
    else if (
      (currentStep?.queue && currentStep.queue.includes(id)) || 
      (currentStep?.stack && currentStep.stack.includes(id))
    ) {
      fillColor = '#A855F7'; // Purple
    }
    // Completed nodes (all neighbors explored)
    else if (currentStep?.completed?.includes(id)) {
      fillColor = '#0284C7'; // Dark blue
    }

    // Highlight the edge if it exists
    const isHighlightedEdge = currentStep?.highlightedEdge && 
      (currentStep.highlightedEdge.source === id || currentStep.highlightedEdge.target === id);
    
    if (isHighlightedEdge) {
      strokeColor = '#EF4444'; // Red
      strokeWidth = 3;
    }

    return (
      <g key={`node-${id}`}>
        <circle
          cx={node.x}
          cy={node.y}
          r={20}
          fill={fillColor}
          stroke={strokeColor}
          strokeWidth={strokeWidth}
        />
        <text
          x={node.x}
          y={node.y}
          textAnchor="middle"
          dominantBaseline="middle"
          fill={textColor}
          fontSize={14}
          fontWeight="bold"
        >
          {id}
        </text>
        {/* Display distance if available */}
        {currentStep?.distances && currentStep.distances[id] !== Infinity && (
          <text
            x={node.x}
            y={node.y + 35}
            textAnchor="middle"
            dominantBaseline="middle"
            fill="white"
            fontSize={12}
            className="bg-gray-800 px-1 rounded"
          >
            {currentStep.distances[id]}
          </text>
        )}
      </g>
    );
  };

  const renderEdge = (edge: { source: string; target: string }, index: number) => {
    const sourceNode = graph.nodes.find(n => n.id === edge.source);
    const targetNode = graph.nodes.find(n => n.id === edge.target);
    
    if (!sourceNode || !targetNode) return null;
    
    // Check if this edge is the highlighted one
    const isHighlighted = currentStep?.highlightedEdge && 
      currentStep.highlightedEdge.source === edge.source && 
      currentStep.highlightedEdge.target === edge.target;
    
    // Calculate midpoint for self-loops
    const isSelfLoop = edge.source === edge.target;
    let path;
    
    if (isSelfLoop) {
      // Draw a circle above the node for self-loops
      const cx = sourceNode.x;
      const cy = sourceNode.y - 40; // Above the node
      const r = 15;
      path = `M ${sourceNode.x} ${sourceNode.y - 20} 
              C ${cx - r * 2} ${cy - r}, ${cx + r * 2} ${cy - r}, ${sourceNode.x} ${sourceNode.y - 20}`;
    } else {
      // Regular edge
      path = `M ${sourceNode.x} ${sourceNode.y} L ${targetNode.x} ${targetNode.y}`;
    }
    
    return (
      <g key={`edge-${index}`}>
        <path
          d={path}
          stroke={isHighlighted ? "#EF4444" : "#64748B"}
          strokeWidth={isHighlighted ? 3 : 1.5}
          fill="none"
          markerEnd={isSelfLoop ? "url(#arrowhead)" : undefined}
        />
        {!isSelfLoop && (
          <marker
            id="arrowhead"
            markerWidth="10"
            markerHeight="7"
            refX="5"
            refY="3.5"
            orient="auto"
          >
            <polygon
              points="0 0, 10 3.5, 0 7"
              fill={isHighlighted ? "#EF4444" : "#64748B"}
            />
          </marker>
        )}
      </g>
    );
  };

  const getQueueOrStackLabel = () => {
    if (currentStep?.queue) return "Queue";
    if (currentStep?.stack) return "Stack";
    return "Queue/Stack";
  };

  // Get visited nodes as a string
  const getVisitedNodesString = () => {
    return currentStep?.visited.join(' → ') || 'None';
  };

  // Get queue or stack as a string
  const getQueueOrStackString = () => {
    if (currentStep?.queue) {
      return currentStep.queue.join(' → ') || 'Empty';
    }
    if (currentStep?.stack) {
      return currentStep.stack.join(' → ') || 'Empty';
    }
    return 'None';
  };

  return (
    <div className="bg-gray-800 p-6 rounded-lg">
      <div className="mb-6">
        <h2 className="text-xl font-semibold mb-4">Visualization</h2>
        <div className="flex justify-between items-center mb-4">
          <div className="flex space-x-4">
            <button
              onClick={handlePrevStep}
              disabled={currentStepIndex <= 0}
              className={`px-3 py-1 rounded ${
                currentStepIndex <= 0 ? 'bg-gray-600 cursor-not-allowed' : 'bg-blue-500 hover:bg-blue-600'
              }`}
            >
              Previous
            </button>
            <button
              onClick={handleNextStep}
              disabled={currentStepIndex >= steps.length - 1}
              className={`px-3 py-1 rounded ${
                currentStepIndex >= steps.length - 1 ? 'bg-gray-600 cursor-not-allowed' : 'bg-blue-500 hover:bg-blue-600'
              }`}
            >
              Next
            </button>
          </div>
          <div className="text-sm">
            Step: {currentStepIndex + 1} / {steps.length}
          </div>
        </div>

        <div className="border-t border-gray-700 pt-4 mb-4">
          <div className="flex flex-wrap gap-2 mb-2">
            <div className="flex items-center gap-1">
              <div className="w-4 h-4 rounded-full bg-blue-500"></div>
              <span>Unvisited</span>
            </div>
            <div className="flex items-center gap-1">
              <div className="w-4 h-4 rounded-full bg-green-500"></div>
              <span>Visited</span>
            </div>
            <div className="flex items-center gap-1">
              <div className="w-4 h-4 rounded-full bg-purple-500"></div>
              <span>{currentStep?.queue ? "In Queue" : "In Stack"}</span>
            </div>
            <div className="flex items-center gap-1">
              <div className="w-4 h-4 rounded-full bg-red-500"></div>
              <span>Current</span>
            </div>
            <div className="flex items-center gap-1">
              <div className="w-4 h-4 rounded-full bg-orange-500"></div>
              <span>Exploring</span>
            </div>
            {currentStep?.completed && (
              <div className="flex items-center gap-1">
                <div className="w-4 h-4 rounded-full bg-blue-700"></div>
                <span>Completed</span>
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="relative bg-gray-900 rounded-lg overflow-hidden mb-4" style={{ height: '500px' }}>
        <svg 
          ref={svgRef}
          width="100%" 
          height="100%" 
          viewBox="0 0 500 500"
          className="mx-auto"
        >
          <defs>
            <marker
              id="arrowhead"
              markerWidth="10"
              markerHeight="7"
              refX="9"
              refY="3.5"
              orient="auto"
            >
              <polygon
                points="0 0, 10 3.5, 0 7"
                fill="#64748B"
              />
            </marker>
          </defs>
          
          {/* Render edges first so they're below nodes */}
          {graph.edges.map(renderEdge)}
          
          {/* Then render nodes */}
          {graph.nodes.map(renderNode)}
        </svg>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
        <div className="bg-gray-700 p-4 rounded-lg">
          <h3 className="font-semibold mb-2">Visited Nodes</h3>
          <div className="bg-gray-800 p-3 rounded break-words max-h-24 overflow-y-auto">
            {getVisitedNodesString()}
          </div>
        </div>
        
        <div className="bg-gray-700 p-4 rounded-lg">
          <h3 className="font-semibold mb-2">{getQueueOrStackLabel()}</h3>
          <div className="bg-gray-800 p-3 rounded break-words max-h-24 overflow-y-auto">
            {getQueueOrStackString()}
          </div>
        </div>
      </div>
    </div>
  );
};

export default GraphVisualizer; 