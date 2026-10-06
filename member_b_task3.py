def recursive_binary_search(sorted_parcels, target_id, low=0, high=None):
    if high is None:
        high = len(sorted_parcels) - 1

    if low > high:
        return None

    mid = (low + high) // 2

    if sorted_parcels[mid]["tracking_id"] == target_id:
        return sorted_parcels[mid]

    if target_id < sorted_parcels[mid]["tracking_id"]:
        return recursive_binary_search(sorted_parcels, target_id, low, mid - 1)

    return recursive_binary_search(sorted_parcels, target_id, mid + 1, high)


def linear_search_by_receiver(parcels, receiver_name):
    matches = []

    for parcel in parcels:
        if parcel["receiver"].lower() == receiver_name.lower():
            matches.append(parcel)

    return matches


def merge_sort(parcels, key):
    if len(parcels) <= 1:
        return list(parcels)

    mid = len(parcels) // 2
    left_half = parcels[:mid]
    right_half = parcels[mid:]

    left_sorted = merge_sort(left_half, key)
    right_sorted = merge_sort(right_half, key)

    return _merge(left_sorted, right_sorted, key)


def _merge(left, right, key):
    merged = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if left[i][key] <= right[j][key]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])

    return merged


def count_bst_nodes(root):
    if root is None:
        return 0

    return 1 + count_bst_nodes(root.left) + count_bst_nodes(root.right)
