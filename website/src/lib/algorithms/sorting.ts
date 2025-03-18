export type SortingStep = {
  array: (number | null)[];
  subArrays?: (number | null)[][];
  comment?: string;
  // For visualization
  comparing?: [number, number];
  swapping?: [number, number];
  sorted?: number[];
  sortedIndices?: number[];
  // For quick sort visualization
  pivot?: number;
  partition?: {
    left: number;
    right: number;
  };
  // For merge sort visualization
  highlight?: number[];
  comparison?: number[];
  subArrayRange?: [number, number];
  subArray?: number[];
  merging?: {
    left: number[];
    right: number[];
    merged: number[];
    leftIndex: number;
    rightIndex: number;
  };
};

// Bubble Sort
export function bubbleSort(array: number[]): SortingStep[] {
  // Ensure we're working with a clean array
  const steps: SortingStep[] = [];
  const arr = [...array].filter(n => typeof n === 'number' && !isNaN(n));
  const n = arr.length;
  const sorted: number[] = [];

  // Log for debugging
  console.log('Starting bubble sort with array:', arr);

  steps.push({ array: [...arr] });

  for (let i = 0; i < n; i++) {
    for (let j = 0; j < n - i - 1; j++) {
      steps.push({ array: [...arr], comparing: [j, j + 1] });
      
      if (arr[j] > arr[j + 1]) {
        steps.push({ array: [...arr], swapping: [j, j + 1] });
        [arr[j], arr[j + 1]] = [arr[j + 1], arr[j]];
        steps.push({ array: [...arr] });
      }
    }
    sorted.unshift(n - i - 1);
    steps.push({ array: [...arr], sorted: [...sorted] });
  }

  // Log for debugging
  console.log('Bubble sort completed, steps:', steps.length);
  
  return steps;
}

// Selection Sort
export function selectionSort(array: number[]): SortingStep[] {
  // Ensure we're working with a clean array
  const steps: SortingStep[] = [];
  const arr = [...array].filter(n => typeof n === 'number' && !isNaN(n));
  const n = arr.length;
  const sorted: number[] = [];

  // Log for debugging
  console.log('Starting selection sort with array:', arr);

  steps.push({ array: [...arr] });

  for (let i = 0; i < n; i++) {
    let minIdx = i;
    
    // Find the minimum element in the unsorted part of the array
    for (let j = i + 1; j < n; j++) {
      steps.push({ array: [...arr], comparing: [minIdx, j] });
      
      if (arr[j] < arr[minIdx]) {
        minIdx = j;
      }
    }
    
    // Swap the found minimum element with the first element of the unsorted part
    if (minIdx !== i) {
      steps.push({ array: [...arr], swapping: [i, minIdx] });
      [arr[i], arr[minIdx]] = [arr[minIdx], arr[i]];
      steps.push({ array: [...arr] });
    }
    
    // Mark the current position as sorted
    sorted.push(i);
    steps.push({ array: [...arr], sorted: [...sorted] });
  }

  // Log for debugging
  console.log('Selection sort completed, steps:', steps.length);
  
  return steps;
}

// Insertion Sort
export function insertionSort(array: number[]): SortingStep[] {
  // Ensure we're working with a clean array
  const steps: SortingStep[] = [];
  const arr = [...array].filter(n => typeof n === 'number' && !isNaN(n));
  const n = arr.length;
  const sorted: number[] = [0]; // First element is initially considered sorted

  // Log for debugging
  console.log('Starting insertion sort with array:', arr);

  // Add initial state
  steps.push({ array: [...arr], sorted: [...sorted] });

  // Start from the second element (index 1)
  for (let i = 1; i < n; i++) {
    // Show the current element we're considering
    steps.push({ array: [...arr], comparing: [i, i] });
    
    let j = i;
    // While element at j is smaller than element at j-1, swap them
    while (j > 0) {
      // Compare elements
      steps.push({ array: [...arr], comparing: [j, j - 1] });
      
      if (arr[j] < arr[j - 1]) {
        // Show swapping
        steps.push({ array: [...arr], swapping: [j, j - 1] });
        
        // Swap elements
        [arr[j], arr[j - 1]] = [arr[j - 1], arr[j]];
        
        // Show array after swap
        steps.push({ array: [...arr] });
        
        j--;
      } else {
        // Element is in correct position, break the loop
        break;
      }
    }
    
    // Update sorted portion
    sorted.push(i);
    steps.push({ array: [...arr], sorted: [...sorted] });
  }

  // Log for debugging
  console.log('Insertion sort completed, steps:', steps.length);
  
  return steps;
}

// Merge Sort Algorithm
export function mergeSort(array: (number | null)[]): SortingStep[] {
  // Filter out non-numeric values
  const filteredArray = array.filter(num => num !== null) as number[];
  
  // Edge case: if array is empty or has only one element, it's already sorted
  if (filteredArray.length <= 1) {
    return [{
      array: [...filteredArray],
      comment: 'Single element array (already sorted)'
    }];
  }
  
  // Initialize steps with the initial state
  const steps: SortingStep[] = [
    {
      array: [...filteredArray],
      subArrays: [filteredArray],
      comment: 'Initial unsorted array'
    }
  ];
  
  // Maximum split depth based on array length
  const maxDepth = Math.ceil(Math.log2(filteredArray.length));
  
  // Store subarray sets for each depth to avoid recalculation
  const subArraysByDepth: number[][][] = [];
  subArraysByDepth[0] = [filteredArray];
  
  // Generate all splits iteratively from level 1 to maxDepth
  for (let depth = 1; depth <= maxDepth; depth++) {
    const currentDepthSubArrays: number[][] = [];
    
    // Process each subarray from the previous depth
    for (const subArray of subArraysByDepth[depth - 1]) {
      if (subArray.length <= 1) {
        // Can't split further, keep as is
        currentDepthSubArrays.push(subArray);
      } else {
        // Split into two parts
        const mid = Math.floor(subArray.length / 2);
        currentDepthSubArrays.push(subArray.slice(0, mid));
        currentDepthSubArrays.push(subArray.slice(mid));
      }
    }
    
    // Store this depth's subarrays
    subArraysByDepth[depth] = currentDepthSubArrays;
    
    // Add a step for this depth
    steps.push({
      array: [...filteredArray],
      subArrays: currentDepthSubArrays,
      comment: `Splitting at depth ${depth}`
    });
  }
  
  // Add a final step showing all elements separated if needed
  const finalSubArrays = subArraysByDepth[maxDepth].filter(arr => arr.length > 0);
  
  if (finalSubArrays.length > 0) {
    steps.push({
      array: [...filteredArray],
      subArrays: finalSubArrays,
      comment: 'Split complete - all elements separated'
    });
  }
  
  // Now handle the merging process (working backwards)
  // Only show completed merges at each depth level, not individual merges
  for (let depth = maxDepth; depth > 0; depth--) {
    // Get the subarrays at this depth
    const currentLevelArrays = [...subArraysByDepth[depth]];
    const resultLevelArrays: number[][] = [];
    
    // Merge pairs of adjacent subarrays without showing individual steps
    for (let i = 0; i < currentLevelArrays.length; i += 2) {
      if (i + 1 < currentLevelArrays.length) {
        // We have a pair to merge
        const left = currentLevelArrays[i];
        const right = currentLevelArrays[i + 1];
        
        // Merge the arrays
        const merged = mergeArrays(left, right);
        resultLevelArrays.push(merged);
      } else {
        // Odd number of arrays, just pass this one up
        resultLevelArrays.push(currentLevelArrays[i]);
      }
    }
    
    // Store these merged arrays for the next level up
    subArraysByDepth[depth - 1] = resultLevelArrays;
    
    // Add a step showing all merges at this level complete
    steps.push({
      array: [...filteredArray],
      subArrays: resultLevelArrays,
      comment: `Merge complete at depth ${depth - 1}`
    });
  }
  
  // Helper function to merge two sorted arrays
  function mergeArrays(left: number[], right: number[]): number[] {
    const result: number[] = [];
    let leftIndex = 0;
    let rightIndex = 0;
    
    while (leftIndex < left.length && rightIndex < right.length) {
      if (left[leftIndex] <= right[rightIndex]) {
        result.push(left[leftIndex]);
        leftIndex++;
      } else {
        result.push(right[rightIndex]);
        rightIndex++;
      }
    }
    
    // Add any remaining elements
    return result.concat(
      leftIndex < left.length ? left.slice(leftIndex) : right.slice(rightIndex)
    );
  }
  
  // Add the final sorted result
  const finalSortedArray = subArraysByDepth[0][0];
  steps.push({
    array: finalSortedArray,
    subArrays: [finalSortedArray],
    comment: 'Sorting complete'
  });
  
  return steps;
}

// Quick Sort
export function quickSort(array: number[]): SortingStep[] {
  // Ensure we're working with a clean array
  const steps: SortingStep[] = [];
  const arr = [...array].filter(n => typeof n === 'number' && !isNaN(n));
  
  // Log for debugging
  console.log('Starting quick sort with array:', arr);

  // Add initial state with a comment
  steps.push({ 
    array: [...arr], 
    comment: "Initial array", 
    subArrayRange: [0, arr.length-1],
    subArray: [...arr],
    sortedIndices: [] // Empty array, nothing sorted yet
  });

  // Skip if array is too small
  if (arr.length <= 1) {
    console.log('Array too small, already sorted');
    
    // Add final state
    if (arr.length === 1) {
      steps.push({ 
        array: [...arr], 
        sortedIndices: [0],
        comment: "Single element array (already sorted)"
      });
    }
    
    return steps;
  }

  // Track globally sorted indices
  const allSortedIndices = new Set<number>();

  const medianOfThreeSubarray = (low: number, high: number): number => {
    const subLen = high - low + 1;
    const mid = low + Math.floor(subLen / 2);
    
    const a = arr[low];
    const b = arr[mid];
    const c = arr[high];
    
    // Return the index of the median value
    if ((a <= b && b <= c) || (c <= b && b <= a)) {
      return mid;
    } else if ((b <= a && a <= c) || (c <= a && a <= b)) {
      return low;
    } else {
      return high;
    }
  };

  const quickSortHelper = (low: number, high: number, sortedIndices: Set<number>) => {
    if (low < high) {
      // Find the partition index using median-of-three pivot selection
      const pivotIndex = partition(low, high, sortedIndices);
      
      // Recursively sort elements before and after partition
      quickSortHelper(low, pivotIndex - 1, allSortedIndices);
      quickSortHelper(pivotIndex + 1, high, allSortedIndices);
    } else if (low === high) {
      // Single element subarray is already sorted
      allSortedIndices.add(low);
    }
  };
  
  const partition = (low: number, high: number, sortedIndices: Set<number>): number => {
    // Store original values for comment
    const firstVal = arr[low];
    const lastVal = arr[high];
    const subSize = high - low + 1;
    const midIndex = low + Math.floor(subSize / 2);
    const midVal = arr[midIndex];
    
    // Select pivot using median-of-three strategy
    const pivotIdx = medianOfThreeSubarray(low, high);
    const pivotVal = arr[pivotIdx];
    
    // Build pivot selection comment
    let howFound = "";
    if (subSize === 2) {
      howFound = `median of ${firstVal} and ${lastVal}`;
    } else if (subSize > 2) {
      howFound = `median of ${firstVal}, ${midVal}, and ${lastVal}`;
    }
    const comment = `Pivot ${pivotVal}\n${howFound}`;
    
    // Move pivot to the end of this subarray
    [arr[pivotIdx], arr[high]] = [arr[high], arr[pivotIdx]];
    
    let storeIndex = low;
    
    // Partition the array
    for (let j = low; j < high; j++) {
      if (arr[j] < pivotVal) {
        [arr[storeIndex], arr[j]] = [arr[j], arr[storeIndex]];
        storeIndex++;
      }
    }
    
    // Move pivot to its final position
    [arr[storeIndex], arr[high]] = [arr[high], arr[storeIndex]];
    
    // Mark this pivot as sorted
    allSortedIndices.add(storeIndex);
    
    // Add the step showing the current state of the full array after partitioning
    steps.push({ 
      array: [...arr], 
      pivot: storeIndex,
      comment: comment,
      subArrayRange: [low, high],
      subArray: arr.slice(low, high + 1),
      sortedIndices: [...allSortedIndices]
    });
    
    return storeIndex;
  };
  
  // Start the quick sort process
  quickSortHelper(0, arr.length - 1, allSortedIndices);
  
  // Final state (all elements are sorted)
  const sortedIndices = Array.from({ length: arr.length }, (_, i) => i);
  steps.push({ 
    array: [...arr], 
    sortedIndices: sortedIndices,
    comment: "Sorted array",
    subArrayRange: [0, arr.length-1],
    subArray: [...arr]
  });
  
  // Log completion
  console.log('Quick sort completed, steps:', steps.length);
  
  return steps;
} 