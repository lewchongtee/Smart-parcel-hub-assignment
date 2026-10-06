"""
member_c_task4.py
Owner: [Kuhavengdesh]
Covers: Task 4 (Van Loading & Delivery Optimisation — Greedy vs DP)
CLO 4 / PLO 2 — 25% of total marks

IMPORTANT:
- Both functions take the same inputs so they can be run on the SAME
  data set and compared directly.
- Includes a test case where greedy is NOT optimal and DP is.
"""

# ============================================================
# Greedy Strategy
# ============================================================


def greedy_van_loading(parcels, max_weight, strategy="value_per_weight"):
  """Select parcels for a van trip using a greedy strategy, without exceeding

  max_weight. Returns (selected_parcels, total_value, total_weight).
  """
  parcels_copy = list(parcels)

  # 1. Decide ordering based on chosen strategy
  if strategy == "value_per_weight":
    # Sort descending by value / weight ratio
    parcels_copy.sort(
        key=lambda p: 
        (
            p["value"] / p["weight"] if p["weight"] > 0 else 0
        ),
        reverse=True,
    )
  elif strategy == "priority":
    # Order: Express (3) > Standard (2) > Economy (1)
    priority_map = {"Express": 3, "Standard": 2, "Economy": 1}
    parcels_copy.sort(
        key=lambda p: (
            priority_map.get(p.get("priority", "Standard"), 1),
            p["value"] / p["weight"] if p["weight"] > 0 else 0,
        ),
        reverse=True,
    )
  else:
    raise ValueError(f"Unknown strategy: '{strategy}'")

  selected_parcels = []
  total_weight = 0.0
  total_value = 0.0

  # 2 & 3. Walk through sorted list; add parcel if capacity permits,
  # skip non-fitting parcels and continue checking remaining items.
  for parcel in parcels_copy:
    p_weight = parcel["weight"]
    p_value = parcel["value"]

    if total_weight + p_weight <= max_weight:
      selected_parcels.append(parcel)
      total_weight += p_weight
      total_value += p_value

  # 4. Return selected parcels, total value, and total weight
  return selected_parcels, round(total_value, 2), round(total_weight, 2)


# ============================================================
# Dynamic Programming — 0/1 Knapsack
# ============================================================
def knapsack_van_loading(parcels, max_weight):
  """Solve the van loading problem as a 0/1 knapsack to MAXIMISE total declared

  value without exceeding max_weight. Returns (selected_parcels, total_value,
  total_weight).
  """
  n = len(parcels)
  if n == 0 or max_weight <= 0:
    return [], 0.0, 0.0

  # 1. Scaling factor handles decimal weights (e.g. 2.5kg scaled by 10)
  scale = (
      10 if any(isinstance(p["weight"], float) for p in parcels) else 1
  )
  # NOTE (integration fix): use floor, not round, for capacity. Rounding the
  # capacity UP (e.g. 4.99kg -> 50 scaled) can let the DP select parcels whose
  # true combined weight exceeds max_weight, even though each item's own
  # weight rounds normally. Floor guarantees the scaled capacity never
  # overstates real capacity.
  scaled_max_weight = int(max_weight * scale)

  # 2. Build DP table dp[i][w] = max value using first i parcels with capacity w
  dp = [[0.0] * (scaled_max_weight + 1) for _ in range(n + 1)]

  for i in range(1, n + 1):
    p_weight = int(round(parcels[i - 1]["weight"] * scale))
    p_value = float(parcels[i - 1]["value"])

    for w in range(1, scaled_max_weight + 1):
      if p_weight > w:
        dp[i][w] = dp[i - 1][w]
      else:
        dp[i][w] = max(
            dp[i - 1][w], dp[i - 1][w - p_weight] + p_value
        )

  # 3. Backtrack through DP table to identify selected parcels
  selected_parcels = []
  w = scaled_max_weight
  for i in range(n, 0, -1):
    if round(dp[i][w], 4) != round(dp[i - 1][w], 4):
      selected_parcel = parcels[i - 1]
      selected_parcels.append(selected_parcel)
      p_weight = int(round(selected_parcel["weight"] * scale))
      w -= p_weight

  selected_parcels.reverse()  # Restore original relative ordering

  # 4. Return results
  total_value = dp[n][scaled_max_weight]
  total_weight = sum(p["weight"] for p in selected_parcels)

  return selected_parcels, round(total_value, 2), round(total_weight, 2)


# ============================================================
# Comparison helper
# ============================================================


def compare_strategies(parcels, max_weight):
  """Run both greedy_van_loading() and knapsack_van_loading() on the same

  parcels/max_weight and print/return a comparison summary.
  """
  greedy_parcels, greedy_val, greedy_wt = greedy_van_loading(
      parcels, max_weight, strategy="value_per_weight"
  )
  dp_parcels, dp_val, dp_wt = knapsack_van_loading(parcels, max_weight)

  greedy_ids = sorted([p["tracking_id"] for p in greedy_parcels])
  dp_ids = sorted([p["tracking_id"] for p in dp_parcels])
  same_selection = greedy_ids == dp_ids
  greedy_is_optimal = greedy_val >= dp_val

  print("===========================================================")
  print("          VAN LOADING STRATEGY COMPARISON SUMMARY          ")
  print("===========================================================")
  print(f"Max Van Capacity : {max_weight} kg")
  print(f"Total Parcels Input: {len(parcels)}")
  print("-" * 59)
  print(
      f"GREEDY STRATEGY  : Loaded {len(greedy_parcels)} parcels | Weight:"
      f" {greedy_wt} kg | Value: RM {greedy_val:.2f}"
  )
  print(f"  Selected IDs   : {greedy_ids}")
  print(
      f"DYNAMIC PROG (DP): Loaded {len(dp_parcels)} parcels | Weight:"
      f" {dp_wt} kg | Value: RM {dp_val:.2f}"
  )
  print(f"  Selected IDs   : {dp_ids}")
  print("-" * 59)
  print(f"Same Selection?  : {same_selection}")
  print(f"Greedy Optimal?  : {greedy_is_optimal}")
  if not greedy_is_optimal:
    print(f"Value Gap        : RM {dp_val - greedy_val:.2f} lost by Greedy")
  print("===========================================================\n")

  return {
      "greedy": {
          "parcels": greedy_parcels,
          "value": greedy_val,
          "weight": greedy_wt,
      },
      "dp": {"parcels": dp_parcels, "value": dp_val, "weight": dp_wt},
      "greedy_is_optimal": greedy_is_optimal,
      "same_selection": same_selection,
  }


# ============================================================
# REQUIRED: Test Case Demonstrating Greedy Failure vs DP
# ============================================================
if __name__ == "__main__":
  # Test Case: Explicit dataset where Greedy yields suboptimal total value
  test_parcels = [
      {
          "tracking_id": "P1",
          "weight": 10,
          "value": 60.0,
          "priority": "Standard",
      },  # Ratio = 6.00
      {
          "tracking_id": "P2",
          "weight": 6,
          "value": 40.0,
          "priority": "Standard",
      },  # Ratio = 5.33
      {
          "tracking_id": "P3",
          "weight": 4,
          "value": 30.0,
          "priority": "Standard",
      },  # Ratio = 6.00
  ]
  # For max_weight = 10:
  # - Greedy picks P1 (Ratio 6.0, 10kg, Value RM60). Rem = 0kg. Total Value = RM 60.00.
  # - Wait, if P2 + P3 = 6kg + 4kg = 10kg, Value = RM 32 + RM 24 = RM 56 (P1 is better).

  # Correct Setup where Greedy fails:
  # P1 has HIGHER ratio than P2 and P3 individually, but P2 + P3 together give higher total value.
  greedy_failure_dataset = [
      {
          "tracking_id": "P1",
          "weight": 6,
          "value": 42.0,
          "priority": "Standard",
      },  # Ratio = 7.00 (Highest density)
      {
          "tracking_id": "P2",
          "weight": 5,
          "value": 30.0,
          "priority": "Standard",
      },  # Ratio = 6.00
      {
          "tracking_id": "P3",
          "weight": 5,
          "value": 30.0,
          "priority": "Standard",
      },  # Ratio = 6.00
  ]
  capacity = 10

  # Step-by-step logic:
  # 1. Greedy sorts by value density: P1 (7.00), P2 (6.00), P3 (6.00).
  # 2. Greedy picks P1 (Weight 6kg, Value RM42). Remaining capacity = 4kg.
  # 3. Greedy attempts P2 (5kg) -> Doesn't fit!
  # 4. Greedy attempts P3 (5kg) -> Doesn't fit!
  #    Greedy Final: [P1] -> Weight = 6kg, Value = RM 42.00.
  #
  # DP Evaluation:
  # - Option 1: Pick P1 (Weight 6kg, Value RM42.00)
  # - Option 2: Pick P2 + P3 (Weight 5 + 5 = 10kg, Value RM30 + RM30 = RM60.00)
  #    DP Final: [P2, P3] -> Weight = 10kg, Value = RM 60.00.
  # Optimality Gap: RM 60.00 (DP) vs RM 42.00 (Greedy) -> RM 18.00 lost by Greedy.

  print("RUNNING TASK 4 VERIFICATION TEST CASE...\n")
  compare_strategies(greedy_failure_dataset, capacity)