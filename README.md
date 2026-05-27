# Nexa Core Gateway Engine: Fleet HUD UI 🏎️🪐

The interactive, high-fidelity mission control dashboard for the Nexa Ecosystem. Engineered using Streamlit, this interface parses cross-platform hardware telemetry vectors and renders real-time animated operational diagnostics.

#### 📡 System Infrastructure Vectors
* **Production Fleet HUD UI:** `https://nexa-frontend-tuhl.onrender.com`
* **Associated API Gateway Backend:** [Nexa Production APIs Engine](https://github.com/davidmitnick99/nexa-backend)

---

## 🛠️ UI Stack & Custom CSS Telemetry Matrix

This workspace forces an absolute slate dark theme (`#020408`) and high-visibility neon cyan (`#00f0ff`) typographic elements via complete theme injection variables inside `.streamlit/config.toml`. 

The application utilizes a custom native CSS animation telemetry grid specifically optimized for tracking distinct competitive robotics modules:
* **Robo Soccer Module:** Omnidirectional kinematics emulation via rotating radar sweeping paths (`@keyframes radarSweep`).
* **Sumo Robot Module:** High-frequency weapon wedge oscillation and oscillating linear laser scanner tracks (`@keyframes laserScan`).
* **RC Car Module:** Real-time differential steering wobble vector angles (`@keyframes steeringWobble`) paired with pulsing tachometer velocity indicators.

---

## 🧠 Integrated Agent Operations

* **Concurrent Strategy Sync:** Translates human operator matrices into JSON frames and coordinates with dual backend sub-agents to compute gap deficits in PKR and deliver sprint blocks.
* **Real-Time Fault Intercepts:** Captures raw serial monitor logs and routes them through hardware grounding RAG pipelines to return pinpointed mechatronics troubleshooting steps.

---

## 📥 Local Environment Bootstrap Setup

1. Clone and enter the frontend application directory:
   ```bash
   git clone https://github.com/davidmitnick99/nexa-frontend.git
   cd nexa-frontend
