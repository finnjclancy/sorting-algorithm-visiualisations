'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import QuickSortVisualizer from '@/components/QuickSortVisualizer';
import SortingVisualizer from '@/components/SortingVisualizer';
import { quickSort } from '@/lib/algorithms/sorting';
import { useRouter } from 'next/navigation';

export default function QuickSortPage() {
  const router = useRouter();
  const [array, setArray] = useState<number[]>([]);
  const [steps, setSteps] = useState<ReturnType<typeof quickSort>>([]);
  const [isPlaying, setIsPlaying] = useState(false);
  const [speed, setSpeed] = useState(5000); // Default to slow speed (5000ms)
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
    const newSteps = quickSort(newArray);
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
      const newSteps = quickSort(normalizedArray);
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
    // This ensures the visualizer component gets completely reset
    const resetSteps = JSON.parse(JSON.stringify(steps));
    setSteps(resetSteps);
    
    console.log('Visualization reset to beginning');
  };

  // Handle completion of the sorting visualization
  const handleComplete = () => {
    setIsPlaying(false);
    setIsComplete(true);
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
          <h1 className="text-3xl font-bold">Quick Sort Visualization</h1>
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
        
        <h1 className="text-4xl font-bold mb-6">Quick Sort</h1>
        
        <div className="mb-8 p-4 bg-gray-800 rounded-lg">
          <h2 className="text-xl font-semibold mb-2">Algorithm Explanation</h2>
          <p className="mb-4">
            Quick Sort is a highly efficient divide-and-conquer sorting algorithm. It works by selecting a 'pivot' element from the array 
            and partitioning the other elements into two sub-arrays according to whether they are less than or greater than the pivot.
            The sub-arrays are then recursively sorted. This process continues until the base case of an empty or single-item array is reached.
          </p>
          <div className="mb-2">
            <span className="font-semibold">Time Complexity:</span>
            <ul className="list-disc list-inside ml-4">
              <li>Best Case: O(n log n) - when the pivot always divides the array in the middle</li>
              <li>Average Case: O(n log n)</li>
              <li>Worst Case: O(n²) - when the smallest or largest element is always chosen as pivot</li>
            </ul>
          </div>
          <div className="mb-2">
            <span className="font-semibold">Space Complexity:</span> O(log n) - due to the recursive call stack
          </div>
          <div>
            <span className="font-semibold">Key Features:</span>
            <ul className="list-disc list-inside ml-4">
              <li>In-place sorting (requires small additional space)</li>
              <li>Unstable sort (relative order of equal elements may change)</li>
              <li>Typically faster than merge sort for arrays that fit in memory</li>
            </ul>
          </div>
        </div>

        <div className="mb-6 p-4 bg-gray-800 rounded-lg">
          <h3 className="text-lg font-semibold mb-3">Visualization Guide</h3>
          <p className="mb-3">
            This visualization shows the step-by-step process of Quick Sort:
          </p>
          <ul className="list-disc list-inside ml-4 mb-3">
            <li>Each row represents a stage in the sorting process</li>
            <li>The black box highlights the current subarray being sorted</li>
            <li>Pivot elements are shown in <span className="bg-purple-500 px-2 py-1 rounded text-white">purple</span></li>
            <li>Sorted elements are shown in <span className="bg-green-500 px-2 py-1 rounded text-white">green</span></li>
            <li>Unsorted elements are shown in <span className="bg-red-500 px-2 py-1 rounded text-white">red</span></li>
            <li>The median-of-three strategy is used to select pivots for better average performance</li>
          </ul>
          <p className="text-sm text-gray-400">
            Note: This visualization style is based on the classic approach used in CS education courses to demonstrate the recursive nature of Quick Sort.
          </p>
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
              <option value={8000}>Very Slow</option>
              <option value={5000}>Slow</option>
              <option value={2000}>Medium</option>
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
            <QuickSortVisualizer
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
            <code>{`function quickSort(arr) {
  // Base case: arrays with 0 or 1 element are already sorted
  if (arr.length <= 1) {
    return arr;
  }
  
  // Choose a pivot (here we choose the last element)
  const pivot = arr[arr.length - 1];
  
  // Create arrays for elements less than and greater than the pivot
  const less = [];
  const greater = [];
  
  // Partition the array
  for (let i = 0; i < arr.length - 1; i++) {
    if (arr[i] < pivot) {
      less.push(arr[i]);
    } else {
      greater.push(arr[i]);
    }
  }
  
  // Recursively sort the sub-arrays and combine with pivot
  return [...quickSort(less), pivot, ...quickSort(greater)];
}`}</code>
          </pre>
        </div>
      </div>
    </main>
  );
} 