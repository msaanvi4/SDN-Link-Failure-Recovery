"""
routing.py - Dynamic Routing with Dijkstra's Algorithm
Link Failure Detection and Recovery
Student: Saanvi Maharana | USN: PES1UG24AM237
"""

import heapq


def dijkstra(adj, source):
    """
    Compute shortest paths from source to all other nodes
    using Dijkstra's algorithm.
    Returns: (dist dict, prev dict)
    """
    dist = {node: float('inf') for node in adj}
    dist[source] = 0
    prev = {node: None for node in adj}
    heap = [(0, source)]

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in adj[u].items():
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(heap, (nd, v))

    return dist, prev


def reconstruct_path(prev, source, dest):
    """Reconstruct the shortest path from source to dest."""
    path = []
    cur = dest
    while cur is not None:
        path.append(cur)
        cur = prev.get(cur)
    path.reverse()
    if path and path[0] == source:
        return path
    return []   # no path exists


def build_routing_table(network):
    """
    Build routing tables for all nodes based on active topology.
    Returns a dict: { node -> { dest -> (next_hop, cost, path) } }
    """
    adj = network.get_active_adjacency()

    # Ensure all nodes appear in adj (even isolated ones)
    for node in network.nodes:
        if node not in adj:
            adj[node] = {}

    routing_tables = {}
    for src in network.nodes:
        dist, prev = dijkstra(adj, src)
        table = {}
        for dest in network.nodes:
            if dest == src:
                continue
            path = reconstruct_path(prev, src, dest)
            if len(path) >= 2:
                next_hop = path[1]
                cost = dist[dest]
            else:
                next_hop = None
                cost = float('inf')
            table[dest] = (next_hop, cost, path)
        routing_tables[src] = table
    return routing_tables


def print_routing_tables(routing_tables):
    """Pretty-print all routing tables."""
    print("\n" + "="*60)
    print("  ROUTING TABLES  (after topology update)")
    print("="*60)
    for src in sorted(routing_tables):
        print(f"\n  Router: {src}")
        print(f"  {'Dest':<8} {'Next Hop':<12} {'Cost':<8} Path")
        print(f"  {'-'*8} {'-'*12} {'-'*8} {'-'*20}")
        for dest in sorted(routing_tables[src]):
            nh, cost, path = routing_tables[src][dest]
            if nh is None:
                print(f"  {dest:<8} {'UNREACHABLE':<12} {'∞':<8} -")
            else:
                path_str = " -> ".join(path)
                print(f"  {dest:<8} {nh:<12} {cost:<8} {path_str}")
    print("="*60)


def print_single_path(routing_tables, src, dest):
    """Print the path between two specific nodes."""
    if src not in routing_tables:
        print(f"  [ERROR] Node '{src}' not in routing table.")
        return
    if dest not in routing_tables[src]:
        print(f"  [ERROR] Node '{dest}' not in routing table.")
        return
    nh, cost, path = routing_tables[src][dest]
    print(f"\n  Path from {src} to {dest}:")
    if nh is None:
        print(f"    ✗ NO PATH — nodes are disconnected!")
    else:
        print(f"    Route : {' -> '.join(path)}")
        print(f"    Cost  : {cost}")
        print(f"    Next  : {nh}")
