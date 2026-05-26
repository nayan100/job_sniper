> [!ABSTRACT] Summary\n> Breakdown of essential skills for AI-native roles, covering terminal fluency, embedded fundamentals, prompt engineering, and MCP mastery.\n\n---
---
tags:
  - skills
  - requirements
  - embedded
  - ai-prompting
---
# Requirements for AI-Native Embedded/IoT Roles

To succeed in these roles where **Claude CLI** or **Gemini CLI** are mandated, the following skills are essential.

## 1. Technical Proficiency (Hard Skills)
*   **Terminal Fluency:** Absolute mastery of Bash/Zsh. You must be able to pipe terminal outputs (`grep`, `cat`, `docker logs`) directly into LLM CLIs for analysis.
*   **Embedded Fundamentals:** C/C++, Rust, Linux Kernel, RTOS (FreeRTOS/Zephyr), and knowledge of hardware interfaces (I2C, SPI, UART).
*   **DevOps Mastery:** CI/CD (GitHub Actions), IaC (Terraform), and containerization (Docker/K3s).

## 2. AI Prompting Mastery (The "New" Requirement)
*   **System Prompt Engineering:** Ability to define "Architect Agent" or "DevOps Agent" personas with strict guardrails.
*   **Chain-of-Thought (CoT) Prompting:** Guiding the AI through multi-step architectural decisions (e.g., "Analyze the memory footprint, then suggest a strategy, then implement the change").
*   **Model Context Protocol (MCP):** Connecting Claude/Gemini to local tools, databases, and private APIs for context-aware coding.

## 3. Professional Mindset (Soft Skills)
*   **AI-First Thinking:** Approaching every problem by first asking, "How can I orchestrate an agent to solve this?"
*   **Security & Oversight:** "Human-in-the-loop" validation. Understanding that AI-generated code must be rigorously audited for security vulnerabilities.
*   **Spec-Driven Development:** Using AI to write the functional specification (`spec.md`) and technical plan (`plan.md`) before any code is written.
