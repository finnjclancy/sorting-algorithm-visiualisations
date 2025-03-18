'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import MergeSortVisualizer from '@/components/MergeSortVisualizer';
import { mergeSort, SortingStep } from '@/lib/algorithms/sorting';

export default function MergeSortPage() {
  const router = useRouter();
  
  // Algorithm state
  const [array, setArray] = useState<number[]>([]);
  const [steps, setSteps] = useState<SortingStep[]>([]);
  const [isPlaying, setIsPlaying] = useState(false);
  const [speed, setSpeed] = useState(2000); // much slower default speed
  const [currentStep, setCurrentStep] = useState(0);
  
  // Custom input state
  const [customInput, setCustomInput] = useState('');
  const [useCustomInput, setUseCustomInput] = useState(false);
  const [inputError, setInputError] = useState('');
  const [arraySize, setArraySize] = useState(10);
  
  // Generate random array of numbers
  const generateRandomArray = (length: number = arraySize) => {
    setArraySize(length);
    const newArray = Array.from({ length }, () => Math.floor(Math.random() * 100) + 1);
    setArray(newArray);
    setUseCustomInput(false);
    return newArray;
  };
  
  // Shuffle the current array
  const shuffleArray = () => {
    const shuffled = [...array];
    // Fisher-Yates shuffle algorithm
    for (let i = shuffled.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    
    setArray(shuffled);
    setUseCustomInput(false);
  };
  
  // Handle custom input
  const handleCustomInput = () => {
    try {
      // Clean input by removing whitespace and replacing commas and other separators
      const cleanInput = customInput
        .replace(/\s+/g, '')
        .replace(/;/g, ',')
        .replace(/\[|\]|\(|\)/g, '')
        .replace(/,,+/g, ',')
        .trim();
        
      // Split by comma and convert to numbers
      const values = cleanInput.split(',')
        .filter(val => val.trim() !== '')
        .map(val => {
          const num = Number(val);
          if (isNaN(num)) {
            throw new Error(`Invalid number: ${val}`);
          }
          return num;
        });
      
      if (values.length === 0) {
        throw new Error('Please enter at least one number');
      }
      
      // Set the new array
      setArray(values);
      setArraySize(values.length);
      setUseCustomInput(true);
      setInputError('');
    } catch (error) {
      setInputError((error as Error).message);
    }
  };
  
  // Initialize steps when array changes
  useEffect(() => {
    if (array.length > 0) {
      const sortingSteps = mergeSort([...array]);
      setSteps(sortingSteps);
      setCurrentStep(0);
      setIsPlaying(false);
    } else {
      // Generate a random array on initial load
      const newArray = generateRandomArray();
      setArray(newArray);
    }
  }, [array]);
  
  // Handle play/pause
  const togglePlay = () => {
    // If we're at the end, reset first
    if (currentStep >= steps.length - 1) {
      resetVisualization();
      // Give time for the reset to complete before starting playback
      setTimeout(() => setIsPlaying(true), 10);
    } else {
      setIsPlaying(!isPlaying);
    }
  };
  
  // Handle reset
  const resetVisualization = () => {
    // Stop any ongoing animation
    setIsPlaying(false);
    
    // Reset to the initial step
    setCurrentStep(0);
    
    // Force regeneration of the steps by recreating the array
    const sortingSteps = mergeSort([...array]);
    setSteps(sortingSteps);
    
    // Force a re-render of the component
    const tempArray = [...array];
    setArray([]);
    setTimeout(() => setArray(tempArray), 10);
  };
  
  // Handle speed change
  const handleSpeedChange = (newSpeed: number) => {
    setSpeed(newSpeed);
  };
  
  // Handle completion
  const handleComplete = () => {
    setIsPlaying(false);
  };
  
  // Handle navigation back to home
  const navigateHome = () => {
    router.push('/');
  };
  
  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      <div className="max-w-6xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-3xl font-bold">Merge Sort Visualization</h1>
          <button 
            onClick={navigateHome}
            className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg text-sm font-medium flex items-center gap-2"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
              <polyline points="9 22 9 12 15 12 15 22"></polyline>
            </svg>
            Home
          </button>
        </div>
        
        <div className="mb-6 p-4 bg-gray-800 rounded-lg shadow">
          <div className="text-lg font-semibold mb-2">What is Merge Sort?</div>
          <p className="text-gray-300 leading-relaxed">
            Merge Sort is a divide-and-conquer algorithm that works by recursively dividing the input array 
            into smaller subarrays until each subarray contains just one element, which is inherently sorted.
            The algorithm then merges these sorted subarrays back together in a way that produces the final 
            sorted result. This visualization shows both the splitting and merging phases of merge sort.
          </p>
          <div className="mt-4">
            <div className="font-semibold mb-1">Time Complexity:</div>
            <ul className="list-disc list-inside text-gray-300 ml-4">
              <li>Best case: O(n log n)</li>
              <li>Average case: O(n log n)</li>
              <li>Worst case: O(n log n)</li>
            </ul>
          </div>
          <div className="mt-4">
            <div className="font-semibold mb-1">Space Complexity:</div>
            <p className="text-gray-300">O(n) - Requires additional space proportional to the input size.</p>
          </div>
        </div>
        
        {/* Custom input section */}
        <div className="mb-6 p-4 bg-gray-800 rounded-lg">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label htmlFor="customInput" className="block text-sm font-medium mb-2">
                Custom Input (comma separated numbers)
              </label>
              <div className="flex gap-2">
                <input
                  id="customInput"
                  type="text"
                  value={customInput}
                  onChange={(e) => setCustomInput(e.target.value)}
                  placeholder="e.g., 5, 3, 8, 4, 2"
                  className="bg-gray-700 rounded-lg px-3 py-2 text-sm flex-grow"
                />
                <button
                  onClick={handleCustomInput}
                  className="px-3 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-sm font-medium"
                >
                  Set
                </button>
              </div>
              {inputError && (
                <p className="mt-2 text-red-400 text-sm">{inputError}</p>
              )}
            </div>
            
            <div className="flex flex-col md:flex-row gap-4 items-center">
              <div className="flex items-center gap-2">
                <span className="text-sm whitespace-nowrap">Array Size:</span>
                <select 
                  value={arraySize}
                  onChange={(e) => generateRandomArray(Number(e.target.value))}
                  className="bg-gray-700 rounded-lg px-3 py-2 text-sm"
                >
                  <option value={5}>5</option>
                  <option value={10}>10</option>
                  <option value={15}>15</option>
                  <option value={20}>20</option>
                  <option value={30}>30</option>
                </select>
              </div>
              
              <div className="flex gap-2">
                <button 
                  onClick={() => generateRandomArray()}
                  className="px-3 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-sm font-medium"
                >
                  Random Array
                </button>
                <button 
                  onClick={shuffleArray}
                  className="px-3 py-2 bg-indigo-600 hover:bg-indigo-700 rounded-lg text-sm font-medium"
                  disabled={array.length === 0}
                >
                  Shuffle
                </button>
              </div>
            </div>
          </div>
          
          {/* Display current array */}
          <div className="mt-4">
            <div className="text-sm font-medium mb-2">Current Array:</div>
            <div className="flex flex-wrap gap-2">
              {array.map((value, index) => (
                <div 
                  key={`current-${index}`}
                  className="px-2 py-1 bg-gray-700 rounded-md text-sm"
                >
                  {value}
                </div>
              ))}
            </div>
          </div>
        </div>
        
        {/* Visualization controls */}
        <div className="mb-6 flex justify-between items-center">
          <div className="flex items-center gap-4">
            <button 
              onClick={togglePlay}
              className={`p-3 rounded-full ${isPlaying ? 'bg-red-600 hover:bg-red-700' : 'bg-green-600 hover:bg-green-700'}`}
            >
              {isPlaying ? (
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <rect x="6" y="4" width="4" height="16"></rect>
                  <rect x="14" y="4" width="4" height="16"></rect>
                </svg>
              ) : (
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <polygon points="5 3 19 12 5 21 5 3"></polygon>
                </svg>
              )}
            </button>
            
            <button 
              onClick={resetVisualization}
              className="p-3 rounded-full bg-blue-600 hover:bg-blue-700"
              title="Reset"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M3 2v6h6"></path>
                <path d="M3 13a9 9 0 1 0 3-7.7L3 8"></path>
              </svg>
            </button>
          </div>
          
          <div className="flex flex-col">
            <label htmlFor="speedRange" className="mb-2 text-sm font-medium">Animation Speed</label>
            <input 
              id="speedRange"
              type="range" 
              min="500" 
              max="5000" 
              step="500" 
              value={speed} 
              onChange={(e) => handleSpeedChange(Number(e.target.value))}
              className="w-64"
            />
            <div className="flex justify-between mt-1 text-xs text-gray-400">
              <span>Fast</span>
              <span>Medium</span>
              <span>Slow</span>
            </div>
          </div>
          
          <div className="text-gray-300 text-sm">
            {currentStep > 0 && (
              <span>Step {currentStep} of {steps.length - 1}</span>
            )}
          </div>
        </div>
        
        {/* Visualization */}
        <div className="mb-8">
          <MergeSortVisualizer 
            steps={steps}
            speed={speed}
            isPlaying={isPlaying}
            onComplete={handleComplete}
            initialStep={currentStep}
            key={`visualizer-${array.join(',')}-${isPlaying}-${speed}`}
          />
        </div>
        
        {/* Algorithm explanation */}
        <div className="bg-gray-800 rounded-lg shadow p-4 mb-8">
          <h2 className="text-xl font-semibold mb-3">How Merge Sort Works</h2>
          <p className="text-gray-300 mb-4">
            Merge Sort works in two main phases:
          </p>
          
          <div className="mb-4">
            <h3 className="text-lg font-medium mb-2">1. Splitting Phase</h3>
            <ol className="list-decimal list-inside text-gray-300 space-y-2 ml-4">
              <li>Start with the complete unsorted array</li>
              <li>Divide the array into two halves (roughly equal size)</li>
              <li>Recursively divide each half into halves</li>
              <li>Continue until each subarray contains only one element</li>
              <li>Single-element arrays are inherently sorted</li>
            </ol>
          </div>
          
          <div>
            <h3 className="text-lg font-medium mb-2">2. Merging Phase</h3>
            <ol className="list-decimal list-inside text-gray-300 space-y-2 ml-4">
              <li>Start merging pairs of adjacent sorted subarrays</li>
              <li>Compare elements from both subarrays and merge in sorted order</li>
              <li>Continue merging larger subarrays until the entire array is sorted</li>
              <li>Each merge combines two sorted subarrays into a single sorted array</li>
            </ol>
          </div>
        </div>
      </div>
      
      {/* Algorithm Code */}
      <div className="mt-8 p-4 bg-gray-800 rounded-lg">
        <h3 className="text-xl font-bold mb-4">Merge Sort Implementation</h3>
        <pre className="bg-gray-900 p-4 rounded-md overflow-x-auto text-sm">
          <code>{`
// Merge Sort Algorithm
function mergeSort(array) {
  // Base case
  if (array.length <= 1) {
    return array;
  }
  
  // Split array into halves
  const middle = Math.floor(array.length / 2);
  const left = array.slice(0, middle);
  const right = array.slice(middle);
  
  // Recursively sort both halves
  return merge(
    mergeSort(left),
    mergeSort(right)
  );
}

// Merge two sorted arrays
function merge(left, right) {
  let result = [];
  let leftIndex = 0;
  let rightIndex = 0;
  
  // Compare elements from both arrays and add smaller one to result
  while (leftIndex < left.length && rightIndex < right.length) {
    if (left[leftIndex] < right[rightIndex]) {
      result.push(left[leftIndex]);
      leftIndex++;
    } else {
      result.push(right[rightIndex]);
      rightIndex++;
    }
  }
  
  // Add remaining elements
  return result
    .concat(left.slice(leftIndex))
    .concat(right.slice(rightIndex));
}
          `}</code>
        </pre>
      </div>
    </div>
  );
} 