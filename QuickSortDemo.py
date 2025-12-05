import random as rnd
import gradio as gr

# Global state
CurrentArray = []
Segments = []          # list of (start, end) indices for unsorted segments
PivotHistory = []      # order of chosen pivots
ComparisonCount = 0    # total comparisons
SplitHistory = []      # list of (left_len, right_len) for each partition
OriginalSize = 0       # N, for reference


def show_randomize_list():
    """Generate a fresh random list and reset all state."""
    global CurrentArray, Segments, PivotHistory, ComparisonCount, SplitHistory, OriginalSize

    CurrentArray = list(range(1, 11)) #this is optimized for expansion edit THIS and line 205 to change length
    rnd.shuffle(CurrentArray) #shuffle it for display purposes

    OriginalSize = len(CurrentArray)
    Segments = [(0, OriginalSize - 1)]  # one big unsorted segment
    PivotHistory = []
    ComparisonCount = 0
    SplitHistory = []

    # initial display: one big block
    arr_str = "[" + ", ".join(map(str, CurrentArray)) + "]"

    #Pretty strings for display in Gradio
    return (
        f"{arr_str}<br>"
        f"<span style='color:green'>Previous pivots: []</span><br>"
        f"<span style='color:blue'>Total comparisons: 0</span>  |  "
        f"<span style='color:purple'>Complexity: N/A (no pivot chosen yet)</span>"
    )


def _complexity_label():
    """Use SplitHistory to classify behavior as ~N log N vs ~N^2."""
    if not SplitHistory:
        return "(no pivot chosen yet)" #Base Case

###BETWEEN THESE HASHTAGS CHATGPT HELPS ME WRITE THIS CODE
    balances = []
    for L, R in SplitHistory: #Split History stores the length of the left and right sub-lists
        if L == 0 or R == 0:
            balances.append(0.0)  # very unbalanced (Minimum and Maximum values will make one list be empty)
        else:
            smaller = min(L, R)
            larger = max(L, R)
            balances.append(smaller / larger) #A ratio of 1 is optimal, closer to 0 is least optimal

    avg_balance = sum(balances) / len(balances) #Compute the average value that each pivot gives to the balance
#Below we compare it to set values (ChatGPT generated) to give a score value in a user-friendly manner
    if avg_balance < 0.2:
        return "≈ O(N²) (very unbalanced pivots overall)"
    elif avg_balance > 0.5:
        return "≈ O(N log N) (mostly well-balanced pivots)"
    else:
        return "Between O(N log N) and O(N²) (mixed pivot quality)"
###BETWEEN THESE HASHTAGS CHATGPT HELPS ME WRITE THIS CODE

def ChoosePivot(BtnPiv):
    global CurrentArray, Segments, PivotHistory, ComparisonCount, SplitHistory

    if not CurrentArray:
        return "Please generate a list first." #Otherwise we get an error message when the big list is empty

    pivot_val = int(BtnPiv) #Call on the value of the button the user selected to be the pivot

    # Find which unsorted segment this pivot belongs to
    try:
        pivot_index = CurrentArray.index(pivot_val)
    except ValueError:
        return "Pivot value not found in array (something went wrong)." #MAYDAYMAYDAY (Should only happen if the user editted the code)

###CHATGPT HELPED WRITE THE BELOW CODE
    seg = None #Set the initial value
    for (start, end) in Segments: #Take the first and last value of each segment for comparison purposes
        if start <= pivot_index <= end: #Compare, if our pivot is within the first to last value then we are in the right sublist
            seg = (start, end) #Set to the correct sublist
            break
###CHATGPT HELPED WRITE THE ABOVE CODE

    if seg is None: #If we don't find a correct sublist...

        arr_str = _build_bracket_display(set(), 0, 0, 0)
        return (
            f"{arr_str}<br>"
            f"<span style='color:red'>That value is already fully sorted. " ###Then we know the pivot exists in a list of length 1
            f"Choose a pivot from an unsorted block.</span><br>"
            f"<span style='color:green'>Previous pivots: [{', '.join(map(str, PivotHistory))}]</span><br>"
            f"<span style='color:blue'>Total comparisons: {ComparisonCount}</span>  |  "
            f"<span style='color:purple'>Complexity: {_complexity_label()}</span>"
        )
##It would be helpful to make a case for when the entire list is completely sorted

    start, end = seg
    sub = CurrentArray[start:end + 1]

    # --- partition this subarray around pivot_val and count comparisons ---
    left, equal, right = [], [], []
    local_comps = 0

    for x in sub:
        local_comps += 1   #Comparison with the pivot for each value in the sublist
        if x < pivot_val:
            left.append(x)
        elif x > pivot_val:
            right.append(x) ##This is the quick sort code I originally wrote
        else:
            equal.append(x)

    ComparisonCount += local_comps #Add the comparisons from this step to the running total for display

    # Replace segment in the main array with left + equal + right
    left_len = len(left)
    equal_len = len(equal)
    right_len = len(right)

    CurrentArray[start:end + 1] = left + equal + right

    # Update segments: remove old, add new ones for left and right if size > 1
    Segments = [s for s in Segments if s != seg]

    if left_len > 1:
        Segments.append((start, start + left_len - 1))
    if right_len > 1:
        right_start = start + left_len + equal_len
        Segments.append((right_start, end))

    PivotHistory.extend(equal)
    SplitHistory.append((left_len, right_len))

    # Indices of the current equal (pivot) elements in the full array
    equal_indices = set(
        range(start + left_len, start + left_len + equal_len)
    )

    # Build full bracketed display of the array, respecting segments
    arr_str = _build_bracket_display(equal_indices, start, left_len, equal_len)

    left_str = "[" + ", ".join(map(str, left)) + "]"
    equal_str = ", ".join(map(str, equal)) if equal else ""
    right_str = "[" + ", ".join(map(str, right)) + "]"

    display = (
        f"{arr_str}<br>"
        f"<span style='color:red'>Current partition (subarray {start}–{end}): "
        f"{left_str} [ {equal_str} ] {right_str}</span><br>"
        f"<span style='color:green'>Previous pivots: [{', '.join(map(str, PivotHistory))}]</span><br>"
        f"<span style='color:blue'>Total comparisons: {ComparisonCount} "
        f"(this step: {local_comps})</span>  |  "
        f"<span style='color:purple'>Complexity so far: {_complexity_label()}</span>"
    )

    return display

###I struggled with the below function for a long while so I got ChatGPT to help with the below
def _build_bracket_display(equal_indices, seg_start, left_len, equal_len):
    """
    Build a string like:
    [1, 2] [3] [4] [5] [6, 7, 8, 9, 10]
    where:
      - any unsorted segment (len > 1) is one bracketed list,
      - any "sorted" single element is its own [x],
      - current pivot elements are colored red.
    """
    N = len(CurrentArray)
    seg_dict = {s: e for (s, e) in Segments}

    blocks = []
    i = 0
    while i < N:
        if i in seg_dict:
            s = i
            e = seg_dict[i]
            elems = []
            for idx in range(s, e + 1):
                val_str = str(CurrentArray[idx])
                if idx in equal_indices:
                    val_str = f"<span style='color:red'>{val_str}</span>"
                elems.append(val_str)
            blocks.append("[" + ", ".join(elems) + "]")
            i = e + 1
        else:
            val_str = str(CurrentArray[i])
            if i in equal_indices:
                val_str = f"<span style='color:red'>{val_str}</span>"
            blocks.append(f"[{val_str}]")
            i += 1

    return " ".join(blocks)


with gr.Blocks() as demo:
    gr.Markdown("## Interactive QuickSort — click a number to choose the pivot")

    out = gr.Markdown()

    gen_btn = gr.Button("Generate & Reset")
    gen_btn.click(fn=show_randomize_list, inputs=None, outputs=out)

    with gr.Row():
        for i in range(10): #Change this value to however long the list is to change length of list
            val = i + 1
            btn = gr.Button(str(val)) #Important to use the value and not the index!!
            btn.click(
                fn=lambda nmbr=val: ChoosePivot(nmbr),
                inputs=None,
                outputs=out,
            )

demo.launch()
