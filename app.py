import streamlit as strl
import requests
import pandas as pd
from datetime import datetime

strl.set_page_config(page_title="Nexa Core Production Gateway", layout="wide")
API_BASE_URL = "https://nexa-backend-tuhl.onrender.com"

strl.title("🤖 Nexa Core Production Gateway")
strl.caption("Autonomous Systems Management & Agentic AI Orchestrator | Team Nexus Cloud Network")
strl.markdown("---")

app_mode = strl.sidebar.selectbox("Select Workspace Domain", [
    "📋 Client Module Dashboard", 
    "🔒 Secure Admin Portal",
    "🧠 Agentic Sprint Planner"
])

# ==========================================
# 1. CLIENT MODULE DASHBOARD
# ==========================================
if app_mode == "📋 Client Module Dashboard":
    target_module = strl.sidebar.selectbox("Active Blueprint Filter", ["Sumo Robot", "RC Car", "Robo Soccer"])
    
    with strl.spinner("Synchronizing with cloud..."):
        try:
            response = requests.get(f"{API_BASE_URL}/modules/{target_module}", timeout=7)
            if response.status_code == 200:
                module_data = response.json()
                left_col, right_col = strl.columns([1, 1.2])
                
                with left_col:
                    strl.markdown("### 🔌 System Circuit Topology")
                    if module_data.get("circuit_diagram_url"):
                        strl.image(module_data["circuit_diagram_url"], use_container_width=True)
                    
                    if "specs" in module_data:
                        strl.markdown("#### ⚙️ Hardware Specifications")
                        for spec, val in module_data["specs"].items():
                            if val:
                                strl.write(f"**{spec}:** {val}")

                with right_col:
                    strl.markdown("### 💰 Component Budget Configuration")
                    if "budget" in module_data and module_data["budget"]:
                        df = pd.DataFrame(module_data["budget"])
                        df['Total (PKR)'] = df['quantity'].astype(int) * df['unit_cost_pkr'].astype(int)
                        df.columns = ['Component Item', 'Qty', 'Unit Cost (PKR)', 'Total Subtotal (PKR)']
                        strl.dataframe(df, use_container_width=True, hide_index=True)
                        
                        grand_total = df['Total Subtotal (PKR)'].sum()
                        strl.metric(label="Calculated Grand Production Cost", value=f"{grand_total:,} PKR")
                    
                    if "firmware" in module_data:
                        strl.markdown("### 💻 Embedded Architecture Code")
                        strl.code(module_data["firmware"], language="cpp")
        except Exception as e:
            strl.error(f"Cloud synchronization failure: {str(e)}")

# ==========================================
# 2. SECURE ADMIN PORTAL
# ==========================================
elif app_mode == "🔒 Secure Admin Portal":
    strl.markdown("## 🔒 Secure Admin Portal")
    access_token = strl.text_input("Enter Production Authorization Token", type="password")
    
    if access_token == "NEXUS_ADMIN_2026":
        if "rows" not in strl.session_state:
            strl.session_state.rows = 4

        mod_name = strl.text_input("Module Name")
        diag_url = strl.text_input("Circuit Diagram Image URL")
        
        strl.markdown("#### ⚙️ Technical Specifications")
        chassis = strl.text_input("Chassis Frame Structure Type")
        mcu = strl.text_input("Microcontroller System")
        motors = strl.text_input("Motors Type")
        drivers = strl.text_input("Motor Driver Type")
        sensors = strl.text_input("Sensors Configuration")
        
        strl.markdown("#### 💰 Component Costing Calculator Matrix")
        budget_list = []
        
        for i in range(strl.session_state.rows):
            col1, col2, col3 = strl.columns([2, 0.5, 1])
            with col1:
                it_name = strl.text_input(f"Item {i+1} Description", key=f"name_{i}")
            with col2:
                it_qty = strl.number_input(f"Qty", min_value=1, value=1, key=f"qty_{i}")
            with col3:
                it_cost = strl.number_input(f"Unit Cost (PKR)", min_value=0, step=50, key=f"ucost_{i}")
            
            if it_name.strip():
                budget_list.append({
                    "item": it_name.strip(),
                    "quantity": int(it_qty),
                    "unit_cost_pkr": int(it_cost)
                })
        
        if strl.button("➕ Add Another Component Line"):
            strl.session_state.rows += 1
            strl.rerun()

        firmware_code = strl.text_area("Paste C++ Code Memory Matrix", height=150)
        
        if strl.button("🚀 Broadcast Module Blueprint to Cloud"):
            payload_package = {
                "module_name": mod_name,
                "circuit_diagram_url": diag_url,
                "specs": {"Chassis": chassis, "Microcontroller": mcu, "Motors": motors, "Motor Driver": drivers, "Sensors": sensors},
                "budget": budget_list,
                "firmware": firmware_code
            }
            res = requests.post(f"{API_BASE_URL}/modules/add", json=payload_package)
            if res.status_code == 200:
                strl.success("🎉 Successfully synchronized item calculations with Atlas Cloud!")

# ==========================================
# 3. AGENTIC SPRINT PLANNER (HACKATHON FEAT)
# ==========================================
elif app_mode == "🧠 Agentic Sprint Planner":
    strl.markdown("## 🧠 Google Agentic AI Sprint Planner")
    strl.caption("Orchestrate roles, analyze inventory deficits, and generate step-by-step developer guides automatically.")
    strl.markdown("---")
    
    # Context Box 1: Team Configuration
    strl.markdown("### 👥 1. Team Context & Specializations")
    team_name = strl.text_input("Team Name", value="Team Nexus")
    
    col_m1, col_m2, col_m3 = strl.columns(3)
    with col_m1:
        member_1 = strl.text_input("Member 1 Name", value="Muhammad Hassaan Awais")
        skills_1 = strl.text_area("Member 1 Skills / Focus", value="Low-level firmware compilation, C++, ESP32/Arduino logic design, Core Infrastructure.")
    with col_m2:
        member_2 = strl.text_input("Member 2 Name", value="Ali")
        skills_2 = strl.text_area("Member 2 Skills / Focus", value="CAD Designing, structural fabrication, hardware modeling, chassis printing optimization.")
    with col_m3:
        member_3 = strl.text_input("Member 3 Name", value="Roshaan")
        skills_3 = strl.text_area("Member 3 Skills / Focus", value="Electronics wiring layout, power distribution tracking, sensor array calibration, Inventory Management.")

    # Context Box 2: Timeline Target
    strl.markdown("### 📅 2. Event Target Parameters")
    c_e1, c_e2 = strl.columns(2)
    with c_e1:
        event_name = strl.text_input("Competition Event Name", value="UET Robocom Hackathon")
    with c_e2:
        event_date = strl.date_input("Target Event Deadline Date", value=datetime.today())
        
    modules_selected = strl.multiselect("Select Registered Categories / Modules", ["Sumo Robot", "RC Car", "Robo Soccer"], default=["Sumo Robot"])

    # Context Box 3: Current Hostel Inventory Pool
    strl.markdown("### 📦 3. Current Local Component Inventory (What you already have)")
    if "inv_rows" not in strl.session_state:
        strl.session_state.inv_rows = 3
        
    inventory_pool = []
    for j in range(strl.session_state.inv_rows):
        col_i1, col_i2 = strl.columns([3, 1])
        with col_i1:
            inv_name = strl.text_input(f"Stock Component {j+1} Name", key=f"inv_name_{j}", placeholder="e.g., ESP32 NodeMCU, N20 Motor")
        with col_i2:
            inv_qty = strl.number_input(f"Stock Qty", min_value=0, value=0, key=f"inv_qty_{j}")
        
        if inv_name.strip():
            inventory_pool.append({"item": inv_name.strip(), "available_qty": int(inv_qty)})
            
    if strl.button("➕ Add Inventory Item to Inventory List"):
        strl.session_state.inv_rows += 1
        strl.rerun()

    strl.markdown("---")
    
    # Big Agent Execution Button
    if strl.button("🚀 ENGAGE GEMINI PROJECT AGENT ENGINE"):
        # Compile everything into a structured schema to send to our Python backend node
        agent_payload = {
            "team_name": team_name,
            "event_details": {
                "event_name": event_name,
                "date": str(event_date),
                "categories": modules_selected
            },
            "team_members": [
                {"name": member_1, "skills": skills_1, "role": "Lead Architect"},
                {"name": member_2, "skills": skills_2, "role": "Hardware Engineer"},
                {"name": member_3, "skills": skills_3, "role": "Electronics & Inventory Manager"}
            ],
            "current_inventory": inventory_pool
        }
        
        strl.info("📦 Form Context compiled perfectly! Transmitting to Render node to spark the Gemini Reasoning Loop...")
        strl.json(agent_payload) # Placeholder to see data packaging working perfectly!
