'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import SortingVisualizer from '@/components/SortingVisualizer';
import { bubbleSort } from '@/lib/algorithms/sorting';
import { useRouter } from 'next/navigation';

export default function BubbleSortPage() {
  const router = useRouter();
  const [array, setArray] = useState<number[]>([]);
  const [steps, setSteps] = useState<ReturnType<typeof bubbleSort>>([]);
  const [isPlaying, setIsPlaying] = useState(false);
  const [speed, setSpeed] = useState(1000);
  const [arraySize, setArraySize] = useState(10);
  const [isComplete, setIsComplete] = useState(false);
  const [isInitialized, setIsInitialized] = useState(false);
  const [customInput, setCustomInput] = useState('');
  const [useCustomInput, setUseCustomInput] = useState(false);
  const [inputError, setInputError] = useState('');
  const [currentStep, setCurrentStep] = useState(0);

  // Generate a new random array
  const generateArray = () => {
    // Reset custom input state
    setUseCustomInput(false);
    setInputError('');
    
    // Generate new random array
    const newArray = Array.from({ length: arraySize }, () => Math.floor(Math.random() * 100) + 1);
    
    // Log for debugging
    console.log('Generated random array:', newArray);
    
    setArray(newArray);
    const newSteps = bubbleSort(newArray);
    setSteps(newSteps);
    setIsPlaying(false);
    setIsComplete(false);
    setIsInitialized(true);
    setCurrentStep(0);
  };

  // Parse and use custom input
  const handleCustomInput = () => {
    try {
      // Clean up the input string first
      const cleanInput = customInput
        .replace(/\s+/g, '') // Remove all whitespace
        .replace(/;/g, ',')  // Replace semicolons with commas
        .replace(/\[|\]|\(|\)/g, '') // Remove brackets and parentheses
        .replace(/,,+/g, ',') // Replace multiple commas with a single comma
        .replace(/^,|,$/g, ''); // Remove leading and trailing commas
      
      if (!cleanInput) {
        setInputError('Please enter some numbers');
        return;
      }
      
      // Parse the cleaned input string into an array of numbers
      const inputArray = cleanInput
        .split(',')
        .map(item => {
          if (!item) return null; // Skip empty entries
          
          const num = parseInt(item, 10);
          if (isNaN(num)) {
            throw new Error('Invalid input: contains non-numeric values');
          }
          if (num < 1) {
            throw new Error('All numbers must be positive (greater than 0)');
          }
          if (num > 1000) {
            throw new Error('Numbers must be less than or equal to 1000');
          }
          return num;
        })
        .filter((num): num is number => num !== null); // Remove null values and type assertion
      
      if (inputArray.length < 2) {
        setInputError('Please enter at least 2 numbers');
        return;
      }
      
      if (inputArray.length > 50) {
        setInputError('Maximum 50 numbers allowed');
        return;
      }

      // Normalize the array if the values are too different in scale
      const max = Math.max(...inputArray);
      const min = Math.min(...inputArray);
      
      // If the range is too large, normalize the values
      let normalizedArray = inputArray;
      if (max > 100 && max / min > 10) {
        // Scale down to a reasonable range (1-100)
        normalizedArray = inputArray.map(val => 
          Math.max(1, Math.min(100, Math.floor((val / max) * 100)))
        );
        setInputError('Note: Values have been normalized to fit the visualization');
      } else {
        setInputError('');
      }
      
      // Log for debugging
      console.log('Original input:', customInput);
      console.log('Cleaned input:', cleanInput);
      console.log('Parsed array:', inputArray);
      console.log('Normalized array:', normalizedArray);
      
      setArray(normalizedArray);
      const newSteps = bubbleSort(normalizedArray);
      setSteps(newSteps);
      setIsPlaying(false);
      setIsComplete(false);
      setIsInitialized(true);
      setUseCustomInput(true);
    } catch (error) {
      setInputError(error instanceof Error ? error.message : 'Invalid input');
    }
  };

  // Initialize the array
  useEffect(() => {
    if (!useCustomInput) {
      generateArray();
    }
  }, [arraySize, useCustomInput]);

  // Handle reset of the visualization
  const handleReset = () => {
    // Stop any ongoing animation
    setIsPlaying(false);
    setIsComplete(false);
    
    // Reset to the first step
    setCurrentStep(0);
    
    // Force a re-render by creating a new steps array with the same content
    // This ensures the SortingVisualizer component gets completely reset
    const resetSteps = JSON.parse(JSON.stringify(steps));
    setSteps(resetSteps);
    
    console.log('Visualization reset to beginning');
  };

  // Handle completion of the sorting visualization
  const handleComplete = () => {
    setIsPlaying(false);
    setIsComplete(true);
    setCurrentStep(steps.length - 1);
    console.log('Sorting visualization completed');
  };

  // Handle navigation back to home
  const navigateHome = () => {
    router.push('/');
  };

  return (
    <main className="min-h-screen bg-gray-900 p-6 text-white">
      <div className="max-w-6xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-3xl font-bold">Bubble Sort Visualization</h1>
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
        
        <h1 className="text-4xl font-bold mb-6">Bubble Sort</h1>
        
        <div className="mb-8 p-4 bg-gray-800 rounded-lg">
          <h2 className="text-xl font-semibold mb-2">Algorithm Explanation</h2>
          <p className="mb-4">
            Bubble Sort is a simple sorting algorithm that repeatedly steps through the list, 
            compares adjacent elements, and swaps them if they are in the wrong order. 
            The pass through the list is repeated until the list is sorted.
          </p>
          <div className="mb-2">
            <span className="font-semibold">Time Complexity:</span>
            <ul className="list-disc list-inside ml-4">
              <li>Best Case: O(n) - when the array is already sorted</li>
              <li>Average Case: O(n²)</li>
              <li>Worst Case: O(n²) - when the array is sorted in reverse order</li>
            </ul>
          </div>
          <div>
            <span className="font-semibold">Space Complexity:</span> O(1)
          </div>
        </div>

        <div className="mb-6 p-4 bg-gray-800 rounded-lg">
          <h3 className="text-lg font-semibold mb-3">Custom Input</h3>
          <div className="flex flex-col md:flex-row gap-3 mb-2">
            <input
              type="text"
              value={customInput}
              onChange={(e) => setCustomInput(e.target.value)}
              placeholder="Enter numbers separated by commas (e.g., 5, 3, 8, 1, 2)"
              className="flex-grow bg-gray-700 rounded px-3 py-2 text-white"
            />
            <button
              onClick={handleCustomInput}
              className="bg-blue-500 hover:bg-blue-600 px-4 py-2 rounded"
            >
              Use Custom Array
            </button>
          </div>
          {inputError && (
            <p className="text-red-500 text-sm mt-1">{inputError}</p>
          )}
          <p className="text-gray-400 text-sm mt-1">
            Enter numbers separated by commas. Example: 5, 3, 8, 1, 2
          </p>
        </div>

        <div className="mb-6 flex flex-wrap gap-4">
          <div>
            <label className="block mb-2">Array Size:</label>
            <select 
              value={arraySize}
              onChange={(e) => setArraySize(Number(e.target.value))}
              className="bg-gray-700 rounded px-3 py-2"
              disabled={useCustomInput}
            >
              <option value={5}>5</option>
              <option value={10}>10</option>
              <option value={15}>15</option>
              <option value={20}>20</option>
              <option value={30}>30</option>
              <option value={50}>50</option>
            </select>
          </div>
          
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
              <option value={10}>Very Fast</option>
            </select>
          </div>
          
          <div className="flex items-end">
            <button 
              onClick={generateArray}
              className="bg-blue-500 hover:bg-blue-600 px-4 py-2 rounded mr-2"
            >
              Generate Random Array
            </button>
          </div>
        </div>

        {/* Current array display */}
        {isInitialized && (
          <div className="mb-6 p-4 bg-gray-800 rounded-lg">
            <h3 className="text-lg font-semibold mb-2">Current Array</h3>
            <div className="flex flex-wrap gap-2">
              {array.map((value, index) => (
                <div key={index} className="bg-blue-500 px-3 py-1 rounded">
                  {value}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Visualization controls */}
        {isInitialized && (
          <div className="mb-6">
            <div className="flex flex-wrap gap-3">
              <button
                onClick={() => setIsPlaying(!isPlaying)}
                className="bg-green-500 hover:bg-green-600 px-4 py-2 rounded"
                disabled={isComplete}
              >
                {isPlaying ? 'Pause' : 'Play'}
              </button>
              
              <button
                onClick={handleReset}
                className="bg-gray-500 hover:bg-gray-600 px-4 py-2 rounded"
              >
                Reset
              </button>
              
              {isComplete && (
                <button
                  onClick={generateArray}
                  className="bg-blue-500 hover:bg-blue-600 px-4 py-2 rounded"
                >
                  New Array
                </button>
              )}
            </div>
          </div>
        )}

        {isInitialized && (
          <div className="mt-8">
            <SortingVisualizer
              key={`visualizer-${currentStep}-${steps.length}`}
              steps={steps}
              speed={speed}
              isPlaying={isPlaying}
              onComplete={handleComplete}
              initialStep={currentStep}
            />
          </div>
        )}
        
        <div className="mt-8 p-4 bg-gray-800 rounded-lg">
          <h2 className="text-xl font-semibold mb-2">Code Implementation</h2>
          <pre className="bg-gray-900 p-4 rounded overflow-x-auto">
            <code>{`function bubbleSort(arr) {
  const n = arr.length;
  
  for (let i = 0; i < n; i++) {
    for (let j = 0; j < n - i - 1; j++) {
      // Compare adjacent elements
      if (arr[j] > arr[j + 1]) {
        // Swap them if they are in the wrong order
        [arr[j], arr[j + 1]] = [arr[j + 1], arr[j]];
      }
    }
  }
  
  return arr;
}`}</code>
          </pre>
        </div>
      </div>
      
      {/* Algorithm Code */}
      <div className="mt-8 p-4 bg-gray-800 rounded-lg">
        <h3 className="text-xl font-bold mb-4">Bubble Sort Implementation</h3>
        <pre className="bg-gray-900 p-4 rounded-md overflow-x-auto text-sm">
          <code>{`
// Bubble Sort Algorithm
function bubbleSort(array) {
  const n = array.length;
  
  // Loop through the entire array
  for (let i = 0; i < n; i++) {
    // Last i elements are already sorted
    for (let j = 0; j < n - i - 1; j++) {
      // Compare adjacent elements
      if (array[j] > array[j + 1]) {
        // Swap if the element is greater than the next one
        [array[j], array[j + 1]] = [array[j + 1], array[j]];
      }
    }
  }
  
  return array;
}
          `}</code>
        </pre>
      </div>
    </main>
  );
} 