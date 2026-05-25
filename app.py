import streamlit as strl
import requests
import pandas as pd
import json
from datetime import datetime

strl.set_page_config(page_title="Nexa SaaS Platform", layout="wide")
API_BASE_URL = "https://nexa-backend-tuhl.onrender.com"

strl.markdown("""
<style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    h1, h2, h3 { color: #58a6ff !important; font-family: 'Courier New', monospace; font-weight: bold; }
    .stButton>button { 
        background: linear-gradient(135deg, #238636 0%, #2ea44f 100%) !important; 
        color: white !important; font-weight: bold !important; border-radius: 8px !important;
        border: none !important; box-shadow: 0 4px 15px rgba(46,164,79,0.3);
    }
</style>
""", unsafe_allow_html=True)

strl.title("🤖 Nexa Core Production Gateway")
strl.caption("Autonomous Systems Hub & Ingested RAG Knowledge Base Engine")
strl.markdown("---")

if "authenticated" not in strl.session_state: strl.session_state.authenticated = False
if "team_id" not in strl.session_state: strl.session_state.team_id = None
if "team_admin_token" not in strl.session_state: strl.session_state.team_admin_token = ""
if "cached_plan" not in strl.session_state: strl.session_state.cached_plan = ""

strl.sidebar.header("🔐 Workspace Access Profile")

if not strl.session_state.authenticated:
    auth_mode = strl.sidebar.radio("Profile Operation", ["Sign In To Team Workspace", "Register New Team"])
    auth_user = strl.sidebar.text_input("Team Unique Username / ID").strip().lower()
    auth_pass = strl.sidebar.text_input("Secret Master Password", type="password")
    
    if auth_mode == "Sign In To Team Workspace":
        if strl.sidebar.button("🔓 Authenticate Workspace"):
            if auth_user and auth_pass:
                try:
                    res = requests.post(f"{API_BASE_URL}/auth/login", json={"team_username": auth_user, "password": auth_pass})
                    if res.status_code == 200:
                        strl.session_state.authenticated = True
                        strl.session_state.team_id = res.json()["team_id"]
                        strl.session_state.team_admin_token = res.json()["admin_token"]
                        hist = requests.get(f"{API_BASE_URL}/agent/cached/{strl.session_state.team_id}")
                        if hist.status_code == 200: strl.session_state.cached_plan = hist.json().get("sprint_plan", "")
                        strl.rerun()
                except Exception as e: strl.sidebar.error(f"Error: {str(e)}")
    elif auth_mode == "Register New Team":
        custom_token = strl.sidebar.text_input("Define Private Admin Modification Token", type="password")
        if strl.sidebar.button("✨ Initialize New Tenant Matrix"):
            if auth_user and auth_pass and custom_token:
                try:
                    res = requests.post(f"{API_BASE_URL}/auth/register", json={"team_username": auth_user, "password": auth_pass, "admin_token": custom_token.strip()})
                    if res.status_code == 200: strl.sidebar.success("🎉 Registered! Swap to Sign In.")
                except Exception as e: strl.sidebar.error(f"Error: {str(e)}")
else:
    strl.sidebar.success(f"🟢 Active Workspace: {strl.session_state.team_id.upper()}")
    if strl.sidebar.button("🚪 Terminate Secure Session"):
        strl.session_state.authenticated = False; strl.session_state.cached_plan = ""; strl.rerun()

if not strl.session_state.authenticated:
    strl.warning("🔒 Please authenticate via the profile sidebar to unlock the cloud asset pipelines.")
else:
    app_mode = strl.sidebar.selectbox("Select Workspace Domain", ["📋 Client Module Dashboard", "🔒 Secure Admin Portal", "🧠 Agentic Sprint Planner"])

    # 1. CLIENT MODULE DASHBOARD
    if app_mode == "📋 Client Module Dashboard":
        target_module = strl.sidebar.selectbox("Active Blueprint Filter", ["Sumo Robot", "RC Car", "Robo Soccer"])
        try:
            response = requests.get(f"{API_BASE_URL}/modules/{strl.session_state.team_id}/{target_module}")
            if response.status_code == 200:
                module_data = response.json()
                left_col, right_col = strl.columns([1, 1.2])
                with left_col:
                    strl.markdown("### 🔌 System Circuit Topology")
                    raw_url = str(module_data.get("circuit_diagram_url", "")).strip()
                    if "http" in raw_url: strl.image(raw_url, use_container_width=True)
                    if "specs" in module_data:
                        strl.markdown("#### ⚙️ Hardware Specifications")
                        for spec, val in module_data["specs"].items(): strl.write(f"**{spec}:** {val}")
                with right_col:
                    strl.markdown("### 💰 Component Budget Configuration")
                    if module_data.get("budget"):
                        df = pd.DataFrame(module_data["budget"])
                        df['Total (PKR)'] = df['quantity'].astype(int) * df['unit_cost_pkr'].astype(int)
                        strl.dataframe(df, use_container_width=True, hide_index=True)
                    if module_data.get("firmware"):
                        strl.markdown("### 💻 Embedded Architecture Code")
                        strl.code(module_data["firmware"], language="cpp")
            else: strl.info("ℹ️ Namespace blank. Seed data in the Admin Portal.")
        except Exception as e: strl.error(f"Sync issue: {str(e)}")

    # 2. SECURE ADMIN PORTAL (RAG GROUNDING UPLOADER WIDGET)
    elif app_mode == "🔒 Secure Admin Portal":
        strl.markdown(f"## 🔒 Profile Writing Desk: {strl.session_state.team_id.upper()}")
        admin_token_input = strl.text_input("Enter Private Admin Modification Token", type="password")
        if admin_token_input == strl.session_state.team_admin_token and strl.session_state.team_admin_token != "":
            strl.success("🔓 Access Authorized.")
            if "rows" not in strl.session_state: strl.session_state.rows = 4
            
            mod_name = strl.selectbox("Select Target Module", ["Sumo Robot", "RC Car", "Robo Soccer"])
            diag_url = strl.text_input("Circuit Diagram Image URL")
            
            # 📁 NEW: Component Technical PDF File Stream Buffer Widget Box
            uploaded_pdf = strl.file_uploader("📥 Upload Component Technical Datasheet PDF (RAG Ingestion Base)", type=["pdf"], help="Drop any component hardware data sheet here (e.g., L298N driver, ESP32 map). The agent will extract pin descriptions natively.")
            
            strl.markdown("#### ⚙️ Technical Specifications")
            chassis = strl.text_input("Chassis Frame Structure Type")
            mcu = strl.text_input("Microcontroller System")
            motors = strl.text_input("Motors Type")
            drivers = strl.text_input("Motor Driver Type")
            sensors = strl.text_input("Sensors Configuration")
            
            budget_list = []
            for i in range(strl.session_state.rows):
                col1, col2, col3 = strl.columns([2, 0.5, 1])
                with col1: it_name = strl.text_input(f"Item {i+1} Description", key=f"name_{i}")
                with col2: it_qty = strl.number_input(f"Qty", min_value=1, value=1, key=f"qty_{i}")
                with col3: it_cost = strl.number_input(f"Unit Cost (PKR)", min_value=0, step=50, key=f"ucost_{i}")
                if it_name.strip(): budget_list.append({"item": it_name.strip(), "quantity": int(it_qty), "unit_cost_pkr": int(it_cost)})
            
            if strl.button("➕ Add Another Component Line"):
                strl.session_state.rows += 1; strl.rerun()
                
            firmware_code = strl.text_area("Paste C++ Code Memory Matrix", height=150)
            
            if strl.button("🚀 Broadcast Module Blueprint to Cloud"):
                form_payload = {
                    "team_id": strl.session_state.team_id, "module_name": mod_name, "circuit_diagram_url": diag_url.strip(),
                    "chassis": chassis, "mcu": mcu, "motors": motors, "drivers": drivers, "sensors": sensors,
                    "firmware": firmware_code, "budget_json": json.dumps(budget_list)
                }
                
                # Bundle file buffer array context defensively
                files_bundle = None
                if uploaded_pdf is not None:
                    files_bundle = {"file": (uploaded_pdf.name, uploaded_pdf.getvalue(), "application/pdf")}
                
                with strl.spinner("Processing RAG embeddings and uploading records..."):
                    res = requests.post(f"{API_BASE_URL}/modules/add", data=form_payload, files=files_bundle)
                    if res.status_code == 200:
                        strl.success("🎉 Blueprint database asset array and PDF datasheet successfully ingested contextually!")
        elif admin_token_input != "": strl.error("🛑 Token mismatch.")

    # 3. AGENTIC SPRINT PLANNER
    elif app_mode == "🧠 Agentic Sprint Planner":
        strl.markdown(f"## 🧠 Google Agentic AI Sprint Planner Workspace")
        if "member_count" not in strl.session_state: strl.session_state.member_count = 3

        strl.markdown("### 👥 1. Team Context & Dynamic Specializations")
        team_members_list = []
        for k in range(strl.session_state.member_count):
            strl.markdown(f"##### 👤 Teammate #{k+1}")
            col_name, col_role = strl.columns([1, 1])
            with col_name: m_name = strl.text_input(f"Name", key=f"mem_name_{k}", value="Muhammad Hassaan Awais" if k==0 else ("Ali" if k==1 else ("Roshaan" if k==2 else "")))
            with col_role: m_role = strl.text_input(f"Core Role Designation", key=f"mem_role_{k}", value="Lead Architect" if k==0 else ("Structural Engineer" if k==1 else ("Procurement Manager" if k==2 else "")))
            m_skills = strl.text_area(f"Technical Skills Matrix & Focus Area", key=f"mem_skills_{k}", value="Firmware development, C++, microcontroller logic." if k==0 else ("CAD layouts, 3D printing modeling." if k==1 else ("Electronics wiring, inventory mapping." if k==2 else "")))
            if m_name.strip(): team_members_list.append({"name": m_name.strip(), "role": m_role.strip(), "skills": m_skills.strip()})
            strl.markdown("---")
            
        btn_col1, btn_col2, _ = strl.columns([1, 1, 3])
        with btn_col1:
            if strl.button("➕ Add New Member Slot"): strl.session_state.member_count += 1; strl.rerun()
        with btn_col2:
            if strl.button("➖ Remove Member Slot") and strl.session_state.member_count > 1: strl.session_state.member_count -= 1; strl.rerun()

        strl.markdown("### 📅 2. Event Target Parameters")
        c_e1, c_e2 = strl.columns(2)
        with c_e1: event_name = strl.text_input("Competition Name", value="UET Robocom Hackathon")
        with c_e2: event_date = strl.date_input("Target Event Deadline Date", value=datetime.today())
        modules_selected = strl.multiselect("Select Registered Categories / Modules", ["Sumo Robot", "RC Car", "Robo Soccer"], default=["Sumo Robot"])

        strl.markdown("### 📦 3. Current Local Component Inventory")
        if "inv_rows" not in strl.session_state: strl.session_state.inv_rows = 3
        inventory_pool = []
        for j in range(strl.session_state.inv_rows):
            col_i1, col_i2 = strl.columns([3, 1])
            with col_i1: inv_name = strl.text_input(f"Stock Component {j+1} Name", key=f"inv_name_{j}")
            with col_i2: inv_qty = strl.number_input(f"Stock Qty", min_value=0, value=0, key=f"inv_qty_{j}")
            if inv_name.strip(): inventory_pool.append({"item": inv_name.strip(), "available_qty": int(inv_qty)})
        if strl.button("➕ Add Inventory Line"): strl.session_state.inv_rows += 1; strl.rerun()

        strl.markdown("---")
        if strl.button("🚀 EXECUTE DYNAMIC AGENT STRATEGY GENERATOR"):
            if not team_members_list: strl.error("❌ Add team members.")
            else:
                with strl.spinner("Triggering cloud agent sequence..."):
                    try:
                        agent_res = requests.post(f"{API_BASE_URL}/agent/sprint", json={
                            "team_id": strl.session_state.team_id, "current_inventory": inventory_pool,
                            "event_details": {"event_name": event_name, "date": str(event_date), "categories": modules_selected}, "team_members": team_members_list
                        }, timeout=30)
                        if agent_res.status_code == 200:
                            strl.session_state.cached_plan = agent_res.json()["sprint_plan"]
                            strl.success("🎯 Strategy Compiled from RAG Dataset Insights!")
                        else: strl.error(f"❌ Error: {agent_res.text}")
                    except Exception as ex: strl.error(f"💥 Collapsed: {str(ex)}")

        if strl.session_state.cached_plan:
            strl.markdown("---")
            strl.markdown("### 📋 Active Synchronized Strategic Roadmap")
            raw_output = strl.session_state.cached_plan
            if "=== PROCUREMENT PROFILE ===" in raw_output:
                parts = raw_output.split("=== PROCUREMENT PROFILE ===")
                main_content = parts[1]
                if "=== DEVELOPER SPRINT BLOCKS ===" in main_content:
                    inventory_block, dev_block = main_content.split("=== DEVELOPER SPRINT BLOCKS ===")
                else: inventory_block = main_content; dev_block = ""
                
                strl.warning("🛍️ AI Logistics Analytics: Procurement List")
                strl.markdown(inventory_block.strip())
                if dev_block:
                    strl.markdown("### 👤 Specialized Teammate Directives")
                    strl.markdown(dev_block.strip())
            else: strl.markdown(raw_output)
