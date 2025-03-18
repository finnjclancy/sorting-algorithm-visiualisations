'use client';

import { useState, useEffect, useRef } from 'react';
import { SortingStep } from '@/lib/algorithms/sorting';
import { motion } from 'framer-motion';

type MergeSortVisualizerProps = {
  steps: SortingStep[];
  speed: number;
  isPlaying: boolean;
  onComplete: () => void;
  initialStep?: number;
};

const MergeSortVisualizer = ({
  steps,
  speed,
  isPlaying,
  onComplete,
  initialStep = 0,
}: MergeSortVisualizerProps) => {
  // Check if steps array is empty
  if (!steps || steps.length === 0) {
    return <div className="w-full h-80 bg-gray-800 rounded-lg p-4 flex items-center justify-center">
      <p>No data to visualize</p>
    </div>;
  }

  const [currentStepIndex, setCurrentStepIndex] = useState(initialStep);
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);
  
  // Reset when initialStep changes or steps array changes
  useEffect(() => {
    setCurrentStepIndex(initialStep);
    stopAllTimers();
  }, [initialStep, steps]);

  // Auto-scroll to the current step
  useEffect(() => {
    if (scrollRef.current && currentStepIndex > 0) {
      const stepElement = document.getElementById(`step-${currentStepIndex}`);
      if (stepElement) {
        stepElement.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }
    }
  }, [currentStepIndex]);

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
      moveToNextStep();
    }

    return stopAllTimers;
  }, [isPlaying, currentStepIndex, steps.length, speed]);

  // Move to the next step in the visualization
  const moveToNextStep = () => {
    if (!isPlaying || currentStepIndex >= steps.length - 1) {
      if (currentStepIndex >= steps.length - 1) {
        onComplete();
      }
      return;
    }

    timeoutRef.current = setTimeout(() => {
      setCurrentStepIndex(prevIndex => prevIndex + 1);
    }, speed);
  };

  // Get the current step
  const currentStep = steps[currentStepIndex];
  
  // Helper function to determine if a step is a merging step
  const isMergingStep = (step: SortingStep) => {
    return step.comment?.includes('Merged') || step.comment?.includes('Merge complete');
  };
  
  // Helper function to determine if we're at the final sorted step
  const isSortingComplete = (step: SortingStep) => {
    return step.comment?.includes('Sorting complete');
  };
  
  // Helper function to determine if this is the "split complete" step
  const isSplitComplete = (step: SortingStep) => {
    return step.comment?.includes('Split complete');
  };
  
  return (
    <div className="w-full bg-gray-800 rounded-lg p-4 shadow-lg overflow-auto" ref={scrollRef}>
      <div className="min-w-full">
        {/* Step progress indicator */}
        <div className="mb-6 text-center text-white sticky top-0 bg-gray-800 p-2 z-20 shadow-md">
          <div className="font-bold text-xl mb-2">Step {currentStepIndex + 1} of {steps.length}</div>
          <div className="text-sm text-gray-300 mb-4">
            {currentStep.comment || "Visualizing Merge Sort"}
          </div>
          
          {/* Color legend */}
          <div className="flex justify-center gap-4 flex-wrap">
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 bg-blue-500 rounded"></div>
              <span>Input Array</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 bg-indigo-500 rounded"></div>
              <span>Splitting</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 bg-purple-500 rounded"></div>
              <span>Split Complete</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 bg-green-500 rounded"></div>
              <span>Merging/Sorted</span>
            </div>
          </div>
        </div>
        
        {/* Display all the steps in a vertical layout */}
        <div className="space-y-6 pb-8">
          {steps.map((step, stepIndex) => {
            const isInitialStep = stepIndex === 0;
            const isCurrentStep = stepIndex === currentStepIndex;
            const isVisibleStep = stepIndex <= currentStepIndex;
            const isMerging = isMergingStep(step);
            const isComplete = isSortingComplete(step);
            const isSplitCompleteStep = isSplitComplete(step);
            
            if (!isVisibleStep) return null;
            
            return (
              <div 
                key={`step-${stepIndex}`}
                id={`step-${stepIndex}`}
                className={`p-4 rounded-lg ${isCurrentStep ? 'border-2 border-yellow-400' : ''}`}
              >
                {/* Step header */}
                <div className="flex items-center mb-4 text-white">
                  <div className={`h-6 w-6 rounded-full ${
                    isInitialStep ? 'bg-blue-500' : 
                    isSplitCompleteStep ? 'bg-purple-500' :
                    isMerging || isComplete ? 'bg-green-500' : 
                    'bg-indigo-500'
                  } mr-2`}></div>
                  <div className="font-medium">
                    {step.comment || `Step ${stepIndex + 1}`}
                  </div>
                  {isCurrentStep && (
                    <div className="ml-2 px-2 py-0.5 bg-yellow-500 text-black rounded-full text-xs font-bold">
                      Current
                    </div>
                  )}
                </div>
                
                {/* Display all subarrays side by side in a horizontal layout */}
                <div className="flex justify-center flex-wrap gap-4 mb-4">
                  {step.subArrays && step.subArrays.map((subArray, subArrayIndex) => {
                    // Determine color based on context
                    const bgColorClass = isInitialStep 
                      ? 'bg-blue-500' 
                      : isSplitCompleteStep
                        ? 'bg-purple-500'
                        : isComplete || isMerging
                          ? 'bg-green-500'
                          : 'bg-indigo-500';
                    
                    // Skip empty subarrays
                    if (subArray.length === 0) return null;
                    
                    return (
                      <div key={`subarray-${stepIndex}-${subArrayIndex}`} className="relative inline-block">
                        <div className="flex">
                          {subArray.map((value, valueIndex) => {
                            if (value === null) return null;
                            
                            return (
                              <motion.div
                                key={`value-${stepIndex}-${subArrayIndex}-${valueIndex}`}
                                initial={{ scale: 0.8, opacity: 0 }}
                                animate={{ scale: 1, opacity: 1 }}
                                transition={{ 
                                  duration: 0.3,
                                  delay: valueIndex * 0.05 
                                }}
                                className={`w-10 h-10 flex items-center justify-center m-1 rounded-md 
                                  font-bold text-white ${bgColorClass}`}
                              >
                                {value}
                              </motion.div>
                            );
                          })}
                        </div>
                        
                        {/* Box around subarray */}
                        <div 
                          className="absolute border-2 rounded-lg border-white"
                          style={{
                            left: '-4px',
                            top: '-4px',
                            width: 'calc(100% + 8px)',
                            height: 'calc(100% + 8px)',
                            zIndex: 5
                          }}
                        ></div>
                      </div>
                    );
                  })}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default MergeSortVisualizer; 