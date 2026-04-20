"""
main.py - Link Failure Detection and Recovery
==============================================
Student : Saanvi Maharana
USN     : PES1UG24AM237
Group   : 14
Topic   : Link Failure Detection and Recovery
Objective: Detect link failures and update routing dynamically.

Requirements:
  • Monitor topology changes
  • Detect link failure
  • Update flow rules
  • Restore connectivity

Run: python main.py
"""

import sys
import time
from network import build_default_network
from routing import (build_routing_table, print_routing_tables,
                     print_single_path)
from monitor import LinkMonitor


BANNER = """
╔══════════════════════════════════════════════════════╗
║     LINK FAILURE DETECTION AND RECOVERY SYSTEM       ║
║──────────────────────────────────────────────────────║
║  Student : Saanvi Maharana                           ║
║  USN     : PES1UG24AM237  |  Group: 14              ║
╚══════════════════════════════════════════════════════╝
"""

MENU = """
  ┌─────────────────────────────────────────────┐
  │                 MAIN MENU                   │
  ├─────────────────────────────────────────────┤
  │  1. View Network Topology                   │
  │  2. View Routing Tables                     │
  │  3. Find Path Between Two Nodes             │
  │  4. Simulate Link Failure                   │
  │  5. Restore a Failed Link                   │
  │  6. Run Auto-Monitor (random events)        │
  │  7. View Event Log                          │
  │  8. Reset Network to Default                │
  │  0. Exit                                    │
  └─────────────────────────────────────────────┘
"""


def get_nodes_prompt(net, prompt):
    nodes = sorted(net.nodes)
    print(f"  Available nodes: {', '.join(nodes)}")
    raw = input(f"  {prompt} (e.g. A B): ").strip().upper().split()
    if len(raw) < 2:
        print("  [ERROR] Please enter two node names.")
        return None, None
    return raw[0], raw[1]


def main():
    print(BANNER)

    # ── Build network & monitor ──────────────────────────────────
    print("  Building default 6-node network...\n")
    net = build_default_network()
    monitor = LinkMonitor(net)

    print("\n  Network topology:")
    net.topology_summary()
    print()

    # ── Menu loop ────────────────────────────────────────────────
    while True:
        print(MENU)
        choice = input("  Enter choice: ").strip()

        # 1 - Topology
        if choice == "1":
            net.topology_summary()

        # 2 - Routing tables
        elif choice == "2":
            rt = build_routing_table(net)
            print_routing_tables(rt)

        # 3 - Path query
        elif choice == "3":
            src, dest = get_nodes_prompt(net, "Enter source and destination")
            if src and dest:
                rt = build_routing_table(net)
                print_single_path(rt, src, dest)

        # 4 - Fail a link
        elif choice == "4":
            net.topology_summary()
            u, v = get_nodes_prompt(net, "Enter link to FAIL")
            if u and v:
                monitor.detect_failure(u, v)
                net.topology_summary()

        # 5 - Restore a link
        elif choice == "5":
            net.topology_summary()
            u, v = get_nodes_prompt(net, "Enter link to RESTORE")
            if u and v:
                monitor.detect_recovery(u, v)
                net.topology_summary()

        # 6 - Auto monitor
        elif choice == "6":
            try:
                dur = int(input("  Duration in seconds (default 20): ").strip() or "20")
            except ValueError:
                dur = 20
            monitor.start_auto_monitor(duration=dur, fail_prob=0.3)
            print(f"\n  Auto-monitor running for {dur}s. Press Enter to return to menu...")
            input()
            monitor.stop_auto_monitor()
            monitor.stats()

        # 7 - Event log
        elif choice == "7":
            net.print_log()

        # 8 - Reset
        elif choice == "8":
            print("\n  Resetting network to default topology...")
            net = build_default_network()
            monitor = LinkMonitor(net)
            net.topology_summary()

        # 0 - Exit
        elif choice == "0":
            print("\n  Goodbye! Network simulation ended.\n")
            sys.exit(0)

        else:
            print("  [ERROR] Invalid choice, please try again.")


if __name__ == "__main__":
    main()
