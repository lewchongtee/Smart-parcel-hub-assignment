"""
member_a_task1_task2.py
Owner: Ooi Yan Zhe
Covers: Task 1 (Parcel Registration & Record Management) and
        Task 2 (Dispatch Queue, Returns Stack, Tracking BST)
CLO 2 / PLO 2 — 25% of total marks
"""

from shared_spec import (validate_parcel_input, ParcelValidationError, PRIORITY_LEVELS, STATUS_LEVELS)


# ============================================================
# TASK 1 — Parcel Registration and Record Management
# ============================================================

def add_parcel(database, tracking_id, sender, receiver, zone, weight, value, priority):
    tracking_id, sender, receiver, zone, weight, value, priority = validate_parcel_input(tracking_id, sender, receiver, zone, weight, value, priority)

    if any(p["tracking_id"] == tracking_id for p in database):
        raise ParcelValidationError("Tracking ID already exists.")

    database.append({
        "tracking_id": tracking_id,
        "sender": sender,
        "receiver": receiver,
        "zone": zone,
        "weight": weight,
        "value": value,
        "priority": priority,
        "status": "In Hub"
    })
    return database


def update_parcel(database, tracking_id, **fields_to_update):
    parcel = next((p for p in database if p["tracking_id"] == tracking_id), None)
    if parcel is None:
        raise ParcelValidationError("Tracking ID not found.")

    temp = parcel.copy()
    temp.update(fields_to_update)

    validate_parcel_input(
        temp["tracking_id"], temp["sender"], temp["receiver"],
        temp["zone"], temp["weight"], temp["value"], temp["priority"]
    )

    if temp.get("status") not in STATUS_LEVELS:
        raise ParcelValidationError(f"Status must be one of {STATUS_LEVELS}.")

    parcel.update(temp)
    return database


def delete_parcel(database, tracking_id):
    for i, p in enumerate(database):
        if p["tracking_id"] == tracking_id:
            database.pop(i)
            return database
    raise ParcelValidationError("Tracking ID not found.")


def display_parcels(database):
    if not database:
        print("No parcels in hub.")
        return

    fmt = "{:<10} {:<12} {:<12} {:<10} {:<8} {:<10} {:<10} {:<12}"
    print(fmt.format("Tracking","Sender","Receiver","Zone","Weight","Value","Priority","Status"))
    print("-"*90)
    for p in database:
        print(fmt.format(
            p["tracking_id"], p["sender"], p["receiver"], p["zone"],
            p["weight"], p["value"], p["priority"], p["status"]
        ))
# ============================================================
# TASK 2a — Dispatch Queue (FIFO)
# ============================================================

def add_to_dispatch_queue(queue, parcel):
    queue.append(parcel)
    return queue

def dispatch_next_parcel(queue):
    if not queue:
        raise ParcelValidationError("Dispatch queue is empty.")
    parcel = queue.pop(0)
    parcel["status"] = "Dispatched"
    return parcel

# ============================================================
# TASK 2b — Returns Stack (LIFO)
# ============================================================

def process_return_stack(stack, parcel):
    parcel["status"] = "Returned"
    stack.append(parcel)
    return stack

def inspect_next_return(stack):
    if not stack:
        raise ParcelValidationError("Returns stack is empty.")
    return stack.pop()

# ============================================================
# TASK 2c — Tracking BST (keyed on tracking_id)
# ============================================================

class BSTNode:
    def __init__(self, parcel):
        self.parcel = parcel
        self.tracking_id = parcel["tracking_id"]
        self.left = None
        self.right = None

def bst_insert(root, parcel):
    if root is None:
        return BSTNode(parcel)
    if parcel["tracking_id"] < root.tracking_id:
        root.left = bst_insert(root.left, parcel)
    elif parcel["tracking_id"] > root.tracking_id:
        root.right = bst_insert(root.right, parcel)
    else:
        raise ParcelValidationError("Tracking ID already exists.")
    return root

def bst_search(root, tracking_id):
    if root is None:
        return None
    if tracking_id == root.tracking_id:
        return root.parcel
    if tracking_id < root.tracking_id:
        return bst_search(root.left, tracking_id)
    return bst_search(root.right, tracking_id)

def bst_inorder(root, result=None):
    if result is None:
        result = []
    if root:
        bst_inorder(root.left, result)
        result.append(root.parcel)
        bst_inorder(root.right, result)
    return result
