# Link Failure Detection and Recovery

**Student:** Saanvi Maharana  
**USN:** PES1UG24AM237 | **Group:** 14  
**Topic:** Link Failure Detection and Recovery  

---

## Objective
Detect link failures in a network and update routing dynamically to restore connectivity.

## Requirements Met
- ✅ Monitor topology changes
- ✅ Detect link failure
- ✅ Update flow rules (routing tables via Dijkstra's)
- ✅ Restore connectivity

---

## Project Structure

```
link_failure_project/
├── main.py        ← Entry point — run this
├── network.py     ← Network topology (nodes + links)
├── routing.py     ← Dijkstra's shortest path algorithm
├── monitor.py     ← Link failure/recovery detection
└── README.md
```

---

## How to Run (VS Code)

### Prerequisites
- Python 3.7+ (no external libraries needed — standard library only)

### Steps
1. Open the `link_failure_project/` folder in VS Code
2. Open a terminal: **Terminal → New Terminal**
3. Run:
   ```
   python main.py
   ```

---

## Network Topology

```
    A ---2--- B ---3--- C
    |         |         |
    4         1         2
    |         |         |
    D ---5--- E ---1--- F
```

- 6 nodes: A, B, C, D, E, F
- 7 links with weights (representing cost/latency)

---

## Features

| Option | Feature |
|--------|---------|
| 1 | View current topology with link status (UP/DOWN) |
| 2 | View routing tables for all nodes |
| 3 | Find shortest path between any two nodes |
| 4 | Simulate a link failure — routes update automatically |
| 5 | Restore a failed link — routes update automatically |
| 6 | Auto-monitor mode — random failures/recoveries over time |
| 7 | View full event log with timestamps |
| 8 | Reset to default topology |

---

## How It Works

1. **Topology** is stored as a weighted graph (adjacency list)
2. **Dijkstra's algorithm** computes shortest paths from every node to every other node
3. When a **link fails**, it's removed from the active topology and routes are recomputed
4. When a **link is restored**, it's re-added and routes are recomputed
5. **Auto-monitor** mode runs a background thread that randomly fails/restores links to simulate a live network environment
