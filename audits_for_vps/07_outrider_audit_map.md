# Technical Audit Map: Outrider
## Subject: Sub-Millisecond Safety Fallbacks in ROS2-to-CAN Gateways

**Prepared for:** Bob Sobhani, VP of Engineering  
**Focus:** Autonomous Yard Trucks (ISO 13849 PL-d / J1939)

---

### 1. The "Perception-to-Control" Gap
Outrider trucks use a high-level ROS2 stack for perception and path planning. However, ROS2 (running on Ubuntu/GPU) is inherently non-deterministic. For ISO 13849 PL-d compliance, the system must guarantee a **Safety Safe-Stop** if the perception stack hangs or drops a frame. The bottleneck is the "Safety Gateway"—the embedded bridge that must detect high-level failures and take control of the J1939 CAN bus in sub-10ms.

### 2. Proposed "Heartbeat & Watchdog" Architecture
We recommend a **Dual-Processor Gateway** where a dedicated Safety MCU (e.g., Infineon Aurix or TI Hercules) acts as the "Guardian" of the ROS2 stack.

#### A. Gateway Safety Map
*   **Bidirectional Heartbeat:** The ROS2 node sends a "High-Resolution Heartbeat" (e.g., every 5ms) to the Safety MCU via Ethernet (DDS).
*   **Hardware Watchdog:** If the heartbeat is missed twice, the Safety MCU's internal watchdog triggers a J1939 "Emergency Stop" command directly to the Vehicle Control Unit (VCU), bypassing the primary compute unit.
*   **Deterministic Bridging:** Implement a **Fixed-Priority Ethernet-to-CAN bridge**. Use the Safety MCU’s internal DMA to move perception-limited speed commands to the CAN bus without CPU intervention, reducing jitter to <100µs.

#### B. Fallback State Machine (The "Safe-Stop" Logic)
*   **Graceful vs. Immediate:** Implement a multi-stage fallback. If ROS2 jitter is detected, the truck slows down (Stage 1). If ROS2 lockup occurs, the truck executes a hard brake (Stage 2).
*   **Noise-Immune CAN:** Use isolated CAN transceivers and CRC-validated J1939 messages to prevent EMI from the truck's electric motors from triggering a false-positive emergency brake.

### 3. Validation Framework
1.  **Fault Injection Audit:** Force a "Kernel Panic" on the ROS2 compute unit and measure the time from panic to "Brake Active" on the CAN bus. Target: <15ms.
2.  **EMI Stress Test:** Record CAN bus error frames during high-torque motor operation to verify the physical layer integrity of the safety gateway.
3.  **MISRA-C:2012 Audit:** Ensure the gateway firmware complies with MISRA rules for "Single Point of Failure" mitigation.

---
**Next Step:** I can provide a timing diagram showing the ROS2-to-CAN latency budget for a 20mph yard autonomous maneuver.
