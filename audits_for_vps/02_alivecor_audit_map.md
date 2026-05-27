# Technical Audit Map: AliveCor
## Subject: Quantizing ECG DNNs for <512KB SRAM on-MCU Inference

**Prepared for:** Siva Somayajula, CTO  
**Focus:** KardiaMobile (Class II FDA / Edge AI)

---

### 1. The Optimization Bottleneck
Running deep learning ECG classifiers on-device (e.g., STM32WB or Apollo4) requires fitting the model, the feature extraction pipeline (DSP), and the BLE stack into <512KB of SRAM. Traditional 8-bit quantization (INT8) often causes precision loss in the high-frequency components of the ECG signal (P-wave, QRS complex), leading to a drop in clinical sensitivity.

### 2. Proposed "Mixed-Precision" Inference Strategy
We recommend a **Layer-Specific Quantization Map** to balance memory footprint with clinical accuracy.

#### A. Architecture Breakdown
*   **Preprocessing (DSP):** Implement 32-bit floating-point Butterworth filters in the early stages to preserve signal integrity, then down-sample to 16-bit for the neural network input.
*   **Feature Extraction (CNN):** Use **INT16** for the first two convolutional layers (highest impact on precision) and **INT8** for the deeper fully connected layers (highest impact on memory).
*   **Buffer Re-use:** Implement a ping-pong buffer strategy for the inference engine to keep peak SRAM usage below 256KB, leaving overhead for the BLE telemetry stack.

#### B. Memory Map (Target: 512KB SRAM)
| Component | Allocated SRAM | Strategy |
| :--- | :--- | :--- |
| **BLE Stack** | 128 KB | Static Allocation |
| **Inference Engine**| 192 KB | TFLite Micro / CMSIS-NN |
| **DSP Buffers** | 64 KB | L1 Cache Optimization |
| **System/Heap** | 128 KB | Zero-Fragmentation |

### 3. Validation & Quality (The "Clinical Proof")
1.  **Bit-Exactness Testing:** Automate a comparison between the original Python/TensorFlow model and the C-embedded model using the MIT-BIH Arrhythmia Database.
2.  **Latency Audit:** Verify that a 30-second ECG strip can be classified in <2 seconds at 48MHz clock speed.
3.  **Power Analysis:** Record the current draw during inference to ensure a 10% reduction in battery impact compared to raw data streaming to the cloud.

---
**Next Step:** I can share a benchmark report showing the sensitivity delta between Global INT8 and Mixed-Precision 8/16 quantization on Kardia-like datasets.
