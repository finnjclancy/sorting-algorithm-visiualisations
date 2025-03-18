'use client';

import { useState, useEffect, useRef } from 'react';
import { SortingStep } from '@/lib/algorithms/sorting';
import { motion } from 'framer-motion';

type SortingVisualizerProps = {
  steps: SortingStep[];
  speed: number;
  isPlaying: boolean;
  onComplete: () => void;
  initialStep?: number;
};

export default function SortingVisualizer({
  steps,
  speed,
  isPlaying,
  onComplete,
  initialStep = 0,
}: SortingVisualizerProps) {
  // Check if steps array is empty
  if (!steps || steps.length === 0) {
    return <div className="w-full h-80 bg-gray-800 rounded-lg p-4 flex items-center justify-center">
      <p>No data to visualize</p>
    </div>;
  }

  const [currentStepIndex, setCurrentStepIndex] = useState(initialStep);
  const [currentStep, setCurrentStep] = useState<SortingStep>(steps[initialStep]);
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);

  // Reset when steps array or initialStep changes
  useEffect(() => {
    setCurrentStepIndex(initialStep);
    setCurrentStep(steps[initialStep]);
  }, [steps, initialStep]);

  // Update current step when step index changes
  useEffect(() => {
    if (currentStepIndex >= steps.length) {
      onComplete();
      return;
    }
    
    setCurrentStep(steps[currentStepIndex]);
  }, [currentStepIndex, steps, onComplete]);

  // Handle play/pause and timing
  useEffect(() => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
      timeoutRef.current = null;
    }

    if (isPlaying && currentStepIndex < steps.length - 1) {
      timeoutRef.current = setTimeout(() => {
        setCurrentStepIndex((prev) => prev + 1);
      }, speed);
    }

    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, [isPlaying, currentStepIndex, steps.length, speed]);

  // Find the global max value for proper scaling across all steps
  const allValues = steps.flatMap(step => step.array.filter(v => v !== null) as number[]);
  const globalMax = Math.max(...allValues);
  
  // Determine if we should show labels based on array size
  const showLabels = steps[0].array.length <= 30;

  // Height for bars (excluding labels)
  const barsContainerHeight = 180;
  // Space for labels
  const labelsHeight = 25;
  // Total visualization height
  const totalHeight = barsContainerHeight + (showLabels ? labelsHeight : 0);
  // Calculate width based on array length
  const barWidth = Math.max(4, Math.min(40, 500 / currentStep.array.length));

  return (
    <div className="w-full h-80 bg-gray-800 rounded-lg p-4">
      <div style={{ height: `${totalHeight}px`, position: 'relative' }}>
        {/* Bars container */}
        <div style={{ 
          height: `${barsContainerHeight}px`, 
          display: 'flex', 
          alignItems: 'flex-end', 
          justifyContent: 'center',
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0
        }}>
          {currentStep.array.map((value, index) => {
            // Skip rendering for null values (masked array elements)
            if (value === null) {
              return (
                <div key={`container-${index}`} style={{ 
                  width: `${barWidth}px`,
                  margin: '0 2px',
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center'
                }}>
                  <div style={{ 
                    width: '100%',
                    height: 0,
                    backgroundColor: 'transparent'
                  }} />
                </div>
              );
            }
            
            // Calculate actual pixel height (10px minimum)
            const barHeight = Math.max(10, (value / globalMax) * barsContainerHeight);
            
            const isSorted = currentStep.sorted?.includes(index);
            const isComparing = currentStep.comparing?.includes(index);
            const isSwapping = currentStep.swapping?.includes(index);
            const isPivot = currentStep.pivot === index;
            
            let barColor = "#3b82f6"; // blue-500
            
            if (isSorted) {
              barColor = "#22c55e"; // green-500
            } else if (isSwapping) {
              barColor = "#ef4444"; // red-500
            } else if (isComparing) {
              barColor = "#eab308"; // yellow-500
            } else if (isPivot) {
              barColor = "#a855f7"; // purple-500
            }
            
            return (
              <div key={`container-${index}`} style={{ 
                width: `${barWidth}px`,
                margin: '0 2px',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center'
              }}>
                <motion.div 
                  key={`bar-${value}-${index}`}
                  layout="position"
                  transition={{ 
                    type: "tween",
                    duration: isSwapping ? 0 : 0.2,
                    ease: "linear"
                  }}
                  style={{ 
                    width: '100%',
                    height: `${barHeight}px`,
                    backgroundColor: barColor,
                    borderRadius: '2px 2px 0 0'
                  }}
                />
              </div>
            );
          })}
        </div>
        
        {/* Fixed non-animated labels based on position */}
        {showLabels && (
          <div style={{ 
            position: 'absolute',
            bottom: 0,
            left: 0,
            right: 0,
            display: 'flex',
            justifyContent: 'center',
            height: `${labelsHeight}px`
          }}>
            {/* Use array indices for stable positioning */}
            {Array.from({ length: currentStep.array.length }).map((_, index) => {
              // const barWidth = Math.max(4, Math.min(40, 500 / currentStep.array.length));
              
              return (
                <div 
                  key={`fixed-label-pos-${index}`}
                  style={{
                    width: `${barWidth}px`,
                    margin: '0 2px',
                    textAlign: 'center'
                  }}
                >
                  <div style={{
                    fontSize: '0.75rem',
                    color: 'white',
                    paddingTop: '5px',
                    overflow: 'hidden',
                    textOverflow: 'ellipsis',
                    whiteSpace: 'nowrap'
                  }}>
                    {currentStep.array[index] !== null ? currentStep.array[index] : ''}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
      
      <div style={{ marginTop: '16px', textAlign: 'center' }}>
        Step {currentStepIndex + 1} of {steps.length}
      </div>
    </div>
  );
} 