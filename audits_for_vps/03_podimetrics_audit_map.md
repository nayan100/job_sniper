# Technical Audit Map: Podimetrics
## Subject: Optimizing LTE-M/NB-IoT Wake-up States & Thermal Drift Compensation

**Prepared for:** Brian Petersen, CTO  
**Focus:** SmartDot (Cellular-Connected Medical IoT)

---

### 1. The Energy-Sensing Bottleneck
The SmartDot mat must maintain high-density spatial thermal resolution while surviving years on battery. The primary "Power Thief" is the LTE-M/NB-IoT transceiver's **Active/Scan state**. If the network experiences high attenuation (indoor use), retransmissions and long paging cycles (eDRX/PSM) can drain months of battery in days. Simultaneously, high-resolution thermal sensors are prone to **ambient drift**, which traditionally requires frequent MCU wake-ups to re-calibrate.

### 2. Proposed "Zero-Wake" Architecture
We recommend offloading the calibration logic to a low-power sensor hub or using **Asynchronous Hardware Triggers**.

#### A. Power-Aware Connectivity Map
*   **PSM/eDRX Tuning:** Implement a "Network-Condition Aware" timer. If RSRP is below -110dBm, the mat shifts to a "Batch & Bursts" mode, caching 24 hours of data to minimize the energy-expensive RRC Connection Setup.
*   **TLS 1.3 session Resumption:** Utilize "0-RTT" (Zero Round Trip Time) handshakes to eliminate the extra RF active-time during cryptographic negotiations.

#### B. Ambient Drift Mitigation (The "Static Calibration" Logic)
*   **Delta-Encoding:** Only wake the primary MCU if the thermal gradient exceeds a specific threshold (e.g., Δ0.05°C) across the array, handled via an ultra-low-power comparator.
*   **Digital Thermal Modeling:** Implement a lightweight 1st-order IIR filter directly in the sensor's digital register (if supported) or a sub-1µA "always-on" domain to compensate for ambient room fluctuations without waking the ARM core.

### 3. Validation Framework
1.  **Current Profile Audit:** Use a Power Profiler (PPK2) to verify that the "Sleep-to-Active" transition is <500ms and that the deep sleep floor is <3µA.
2.  **Long-Tail Simulation:** Simulate a 10-year deployment using AI-modeled cellular "dead zones" to verify battery longevity under worst-case RF conditions.
3.  **FOTA Resilience:** Verify a "Partial Chunk" FOTA update that can resume across 10+ sleep cycles without corrupting the thermal calibration tables.

---
**Next Step:** I can provide a power-budget breakdown for an NB-IoT vs. LTE-M handshake in a -120dBm signal environment.
