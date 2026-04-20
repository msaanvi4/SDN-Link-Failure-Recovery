"""
network.py - Network Topology Management
Link Failure Detection and Recovery
Student: Saanvi Maharana | USN: PES1UG24AM237
"""

import time
import random
from collections import defaultdict


class Network:
    """Represents a network topology as a weighted undirected graph."""

    def __init__(self):
        self.nodes = set()
        self.links = {}           # (u, v) -> weight
        self.active_links = {}    # (u, v) -> True/False
        self.link_history = []    # log of events

    def add_node(self, node):
        self.nodes.add(node)

    def add_link(self, u, v, weight=1):
        """Add a bidirectional link between two nodes."""
        self.nodes.add(u)
        self.nodes.add(v)
        key = tuple(sorted([u, v]))
        self.links[key] = weight
        self.active_links[key] = True
        self._log(f"[LINK ADDED]    {u} <--({weight})--> {v}")

    def fail_link(self, u, v):
        """Simulate a link failure."""
        key = tuple(sorted([u, v]))
        if key not in self.links:
            print(f"  [ERROR] Link {u}-{v} does not exist.")
            return False
        if not self.active_links[key]:
            print(f"  [WARN]  Link {u}-{v} is already down.")
            return False
        self.active_links[key] = False
        self._log(f"[LINK FAILURE]  {u} <--> {v} went DOWN")
        return True

    def restore_link(self, u, v):
        """Restore a failed link."""
        key = tuple(sorted([u, v]))
        if key not in self.links:
            print(f"  [ERROR] Link {u}-{v} does not exist.")
            return False
        if self.active_links[key]:
            print(f"  [WARN]  Link {u}-{v} is already UP.")
            return False
        self.active_links[key] = True
        self._log(f"[LINK RESTORED] {u} <--> {v} came BACK UP")
        return True

    def get_active_adjacency(self):
        """Return adjacency dict for only active (up) links."""
        adj = defaultdict(dict)
        for (u, v), active in self.active_links.items():
            if active:
                w = self.links[(u, v)]
                adj[u][v] = w
                adj[v][u] = w
        return adj

    def topology_summary(self):
        """Print current topology status."""
        print("\n" + "="*55)
        print("  CURRENT NETWORK TOPOLOGY")
        print("="*55)
        print(f"  Nodes  : {', '.join(sorted(self.nodes))}")
        print(f"  Links  : {len(self.links)} total")
        print()
        print(f"  {'Link':<15} {'Weight':<8} {'Status'}")
        print(f"  {'-'*15} {'-'*8} {'-'*10}")
        for (u, v), w in sorted(self.links.items()):
            status = "  UP  ✓" if self.active_links[(u, v)] else "  DOWN ✗"
            print(f"  {u} -- {v:<10} {w:<8} {status}")
        print("="*55)

    def _log(self, msg):
        ts = time.strftime("%H:%M:%S")
        entry = f"[{ts}] {msg}"
        self.link_history.append(entry)
        print(f"  {entry}")

    def print_log(self):
        print("\n" + "="*55)
        print("  EVENT LOG")
        print("="*55)
        for entry in self.link_history:
            print(f"  {entry}")
        print("="*55)


def build_default_network():
    """
    Build a sample 6-node network topology.

        A ---2--- B ---3--- C
        |         |         |
        4         1         2
        |         |         |
        D ---5--- E ---1--- F
    """
    net = Network()
    links = [
        ("A", "B", 2),
        ("B", "C", 3),
        ("A", "D", 4),
        ("B", "E", 1),
        ("C", "F", 2),
        ("D", "E", 5),
        ("E", "F", 1),
    ]
    for u, v, w in links:
        net.add_link(u, v, w)
    return net
