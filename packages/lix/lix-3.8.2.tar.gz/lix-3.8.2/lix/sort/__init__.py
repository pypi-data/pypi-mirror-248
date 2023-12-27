class bubblesort(object):
    '''
    Bubblesort class

    How it works:
        1. Compare the first two elements
        2. If the first element is greater than the second element, swap them
        3. Repeat step 1 and 2 until the end of the list
        4. Repeat step 3 until the list is sorted
    '''
    def __init__(self, array: list, *args, **kwargs) -> None:
        self.array:          list = array
        self.length:         int  = len(array)
        self.sorted:         bool = False
        self.swaps:          int  = 0
        self.comparisons:    int  = 0
        self.swapped:        bool = False
        self.sort()

    def sort(self) -> list:
        '''
        Sorts the list
        '''
        while not self.sorted:
            self.swapped = False
            for i in range(self.length - 1):
                self.comparisons += 1
                if self.array[i] > self.array[i + 1]:
                    self.array[i], self.array[i + 1] = self.array[i + 1], self.array[i]
                    self.swaps += 1
                    self.swapped = True

            if not self.swapped:
                self.sorted = True

        return self.array

    def __repr__(self) -> str:
        return f"bubblesort(length={self.length}, sorted={self.sorted}, swaps={self.swaps}, comparisons={self.comparisons})"

    def __str__(self) -> str:
        return f"bubblesort(length={self.length}, sorted={self.sorted}, swaps={self.swaps}, comparisons={self.comparisons})"

class quicksort(object):
    '''
    Quicksort class

    How it works:
        1. Choose a pivot element from the array
        2. Partition the array into two sub-arrays: elements less than the pivot and elements greater than the pivot
        3. Recursively apply steps 1 and 2 to the sub-arrays
        4. Combine the sorted sub-arrays to get the final sorted array
    '''
    def __init__(self, array: list, *args, **kwargs) -> None:
        self.array:          list = array
        self.length:         int  = len(array)
        self.sort()

    def sort(self) -> list:
        '''
        Sorts the list
        '''
        self._quicksort(0, self.length - 1)
        return self.array

    def _quicksort(self, low: int, high: int) -> None:
        '''
        Recursive helper function for Quicksort
        '''
        if low < high:
            pivot_index = self._partition(low, high)
            self._quicksort(low, pivot_index - 1)
            self._quicksort(pivot_index + 1, high)

    def _partition(self, low: int, high: int) -> int:
        '''
        Partition the array and return the pivot index
        '''
        pivot = self.array[high]
        i = low - 1

        for j in range(low, high):
            if self.array[j] <= pivot:
                i += 1
                self.array[i], self.array[j] = self.array[j], self.array[i]

        self.array[i + 1], self.array[high] = self.array[high], self.array[i + 1]
        return i + 1

    def __repr__(self) -> str:
        return f"quicksort(length={self.length})"

    def __str__(self) -> str:
        return f"quicksort(length={self.length})"

class mergesort(object):
    '''
    Mergesort class

    How it works:
        1. Divide the unsorted list into n sublists, each containing one element
        2. Repeatedly merge sublists to produce new sorted sublists until there is only one sublist remaining
    '''
    def __init__(self, array: list, *args, **kwargs) -> None:
        self.array:          list = array
        self.length:         int  = len(array)
        self.sort()

    def sort(self) -> list:
        '''
        Sorts the list
        '''
        self._mergesort(self.array)
        return self.array

    def _mergesort(self, array: list) -> None:
        '''
        Recursive helper function for Mergesort
        '''
        if len(array) > 1:
            mid = len(array) // 2
            left_half = array[:mid]
            right_half = array[mid:]

            self._mergesort(left_half)
            self._mergesort(right_half)

            i = j = k = 0

            while i < len(left_half) and j < len(right_half):
                if left_half[i] < right_half[j]:
                    array[k] = left_half[i]
                    i += 1
                else:
                    array[k] = right_half[j]
                    j += 1
                k += 1

            while i < len(left_half):
                array[k] = left_half[i]
                i += 1
                k += 1

            while j < len(right_half):
                array[k] = right_half[j]
                j += 1
                k += 1

    def __repr__(self) -> str:
        return f"mergesort(length={self.length})"

    def __str__(self) -> str:
        return f"mergesort(length={self.length})"

class radixsort(object):
    '''
    Radixsort class

    How it works:
        1. Sort the elements based on the least significant digit (LSB)
        2. Sort the elements based on the next significant digit, and repeat until all digits have been considered
    '''
    def __init__(self, array: list, *args, **kwargs) -> None:
        self.array:          list = array
        self.length:         int  = len(array)
        self.sort()

    def sort(self) -> list:
        '''
        Sorts the list
        '''
        max_element = max(self.array)
        exp = 1

        while max_element // exp > 0:
            self._counting_sort(exp)
            exp *= 10

        return self.array

    def _counting_sort(self, exp: int) -> None:
        '''
        Perform counting sort based on a given digit (exp)
        '''
        n = len(self.array)
        output = [0] * n
        count = [0] * 10

        for i in range(n):
            index = self.array[i] // exp
            count[index % 10] += 1

        for i in range(1, 10):
            count[i] += count[i - 1]

        i = n - 1
        while i >= 0:
            index = self.array[i] // exp
            output[count[index % 10] - 1] = self.array[i]
            count[index % 10] -= 1
            i -= 1

        i = 0
        for i in range(0, len(self.array)):
            self.array[i] = output[i]

    def __repr__(self) -> str:
        return f"radixsort(length={self.length})"

    def __str__(self) -> str:
        return f"radixsort(length={self.length})"

class heapsort(object):
    '''
    Heapsort class

    How it works:
        1. Build a max-heap from the input array
        2. Swap the root element (maximum value) with the last element of the heap
        3. Remove the last element (maximum value) from the heap, and decrease the heap size
        4. Restore the heap property by performing heapify on the new root
        5. Repeat steps 2-4 until the heap is empty
    '''
    def __init__(self, array: list, *args, **kwargs) -> None:
        self.array: list = array
        self.length: int = len(array)
        self.sort()

    def sort(self) -> list:
        '''
        Sorts the list
        '''
        n = len(self.array)

        # Build a max-heap
        for i in range(n // 2 - 1, -1, -1):
            self._heapify(n, i)

        # Extract elements one by one
        for i in range(n - 1, 0, -1):
            self.array[i], self.array[0] = self.array[0], self.array[i]  # swap
            self._heapify(i, 0)

        return self.array

    def _heapify(self, n: int, root: int) -> None:
        '''
        Perform heapify operation on a subtree rooted at the given index
        '''
        largest = root
        left = 2 * root + 1
        right = 2 * root + 2

        if left < n and self.array[root] < self.array[left]:
            largest = left

        if right < n and self.array[largest] < self.array[right]:
            largest = right

        if largest != root:
            self.array[root], self.array[largest] = self.array[largest], self.array[root]
            self._heapify(n, largest)

    def __repr__(self) -> str:
        return f"heapsort(length={self.length})"

    def __str__(self) -> str:
        return f"heapsort(length={self.length})"

class insertionsort(object):
    '''
    Insertion sort class

    How it works:
        1. Iterate over the list and consider each element as the "key"
        2. Compare the key with the elements before it and shift those elements to the right if they are greater than the key
        3. Insert the key into the correct position in the sorted portion of the list
        4. Repeat steps 1-3 until the entire list is sorted
    '''
    def __init__(self, array: list, *args, **kwargs) -> None:
        self.array: list = array
        self.length: int = len(array)
        self.sort()

    def sort(self) -> list:
        '''
        Sorts the list
        '''
        for i in range(1, self.length):
            key = self.array[i]
            j = i - 1

            while j >= 0 and self.array[j] > key:
                self.array[j + 1] = self.array[j]
                j -= 1

            self.array[j + 1] = key

        return self.array

    def __repr__(self) -> str:
        return f"insertionsort(length={self.length})"

    def __str__(self) -> str:
        return f"insertionsort(length={self.length})"


class selectionsort(object):
    '''
    Selection sort class

    How it works:
        1. Find the minimum element in the unsorted part of the list
        2. Swap the minimum element with the first element of the unsorted part
        3. Move the boundary of the sorted part one element to the right
        4. Repeat steps 1-3 until the entire list is sorted
    '''
    def __init__(self, array: list, *args, **kwargs) -> None:
        self.array: list = array
        self.length: int = len(array)
        self.sort()

    def sort(self) -> list:
        '''
        Sorts the list
        '''
        for i in range(self.length):
            min_index = i

            for j in range(i + 1, self.length):
                if self.array[j] < self.array[min_index]:
                    min_index = j

            self.array[i], self.array[min_index] = self.array[min_index], self.array[i]

        return self.array

    def __repr__(self) -> str:
        return f"selectionsort(length={self.length})"

    def __str__(self) -> str:
        return f"selectionsort(length={self.length})"

class shellsort(object):
    '''
    Shellsort class

    How it works:
        1. Divide the list into multiple sublists and sort each sublist using insertion sort
        2. Gradually reduce the gap between elements to sort the entire list efficiently
        3. Finally, perform an insertion sort on the entire list
    '''
    def __init__(self, array: list, *args, **kwargs) -> None:
        self.array: list = array
        self.length: int = len(array)
        self.sort()

    def sort(self) -> list:
        '''
        Sorts the list
        '''
        gap = self.length // 2

        while gap > 0:
            for i in range(gap, self.length):
                temp = self.array[i]
                j = i

                while j >= gap and self.array[j - gap] > temp:
                    self.array[j] = self.array[j - gap]
                    j -= gap

                self.array[j] = temp

            gap //= 2

        return self.array

    def __repr__(self) -> str:
        return f"shellsort(length={self.length})"

    def __str__(self) -> str:
        return f"shellsort(length={self.length})"

