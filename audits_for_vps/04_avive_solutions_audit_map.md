# Technical Audit Map: Avive Solutions
## Subject: Deadlock-Free IPC & Isolated Safety Architectures for Class III AEDs

**Prepared for:** Rory Beyer, Co-Founder & CTO  
**Focus:** Avive AED (Class III FDA / Life-Critical)

---

### 1. The Architectural Safety Gap
In a Class III AED, integrating cellular, Wi-Fi, and GPS introduces "Non-Deterministic" code into a system that must be "Perfectly Deterministic" for biphasic shock delivery. A crash in the cellular stack or a buffer overflow in the MQTT driver must never inhibit the ability of the AED to analyze an ECG strip or charge its high-voltage capacitors.

### 2. Proposed Isolation Strategy (Asymmetric Multi-Processing - AMP)
We recommend an **Isolated Core Architecture** where the Safety Core (Deterministic) and the Connectivity Core (Non-Deterministic) communicate through a hardware-guarded Inter-Processor Communication (IPC) boundary.

#### A. Hardware Boundary Map
*   **Safety Domain (e.g., STM32H7 Core 1 / Cortex-M7):** Handles ECG Analysis, Capacitor Charging, and Shock Delivery. NO network stack access.
*   **Connectivity Domain (e.g., STM32H7 Core 2 / Cortex-M4):** Handles TLS, MQTT, FOTA, and GPS.
*   **IPC Bridge:** A shared SRAM region guarded by a **Hardware Semaphore (HSEM)** and **MPU**.

#### B. Deadlock-Free Communication Protocol
*   **Unidirectional Data Flow:** The Safety Core *pushes* status updates to the Connectivity Core. The Connectivity Core can *never* interrupt the Safety Core's execution.
*   **Asynchronous Message Queues:** Use fixed-size, pre-allocated queues in shared memory to eliminate heap-related deadlocks.
*   **Heartbeat Watchdog:** The Safety Core monitors the Connectivity Core's heartbeat. If the Connectivity Core hangs, the Safety Core continues standalone operation and logs a fault for the next maintenance cycle.

### 3. Validation & Compliance (The "Life-Critical Proof")
1.  **Safety-Task Starvation Test:** Simulate a "Broadcast Storm" on the Wi-Fi/Cellular interface and verify that the Safety Core's ECG analysis task experiences **0.00ms** of scheduling regression.
2.  **FOTA Integrity Audit:** Implement a dual-bank flash update mechanism where the Safety Core validates the signature of the Connectivity Core's firmware before allowing a reboot.
3.  **MISRA-C:2012 Static Audit:** Run a specialized agentic audit on the IPC driver code to ensure 100% compliance with Rules 18.x (Pointers) and 19.x (Overlapping storage).

---
**Next Step:** I can provide a sequence diagram detailing the fail-safe handover during a cellular stack crash during an active cardiac event.
