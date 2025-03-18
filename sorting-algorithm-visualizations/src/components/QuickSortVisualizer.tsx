'use client';

import { useState, useEffect, useRef } from 'react';
import { SortingStep } from '@/lib/algorithms/sorting';
import { motion } from 'framer-motion';

type QuickSortVisualizerProps = {
  steps: SortingStep[];
  speed: number;
  isPlaying: boolean;
  onComplete: () => void;
  initialStep?: number;
};

export default function QuickSortVisualizer({
  steps,
  speed,
  isPlaying,
  onComplete,
  initialStep = 0,
}: QuickSortVisualizerProps) {
  // Check if steps array is empty
  if (!steps || steps.length === 0) {
    return <div className="w-full h-80 bg-gray-800 rounded-lg p-4 flex items-center justify-center">
      <p>No data to visualize</p>
    </div>;
  }

  const [currentStepIndex, setCurrentStepIndex] = useState(initialStep);
  const [drawnRows, setDrawnRows] = useState(initialStep);
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);
  
  // Calculate canvas dimensions and check if scrolling is needed
  const rowHeight = 60;
  const rowPadding = 15;
  const totalContentHeight = (steps.length * rowHeight) + ((steps.length - 1) * rowPadding) + 50;
  const canvasHeight = Math.min(600, totalContentHeight);
  
  // Calculate if horizontal scrolling is needed based on array size
  const hasLargeArray = steps[0]?.array.length > 15; // Show scrolling message if more than 15 elements
  const containerWidth = Math.max(800, (steps[0]?.array.length || 10) * 50);

  // Animation speeds
  const mainDelay = speed;

  // Reset when steps array or initialStep changes
  useEffect(() => {
    setCurrentStepIndex(initialStep);
    setDrawnRows(initialStep);
    stopAllTimers();
  }, [steps, initialStep]);

  // Stop all running timers
  const stopAllTimers = () => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
      timeoutRef.current = null;
    }
  };

  // Handle play/pause and timing
  useEffect(() => {
    stopAllTimers();

    if (isPlaying && currentStepIndex < steps.length - 1) {
      visualizeNextRow();
    }

    return stopAllTimers;
  }, [isPlaying, currentStepIndex, steps.length, speed]);

  // Visualize the next row in the visualization
  const visualizeNextRow = () => {
    if (!isPlaying || currentStepIndex >= steps.length - 1) {
      if (currentStepIndex >= steps.length - 1) {
        onComplete();
      }
      return;
    }

    // Increment drawn rows to show next row
    const nextRowIndex = Math.min(currentStepIndex + 1, steps.length - 1);
    setDrawnRows(Math.max(nextRowIndex, drawnRows));
    
    // Move to the next step after a delay
    timeoutRef.current = setTimeout(() => {
      setCurrentStepIndex(nextRowIndex);
    }, mainDelay);
  };

  return (
    <div className="w-full bg-gray-800 rounded-lg p-4 shadow-lg">
      {/* Message to inform users about horizontal scrolling when needed */}
      {hasLargeArray && (
        <div style={{
          backgroundColor: 'rgba(30, 41, 59, 0.8)',
          color: '#e2e8f0',
          fontSize: '14px',
          padding: '8px 12px',
          marginBottom: '12px',
          borderRadius: '6px',
          textAlign: 'center'
        }}>
          <span style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '6px' }}>
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <line x1="2" y1="12" x2="22" y2="12"></line>
              <polyline points="9 5 2 12 9 19"></polyline>
              <polyline points="15 5 22 12 15 19"></polyline>
            </svg>
            Scroll horizontally to see all elements
          </span>
        </div>
      )}
      
      <div 
        id="quick-sort-canvas" 
        style={{ 
          height: `${canvasHeight}px`, 
          position: 'relative',
          overflowY: 'auto',
          overflowX: 'auto', // Enable horizontal scrolling
          border: '1px solid #374151',
          borderRadius: '0.5rem',
          backgroundColor: '#1e293b',
          boxShadow: 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.2)'
        }}
      >
        <div style={{ 
          height: `${totalContentHeight}px`,
          position: 'relative',
          width: containerWidth + 'px' // Set a fixed width based on array size
        }}>
          {steps.map((step, rowIndex) => {
            if (rowIndex > drawnRows) return null;
            
            const y = 25 + rowIndex * (rowHeight + rowPadding);
            const comment = step.comment || '';
            const [low, high] = step.subArrayRange || [0, 0];
            
            return (
              <div key={`row-${rowIndex}`} style={{ position: 'absolute', top: y, left: 0, width: '100%' }}>
                {/* Comment section - fixed position on the left */}
                <div style={{ 
                  position: 'absolute', 
                  left: 20, 
                  top: rowHeight / 2 - 10, 
                  width: 160,
                  textAlign: 'right',
                  zIndex: 5 // Ensure it stays above other elements
                }}>
                  {comment.includes("Pivot") ? (
                    <div style={{
                      color: '#f1f5f9',
                      lineHeight: '1.2',
                      textAlign: 'right'
                    }}>
                      <div style={{ 
                        fontWeight: 'bold', 
                        fontSize: '13px',
                        color: '#8b5cf6',
                        marginBottom: '2px' 
                      }}>
                        {comment.split('\n')[0]}
                      </div>
                      <div style={{ 
                        fontSize: '11px',
                        opacity: 0.9,
                        color: '#e2e8f0',
                        whiteSpace: 'nowrap'
                      }}>
                        {comment.split('\n')[1] || ''}
                      </div>
                    </div>
                  ) : (
                    <div style={{ 
                      fontSize: '13px',
                      color: '#f1f5f9'
                    }}>
                      {comment}
                    </div>
                  )}
                </div>
                
                {/* Array container with horizontal centering */}
                <div style={{
                  width: '100%',
                  position: 'relative',
                  paddingLeft: 190, // Increased offset to account for wider comment section
                  height: rowHeight
                }}>
                
                  {/* Subarray highlight box */}
                  {step.subArrayRange && (
                    <div style={{
                      position: 'absolute',
                      height: rowHeight,
                      display: 'flex',
                      justifyContent: 'center',
                      alignItems: 'center',
                      zIndex: 1
                    }}>
                      <div
                        style={{
                          position: 'absolute',
                          left: `${low * 44}px`,
                          width: ((high - low + 1) * 44) + 'px',
                          height: '46px',
                          backgroundColor: 'rgba(30, 41, 59, 0.5)',
                          borderRadius: '8px',
                          boxShadow: 'inset 0 0 0 2px rgba(71, 85, 105, 0.5)',
                          zIndex: 1
                        }}
                      />
                    </div>
                  )}
                  
                  {/* Array boxes */}
                  <div style={{ 
                    height: rowHeight,
                    display: 'flex',
                    alignItems: 'center',
                    zIndex: 2,
                    position: 'relative'
                  }}>
                    {step.array.map((value, index) => {
                      const isSorted = step.sortedIndices?.includes(index);
                      const isPivot = step.pivot === index;
                      const isInSubArray = index >= (step.subArrayRange?.[0] || 0) && 
                                            index <= (step.subArrayRange?.[1] || step.array.length - 1);
                      
                      // Show all numbers - find the value across all steps
                      let actualValue = value;
                      
                      // If this step doesn't show the value (is null), get it from initial array
                      if (actualValue === null) {
                        // Find first step where this index has a value
                        for (let i = 0; i <= rowIndex; i++) {
                          const earlierValue = steps[i].array[index];
                          if (earlierValue !== null) {
                            actualValue = earlierValue;
                            break;
                          }
                        }
                          
                        // If still null, get from initial array
                        if (actualValue === null && steps[0].array[index] !== null) {
                          actualValue = steps[0].array[index];
                        }
                      }
                      
                      // Determine styles based on element state
                      let styles = {
                        // Default styles for elements outside current subarray
                        bgColor: '#f8fafc',
                        textColor: 'white',
                        boxShadow: '0 1px 2px rgba(0,0,0,0.1)',
                        opacity: 1, // Make all numbers fully visible
                        transform: 'scale(1)',
                        border: 'none',
                        fontWeight: '600' as 'bold' | '600'
                      };
                      
                      // Special handling for the first row with a pivot (second row)
                      const isFirstPivotRow = rowIndex === 1;
                      
                      if (isInSubArray) {
                        // Active elements in current subarray
                        styles.opacity = 1; // Always fully visible
                        styles.textColor = 'white';
                        
                        if (isPivot) {
                          // Pivot element
                          styles.bgColor = '#8b5cf6'; // Purple for pivot
                          styles.boxShadow = '0 4px 6px rgba(139,92,246,0.5)';
                          styles.transform = 'scale(1.08)';
                          styles.border = '2px solid #7e22ce';
                          styles.fontWeight = 'bold';
                        } else if (isSorted) {
                          // Sorted elements
                          styles.bgColor = '#10b981'; // Emerald green
                          styles.boxShadow = '0 2px 4px rgba(16,185,129,0.4)';
                        } else {
                          // Unsorted elements in current subarray
                          styles.bgColor = '#ef4444'; // Red
                          styles.boxShadow = '0 2px 4px rgba(239,68,68,0.4)';
                        }
                      } else if (isSorted) {
                        // Sorted elements outside current subarray
                        styles.bgColor = '#10b981'; // Emerald green
                        styles.textColor = 'white';
                        styles.boxShadow = '0 2px 4px rgba(16,185,129,0.4)';
                      } else {
                        // Elements outside the current subarray
                        if (isFirstPivotRow) {
                          // For the first pivot row (second row), make all elements red except the sorted ones
                          styles.bgColor = '#ef4444'; // Red
                          styles.textColor = 'white';
                          styles.boxShadow = '0 2px 4px rgba(239,68,68,0.4)';
                        } else {
                          // For other rows, grey out elements outside the subarray
                          styles.bgColor = '#475569'; // Slate gray
                          styles.textColor = 'white';
                          styles.opacity = 0.7; // Slightly dimmed but still clearly visible
                        }
                      }
                      
                      // For first row (initial array), make all elements red
                      if (rowIndex === 0) {
                        styles.bgColor = '#ef4444';
                        styles.textColor = 'white';
                        styles.opacity = 1;
                      }
                      
                      // For last row (sorted array), make all elements green
                      if (rowIndex === steps.length - 1) {
                        styles.bgColor = '#10b981';
                        styles.textColor = 'white';
                        styles.opacity = 1;
                      }
                      
                      return (
                        <motion.div 
                          key={`box-${index}`}
                          initial={{ opacity: styles.opacity * 0.8 }}
                          animate={{ 
                            opacity: styles.opacity,
                            scale: isPivot ? 1.08 : 1
                          }}
                          transition={{ 
                            duration: 0.2,
                            ease: "easeOut"
                          }}
                          style={{
                            width: '36px',
                            height: '36px',
                            margin: '0 4px',
                            backgroundColor: styles.bgColor,
                            border: styles.border,
                            borderRadius: '6px',
                            boxShadow: styles.boxShadow,
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            fontWeight: styles.fontWeight,
                            color: styles.textColor,
                            position: 'relative',
                            zIndex: isPivot ? 3 : 2
                          }}
                        >
                          {/* Special indicator for pivot elements */}
                          {isPivot && (
                            <div style={{
                              position: 'absolute',
                              bottom: '-18px',
                              left: '50%',
                              transform: 'translateX(-50%)',
                              color: '#8b5cf6',
                              fontSize: '18px',
                              lineHeight: 1,
                              textShadow: '0 1px 2px rgba(0,0,0,0.3)'
                            }}>
                              ▲
                            </div>
                          )}
                          {actualValue !== null ? actualValue : ''}
                        </motion.div>
                      );
                    })}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
      
      {/* Key/Legend to explain the colors */}
      <div style={{
        marginTop: '12px',
        padding: '10px',
        backgroundColor: 'rgba(30, 41, 59, 0.8)',
        borderRadius: '8px',
        display: 'flex',
        flexWrap: 'wrap',
        justifyContent: 'center',
        gap: '16px',
        boxShadow: '0 2px 4px rgba(0, 0, 0, 0.2)'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <div style={{ width: '16px', height: '16px', backgroundColor: '#ef4444', borderRadius: '3px' }}></div>
          <span style={{ fontSize: '13px', color: '#f1f5f9', fontWeight: '500' }}>Active Subarray</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <div style={{ width: '16px', height: '16px', backgroundColor: '#8b5cf6', borderRadius: '3px' }}></div>
          <span style={{ fontSize: '13px', color: '#f1f5f9', fontWeight: '500' }}>Pivot Element</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <div style={{ width: '16px', height: '16px', backgroundColor: '#10b981', borderRadius: '3px' }}></div>
          <span style={{ fontSize: '13px', color: '#f1f5f9', fontWeight: '500' }}>Sorted Element</span>
        </div>
      </div>
      
      <div style={{ 
        marginTop: '12px', 
        textAlign: 'center',
        color: '#f1f5f9',
        fontWeight: '500',
        fontSize: '14px',
        padding: '8px 12px',
        backgroundColor: 'rgba(30, 41, 59, 0.8)',
        borderRadius: '8px',
        boxShadow: '0 2px 4px rgba(0, 0, 0, 0.2)'
      }}>
        Step {Math.min(currentStepIndex + 1, steps.length)} of {steps.length}
      </div>
    </div>
  );
} 