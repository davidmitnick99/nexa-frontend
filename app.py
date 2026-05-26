import streamlit as st
import requests
import pandas as pd
import json
import time
from datetime import datetime

# ==========================================
# 🌌 GLOBAL LAYOUT CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Nexa Core Gateway Engine", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 📡 PRODUCTION BACKEND TARGET GATEWAY
API_BASE_URL = "https://nexa-backend-tuhl.onrender.com"

# Session State Sanitization Array
for key, default_val in [
    ("authenticated", False), ("team_id", None), 
    ("team_admin_token", ""), ("cached_plan", ""), 
    ("rows", 4), ("inv_rows", 3), ("member_count", 3),
    ("logout_sequence", False)
]:
    if key not in st.session_state:
        st.session_state[key] = default_val

# ==========================================
# 🎨 PREMIUM CYBERPUNK HUD STYLE INJECTION
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Share+Tech+Mono&display=swap');

    .stApp { 
        background: radial-gradient(circle at center, #060b16 0%, #020408 100%) !important;
        background-image: linear-gradient(rgba(18, 30, 49, 0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(18, 30, 49, 0.1) 1px, transparent 1px) !important;
        background-size: 30px 30px !important;
        color: #00f0ff !important; font-family: 'Share Tech Mono', monospace !important;
        animation: gridScroll 20s linear infinite;
    }
    @keyframes gridScroll { from { background-position: 0 0; } to { background-position: 0 600px; } }

    h1, h2, h3, h4 { 
        font-family: 'Orbitron', sans-serif !important; color: #00f0ff !important; 
        text-shadow: 0 0 10px rgba(0, 240, 255, 0.6) !important; font-weight: 700 !important; letter-spacing: 2px !important;
    }
    section[data-testid="stSidebar"] { background-color: rgba(6, 11, 22, 0.85) !important; border-right: 2px solid #00f0ff !important; }
    
    .stButton>button { 
        background: linear-gradient(135deg, #005f73 0%, #0a9396 100%) !important; 
        color: #ffffff !important; font-family: 'Orbitron', sans-serif !important;
        border: 1px solid #00f0ff !important; padding: 0.6rem 2rem !important; box-shadow: 0 0 15px rgba(0, 240, 255, 0.3);
    }
    div.cyber-card {
        background: rgba(10, 15, 29, 0.75) !important; border: 1px solid #00f0ff !important; border-radius: 6px; padding: 2rem; margin-bottom: 1.5rem;
    }
    
    /* 📟 HOME PORTAL SPIN CONTROL */
    .robot-iris-portal {
        display: flex; justify-content: center; align-items: center; margin: 1.5rem auto;
        width: 100px; height: 100px; border-radius: 50%; border: 3px dashed #00f0ff; animation: spinControl 8s linear infinite;
    }
    .robot-iris-core { width: 35px; height: 35px; border-radius: 50%; background: #00f0ff; box-shadow: 0 0 20px #00f0ff; }
    @keyframes spinControl { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }

    /* ⚽ SOCCER MODULE ANIMATION */
    .soccer-blueprint-arena { position: relative; width: 150px; height: 150px; margin: 1.5rem auto; border: 2px solid rgba(0, 240, 255, 0.3); border-radius: 50%; }
    .soccer-radar-line { position: absolute; width: 50%; height: 2px; background: linear-gradient(90deg, #00f0ff, transparent); top: 50%; left: 50%; transform-origin: left center; animation: radarSweep 2.5s linear infinite; }
    .soccer-omni-wheel { position: absolute; width: 22px; height: 12px; background: #00f0ff; border-radius: 3px; }
    .sw-1 { top: 5px; left: 64px; transform: rotate(0deg); }
    .sw-2 { bottom: 15px; left: 15px; transform: rotate(120deg); }
    .sw-3 { bottom: 15px; right: 15px; transform: rotate(240deg); }

    /* 🥊 SUMO MODULE ANIMATION */
    .sumo-combat-telemetry { position: relative; width: 140px; height: 90px; margin: 2rem auto; border: 2px solid #ff0055; border-radius: 4px; }
    .sumo-attack-wedge { position: absolute; bottom: 0; left: 20px; width: 100px; height: 0; border-bottom: 30px solid #ff0055; border-left: 15px solid transparent; border-right: 15px solid transparent; animation: wedgeOscillate 0.6s ease-in-out infinite alternate; }
    .sumo-laser-line { position: absolute; width: 100%; height: 2px; background-color: #ff0055; top: 20px; animation: laserScan 1.5s ease-in-out infinite alternate; }

    /* 🏎️ RC CAR DRIVE TELEMETRY ANIMATION */
    .rc-drivetrain-hud { position: relative; width: 160px; height: 100px; margin: 1.5rem auto; border-left: 2px dashed #00f0ff; border-right: 2px dashed #00f0ff; }
    .rc-wheel { position: absolute; width: 14px; height: 28px; background: #020408; border: 2px solid #00f0ff; border-radius: 4px; box-shadow: 0 0 8px #00f0ff; }
    .rc-wl-f { top: 5px; left: -8px; animation: steeringWobble 1.5s ease-in-out infinite alternate; }
    .rc-wr-f { top: 5px; right: -8px; animation: steeringWobble 1.5s ease-in-out infinite alternate; }
    .rc-wl-r { bottom: 5px; left: -8px; }
    .rc-wr-r { bottom: 5px; right: -8px; }
    .rc-velocity-pulse { position: absolute; width: 80%; height: 4px; background: #00f0ff; left: 10%; top: 48%; opacity: 0.7; animation: tachometerPulse 0.4s ease-in-out infinite alternate; }

    /* ANIMATION KEYFRAMES REFERENCE */
    @keyframes radarSweep { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
    @keyframes wedgeOscillate { from { transform: translateY(0); } to { transform: translateY(-8px); } }
    @keyframes laserScan { from { top: 10px; } to { top: 80px; } }
    @keyframes steeringWobble { from { transform: rotate(-15deg); } to { transform: rotate(15deg); } }
    @keyframes tachometerPulse { from { background: #005f73; box-shadow: 0 0 2px #005f73; } to { background: #00f0ff; box-shadow: 0 0 12px #00f0ff; } }
    div[data-testid="stDialog"] div[role="dialog"] { background-color: #050912 !important; border: 2px solid #00f0ff !important; }
</style>
""", unsafe_allow_html=True)

# Session Termination Handle
if st.session_state.logout_sequence:
    st.session_state.authenticated = False
    st.session_state.team_id = None
    st.session_state.team_admin_token = ""
    st.session_state.cached_plan = ""
    st.session_state.logout_sequence = False
    st.rerun()

# ==========================================
# 🌍 PUBLIC COMMUNITY MODAL DIALOG
# ==========================================
@st.dialog("🌍 GLOBAL COMMUNITY SOLUTIONS MATRIX")
def open_public_community_dialog():
    st.markdown("<div class='robot-iris-portal'><div class='robot-iris-core'></div></div>", unsafe_allow_html=True)
    tab_write, tab_delete = st.tabs(["✏️ Broadcast Solution Profile", "🗑️ Revoke Entry Document"])
    
    with tab_write:
        with st.form("community_input_form", clear_on_submit=True):
            scrapped_text = st.text_area("Describe your available scrap component or hardware problem parameters:")
            target_mcu = st.text_input("Target Microcontroller Core System", value="Arduino Uno / ESP32")
            author_sig = st.text_input("Enter Secret Author Signature Name", type="password")
            submit_btn = st.form_submit_button("🛰️ BROADCAST TO COMMUNITY LEDGER", use_container_width=True)
            
            if submit_btn:
                if scrapped_text.strip() and author_sig.strip():
                    with st.spinner("Invoking web-grounded community sub-agents..."):
                        try:
                            res = requests.post(f"{API_BASE_URL}/public/community/resolve", json={
                                "scrapped_component_text": scrapped_text, "target_mcu": target_mcu, "author_signature": author_sig
                            })
                            if res.status_code == 200:
                                st.success("🎉 SECURE MEMORY SYNCED!")
                                time.sleep(1.2)
                                st.rerun(scope="app")
                        except Exception as e: st.error(f"💥 Ground Link Error: {str(e)}")

    with tab_delete:
        with st.form("community_delete_form", clear_on_submit=True):
            target_comm_id = st.text_input("Enter Target Component Document ID to Delete")
            confirm_sig = st.text_input("Confirm Secret Author Signature Name", type="password")
            delete_btn = st.form_submit_button("🚨 PERMANENTLY PURGE DOCUMENT RECORD", use_container_width=True)
            
            if delete_btn:
                if target_comm_id.strip() and confirm_sig.strip():
                    with st.spinner("Verifying signatures..."):
                        try:
                            del_res = requests.post(f"{API_BASE_URL}/public/community/delete", json={
                                "comment_id": target_comm_id, "author_signature": confirm_sig
                            })
                            if del_res.status_code == 200:
                                st.success("🚨 Post wiped successfully!")
                                time.sleep(1.2)
                                st.rerun(scope="app")
                        except Exception as e: st.error(f"💥 Error: {str(e)}")

# ==========================================
# 📟 RUN-TIME DIAGNOSTICS MODAL DIALOG
# ==========================================
@st.dialog("📟 RUN-TIME HARDWARE HEALTH DIAGNOSTIC CORE")
def open_hardware_diagnostics_dialog():
    st.markdown("<div class='robot-iris-portal'><div class='robot-iris-core'></div></div>", unsafe_allow_html=True)
    target_mod = st.selectbox("Select Target Blueprint Environment", ["Sumo Robot", "RC Car", "Robo Soccer"])
    symptom = st.text_input("Describe Physical Fault Symptom:")
    raw_logs = st.text_area("Paste Raw Serial Monitor Logs", height=100)
    
    if st.button("⚡ EXECUTE REAL-TIME RADAR INTERCEPT", use_container_width=True):
        if symptom.strip():
            with st.spinner("Isolating telemetry vectors against RAG registers..."):
                try:
                    res = requests.post(f"{API_BASE_URL}/agent/diagnose", json={
                        "team_id": st.session_state.team_id, "module_name": target_mod,
                        "error_log_text": raw_logs, "symptom_description": symptom
                    })
                    if res.status_code == 200:
                        st.success("📟 Systems Diagnosis Complete:")
                        st.markdown(res.json()["diagnostic_report"])
                except Exception as e: st.error(f"💥 Link Down: {str(e)}")

# ==========================================
# CENTRAL AUTHENTICATION PRESENTATION SCREEN
# ==========================================
def render_authentication_gate():
    st.markdown("<div class='robot-iris-portal'><div class='robot-iris-core'></div></div>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'>NEXA COMMAND ACCESS TUNNEL</h1>", unsafe_allow_html=True)
    
    st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
    auth_mode = st.radio("SYSTEM HANDSHAKE SCHEMATIC PROFILE", ["Sign In To Active Workspace", "Provision New Multi-Tenant Instance"])
    
    c1, c2 = st.columns(2)
    with c1: auth_user = st.text_input("ENTER TENANT NAMESPACE UNIQUE KEY ID").strip().lower()
    with c2: auth_pass = st.text_input("ENTER VAULT SECURE PASSWORD", type="password")
    
    if auth_mode == "Sign In To Active Workspace":
        if st.button("🔓 AUTHORIZE COMMAND GATEWAY LINK", use_container_width=True):
            if auth_user and auth_pass:
                try:
                    res = requests.post(f"{API_BASE_URL}/auth/login", json={"team_username": auth_user, "password": auth_pass})
                    if res.status_code == 200:
                        st.session_state.authenticated = True
                        st.session_state.team_id = res.json()["team_id"]
                        st.session_state.team_admin_token = res.json()["admin_token"]
                        hist = requests.get(f"{API_BASE_URL}/agent/cached/{st.session_state.team_id}")
                        if hist.status_code == 200: st.session_state.cached_plan = hist.json().get("sprint_plan", "")
                        st.success("🤝 Handshake Established. Mounting Neural UI Arrays...")
                        time.sleep(0.8)
                        st.rerun()
                    else: st.error("🛑 Security Failure: Authentication Parameter Rejection.")
                except Exception as e: st.error(f"💥 Ground Link Down: {str(e)}")
                    
    elif auth_mode == "Provision New Multi-Tenant Instance":
        custom_token = st.text_input("DEFINE PRIVATE ADMIN OVERWRITE MASTER TOKEN", type="password")
        if st.button("✨ ALLOCATE MULTI-TENANT ISOLATED NODE MATRIX", use_container_width=True):
            if auth_user and auth_pass and custom_token:
                try:
                    res = requests.post(f"{API_BASE_URL}/auth/register", json={
                        "team_username": auth_user, "password": auth_pass, "admin_token": custom_token.strip()
                    })
                    if res.status_code == 200: st.success("🎉 Node Allocated! Toggle parameter above to Sign In.")
                except Exception as e: st.error("💥 Network Anomaly.")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<h4 style='text-align: center; margin-top: 2rem;'>💡 PUBLIC COMMUNITY DEPLOYMENTS</h4>", unsafe_allow_html=True)
    if st.button("🌍 ACCESS GLOBAL COMMUNITY TERMINAL INTERFACE", use_container_width=True):
        open_public_community_dialog()
        
    # 📡 DEFINITIVE RAW LIST PARSING INTERCEPT FEED
    st.markdown("### 📡 Active Community Intelligence Ledger Feed")
    try:
        feed_res = requests.get(f"{API_BASE_URL}/public/community/all")
        if feed_res.status_code == 200:
            posts = feed_res.json()
            if not isinstance(posts, list) or len(posts) == 0:
                st.info("ℹ️ Community ledger is empty. Submit a hardware scenario profile above!")
            else:
                for post in posts:
                    try:
                        c_id = post.get("comment_id", "UNKNOWN_ID")
                        mcu_val = post.get("target_mcu", "GENERIC_MCU")
                        t_stamp = post.get("timestamp", "RECENT")
                        prob_desc = post.get("scrapped_component_text", "No problem trace log data listed.")
                        ai_sol = post.get("mentor_guidance", "Processing solution profile...")
                        
                        with st.expander(f"📦 MODULE ISSUE ID: {c_id} | Target MCU: {mcu_val} ({t_stamp})"):
                            st.markdown(f"**Student Hardware Scenario Description:**\n`{prob_desc}`")
                            st.markdown("---")
                            st.markdown(f"**Nexa Agentic Mentorship Output Solutions:**\n{ai_sol}")
                    except Exception as item_err:
                        print(f"Skipping malformed feed index log: {str(item_err)}")
    except Exception as f_err: st.error(f"Feed sync anomaly: {str(f_err)}")

# ==========================================
# MODULE VIEWPORT AUTHENTICATED DOMAINS
# ==========================================
def run_client_dashboard_scope():
    st.markdown("<h2>📋 TELEMETRY RECEPTOR: TEAM VIEWPORT</h2>", unsafe_allow_html=True)
    target_module = st.sidebar.selectbox("CHOOSE SYSTEM SUBSYSTEM TARGET", ["Sumo Robot", "RC Car", "Robo Soccer"])
    
    if target_module == "Robo Soccer":
        st.markdown("<div class='soccer-blueprint-arena'><div class='soccer-radar-line'></div><div class='soccer-omni-wheel sw-1'></div><div class='soccer-omni-wheel sw-2'></div><div class='soccer-omni-wheel sw-3'></div></div><p style='text-align:center; color:#00f0ff;'><b>OMNIDIRECTIONAL KINEMATICS ACTIVE</b></p>", unsafe_allow_html=True)
    elif target_module == "Sumo Robot":
        st.markdown("<div class='sumo-combat-telemetry'><div class='sumo-laser-line'></div><div class='sumo-attack-wedge'></div></div><p style='text-align:center; color:#ff0055;'><b>COMBAT CHARGE ATTACK VECTOR ONLINE</b></p>", unsafe_allow_html=True)
    elif target_module == "RC Car":
        st.markdown("<div class='rc-drivetrain-hud'><div class='rc-wheel rc-wl-f'></div><div class='rc-wheel rc-wr-f'></div><div class='rc-wheel rc-wl-r'></div><div class='rc-wheel rc-wr-r'></div><div class='rc-velocity-pulse'></div></div><p style='text-align:center; color:#00f0ff;'><b>HIGH-VELOCITY REAR WHEEL DRIVE ACTIVE</b></p>", unsafe_allow_html=True)
    else: 
        st.markdown("<div class='robot-iris-portal'><div class='robot-iris-core'></div></div>", unsafe_allow_html=True)

    try:
        response = requests.get(f"{API_BASE_URL}/modules/{st.session_state.team_id}/{target_module}")
        if response.status_code == 200:
            module_data = response.json()
            left_col, right_col = st.columns([1, 1.2])
            with left_col:
                st.markdown("### 🔌 CIRCUIT LAYOUT SCHEMATIC VECTOR")
                raw_url = str(module_data.get("circuit_diagram_url", "")).strip()
                if "http" in raw_url: st.image(raw_url, use_container_width=True)
                if "specs" in module_data:
                    st.markdown("#### ⚙️ SYSTEM ATTRIBUTES INGESTED")
                    for spec, val in module_data["specs"].items():
                        if val: st.write(f"⚙️ **{spec}:** `{val}`")
            with right_col:
                st.markdown("### 💰 ALLOCATED PKR SUPPLY BLOCK BALANCES")
                if module_data.get("budget"):
                    df = pd.DataFrame(module_data["budget"])
                    df['Total Subtotal (PKR)'] = df['quantity'].astype(int) * df['unit_cost_pkr'].astype(int)
                    df.columns = ['Subsystem Part Line', 'Quantity', 'Unit Value (PKR)', 'Total Subtotal (PKR)']
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    st.metric(label="COMBINED PORTFOLIO VALUATION ASSET VALUE", value=f"{df['Total Subtotal (PKR)'].sum():,} PKR")
                if module_data.get("firmware"):
                    st.markdown("### 💻 FIRMWARE LOGIC REGISTERS (C++)")
                    st.code(module_data["firmware"], language="cpp")
    except Exception as e: st.error(f"Sync Issue: {str(e)}")

def run_admin_portal_scope():
    st.markdown("<h2>🔒 ADMINISTRATIVE CORE WRITE MODULE</h2>", unsafe_allow_html=True)
    admin_token_input = st.text_input("ENTER VAULT SECURE WRITE AUTHORIZATION TOKEN", type="password")
    
    if admin_token_input == st.session_state.team_admin_token and st.session_state.team_admin_token != "":
        st.success("🔓 Cryptographic Write Token Match. Access Pipeline Enabled.")
        mod_name = st.selectbox("SELECT SUBSYSTEM MEMORY BUFFER RECEPTACLE", ["Sumo Robot", "RC Car", "Robo Soccer"])
        
        c_u1, c_u2 = st.columns([2, 1])
        with c_u1: diag_url = strl.text_input("SCHEMATIC TOPOLOGY LINK (URL)")
        with c_u2: uploaded_pdf = st.file_uploader("📥 INGEST GROUNDING PDF DATA SHEET", type=["pdf"])
        
        cl1, cl2, cl3 = st.columns(3)
        with cl1: chassis = st.text_input("CHASSIS FRAME GEOMETRY")
        with cl2: mcu = st.text_input("MCU SYSTEM ARCHITECTURE")
        with cl3: motors = st.text_input("ACTUATOR DRIVETRAIN LINES")
        
        cl4, cl5 = st.columns(2)
        with cl4: drivers = st.text_input("H-BRIDGE MODULE PROFILE")
        with cl5: sensors = st.text_input("TELEMETRY SENSOR ARRAYS")
        
        budget_list = []
        for i in range(st.session_state.rows):
            col1, col2, col3 = st.columns([2.5, 0.6, 1.2])
            with col1: it_name = st.text_input(f"Item {i+1} Description", key=f"name_{i}")
            with col2: it_qty = st.number_input(f"Qty", min_value=1, value=1, key=f"qty_{i}")
            with col3: it_cost = st.number_input(f"Unit Cost (PKR)", min_value=0, step=50, key=f"ucost_{i}")
            if it_name.strip(): budget_list.append({"item": it_name.strip(), "quantity": int(it_qty), "unit_cost_pkr": int(it_cost)})
        
        if st.button("➕ PROVISION ADDITIONAL COST COMPONENT LINE"):
            st.session_state.rows += 1; st.rerun()
            
        firmware_code = st.text_area("C++ EMBEDDED MEMORY PROGRAM MACHINE CODES PUSH", height=180)
        
        if st.button("🚀 BROADCAST STRUCTURAL BLUEPRINTS TO NODES", use_container_width=True):
            form_payload = {
                "team_id": st.session_state.team_id, "module_name": mod_name, "circuit_diagram_url": diag_url.strip(),
                "chassis": chassis, "mcu": mcu, "motors": motors, "drivers": drivers, "sensors": sensors,
                "firmware": firmware_code, "budget_json": json.dumps(budget_list)
            }
            files_bundle = {"file": (uploaded_pdf.name, uploaded_pdf.getvalue(), "application/pdf")} if uploaded_pdf else None
            with st.spinner("Parsing RAG technical text bytes and syncing Atlas documents..."):
                res = requests.post(f"{API_BASE_URL}/modules/add", data=form_payload, files=files_bundle)
                if res.status_code == 200: st.success("🎉 Transmission approved! Subsystem architecture synchronized.")
    elif admin_token_input != "": st.error("🛑 ACCESS VIOLATION: Secure key vector alignment discrepancy.")

def run_agentic_planner_scope():
    st.markdown("<h2>🧠 AGENTIC SPRINT CONTEXT ORCHESTRATION HIVE</h2>", unsafe_allow_html=True)
    
    col_l, col_r = st.columns([2, 1])
    with col_l: st.markdown("### 📋 ACTIVE CORE TRACKER OPERATORS")
    with col_r:
        if st.button("📟 ACTIVATE DIAGNOSTIC TERMINAL HUD", use_container_width=True):
            open_hardware_diagnostics_dialog()

    st.markdown("### 👥 1. HUMAN RESOURCE ASSETS & SKILLS MATRIX")
    team_members_list = []
    for k in range(st.session_state.member_count):
        st.markdown(f"##### Asset Node #{k+1}")
        col_name, col_role = st.columns([1, 1])
        with col_name: m_name = st.text_input(f"OPERATOR NAME", key=f"mem_name_{k}", value="Muhammad Hassaan Awais" if k==0 else ("Ali" if k==1 else ("Roshaan" if k==2 else "")))
        with col_role: m_role = st.text_input(f"DESIGNATION", key=f"mem_role_{k}", value="Lead Systems Architect" if k==0 else ("Mechatronics Engineer" if k==1 else ("Supply Specialist" if k==2 else "")))
        m_skills = st.text_area(f"SKILLS MATRIX LAYER PROFILE", key=f"mem_skills_{k}", value="Low-level firmware optimization, hardware interrupt C++ mapping, async logic core nodes." if k==0 else ("CAD mechanical modeling layout engineering, high-velocity kinematics design profiles." if k==1 else ("Inventory ledger processing, scarcity tracking variables and budget monitoring." if k==2 else ""))[:100])
        if m_name.strip(): team_members_list.append({"name": m_name.strip(), "role": m_role.strip(), "skills": m_skills.strip()})
    
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("➕ ONBOARD TEAM ASSET"): st.session_state.member_count += 1; st.rerun()
    with btn_col2:
        if st.button("➖ OFFBOARD TEAM ASSET") and st.session_state.member_count > 1: st.session_state.member_count -= 1; st.rerun()
            
    st.markdown("---")
    st.markdown("### 📅 2. COMPETITION VECTOR MILESTONES & SCHEDULING")
    c_e1, c_e2 = st.columns(2)
    with c_e1: event_name = st.text_input("TARGET EVENT MISSION DESCRIPTION", value="UET Robocom Hackathon")
    with c_e2: event_date = st.date_input("TARGET EVALUATION DATE INDEX", value=datetime.today())
    modules_selected = st.multiselect("BLUEPRINT TRACKING CONSTRAINTS LOADED", ["Sumo Robot", "RC Car", "Robo Soccer"], default=["Sumo Robot"])

    date_str = event_date.strftime("%Y%m%d")
    ics_data = f"BEGIN:VCALENDAR\nVERSION:2.0\nBEGIN:VEVENT\nDTSTART;VALUE=DATE:{date_str}\nSUMMARY:🏁 Target: {event_name}\nEND:VEVENT\nEND:VCALENDAR"

    st.download_button(
        label="📅 INJECT ACTIVE MILESTONES DIRECTLY INTO PERSONAL DEVICE CALENDAR (.ics)",
        data=ics_data, file_name=f"nexa_target_{st.session_state.team_id}.ics", mime="text/calendar", use_container_width=True
    )

    st.markdown("### 📦 3. HOSTEL LAB ROOM INVENTORY COUNTS")
    if "inv_rows" not in st.session_state: st.session_state.inv_rows = 3
    inventory_pool = []
    for j in range(st.session_state.inv_rows):
        col_i1, col_i2 = st.columns([3, 1])
        with col_i1: inv_name = st.text_input(f"Stock Component {j+1} String Name", key=f"inv_name_{j}")
        with col_i2: inv_qty = st.number_input(f"Stock Volume", min_value=0, value=0, key=f"inv_qty_{j}")
        if inv_name.strip(): inventory_pool.append({"item": inv_name.strip(), "available_qty": int(inv_qty)})
    if st.button("➕ EXPAND INVENTORY QUANTITY LEDGER MATRIX INDEX"): st.session_state.inv_rows += 1; st.rerun()

    st.markdown("---")
    if st.button("🚀 INITIATE WEB-GROUNDED CONCURRENT CRITIC-ACTOR STRATEGY SEQUENCE", use_container_width=True):
        if not team_members_list: st.error("❌ Array Empty: Cannot execute with no tracked personnel.")
        else:
            with st.spinner("Parallel sub-agents tracking data vectors concurrently..."):
                try:
                    agent_res = requests.post(f"{API_BASE_URL}/agent/sprint", json={
                        "team_id": st.session_state.team_id, "current_inventory": inventory_pool,
                        "event_details": {"event_name": event_name, "date": str(event_date), "categories": modules_selected}, "team_members": team_members_list
                    }, timeout=45)
                    if agent_res.status_code == 200:
                        st.session_state.cached_plan = agent_res.json()["sprint_plan"]
                        st.success("🎯 Parallel Concurrency Strategy Cycle Complete!")
                        st.rerun()
                except Exception as ex: st.error(f"💥 Ground Link Down: {str(ex)}")

    if st.session_state.cached_plan:
        st.markdown("---")
        st.markdown("<h2>📋 COLLABORATIVE AGENT CONTEXT INSTRUCTIONS</h2>", unsafe_allow_html=True)
        raw_output = st.session_state.cached_plan
        if "=== PROCUREMENT PROFILE ===" in raw_output:
            parts = raw_output.split("=== PROCUREMENT PROFILE ===")
            main_content = parts[1]
            if "=== DEVELOPER SPRINT BLOCKS ===" in main_content:
                inventory_block, dev_block = main_content.split("=== DEVELOPER SPRINT BLOCKS ===")
            else: inventory_block = main_content; dev_block = ""
            st.warning("🛍️ Web-Verified Supply Logistics: Shortage Market Ingestion Pricing")
            st.markdown(inventory_block.strip())
            if dev_block:
                st.info("👤 Active Target Task Milestones Assigned to Human Operators")
                st.markdown(dev_block.strip())
        else: st.markdown(raw_output)

# ==========================================
# CENTRAL ROUTER MANAGEMENT MATRIX
# ==========================================
if not st.session_state.authenticated: render_authentication_gate()
else:
    st.sidebar.markdown(f"### 🪐 ACTIVE HUD NODE")
    app_mode = st.sidebar.selectbox("CHOOSE SYSTEM DOMAIN ROUTE", ["📋 Client Module Dashboard", "🔒 Secure Admin Portal", "🧠 Agentic Sprint Planner"])
    st.sidebar.markdown("---")
    if st.sidebar.button("🚨 TERMINATE ACTIVE COMMAND DISPATCH NODE", use_container_width=True):
        st.session_state.logout_sequence = True
        st.rerun()
    if app_mode == "📋 Client Module Dashboard": run_client_dashboard_scope()
    elif app_mode == "🔒 Secure Admin Portal": run_admin_portal_scope()
    elif app_mode == "🧠 Agentic Sprint Planner": run_agentic_planner_scope()
