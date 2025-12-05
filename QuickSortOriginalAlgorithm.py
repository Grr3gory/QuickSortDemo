def QuickSort(slist):
    '''
    The simplest function I will make for this project, input a list then out it comes sorted
    This will be the basis of everything I iterate on as this project goes forward into
    becoming an app.
    '''
    if len(slist) <= 1: #Base Case to Break the loop
        return slist

    pivot = slist[len(slist) // 2] #For now, just choose the middle value to be the pivot

    slist_small = []
    slist_big = []  #--> These three empty lists are necessary to sort the items
    slist_pivot = []
#BELOW: Sort through the three. Comparing each value to the pivot.
    for i in slist:
        if i < pivot:
            slist_small.append(i)
        elif i > pivot:
            slist_big.append(i)
        else:
            slist_pivot.append(i)

    return QuickSort(slist_small) + QuickSort(slist_pivot) + QuickSort(slist_big) #Recursion + sort
