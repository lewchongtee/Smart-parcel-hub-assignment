import time
import matplotlib.pyplot as plt

from shared_spec import (
    ParcelValidationError, validate_parcel_input,
    PRIORITY_LEVELS, STATUS_LEVELS,
)
from member_a_task1_task2 import (
    add_parcel, update_parcel, delete_parcel, display_parcels,
    add_to_dispatch_queue, dispatch_next_parcel,
    process_return_stack, inspect_next_return,
    bst_insert, bst_search, bst_inorder,
)
from member_b_task3 import (
    recursive_binary_search, linear_search_by_receiver,
    merge_sort, count_bst_nodes,
)
from member_c_task4 import (
    greedy_van_loading, knapsack_van_loading, compare_strategies,
)

import random
# FAKE TEST DATA GENERATOR (used for benchmarking + demo seeding)

def generate_fake_parcels(n):
    zones = ["North", "South", "East", "West", "Central"]
    fake_database = []

    for i in range(n):
        parcel = {
            "tracking_id": f"MY{i:05d}",
            "sender": f"Sender_{i}",
            "receiver": f"Receiver_{i}",
            "zone": random.choice(zones),
            "weight": round(random.uniform(0.5, 50.0), 2),
            "value": round(random.uniform(10.0, 1000.0), 2),
            "priority": random.choice(PRIORITY_LEVELS),
            "status": "In Hub",
        }
        fake_database.append(parcel)

    return fake_database

# TASK 5a — Zone-wise and Priority-wise Reports

def generate_zone_report(parcels):
    print("\n--- Zone-Wise Operational Report ---")
    if not parcels:
        print("No parcels in the system.")
        return

    zone_data = {}
    for p in parcels:
        z = p["zone"]
        if z not in zone_data:
            zone_data[z] = {"count": 0, "total_weight": 0.0, "total_value": 0.0}
        zone_data[z]["count"] += 1
        zone_data[z]["total_weight"] += p["weight"]
        zone_data[z]["total_value"] += p["value"]

    for z, data in zone_data.items():
        print(f"Zone: {z} | Parcels: {data['count']} | "
              f"Total Weight: {data['total_weight']:.2f}kg | "
              f"Total Value: RM{data['total_value']:.2f}")


def generate_priority_report(parcels):
    print("\n--- Priority-Wise Operational Report ---")
    if not parcels:
        print("No parcels in the system.")
        return

    priority_data = {}
    for p in parcels:
        pri = p["priority"]
        if pri not in priority_data:
            priority_data[pri] = {"count": 0, "total_weight": 0.0, "total_value": 0.0}
        priority_data[pri]["count"] += 1
        priority_data[pri]["total_weight"] += p["weight"]
        priority_data[pri]["total_value"] += p["value"]

    for pri, data in priority_data.items():
        print(f"Priority: {pri} | Parcels: {data['count']} | "
              f"Total Weight: {data['total_weight']:.2f}kg | "
              f"Total Value: RM{data['total_value']:.2f}")


# TASK 5b — Empirical Timing vs Theoretical Complexity (REAL FUNCTIONS)

def benchmark_algorithms(sample_sizes, van_capacity=200):
    """Time all five real algorithms on increasing dataset sizes."""
    print("\n--- Running Benchmarks (real algorithms) ---")
    results = {
        "merge_sort": [],
        "binary_search": [],
        "linear_search": [],
        "greedy": [],
        "knapsack": [],
    }

    for n in sample_sizes:
        print(f"Testing with {n} parcels...")
        test_data = generate_fake_parcels(n)

        start_time = time.perf_counter()
        sorted_by_id = merge_sort(test_data, "tracking_id")
        results["merge_sort"].append(time.perf_counter() - start_time)

        target = sorted_by_id[n // 2]["tracking_id"]
        start_time = time.perf_counter()
        recursive_binary_search(sorted_by_id, target)
        results["binary_search"].append(time.perf_counter() - start_time)

        start_time = time.perf_counter()
        linear_search_by_receiver(test_data, "Receiver_1")
        results["linear_search"].append(time.perf_counter() - start_time)

        start_time = time.perf_counter()
        greedy_van_loading(test_data, van_capacity)
        results["greedy"].append(time.perf_counter() - start_time)

        start_time = time.perf_counter()
        knapsack_van_loading(test_data, van_capacity)
        results["knapsack"].append(time.perf_counter() - start_time)

    return results


def plot_benchmark_results(sample_sizes, results):
    plt.figure(figsize=(10, 6))
    for algo_name, times in results.items():
        plt.plot(sample_sizes, times, marker='o', label=algo_name.replace("_", " ").title())
    plt.title("Algorithm Performance: Empirical Timing vs Input Size (log scale)")
    plt.xlabel("Input Size (Number of Parcels)")
    plt.ylabel("Execution Time (Seconds, log scale)")
    plt.yscale("log")
    plt.grid(True, which="both")
    plt.legend()
    plt.savefig("benchmark_results_all.png")
    plt.close()

    plt.figure(figsize=(10, 6))
    for algo_name, times in results.items():
        if algo_name == "knapsack":
            continue
        plt.plot(sample_sizes, times, marker='o', label=algo_name.replace("_", " ").title())
    plt.title("Merge Sort / Binary Search / Linear Search / Greedy — Timing vs Input Size")
    plt.xlabel("Input Size (Number of Parcels)")
    plt.ylabel("Execution Time (Seconds)")
    plt.grid(True)
    plt.legend()
    plt.savefig("benchmark_results_fast4.png")
    plt.close()

    print("\nBenchmark complete! Saved 'benchmark_results_all.png' (log scale, "
          "all 5) and 'benchmark_results_fast4.png' (linear scale, excludes "
          "Knapsack) — use both in your report: the log chart shows Knapsack's "
          "cost relative to the rest, the linear chart shows the other four's "
          "actual growth shapes clearly.")


# TASK 6 — Input Validation Wrapper for the Console Menu

def safe_input_float(prompt):
    while True:
        user_input = input(prompt)
        try:
            value = float(user_input)
        except ValueError:
            print("Error: Invalid input. Please enter a numerical value.")
            continue
        if value <= 0:
            print("Error: Value must be a positive number greater than 0.")
            continue
        return value


def safe_input_choice(prompt, valid_choices):
    while True:
        choice = input(prompt).strip().title()
        if choice in valid_choices:
            return choice
        print(f"Error: Invalid choice. Please select from {valid_choices}.")


# MAIN — Console Menu Integration

def main():
    database = generate_fake_parcels(20)
    dispatch_queue = []
    returns_stack = []

    bst_root = None
    for p in database:
        bst_root = bst_insert(bst_root, p)
    print("Loaded 20 fake parcels for testing (also indexed into the BST).")

    while True:
        print("\n=== Smart Parcel Delivery Hub ===")
        print("1. Add New Parcel")
        print("2. Update Parcel")
        print("3. Delete Parcel")
        print("4. Display All Parcels")
        print("5. Dispatch Next Parcel (FIFO)")
        print("6. Process Return (LIFO)")
        print("7. Search Parcel by Tracking ID (BST)")
        print("8. Search Parcels by Receiver (Linear)")
        print("9. Generate Zone Report")
        print("10. Generate Priority Report")
        print("11. Van Loading — Compare Greedy vs DP")
        print("12. Run Algorithm Benchmarks (Generates Graph)")
        print("13. Exit")

        choice = input("Enter your choice: ").strip()

        try:
            if choice == '1':
                tracking_id = input("Enter Tracking ID: ").strip()
                sender = input("Enter Sender Name: ").strip()
                receiver = input("Enter Receiver Name: ").strip()
                zone = input("Enter Zone: ").strip()
                weight = safe_input_float("Enter Parcel Weight (kg): ")
                value = safe_input_float("Enter Declared Value (RM): ")
                priority = safe_input_choice(
                    "Enter Priority (Express/Standard/Economy): ", PRIORITY_LEVELS
                )
                database = add_parcel(database, tracking_id, sender, receiver, zone, weight, value, priority)
                new_parcel = next(p for p in database if p["tracking_id"] == tracking_id)
                bst_root = bst_insert(bst_root, new_parcel)
                print(f"Success! Parcel {tracking_id} added.")

            elif choice == '2':
                tracking_id = input("Enter Tracking ID to update: ").strip()
                field = input("Field to update (weight/value/zone/priority/status): ").strip().lower()
                if field == "weight":
                    new_val = safe_input_float("Enter new weight (kg): ")
                elif field == "value":
                    new_val = safe_input_float("Enter new declared value (RM): ")
                elif field == "priority":
                    new_val = safe_input_choice("Enter new priority: ", PRIORITY_LEVELS)
                elif field == "status":
                    new_val = safe_input_choice("Enter new status: ", STATUS_LEVELS)
                else:
                    new_val = input(f"Enter new {field}: ").strip()
                database = update_parcel(database, tracking_id, **{field: new_val})
                print(f"Success! Parcel {tracking_id} updated.")

            elif choice == '3':
                tracking_id = input("Enter Tracking ID to delete: ").strip()
                database = delete_parcel(database, tracking_id)
                print(f"Success! Parcel {tracking_id} deleted.")

            elif choice == '4':
                display_parcels(database)

            elif choice == '5':
                if dispatch_queue:
                    dispatched = dispatch_next_parcel(dispatch_queue)
                    print(f"Dispatched: {dispatched['tracking_id']}")
                else:
                    tracking_id = input("Queue empty. Enter Tracking ID to add & dispatch: ").strip()
                    parcel = next((p for p in database if p["tracking_id"] == tracking_id), None)
                    if parcel is None:
                        raise ParcelValidationError("Tracking ID not found in database.")
                    dispatch_queue = add_to_dispatch_queue(dispatch_queue, parcel)
                    dispatched = dispatch_next_parcel(dispatch_queue)
                    print(f"Dispatched: {dispatched['tracking_id']}")

            elif choice == '6':
                tracking_id = input("Enter Tracking ID being returned: ").strip()
                parcel = next((p for p in database if p["tracking_id"] == tracking_id), None)
                if parcel is None:
                    raise ParcelValidationError("Tracking ID not found in database.")
                returns_stack = process_return_stack(returns_stack, parcel)
                inspected = inspect_next_return(returns_stack)
                print(f"Inspected return: {inspected['tracking_id']}")

            elif choice == '7':
                tracking_id = input("Enter Tracking ID to search: ").strip()
                found = bst_search(bst_root, tracking_id)
                print(f"Found: {found}" if found else "Not found.")

            elif choice == '8':
                receiver = input("Enter Receiver name to search: ").strip()
                matches = linear_search_by_receiver(database, receiver)
                print(f"{len(matches)} match(es) found.")
                for m in matches:
                    print(f"  {m['tracking_id']} -> {m['receiver']}")

            elif choice == '9':
                generate_zone_report(database)

            elif choice == '10':
                generate_priority_report(database)

            elif choice == '11':
                max_weight = safe_input_float("Enter van capacity (kg): ")
                compare_strategies(database, max_weight)

            elif choice == '12':
                sizes = [50, 100, 500, 1000, 2000]
                results = benchmark_algorithms(sizes)
                plot_benchmark_results(sizes, results)

            elif choice == '13':
                print("Exiting system. Goodbye!")
                break

            else:
                print("Invalid choice. Please enter a number between 1 and 13.")

        except ParcelValidationError as e:
            print(f"\n[!] VALIDATION ERROR: {e}")
        except Exception as e:
            print(f"\n[!] UNEXPECTED SYSTEM ERROR: {e}")


if __name__ == "__main__":
    main()
