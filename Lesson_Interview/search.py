"""
Search by full sequence scanning

Complexity: O(n)
Memory complexity: O(1)
"""

unordered_elements = [12, 43, 1, 3, 44, 21, 18, 15, 19, 33, 45, 22, 2]


def search(element, elements):
    for index, candidate in enumerate(elements):
        if candidate == element:
            return index
    return -1


print(search(21, unordered_elements))
