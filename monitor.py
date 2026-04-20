"""
monitor.py - Link Failure Detection and Monitoring
Link Failure Detection and Recovery
Student: Saanvi Maharana | USN: PES1UG24AM237
"""

import time
import threading
import random
from routing import build_routing_table, print_routing_tables


class LinkMonitor:
    """
    Monitors all links in the network and detects failures.
    On failure → updates routing tables automatically.
    """

    def __init__(self, network, poll_interval=3):
        self.network = network
        self.poll_interval = poll_interval  # seconds between checks
        self.routing_tables = {}
        self._running = False
        self._thread = None
        self.failure_count = 0
        self.recovery_count = 0

        # Build initial routing tables
        self._recompute_routing("Initial topology loaded")

    def _recompute_routing(self, reason="Topology change"):
        """Recompute all routing tables and print them."""
        print(f"\n  [MONITOR] Recomputing routes — {reason}")
        self.routing_tables = build_routing_table(self.network)
        self._check_connectivity()
        return self.routing_tables

    def _check_connectivity(self):
        """Check if any nodes are unreachable and warn."""
        unreachable = []
        for src, table in self.routing_tables.items():
            for dest, (nh, cost, path) in table.items():
                if nh is None:
                    unreachable.append((src, dest))
        if unreachable:
            print(f"  [MONITOR] ⚠  {len(unreachable)} node pair(s) UNREACHABLE:")
            for (s, d) in unreachable:
                print(f"             • {s} → {d}")
        else:
            print(f"  [MONITOR] ✓  All nodes are REACHABLE")

    def detect_failure(self, u, v):
        """Call when a link failure is detected. Updates routes."""
        print(f"\n{'!'*55}")
        print(f"  ⚡ LINK FAILURE DETECTED: {u} <--> {v}")
        print(f"{'!'*55}")
        success = self.network.fail_link(u, v)
        if success:
            self.failure_count += 1
            self._recompute_routing(f"Link {u}-{v} failed")
            print_routing_tables(self.routing_tables)
        return self.routing_tables

    def detect_recovery(self, u, v):
        """Call when a link is restored. Updates routes."""
        print(f"\n{'+'*55}")
        print(f"  ✅ LINK RECOVERY DETECTED: {u} <--> {v}")
        print(f"{'+'*55}")
        success = self.network.restore_link(u, v)
        if success:
            self.recovery_count += 1
            self._recompute_routing(f"Link {u}-{v} restored")
            print_routing_tables(self.routing_tables)
        return self.routing_tables

    def start_auto_monitor(self, duration=30, fail_prob=0.15):
        """
        Start background thread that randomly fails/restores links
        to simulate a live network. Runs for `duration` seconds.
        """
        self._running = True
        print(f"\n  [MONITOR] Auto-monitor started for {duration}s")
        print(f"            Checking every {self.poll_interval}s | "
              f"Failure probability: {int(fail_prob*100)}%\n")

        def _run():
            elapsed = 0
            while self._running and elapsed < duration:
                time.sleep(self.poll_interval)
                elapsed += self.poll_interval
                self._simulate_event(fail_prob)

            self._running = False
            print(f"\n  [MONITOR] Auto-monitor finished.")
            print(f"  Summary: {self.failure_count} failure(s), "
                  f"{self.recovery_count} recovery(ies)")

        self._thread = threading.Thread(target=_run, daemon=True)
        self._thread.start()

    def stop_auto_monitor(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=2)

    def _simulate_event(self, fail_prob):
        """Randomly fail or restore a link."""
        link_keys = list(self.network.links.keys())
        if not link_keys:
            return
        u, v = random.choice(link_keys)
        is_active = self.network.active_links[(u, v)]

        if is_active and random.random() < fail_prob:
            self.detect_failure(u, v)
        elif not is_active and random.random() < 0.6:
            self.detect_recovery(u, v)

    def stats(self):
        print(f"\n  Monitor Stats:")
        print(f"    Failures detected  : {self.failure_count}")
        print(f"    Recoveries detected: {self.recovery_count}")
