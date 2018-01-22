"""
return only unique values

Complexity: O(n)
Memory complexity: O(n)
"""

unordered_elements = [12, 43, 1, 3, 1, 3, 44, 21, 2, 18, 15, 19, 1, 33, 45, 2, 22, 2]


def unique(elements):
    seen = set()
    for element in elements:
        if element in seen:
            continue
        seen.add(element)
        yield element


print(list(unique(unordered_elements)))
