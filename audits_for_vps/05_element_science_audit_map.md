# Technical Audit Map: Element Science, Inc.
## Subject: Mitigating Motion Artifacts in Dual-Core ECG DSP Pipelines

**Prepared for:** John Solano, VP of Engineering  
**Focus:** Jewel Patch Wearable Cardioverter Defibrillator (WCD)

---

### 1. The Class C Signal Challenge
A wearable patch defibrillator (WCD) operates in a high-noise environment (EMG noise, motion artifacts, garment friction). For a Class C device (IEC 62304), the detection algorithm must distinguish between Ventricular Fibrillation (VF) and "Running Artifacts" with near-zero latency. The bottleneck is the **Inter-Processor Synchronization** required to run heavy adaptive filters (DSP) on one core while maintaining the Safety State Machine on the other.

### 2. Proposed Dual-Core DSP Architecture
We recommend a **Tightly-Coupled Memory (TCM)** architecture to minimize latency between the signal processing and decision logic.

#### A. Multi-Core Signal Map
*   **Core 0 (DSP/ML Core):** Executes an Adaptive LMS (Least Mean Squares) filter using 3-axis accelerometer data as the noise reference to "subtract" motion from the ECG.
*   **Core 1 (Safety Core):** Executes the MISRA-compliant Arrhythmia Detection state machine. It only receives "Cleaned" data via a zero-copy circular buffer in TCM.
*   **Clock Sync:** Implement a hardware timer-based "Sync Pulse" to ensure that the ECG sample and the IMU (motion) sample are timestamped within 1ms of each other to prevent phase-shift errors in the filter.

#### B. Thermal Mitigation in Sealed Enclosures
*   **Offloading to Hardware Accelerators:** Utilize the MCU's internal MAC (Multiply-Accumulate) units or Cordic co-processors for the LMS filter instead of pure software loops, reducing CPU thermal dissipation by ~30%.
*   **Skin-Temp Protection:** Implement a hardware interrupt tied to a thermistor near the enclosure surface that throttles the DSP core if skin-contact temperature exceeds 41°C.

### 3. Validation Framework
1.  **Motion-Noise Injection:** Use a patient simulator (e.g., Fluke ProSim) combined with recorded "Motion Noise" to verify the signal-to-noise ratio (SNR) improvement in real-time.
2.  **Deadlock/Race Audit:** Formally verify the IPC (Inter-Processor Communication) buffer logic to ensure that a "Locked" DSP core cannot stall the Safety Core's ability to issue a shock.
3.  **MISRA Compliance:** Audit the DSP codebase for Rule 13.x (Side effects) and 10.x (Type promotion) which are common failure points in signal processing math.

---
**Next Step:** I can share a benchmark of LMS filter latency on a Cortex-M4F vs. Cortex-M7 with hardware DSP extensions.
