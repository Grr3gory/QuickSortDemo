Gregory Langille
Dr. Rahatara Ferdousi
CISC – 121
2025 – 12 – 06

# Selective pivot Quick Sort Demo

##![QuickSortAppDemo](https://github.com/user-attachments/assets/99394fd2-8df6-44b2-bf05-fd2190f02daf)

## 
Step 2 — Plan Using Computational Thinking
### Decomposition: What smaller steps form your algorithm?

#### 1.	Choose a pivot
The user selects a pivot using buttons 1 through 10.
#### 2.	Split the list around the pivot
Use a quicksort algorithm to compare the values to the pivot, keeping track of how many comparisons have been made (for complexity comparison). Split the list into smaller, equal (won’t happen given the list is 1 to 10) and larger sub - lists. 
#### 3.	Recursion until base case
Steps 1 and 2 are repeated on each sub-list, until a length of 1 is reached in which case we know that the sublist is in it’s sorted spot. 

### Pattern Recognition: How does it repeatedly compare or swap values?
1.	At each ‘split the list’ step we will need to compare every item in the     list/sub-list to the pivot to determine whether the item needs to go to     the left or to the right. 
2.	The pattern is simply: Choose pivot in the list/sub-list, put pivot in       right spot and split the list into sub-lists, repeat.

### Abstraction: What details are simplified for the user?
#### 1.	Pivot buttons
Instead of worrying about indices, or inputting a valid input, the user simply clicks a value, which is slightly more complex in coding but is more intuitive when using the app. Conceptually, this can represent different pivot strategies (e.g., first element, last element, random element, “middle” element), but the UI reduces this to “pick the number you want as the pivot”. [Colours to represent first, last, random, and mean average value could be used to give more of an educational feel, with the benefits and risks to each in a separate block like an interactive museum kiosk]
#### 2.	Visual blocks instead of raw lists
The user sees clearly separated bracketed lists (sub-arrays) on the screen, (Writing this point after finishing the code, my first demo kept the list together except for the pivot and it was not evident what counted as a ‘sorted’ list)
#### 3. unused idea: 
I had the idea of simplifying the buttons to just be first, last, median, or random, which would simplify further, but I feel it is more educational and fun to try and find the exact right order to get the lowest # of comparisons. 
### Algorithm Design
Inputs: Generate and Reset (Reset the simulation) & Pivot buttons (Select pivot to use for next step of recursion)

Processing: Locate the sub-list that contains a chosen pivot
Perform a recursion step of the quick sort algorithm on said sublist using the pivot value as the pivot.
Update the display list (Separating the sublists by square bracket)

Outputs: Sublists, comparison value, and rough complexity notation

## Steps to Run:
Click generate and Reset, then select various pivots until the list is completely sorted

## https://huggingface.co/spaces/Grr3g/QuickSortDemo
## Gregory Langille & ChatGPT




