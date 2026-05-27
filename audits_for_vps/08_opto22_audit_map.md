# Technical Audit Map: Opto 22
## Subject: Eliminating CODESYS Jitter on PREEMPT_RT Linux Architectures

**Prepared for:** Bill Sherwood, VP of Engineering  
**Focus:** groov EPIC / groov RIO (Edge Controllers / ISA-95)

---

### 1. The "IT vs. OT" Scheduling Conflict
The groov EPIC's strength—running Linux applications (IT) alongside CODESYS (OT)—is also its primary technical bottleneck. Even with a `PREEMPT_RT` patched kernel, a sudden burst of MQTT traffic or a database-heavy Docker container can cause **Priority Inversion** or cache thrashing, leading to microsecond-level jitter in the PLC control loop. For sub-millisecond I/O response times, pure kernel patching is insufficient.

### 2. Proposed "Hard-Real-Time" Partitioning Strategy
We recommend a **Strict CPU Isolation & Cgroups** approach to separate the OT and IT domains at the hardware level.

#### A. Resource Partitioning Map
*   **CPU Pinning:** Dedicate CPU Core 0 and Core 1 exclusively to the Linux OS, Docker, and MQTT. Dedicate CPU Core 2 and Core 3 exclusively to the CODESYS runtime and high-speed I/O drivers.
*   **`isolcpus` & `cgroups`:** Configure the bootloader to hide the OT cores from the standard Linux scheduler. Use `cgroups v2` to strictly limit the memory and disk I/O bandwidth of non-essential containers.
*   **Interrupt Affinity:** Manually route all non-real-time interrupts (Wi-Fi, USB, Ethernet 1) to the IT cores, ensuring that the OT cores only process I/O and hardware-timer interrupts.

#### B. Secure Boot & Latency
*   **Root of Trust (TPM 2.0):** Implement a TPM-backed secure boot sequence. To prevent this from slowing down the "Boot-to-Control" time, use a parallelized initialization where the CODESYS engine starts in a restricted state *while* the high-level OS signature is being verified.

### 3. Validation Framework
1.  **Cyclictest Audit:** Run `cyclictest` on the isolated OT cores while simultaneously running a "Worst-Case" IT load (e.g., `stress-ng`). Target: Max jitter < 50µs.
2.  **I/O Latency Trace:** Use an oscilloscope to measure the time from a digital input trigger to a CODESYS-driven output response.
3.  **Kernel Preemption Audit:** Audit the custom Linux drivers for any non-preemptible regions (spinlocks) that could block the real-time scheduler.

---
**Next Step:** I can share a reference `GRUB` and `systemd` configuration for implementing CPU isolation on an ARMv8-based industrial edge controller.
