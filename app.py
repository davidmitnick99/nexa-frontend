import streamlit as strl
import requests
import pandas as pd
import json
from datetime import datetime

# 1. Page Configuration & Cryptographic Structural Anchors
strl.set_page_config(page_title="Nexa Core Gateway Engine", layout="wide", initial_sidebar_state="expanded")
API_BASE_URL = "https://nexa-backend-tuhl.onrender.com"

# Initialize Session State keys safely
for key, default_val in [
    ("authenticated", False), ("team_id", None), 
    ("team_admin_token", ""), ("cached_plan", ""), 
    ("rows", 4), ("inv_rows", 3), ("member_count", 3)
]:
    if key not in strl.session_state:
        strl.session_state[key] = default_val

# 🎨 Custom Glassmorphic Cyber-Glow Visual Injection Matrix
strl.markdown("""
<style>
    /* Global Background and Typography Polish */
    .stApp { background-color: #0b0e14; color: #adbac7; font-family: 'Segoe UI', Roboto, Helvetica, sans-serif; }
    h1, h2, h3, h4 { color: #58a6ff !important; font-family: 'Courier New', monospace; font-weight: 700; letter-spacing: 0.5px; }
    
    /* Neon Sidebar styling */
    section[data-testid="stSidebar"] { background-color: #10141d !important; border-right: 1px solid #1f242c !important; }
    
    /* Interactive Cyber Button Formats */
    .stButton>button { 
        background: linear-gradient(135deg, #1f6feb 0%, #094cbc 100%) !important; 
        color: #ffffff !important; font-weight: bold !important; border-radius: 6px !important;
        border: 1px solid #388bfd !important; padding: 0.5rem 1.5rem !important;
        box-shadow: 0 4px 12px rgba(31,111,235,0.2); transition: all 0.25s ease-in-out;
    }
    .stButton>button:hover { transform: translateY(-1px); box-shadow: 0 6px 20px rgba(31,111,235,0.4); border-color: #58a6ff !important; }
    
    /* Injected Strategic Container Profiles (Glassmorphism Cards) */
    div.cyber-card {
        background-color: #151b26 !important; border: 1px solid #21262d !important;
        border-radius: 8px; padding: 1.5rem; margin-bottom: 1rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    }
    
    /* Metrics Layout Customization */
    div[data-testid="stMetricValue"] { color: #58a6ff !important; font-family: 'Courier New', monospace; font-weight: bold; }
    div[data-testid="stMetricLabel"] { color: #768390 !important; font-size: 0.85rem; letter-spacing: 1px; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# AUTHENTICATION HUB LAYER (SECURE INPUT GATE)
# ==========================================
def render_authentication_gate():
    strl.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
    strl.subheader("🔐 Nexa Cryptographic Gateway Access")
    strl.markdown("---")
    
    auth_mode = strl.radio("Choose System Operation Token Mappings", ["Sign In To Active Workspace", "Provision New Multi-Tenant Instance"])
    
    c1, c2 = strl.columns(2)
    with c1: auth_user = strl.text_input("Tenant Namespace Unique ID / Identifier").strip().lower()
    with c2: auth_pass = strl.text_input("Secure Vault Access Password", type="password")
    
    if auth_mode == "Sign In To Active Workspace":
        if strl.button("🔓 Authenticate Tunnel Handshake", use_container_width=True):
            if not auth_user or not auth_pass:
                strl.error("❌ Identification keys cannot be empty strings.")
                return
            try:
                res = requests.post(f"{API_BASE_URL}/auth/login", json={"team_username": auth_user, "password": auth_pass})
                if res.status_code == 200:
                    strl.session_state.authenticated = True
                    strl.session_state.team_id = res.json()["team_id"]
                    strl.session_state.team_admin_token = res.json()["admin_token"]
                    
                    # Core Sync Loop: Immediate historical pipeline pull upon gate clearance
                    hist = requests.get(f"{API_BASE_URL}/agent/cached/{strl.session_state.team_id}")
                    if hist.status_code == 200:
                        strl.session_state.cached_plan = hist.json().get("sprint_plan", "")
                    strl.success("🤝 Cryptographic Verification Complete. Mounting Workspace Interfaces...")
                    strl.rerun()
                else: strl.error("🛑 Security Rejection: Invalid Namespace ID or Password mismatch.")
            except Exception as e: strl.error(f"💥 Backend Connection Failure: {str(e)}")
                    
    elif auth_mode == "Provision New Multi-Tenant Instance":
        custom_token = strl.text_input("Define Private Admin Modification Token (Crucial for Data Overwrites)", type="password")
        if strl.button("✨ Initialize Isolated Tenant Memory Matrix", use_container_width=True):
            if auth_user and auth_pass and custom_token:
                try:
                    res = requests.post(f"{API_BASE_URL}/auth/register", json={
                        "team_username": auth_user, "password": auth_pass, "admin_token": custom_token.strip()
                    })
                    if res.status_code == 200:
                        strl.success("🎉 Multi-Tenant Workspace Provisioned! Switch to Sign In above.")
                    else: strl.error("❌ Provisioning Rejected: Namespace string may already be claimed.")
                except Exception as e: strl.error(f"💥 Core Infrastructure Fault: {str(e)}")
    strl.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# MODULE DOMAIN 1: CLIENT ENGINE VIEWPORT
# ==========================================
def run_client_dashboard_scope():
    strl.subheader("📋 Core Infrastructure Viewport Client Hub")
    target_module = strl.sidebar.selectbox("Active Component Filter", ["Sumo Robot", "RC Car", "Robo Soccer"])
    
    with strl.spinner("Synchronizing partitioned structures..."):
        try:
            response = requests.get(f"{API_BASE_URL}/modules/{strl.session_state.team_id}/{target_module}")
            if response.status_code == 200:
                module_data = response.json()
                left_col, right_col = strl.columns([1, 1.2])
                
                with left_col:
                    strl.markdown("### 🔌 System Circuit Topology Vector")
                    raw_url = str(module_data.get("circuit_diagram_url", "")).strip()
                    if "http" in raw_url:
                        strl.image(raw_url[raw_url.find("http"):], use_container_width=True)
                    
                    if "specs" in module_data:
                        strl.markdown("#### ⚙️ Ingested Hardware Parameters")
                        for spec, val in module_data["specs"].items():
                            if val: strl.write(f"🔹 **{spec}:** `{val}`")
                            
                with right_col:
                    strl.markdown("### 💰 Component Budget Evaluation Matrix")
                    if module_data.get("budget"):
                        df = pd.DataFrame(module_data["budget"])
                        df['Total Subtotal (PKR)'] = df['quantity'].astype(int) * df['unit_cost_pkr'].astype(int)
                        df.columns = ['Component Line Item', 'Quantity', 'Unit Cost (PKR)', 'Total Subtotal (PKR)']
                        strl.dataframe(df, use_container_width=True, hide_index=True)
                        
                        grand_sum = df['Total Subtotal (PKR)'].sum()
                        strl.metric(label="Calculated Asset Value Profile", value=f"{grand_sum:,} PKR")
                        
                    if module_data.get("firmware"):
                        strl.markdown("### 💻 Active Registered Embedded Firmware Memory")
                        strl.code(module_data["firmware"], language="cpp")
            else:
                strl.info("ℹ️ Workspace module array empty. Seed technical values inside the Secure Admin Portal.")
        except Exception as e: strl.error(f"Sync Issue: {str(e)}")

# ==========================================
# MODULE DOMAIN 2: SECURE WRITE ACCESS GATE
# ==========================================
def run_admin_portal_scope():
    strl.subheader("🔒 Executive Write & Data Modification Access Hub")
    admin_token_input = strl.text_input("Enter Private Workspace Validation Modification Token", type="password")
    
    if admin_token_input == strl.session_state.team_admin_token and strl.session_state.team_admin_token != "":
        strl.success("🔓 Cryptographic Token Confirmed. Read/Write Streams Mounted.")
        
        mod_name = strl.selectbox("Select Core Blueprint Array Slot", ["Sumo Robot", "RC Car", "Robo Soccer"])
        
        c_u1, c_u2 = strl.columns([2, 1])
        with c_u1: diag_url = strl.text_input("System Schematic Circuit Diagram Vector Link (URL Only)")
        with c_u2: uploaded_pdf = strl.file_uploader("📥 Grounding Datasheet PDF", type=["pdf"])
        
        strl.markdown("#### ⚙️ Technical Blueprint Hardware Parameter Ingestion")
        cl1, cl2, cl3 = strl.columns(3)
        with cl1: chassis = strl.text_input("Chassis / Suspension Setup Frame")
        with cl2: mcu = strl.text_input("Main Core Processing MCU Node")
        with cl3: motors = strl.text_input("Drive System Actuator Motor Lines")
        
        cl4, cl5 = strl.columns(2)
        with cl4: drivers = strl.text_input("Power H-Bridge Driver Arrays")
        with cl5: sensors = strl.text_input("Telemetry Sensor Module Matrix")
        
        strl.markdown("#### 💰 Financial Ledger Allocation Matrix")
        budget_list = []
        for i in range(strl.session_state.rows):
            col1, col2, col3 = strl.columns([2.5, 0.6, 1.2])
            with col1: it_name = strl.text_input(f"Item {i+1} Description", key=f"name_{i}")
            with col2: it_qty = strl.number_input(f"Qty", min_value=1, value=1, key=f"qty_{i}")
            with col3: it_cost = strl.number_input(f"Unit Cost (PKR)", min_value=0, step=50, key=f"ucost_{i}")
            if it_name.strip(): budget_list.append({"item": it_name.strip(), "quantity": int(it_qty), "unit_cost_pkr": int(it_cost)})
        
        if strl.button("➕ Allocate Additional Financial Line Asset"):
            strl.session_state.rows += 1; strl.rerun()
            
        firmware_code = strl.text_area("C++ Low-Level Main Execution Loop Firmware Code Segment Block", height=180)
        
        if strl.button("🚀 Push Verified Assets and RAG Documents to Cloud Cluster", use_container_width=True):
            form_payload = {
                "team_id": strl.session_state.team_id, "module_name": mod_name, "circuit_diagram_url": diag_url.strip(),
                "chassis": chassis, "mcu": mcu, "motors": motors, "drivers": drivers, "sensors": sensors,
                "firmware": firmware_code, "budget_json": json.dumps(budget_list)
            }
            files_bundle = {"file": (uploaded_pdf.name, uploaded_pdf.getvalue(), "application/pdf")} if uploaded_pdf else None
            
            with strl.spinner("Encrypting arrays and performing vector text chunk processing..."):
                res = requests.post(f"{API_BASE_URL}/modules/add", data=form_payload, files=files_bundle)
                if res.status_code == 200: strl.success("🎉 Asset arrays broadcast and synced to cluster memory seamlessly!")
    elif admin_token_input != "": strl.error("🛑 Verification Access Violation: Structural token keys mismatch.")

# ==========================================
# MODULE DOMAIN 3: AGENTIC CRITIC-ACTOR PLANNER
# ==========================================
def run_agentic_planner_scope():
    strl.subheader("🧠 Multi-Agent Actor-Critic Strategy Planning Matrix")
    
    strl.markdown("### 👥 1. Human Capital Rosters & Core Skill Metrics")
    team_members_list = []
    for k in range(strl.session_state.member_count):
        strl.markdown(f"##### Asset Node #{k+1}")
        col_name, col_role = strl.columns([1, 1])
        with col_name: m_name = strl.text_input(f"Operator Name String", key=f"mem_name_{k}", value="Muhammad Hassaan Awais" if k==0 else ("Ali" if k==1 else ("Roshaan" if k==2 else "")))
        with col_role: m_role = strl.text_input(f"Assigned Execution Designation", key=f"mem_role_{k}", value="Lead Systems Architect" if k==0 else ("Structural Mechatronics Lead" if k==1 else ("Logistics Infrastructure Manager" if k==2 else "")))
        m_skills = strl.text_area(f"Specialized Technical Skillsets Matrix Arrays", key=f"mem_skills_{k}", value="Low-level firmware development, async C++, embedded register mapping logic." if k==0 else ("CAD mechanical construction framing, high-velocity kinematics design profiles." if k==1 else ("Supply infrastructure mappings, component verification and budget monitoring." if k==2 else "")))
        if m_name.strip(): team_members_list.append({"name": m_name.strip(), "role": m_role.strip(), "skills": m_skills.strip()})
        strl.markdown("---")
        
    btn_col1, btn_col2, _ = strl.columns([1.2, 1.2, 3])
    with btn_col1:
        if strl.button("➕ Onboard Team Asset Slot"): strl.session_state.member_count += 1; strl.rerun()
    with btn_col2:
        if strl.button("➖ Offboard Team Asset Slot") and strl.session_state.member_count > 1: strl.session_state.member_count -= 1; strl.rerun()

    strl.markdown("### 📅 2. Event Vector Parameters & Digital Calendar Synchronization")
    c_e1, c_e2 = strl.columns(2)
    with c_e1: event_name = strl.text_input("Target Competition Title Name", value="UET Robocom Hackathon")
    with c_e2: event_date = strl.date_input("Target Milestone Target Evaluation Date", value=datetime.today())
    modules_selected = strl.multiselect("Active Domain Blueprint Tracking Targets", ["Sumo Robot", "RC Car", "Robo Soccer"], default=["Sumo Robot"])

    # Automated .ics background computation matrix
    date_str = event_date.strftime("%Y%m%d")
    ics_data = f"BEGIN:VCALENDAR\nVERSION:2.0\nBEGIN:VEVENT\nDTSTART;VALUE=DATE:{date_str}\nSUMMARY:🏁 Target: {event_name}\nDESCRIPTION:Active multi-agent modules under optimization tracking: {', '.join(modules_selected)}\nBEGIN:VALARM\nTRIGGER:-PT24H\nACTION:DISPLAY\nDESCRIPTION:Nexa Core Alert: 24h Left to Milestone Target Evaluation!\nEND:VALARM\nEND:VEVENT\nEND:VCALENDAR"

    strl.download_button(
        label="📅 Inject Competition Milestones straight into Device Calendar App (.ics file Download)",
        data=ics_data, file_name=f"nexa_sprint_{strl.session_state.team_id}_target.ics", mime="text/calendar", use_container_width=True
    )

    strl.markdown("### 📦 3. Live Physical Local Inventory Parameters")
    if "inv_rows" not in strl.session_state: strl.session_state.inv_rows = 3
    inventory_pool = []
    for j in range(strl.session_state.inv_rows):
        col_i1, col_i2 = strl.columns([3, 1])
        with col_i1: inv_name = strl.text_input(f"Available Stock Item {j+1} Identifier Name", key=f"inv_name_{j}")
        with col_i2: inv_qty = strl.number_input(f"Stock Vol", min_value=0, value=0, key=f"inv_qty_{j}")
        if inv_name.strip(): inventory_pool.append({"item": inv_name.strip(), "available_qty": int(inv_qty)})
    if strl.button("➕ Increment Local Stock Track Index Line"): strl.session_state.inv_rows += 1; strl.rerun()

    strl.markdown("---")
    if strl.button("🚀 TRIGGER WEB-GROUNDED SELF-CORRECTING AGENT DIRECTIVE CLUSTER", use_container_width=True):
        if not team_members_list: strl.error("❌ Action Blocked: Roster tracking arrays are fully empty.")
        else:
            with strl.spinner("Actors creating draft plans... Critic executing Google Search market pricing verification loops..."):
                try:
                    agent_res = requests.post(f"{API_BASE_URL}/agent/sprint", json={
                        "team_id": strl.session_state.team_id, "current_inventory": inventory_pool,
                        "event_details": {"event_name": event_name, "date": str(event_date), "categories": modules_selected}, "team_members": team_members_list
                    }, timeout=45)
                    if agent_res.status_code == 200:
                        strl.session_state.cached_plan = agent_res.json()["sprint_plan"]
                        strl.success("🎯 Strategy Pipeline Self-Correction Loop Concluded successfully!")
                    else: strl.error(f"❌ Processing Fault: {agent_res.text}")
                except Exception as ex: strl.error(f"💥 Backend Connection Failure: {str(ex)}")

    # Display Strategic Roadmap Layout Context (Always Loaded)
    if strl.session_state.cached_plan:
        strl.markdown("---")
        strl.markdown("## 📋 Active Multi-Agent Orchestrated Blueprint Strategy")
        raw_output = strl.session_state.cached_plan
        
        if "=== PROCUREMENT PROFILE ===" in raw_output:
            parts = raw_output.split("=== PROCUREMENT PROFILE ===")
            main_content = parts[1]
            if "=== DEVELOPER SPRINT BLOCKS ===" in main_content:
                inventory_block, dev_block = main_content.split("=== DEVELOPER SPRINT BLOCKS ===")
            else: inventory_block = main_content; dev_block = ""
            
            strl.warning("🛍️ Web-Verified Logistics Analytics: Deficit Market Procurement Strategy")
            strl.markdown(inventory_block.strip())
            if dev_block:
                strl.info("👤 Active Human Asset Target Allocation Parameters")
                strl.markdown(dev_block.strip())
        else: strl.markdown(raw_output)

# ==========================================
# CENTRAL CORE EXECUTIVE DESK (CONTROL ROUTER)
# ==========================================
strl.title("🛠️ Nexa Executive Workspace Control Panel")

if not strl.session_state.authenticated:
    render_authentication_gate()
else:
    # Sidebar Session Control Interfaces
    strl.sidebar.markdown(f"### Workspace Context")
    app_mode = strl.sidebar.selectbox("Navigate Active Systems Control", [
        "📋 Client Module Dashboard", "🔒 Secure Admin Portal", "🧠 Agentic Sprint Planner"
    ])
    strl.sidebar.markdown("---")
    
    # Render isolated scope spaces dynamically based on router mapping
    if app_mode == "📋 Client Module Dashboard": run_client_dashboard_scope()
    elif app_mode == "🔒 Secure Admin Portal": run_admin_portal_scope()
    elif app_mode == "🧠 Agentic Sprint Planner": run_agentic_planner_scope()
