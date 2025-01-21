# Discuss the Impact of Heterogeneous Network on PLB Performance

## Authors
- Yu-Chen (Tony) Liu
- Yu-Chi (Brian) Ho
- Chih-Hao (Morris) Chuang

Advisor: Prof. Ramesh Govindan

---

## Introduction
- **PLB (Protective Load Balancing)**:
  - A host-based design for link load balancing using transport protocols and ECMP/WCMP to reduce network hotspots.
  - PLB reroutes packets to other paths when congestion occurs.
  - Proven to improve performance in older Jupiter environments, but its performance remains untested in the latest Jupiter.

---

## Background
### **ECMP (Equal-Cost Multi-Path)**
- Distributes network traffic across multiple equal-cost paths.
- **Load Balancing**: Balances traffic using a hashing algorithm.
- **Path Selection**: Chooses a path based on a hash of data packets.
- **WCMP**: A weighted version of ECMP for better control.

### **PLB (Protective Load Balancing)**
- Randomly changes paths for connections experiencing congestion by modifying the IPv6 Flow Label.
- Supports congestion signals such as ECN and Swift.
- Decentralized design allows independent load-balancing decisions.

---

## PLB Algorithm
1. Detect multiple congestion signals (e.g., ECN, Swift).
2. Mark a round as "congested" if a large proportion of packets encounter congestion.
3. Randomly rehash the flow label when congestion exceeds a configurable threshold.

---

## Problems
1. Modern data center networks with multiple links in parallel face fluctuating traffic patterns.
2. Google's OCS (Optical Circuit Switch) introduces heterogeneity, impacting PLB + ECMP performance.
3. Suboptimal routing consumes unnecessary CPU resources and may choose inefficient paths.

---

## Experiment Design
1. Simulate heterogeneous network topologies using Mininet.
2. Compare PLB + ECMP performance under homogeneous and heterogeneous networks.
3. Adjust parameters to trigger rerouting under congestion.

---

## Results
### Homogeneous Networks
- PLB performs well, improving load balancing and reducing congestion.

### Heterogeneous Networks
- PLB + ECMP fail to maximize link utilization under heterogeneity.
- Congestion control wastes CPU cycles unnecessarily.

---

## Proposed Improvements
### **Install Policy**
1. Modify flow entries with OpenFlow control commands based on conditions.
2. Metrics to determine thresholds:
   - ECN: Same congestion signals as PLB.
   - Load Imbalance: Max-min utilization across switch ports.
   - Throughput and connection time.

### **Apply EWMA (Exponentially Weighted Moving Average)**
1. Compute congestion ratio using EWMA:
   - Update `ewma_ratio` with a weighted average of historical and current congestion.
2. Use `ewma_ratio` to trigger reroutes.

---

## Challenges
1. Performance evaluation is difficult due to kernel modifications required for each VM in Mininet.
2. Overhead caused by Kprobe, involving breakpoint traps.
3. Complexity in parameter tuning, such as adjusting Lambda for EWMA.

---

## Conclusion
1. PLB + ECMP do not perform well under heterogeneity, failing to maximize all paths.
2. Significant CPU cycles are wasted on congestion control.
3. Potential improvements:
   - Install policies with SDN switches.
   - Use PLB as a fallback when SDN fails.
