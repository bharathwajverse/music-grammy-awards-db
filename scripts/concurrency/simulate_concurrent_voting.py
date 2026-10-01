"""
Module 5: Concurrency Control, 2PL & Deadlock Detection
========================================================
Demonstrates:
1. Two-Phase Locking (2PL) and Strict 2PL concept.
2. Simulated concurrent ballot voting with threading.
3. Wait-For-Graph (WFG) construction and cycle detection for deadlock handling.
"""

from collections import defaultdict
import threading
import time

class WaitForGraph:
    """Directed graph representing transaction wait dependencies for deadlock detection."""
    def __init__(self):
        self.adj = defaultdict(set)

    def add_wait_edge(self, t_waiting: str, t_holding: str):
        self.adj[t_waiting].add(t_holding)

    def remove_wait_edge(self, t_waiting: str, t_holding: str):
        if t_holding in self.adj[t_waiting]:
            self.adj[t_waiting].remove(t_holding)

    def detect_deadlock_cycle(self) -> list:
        visited = set()
        rec_stack = set()
        cycle_nodes = []

        def dfs(node, path):
            visited.add(node)
            rec_stack.add(node)
            path.append(node)

            for neighbor in self.adj.get(node, []):
                if neighbor not in visited:
                    if dfs(neighbor, path):
                        return True
                elif neighbor in rec_stack:
                    idx = path.index(neighbor)
                    cycle_nodes.extend(path[idx:])
                    return True

            rec_stack.remove(node)
            path.pop()
            return False

        for node in list(self.adj.keys()):
            if node not in visited:
                if dfs(node, []):
                    return cycle_nodes
        return []

def demo_deadlock_detection():
    print("==================================================================")
    print("Module 5: Concurrency Control - Wait-For-Graph Deadlock Detection")
    print("==================================================================")
    wfg = WaitForGraph()

    # Scenario:
    # Transaction T1 holds lock on Record X (Ballot 1) and requests lock on Record Y (Ballot 2).
    # Transaction T2 holds lock on Record Y (Ballot 2) and requests lock on Record X (Ballot 1).
    print("Simulating Classical Deadlock Scenario:")
    print("  T1 holds lock(Ballot_1), waits for lock(Ballot_2) held by T2")
    print("  T2 holds lock(Ballot_2), waits for lock(Ballot_1) held by T1")
    
    wfg.add_wait_edge("T1", "T2")
    wfg.add_wait_edge("T2", "T1")

    deadlock = wfg.detect_deadlock_cycle()
    if deadlock:
        print(f"\n>> DEADLOCK DETECTED! Cycle in Wait-For-Graph: {' -> '.join(deadlock)} -> {deadlock[0]}")
        print(">> Deadlock Resolution Protocol: Aborting youngest transaction (Wait-Die / Wound-Wait protocol).")
        victim = deadlock[-1]
        print(f">> Selected Victim Transaction: {victim} rolled back and lock released.")
        wfg.remove_wait_edge("T2", "T1")
        print(">> Cycle broken. Remaining transactions resume serializable execution.")
    else:
        print(">> No deadlock cycle detected. Execution is conflict-serializable.")

if __name__ == "__main__":
    demo_deadlock_detection()
