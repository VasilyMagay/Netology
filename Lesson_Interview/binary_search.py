"""
Binary tree search

Complexity: O(log n)
Memory complexity: O(log n)
"""

ordered_elements = [1, 2, 3, 12, 15, 18, 19, 21, 22, 33, 43, 44, 45]


def search(element, elements):
    for index, candidate in enumerate(elements):
        if candidate == element:
            return index
    return -1


def binary_search(element, elements, delta=0):
    length = len(elements)
    if length <= 2:
        result = search(element, elements)
        return result if result == -1 else result + delta
    index = length // 2
    candidate = elements[index]
    if candidate == element:
        return index + delta
    if candidate > element:
        return binary_search(element, elements[:index], delta)
    return binary_search(element, elements[index:], delta + index)


print(binary_search(21, ordered_elements))
