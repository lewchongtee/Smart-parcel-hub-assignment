def greedy_van_loading(parcels, max_weight, strategy="value_per_weight"):
  parcels_copy = list(parcels)


  if strategy == "value_per_weight":

    parcels_copy.sort(
        key=lambda p: 
        (
            p["value"] / p["weight"] if p["weight"] > 0 else 0
        ),
        reverse=True,
    )
  elif strategy == "priority":

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


  for parcel in parcels_copy:
    p_weight = parcel["weight"]
    p_value = parcel["value"]

    if total_weight + p_weight <= max_weight:
      selected_parcels.append(parcel)
      total_weight += p_weight
      total_value += p_value


  return selected_parcels, round(total_value, 2), round(total_weight, 2)


def knapsack_van_loading(parcels, max_weight):
  n = len(parcels)
  if n == 0 or max_weight <= 0:
    return [], 0.0, 0.0


  scale = (
      10 if any(isinstance(p["weight"], float) for p in parcels) else 1
  )


  scaled_max_weight = int(max_weight * scale)


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


  selected_parcels = []
  w = scaled_max_weight
  for i in range(n, 0, -1):
    if round(dp[i][w], 4) != round(dp[i - 1][w], 4):
      selected_parcel = parcels[i - 1]
      selected_parcels.append(selected_parcel)
      p_weight = int(round(selected_parcel["weight"] * scale))
      w -= p_weight

  selected_parcels.reverse()


  total_value = dp[n][scaled_max_weight]
  total_weight = sum(p["weight"] for p in selected_parcels)

  return selected_parcels, round(total_value, 2), round(total_weight, 2)


def compare_strategies(parcels, max_weight):
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


if __name__ == "__main__":

  test_parcels = [
      {
          "tracking_id": "P1",
          "weight": 10,
          "value": 60.0,
          "priority": "Standard",
      },
      {
          "tracking_id": "P2",
          "weight": 6,
          "value": 40.0,
          "priority": "Standard",
      },
      {
          "tracking_id": "P3",
          "weight": 4,
          "value": 30.0,
          "priority": "Standard",
      },
  ]


  greedy_failure_dataset = [
      {
          "tracking_id": "P1",
          "weight": 6,
          "value": 42.0,
          "priority": "Standard",
      },
      {
          "tracking_id": "P2",
          "weight": 5,
          "value": 30.0,
          "priority": "Standard",
      },
      {
          "tracking_id": "P3",
          "weight": 5,
          "value": 30.0,
          "priority": "Standard",
      },
  ]
  capacity = 10


  print("RUNNING TASK 4 VERIFICATION TEST CASE...\n")
  compare_strategies(greedy_failure_dataset, capacity)
