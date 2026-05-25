import streamlit as strl
import requests
import pandas as pd
from datetime import datetime

strl.set_page_config(page_title="Nexa Core Multi-Tenant Platform", layout="wide")
API_BASE_URL = "https://nexa-backend-tuhl.onrender.com"

strl.title("🤖 Nexa Core Production Gateway")
strl.caption("Multi-Tenant Autonomous Systems Hub & Agentic AI Orchestrator")
strl.markdown("---")

# 🔐 Initialize Global Authentication State Engine
if "authenticated" not in strl.session_state:
    strl.session_state.authenticated = False
if "team_id" not in strl.session_state:
    strl.session_state.team_id = None

# ==========================================
# SIDEBAR AUTHENTICATION PORTAL INTERFACE
# ==========================================
strl.sidebar.header("🔐 Workspace Access Profile")

if not strl.session_state.authenticated:
    auth_mode = strl.sidebar.radio("Profile Operation", ["Sign In To Team Workspace", "Register New Team"])
    auth_user = strl.sidebar.text_input("Team Unique Username / ID").strip().lower()
    auth_pass = strl.sidebar.text_input("Secret Master Password", type="password")
    
    if auth_mode == "Sign In To Team Workspace":
        if strl.sidebar.button("🔓 Authenticate Workspace"):
            if not auth_user or not auth_pass:
                strl.sidebar.error("❌ Both credential fields are required.")
            else:
                try:
                    res = requests.post(f"{API_BASE_URL}/auth/login", json={"team_username": auth_user, "password": auth_pass})
                    if res.status_code == 200:
                        strl.session_state.authenticated = True
                        strl.session_state.team_id = res.json()["team_id"]
                        strl.success(f"🤝 Handshake complete! Welcome back, {auth_user}.")
                        strl.rerun()
                    else:
                        strl.sidebar.error(f"🛑 {res.json().get('detail', 'Access Denied.')}")
                except Exception as e:
                    strl.sidebar.error(f"💥 Auth server offline: {str(e)}")
                    
    elif auth_mode == "Register New Team":
        if strl.sidebar.button("✨ Initialize New Tenant Matrix"):
            if not auth_user or not auth_pass:
                strl.sidebar.error("❌ Credentials required to claim namespace.")
            else:
                try:
                    res = requests.post(f"{API_BASE_URL}/auth/register", json={"team_username": auth_user, "password": auth_pass})
                    if res.status_code == 200:
                        strl.sidebar.success("🎉 Registration confirmed! Shift to Sign In to login.")
                    else:
                        strl.sidebar.error(f"❌ Registration failed: {res.json().get('detail')}")
                except Exception as e:
                    strl.sidebar.error(f"💥 Network error: {str(e)}")

else:
    strl.sidebar.success(f"🟢 Active Session: {strl.session_state.team_id.upper()}")
    if strl.sidebar.button("🚪 Terminate Secure Session"):
        strl.session_state.authenticated = False
        strl.session_state.team_id = None
        strl.rerun()

# ==========================================
# MAIN APPLICATION INTERFACE (LOCKED LAYER)
# ==========================================
if not strl.session_state.authenticated:
    strl.warning("🔒 SECURE INTERFACE DISCONNECT: Please authenticate via the profile sidebar to access cloud data assets.")
    strl.info("💡 **Hackathon Evaluator Tip:** You can quickly register a fresh custom team name right now, or sign into an established cluster framework.")
else:
    # Navigation mapping for verified tenants
    app_mode = strl.sidebar.selectbox("Select Workspace Domain", [
        "📋 Client Module Dashboard", 
        "🔒 Secure Admin Portal",
        "🧠 Agentic Sprint Planner"
    ])

    # ------------------------------------------
    # 1. CLIENT MODULE DASHBOARD (ISOLATED)
    # ------------------------------------------
    if app_mode == "📋 Client Module Dashboard":
        target_module = strl.sidebar.selectbox("Active Blueprint Filter", ["Sumo Robot", "RC Car", "Robo Soccer"])
        
        with strl.spinner("Synchronizing with target team cloud partition..."):
            try:
                response = requests.get(f"{API_BASE_URL}/modules/{strl.session_state.team_id}/{target_module}", timeout=7)
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
                else:
                    strl.info(f"ℹ️ No profile records found matching '{target_module}' inside your cluster space. Head over to the Secure Admin Portal to register this module profile.")
            except Exception as e:
                strl.error(f"Cloud synchronization failure: {str(e)}")

    # ------------------------------------------
    # 2. SECURE ADMIN PORTAL (ISOLATED)
    # ------------------------------------------
    elif app_mode == "🔒 Secure Admin Portal":
        strl.markdown(f"## 🔒 Profile Writing Desk: {strl.session_state.team_id.upper()}")
        
        if "rows" not in strl.session_state:
            strl.session_state.rows = 4

        mod_name = strl.selectbox("Select Target Module Target", ["Sumo Robot", "RC Car", "Robo Soccer"])
        diag_url = strl.text_input("Circuit Diagram Image URL")
        
        strl.markdown("#### ⚙️ Technical Specifications (Descriptions)")
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
                "team_id": strl.session_state.team_id,
                "module_name": mod_name,
                "circuit_diagram_url": diag_url,
                "specs": {"Chassis": chassis, "Microcontroller": mcu, "Motors": motors, "Motor Driver": drivers, "Sensors": sensors},
                "budget": budget_list,
                "firmware": firmware_code
            }
            res = requests.post(f"{API_BASE_URL}/modules/add", json=payload_package)
            if res.status_code == 200:
                strl.success(f"🎉 Successfully synchronized item configurations under workspace: {strl.session_state.team_id}")

    # ------------------------------------------
    # 3. AGENTIC SPRINT PLANNER (ISOLATED PROCESSING)
    # ------------------------------------------
    elif app_mode == "🧠 Agentic Sprint Planner":
        strl.markdown(f"## 🧠 Google Agentic AI Sprint Planner Workspace")
        strl.caption("Orchestrating isolated sprints using real-time tenant context parameters.")
        strl.markdown("---")
        
        strl.markdown("### 👥 1. Team Context & Specializations")
        
        col_m1, col_m2, col_m3 = strl.columns(3)
        with col_m1:
            member_1 = strl.text_input("Lead / Member 1 Name", value="Muhammad Hassaan Awais")
            skills_1 = strl.text_area("Member 1 Specialization Profile", value="Firmware systems, C++, low-level hardware control blocks.")
        with col_m2:
            member_2 = strl.text_input("Member 2 Name", value="Ali")
            skills_2 = strl.text_area("Member 2 Specialization Profile", value="Mechanical structures, CAD optimization, chassis topology designing.")
        with col_m3:
            member_3 = strl.text_input("Member 3 Name", value="Roshaan")
            skills_3 = strl.text_area("Member 3 Specialization Profile", value="Electrical distributions, routing pathways, hardware inventory tracking.")

        strl.markdown("### 📅 2. Event Target Parameters")
        c_e1, c_e2 = strl.columns(2)
        with c_e1:
            event_name = strl.text_input("Competition Name", value="UET Robocom Hackathon")
        with c_e2:
            event_date = strl.date_input("Target Event Deadline Date", value=datetime.today())
            
        modules_selected = strl.multiselect("Select Registered Categories / Modules", ["Sumo Robot", "RC Car", "Robo Soccer"], default=["Sumo Robot"])

        strl.markdown("### 📦 3. Current Local Component Inventory")
        if "inv_rows" not in strl.session_state:
            strl.session_state.inv_rows = 3
            
        inventory_pool = []
        for j in range(strl.session_state.inv_rows):
            col_i1, col_i2 = strl.columns([3, 1])
            with col_i1:
                inv_name = strl.text_input(f"Stock Component {j+1} Name", key=f"inv_name_{j}")
            with col_i2:
                inv_qty = strl.number_input(f"Stock Qty", min_value=0, value=0, key=f"inv_qty_{j}")
            
            if inv_name.strip():
                inventory_pool.append({"item": inv_name.strip(), "available_qty": int(inv_qty)})
                
        if strl.button("➕ Add Inventory Line"):
            strl.session_state.inv_rows += 1
            strl.rerun()

        strl.markdown("---")
        
        if strl.button("🚀 EXECUTE DYNAMIC AGENT STRATEGY GENERATOR"):
            agent_payload = {
                "team_id": strl.session_state.team_id,
                "event_details": {"event_name": event_name, "date": str(event_date), "categories": modules_selected},
                "team_members": [
                    {"name": member_1, "skills": skills_1, "role": "Lead Architect"},
                    {"name": member_2, "skills": skills_2, "role": "Structural Engineer"},
                    {"name": member_3, "skills": skills_3, "role": "Logistics & Procurement Manager"}
                ],
                "current_inventory": inventory_pool
            }
            
            with strl.spinner("Triggering cloud agent sequence matrix via Gemini Core node..."):
                try:
                    agent_res = requests.post(f"{API_BASE_URL}/agent/sprint", json=agent_payload, timeout=30)
                    if agent_res.status_code == 200:
                        raw_markdown_output = agent_res.json()["sprint_plan"]
                        
                        strl.success("🎯 Agent Execution Sequence Terminated Successfully! Strategic output compiled below:")
                        strl.markdown("---")
                        
                        # High-level strategic parsing of response blocks
                        if "=== PROCUREMENT PROFILE ===" in raw_markdown_output:
                            parts = raw_markdown_output.split("=== PROCUREMENT PROFILE ===")
                            main_content = parts[1]
                            
                            if "=== DEVELOPER SPRINT BLOCKS ===" in main_content:
                                inventory_block, dev_block = main_content.split("=== DEVELOPER SPRINT BLOCKS ===")
                            else:
                                inventory_block = main_content
                                dev_block = ""
                            
                            strl.warning("🛍️ AI Logistics Analytics: Inventory Manager Procurement Briefing")
                            strl.markdown(inventory_block.strip())
                            
                            if dev_block:
                                strl.markdown("### 📋 Specialized Teammate Directives")
                                strl.markdown(dev_block.strip())
                        else:
                            # Fallback rendering container if headers drift out of style
                            strl.markdown(raw_markdown_output)
                            
                    else:
                        strl.error(f"❌ Core processing error: {agent_res.json().get('detail')}")
                except Exception as ex:
                    strl.error(f"💥 Agent pipeline collapsed: {str(ex)}")
