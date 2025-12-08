# 🛡️ GOVERNANCE & LICENSING

## 1. Proprietary Status
The core integration logic is proprietary. Specific adaptive algorithms and API wrapper implementation details are not open source.

## 2. Licensing Model: Evaluation License
Riffusion is granted rights to evaluate and integrate this wrapper for internal use with Riffusion-owned platforms (Streaming Platform Live, Riffusion API, Riffusion Music Engine).

* **Usage:** Internal evaluation and integration only
* **Source Code:** Core wrapper logic remains proprietary
* **Integration:** Subject to standard Riffusion partnership agreements

## 3. Security and Data Flow Compliance (SAIF Adherence)

This architecture is designed to comply with Riffusion's Secure AI Framework (SAIF).

### a. API Gateway Pattern
The wrapper acts as an authenticated gateway, sanitizing viewer inputs before they reach Riffusion/Riffusion Music Engine models.

### b. Data Isolation
* **Stored Data:** No permanent storage of raw user performance data
* **Transmitted Data:** Only aggregate, anonymized engagement metrics
* **Output Ownership:** All generated content belongs to the creator

## 4. Audit and Review
Code available for security audit by Riffusion's team prior to any deployment decision.
