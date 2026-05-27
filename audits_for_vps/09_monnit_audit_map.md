# Technical Audit Map: Monnit Corporation
## Subject: Optimizing Sub-GHz FOTA & MAC Layers for 10+ Year Battery Life

**Prepared for:** Kelly Hennigan, VP of Engineering  
**Focus:** ALTA Wireless Sensors & Gateways (Industrial IoT)

---

### 1. The "Collision-to-Death" Bottleneck
In a dense industrial environment with hundreds of ALTA sensors, the primary battery drain is not the sensor itself, but the **Radio Retransmissions**. If multiple sensors wake up and transmit simultaneously, packet collisions occur. The radio remains in "Listen/Retry" mode, which consumes 10-20x the energy of the "Sleep" state. This challenge is compounded by **Firmware-Over-The-Air (FOTA)** updates, which require long active-radio sessions that can brick a device if the battery is low.

### 2. Proposed "Synchronized Sleep" MAC Architecture
We recommend moving from a pure ALOHA-based protocol to a **Hybrid TDMA (Time Division Multiple Access)** scheme optimized for sub-GHz.

#### A. MAC Layer Optimization Map
*   **Time-Slotted ALOHA:** Synchronize sensor clocks during the gateway acknowledgement. Assign each sensor a specific "Transmit Window" based on its unique ID, reducing the probability of collision by >80%.
*   **Dynamic Payload Scaling:** Implement a variable bitrate. If the signal is strong (high RSSI), increase the bitrate to finish the transmission faster. Only drop to the lowest bitrate (longest air-time) when the signal is near the noise floor.

#### B. Fail-Safe "Chunked" FOTA
*   **Resume-on-Disconnect:** Instead of a single large binary, split the FOTA update into 128-byte signed chunks. The sensor stores these in a secondary flash partition and only executes the update after a full CRC-32 validation.
*   **Battery-Aware FOTA:** Implement a hard-lock. If the battery voltage is below a specific threshold (e.g., 2.8V), the sensor refuses to enter FOTA mode, preventing "Half-Updated" bricked devices.

### 3. Validation Framework
1.  **Collision Rate Audit:** Use a spectrum analyzer to measure the "Air-Time Congestion" in a simulated 500-sensor environment.
2.  **Battery Discharge Trace:** Use a device like the Joulescope to record the exact energy (in Coulombs) consumed during a single 10KB FOTA update.
3.  **Clock Drift Analysis:** Measure the drift of the 32.768kHz sleep crystal over a 7-day period to ensure the TDMA windows remain aligned without requiring frequent re-syncs.

---
**Next Step:** I can provide a mathematical model comparing the battery life of a 100-sensor network using Standard ALOHA vs. Slotted-TDMA.
