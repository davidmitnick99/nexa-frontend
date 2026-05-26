import streamlit as strl
import requests
import pandas as pd
import json
import time
from datetime import datetime

# 1. Production Config & Core Frame Anchors
strl.set_page_config(page_title="Nexa Core Gateway Engine", layout="wide", initial_sidebar_state="expanded")
API_BASE_URL = "https://nexa-backend-tuhl.onrender.com"

# Session State Sanitization Array
for key, default_val in [
    ("authenticated", False), ("team_id", None), 
    ("team_admin_token", ""), ("cached_plan", ""), 
    ("rows", 4), ("inv_rows", 3), ("member_count", 3),
    ("logout_sequence", False),
    ("trigger_community_broadcast", False),
    ("com_scrapped_text", ""), ("com_target_mcu", ""), ("com_author_sig", "")
]:
    if key not in strl.session_state:
        strl.session_state[key] = default_val

# 🌌🎨 ROBOTICS MISSION CONTROL HUD DESIGN MATRIX
strl.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Share+Tech+Mono&display=swap');

    .stApp { 
        background: radial-gradient(circle at center, #060b16 0%, #020408 100%) !important;
        background-image: linear-gradient(rgba(18, 30, 49, 0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(18, 30, 49, 0.1) 1px, transparent 1px) !important;
        background-size: 30px 30px !important;
        color: #00f0ff !important;
        font-family: 'Share Tech Mono', monospace !important;
        animation: gridScroll 20s linear infinite;
    }
    
    @keyframes gridScroll { from { background-position: 0 0; } to { background-position: 0 600px; } }

    h1, h2, h3, h4 { 
        font-family: 'Orbitron', sans-serif !important; 
        color: #00f0ff !important; 
        text-shadow: 0 0 10px rgba(0, 240, 255, 0.6) !important;
        font-weight: 700 !important; letter-spacing: 2px !important;
    }
    
    section[data-testid="stSidebar"] { 
        background-color: rgba(6, 11, 22, 0.85) !important; 
        border-right: 2px solid #00f0ff !important;
        box-shadow: 5px 0 25px rgba(0, 240, 255, 0.15);
    }
    
    .stButton>button { 
        background: linear-gradient(135deg, #005f73 0%, #0a9396 100%) !important; 
        color: #ffffff !important; font-family: 'Orbitron', sans-serif !important;
        font-weight: bold !important; border-radius: 4px !important;
        border: 1px solid #00f0ff !important; padding: 0.6rem 2rem !important;
        text-shadow: 0 0 5px #00f0ff; box-shadow: 0 0 15px rgba(0, 240, 255, 0.3);
        transition: all 0.3s ease-in-out;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 25px #00f0ff; background: #00f0ff !important; color: #060b16 !important; }
    
    div.cyber-card {
        background: rgba(10, 15, 29, 0.75) !important; 
        border: 1px solid #00f0ff !important; border-radius: 6px; padding: 2rem; margin-bottom: 1.5rem;
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.1); backdrop-filter: blur(10px);
    }

    .robot-iris-portal {
        display: flex; justify-content: center; align-items: center; margin: 1.5rem auto;
        width: 100px; height: 100px; border-radius: 50%; border: 3px dashed #00f0ff;
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.4), inset 0 0 15px rgba(0, 240, 255, 0.4);
        animation: spinControl 8s linear infinite;
    }
    .robot-iris-core {
        width: 35px; height: 35px; border-radius: 50%; background: #00f0ff;
        box-shadow: 0 0 20px #00f0ff; animation: pulseCore 1s ease-in-out infinite alternate;
    }

    .soccer-blueprint-arena {
        position: relative; width: 150px; height: 150px; margin: 1.5rem auto;
        border: 2px solid rgba(0, 240, 255, 0.3); border-radius: 50%;
        background: radial-gradient(circle, rgba(10,93,150,0.1) 0%, transparent 70%);
    }
    .soccer-radar-line {
        position: absolute; width: 50%; height: 2px; background: linear-gradient(90deg, #00f0ff, transparent);
        top: 50%; left: 50%; transform-origin: left center; animation: radarSweep 2.5s linear infinite;
    }
    .soccer-omni-wheel {
        position: absolute; width: 22px; height: 12px; background: #00f0ff; border-radius: 3px; box-shadow: 0 0 12px #00f0ff;
    }
    .sw-1 { top: 5px; left: 64px; transform: rotate(0deg); }
    .sw-2 { bottom: 15px; left: 15px; transform: rotate(120deg); }
    .sw-3 { bottom: 15px; right: 15px; transform: rotate(240deg); }

    .sumo-combat-telemetry {
        position: relative; width: 140px; height: 90px; margin: 2rem auto; border: 2px solid #ff0055; border-radius: 4px;
        background: linear-gradient(0deg, rgba(255,0,85,0.05) 0%, transparent 100%); box-shadow: 0 0 20px rgba(255,0,85,0.2);
    }
    .sumo-attack-wedge {
        position: absolute; bottom: 0; left: 20px; width: 100px; height: 0;
        border-bottom: 30px solid #ff0055; border-left: 15px solid transparent; border-right: 15px solid transparent;
        filter: drop-shadow(0 0 10px #ff0055); animation: wedgeOscillate 0.6s ease-in-out infinite alternate;
    }
    .sumo-laser-line {
        position: absolute; width: 100%; height: 2px; background-color: #ff0055; box-shadow: 0 0 10px #ff0055; top: 20px; animation: laserScan 1.5s ease-in-out infinite alternate;
    }

    @keyframes spinControl { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
    @keyframes pulseCore { from { transform: scale(0.85); filter: brightness(1); } to { transform: scale(1.1); filter: brightness(1.5); } }
    @keyframes radarSweep { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
    @keyframes wedgeOscillate { from { transform: translateY(0); } to { transform: translateY(-8px); } }
    @keyframes laserScan { from { top: 10px; } to { top: 80px; } }

    .disconnect-banner {
        background-color: #1a020c !important; border: 2px solid #ff0055 !important; color: #ff0055 !important;
        font-family: 'Share Tech Mono', monospace; padding: 2.5rem; border-radius: 4px; text-align: center; box-shadow: 0 0 40px rgba(255,0,85,0.3);
    }
    
    div[data-testid="stDialog"] div[role="dialog"] {
        background-color: #050912 !important; border: 2px solid #00f0ff !important; box-shadow: 0 0 30px #00f0ff;
    }
</style>
""", unsafe_allow_html=True)

# Session Termination Handle
if strl.session_state.logout_sequence:
    strl.markdown("<div class='disconnect-banner'>", unsafe_allow_html=True)
    strl.markdown("### ⚠️ [SECURITY] DISCONNECTING NEXA COMMAND CORE HIVE...")
    strl.markdown("</div>", unsafe_allow_html=True)
    time.sleep(1.5)
    strl.session_state.authenticated = False
    strl.session_state.team_id = None
    strl.session_state.team_admin_token = ""
    strl.session_state.cached_plan = ""
    strl.session_state.logout_sequence = False
    strl.rerun()

# ==========================================
# 🌍 PUBLIC OPEN PORTAL DIALOG BOX MODAL
# ==========================================
@strl.dialog("🌍 GLOBAL COMMUNITY SOLUTIONS MATRIX")
def open_public_community_dialog():
    strl.markdown("<div class='robot-iris-portal'><div class='robot-iris-core'></div></div>", unsafe_allow_html=True)
    tab_write, tab_delete = strl.tabs(["✏️ Broadcast Solution Profile", "🗑️ Revoke Entry Document"])
    
    with tab_write:
        scrapped_text = strl.text_area("Describe your available scrap component or hardware problem parameters:", key="modal_txt_field")
        target_mcu = strl.text_input("Target Microcontroller Core System", value="Arduino Uno / ESP32", key="modal_mcu_field")
        strl.markdown("🔒 *Enter your signature token to manage or delete this post later anonymously.*")
        author_sig = strl.text_input("Enter Secret Author Signature Name", type="password", key="modal_sig_field")
        
        # Capture input states and pass the control flag straight out to the main page thread
        if strl.button("🛰️ BROADCAST TO COMMUNITY LEDGER", use_container_width=True):
            if not scrapped_text.strip() or not author_sig.strip():
                strl.error("❌ Problem logs and Signature keys are required parameters.")
            else:
                strl.session_state.com_scrapped_text = scrapped_text
                strl.session_state.com_target_mcu = target_mcu
                strl.session_state.com_author_sig = author_sig
                strl.session_state.trigger_community_broadcast = True
                strl.rerun()

    with tab_delete:
        target_comm_id = strl.text_input("Enter Target Component Document ID to Delete")
        confirm_sig = strl.text_input("Confirm Secret Author Signature Name to Verify Ownership", type="password")
        
        if strl.button("🚨 PERMANENTLY PURGE DOCUMENT RECORD", use_container_width=True):
            if target_comm_id.strip() and confirm_sig.strip():
                with strl.spinner("Purging record..."):
                    try:
                        del_res = requests.post(f"{API_BASE_URL}/public/community/delete", json={
                            "comment_id": target_comm_id, "author_signature": confirm_sig
                        })
                        if del_res.status_code == 200:
                            strl.success("🚨 Post wiped successfully!")
                            time.sleep(1)
                            strl.rerun()
                        else: strl.error("🛑 Deletion Rejected: Key mismatch.")
                    except Exception as e: strl.error(f"💥 Error: {str(e)}")

# ==========================================
# 📟 RUN-TIME DIAGNOSTICS DIALOG BOX MODAL
# ==========================================
@strl.dialog("📟 RUN-TIME HARDWARE HEALTH DIAGNOSTIC CORE")
def open_hardware_diagnostics_dialog():
    strl.markdown("<div class='robot-iris-portal'><div class='robot-iris-core'></div></div>", unsafe_allow_html=True)
    target_mod = strl.selectbox("Select Target Blueprint Environment", ["Sumo Robot", "RC Car", "Robo Soccer"])
    symptom = strl.text_input("Describe Physical Fault Symptom:")
    raw_logs = strl.text_area("Paste Raw Serial Monitor Hex Arrays / Compiler Crash Stack Traces", height=100)
    
    if strl.button("⚡ EXECUTE REAL-TIME RADAR INTERCEPT", use_container_width=True):
        if symptom.strip():
            with strl.spinner("Isolating telemetry vectors against RAG grounding registers..."):
                try:
                    res = requests.post(f"{API_BASE_URL}/agent/diagnose", json={
                        "team_id": strl.session_state.team_id, "module_name": target_mod,
                        "error_log_text": raw_logs, "symptom_description": symptom
                    })
                    if res.status_code == 200:
                        strl.success("📟 Systems Diagnosis Complete:")
                        strl.markdown(res.json()["diagnostic_report"])
                except Exception as e: strl.error(f"💥 Link Down: {str(e)}")

# ==========================================
# AUTHENTICATION GATE SCREEN
# ==========================================
def render_authentication_gate():
    # ⚡ EXECUTING DECOUPLED BACKEND BROADCST SAFELY ON MAIN RENDERING PAGE
    if strl.session_state.trigger_community_broadcast:
        strl.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        strl.markdown("<div class='robot-iris-portal'><div class='robot-iris-core'></div></div>", unsafe_allow_html=True)
        with strl.spinner("🛰️ CONNECTED: Processing Web-Searching Multi-Agent Compilation Pipeline..."):
            try:
                res = requests.post(f"{API_BASE_URL}/public/community/resolve", json={
                    "scrapped_component_text": strl.session_state.com_scrapped_text,
                    "target_mcu": strl.session_state.com_target_mcu,
                    "author_signature": strl.session_state.com_author_sig
                })
                if res.status_code == 200:
                    strl.success(f"🎉 SECURE MEMORY SYNCED: Solution added under ID: {res.json()['comment_id']}")
                    # Clear transient state registers completely
                    strl.session_state.trigger_community_broadcast = False
                    strl.session_state.com_scrapped_text = ""
                    strl.session_state.com_target_mcu = ""
                    strl.session_state.com_author_sig = ""
                    time.sleep(1.5)
                    strl.rerun()
            except Exception as e:
                strl.error(f"💥 Transmission Interrupted: {str(e)}")
                strl.session_state.trigger_community_broadcast = False
        strl.markdown("</div>", unsafe_allow_html=True)

    strl.markdown("<div class='robot-iris-portal'><div class='robot-iris-core'></div></div>", unsafe_allow_html=True)
    strl.markdown("<h1 style='text-align: center;'>NEXA COMMAND ACCESS TUNNEL</h1>", unsafe_allow_html=True)
    
    strl.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
    auth_mode = strl.radio("SYSTEM HANDSHAKE SCHEMATIC PROFILE", ["Sign In To Active Workspace", "Provision New Multi-Tenant Instance"])
    
    c1, c2 = strl.columns(2)
    with c1: auth_user = strl.text_input("ENTER TENANT NAMESPACE UNIQUE KEY ID").strip().lower()
    with c2: auth_pass = strl.text_input("ENTER VAULT SECURE PASSWORD", type="password")
    
    if auth_mode == "Sign In To Active Workspace":
        if strl.button("🔓 AUTHORIZE COMMAND GATEWAY LINK", use_container_width=True):
            if auth_user and auth_pass:
                try:
                    res = requests.post(f"{API_BASE_URL}/auth/login", json={"team_username": auth_user, "password": auth_pass})
                    if res.status_code == 200:
                        strl.session_state.authenticated = True
                        strl.session_state.team_id = res.json()["team_id"]
                        strl.session_state.team_admin_token = res.json()["admin_token"]
                        hist = requests.get(f"{API_BASE_URL}/agent/cached/{strl.session_state.team_id}")
                        if hist.status_code == 200: strl.session_state.cached_plan = hist.json().get("sprint_plan", "")
                        strl.success("🤝 Handshake Established. Mounting Neural UI Arrays...")
                        time.sleep(0.8)
                        strl.rerun()
                    else: strl.error("🛑 Security Failure: Authentication Parameter Rejection.")
                except Exception as e: strl.error(f"💥 Ground Link Down: {str(e)}")
                    
    elif auth_mode == "Provision New Multi-Tenant Instance":
        custom_token = strl.text_input("DEFINE PRIVATE ADMIN OVERWRITE MASTER TOKEN", type="password")
        if strl.button("✨ ALLOCATE MULTI-TENANT ISOLATED NODE MATRIX", use_container_width=True):
            if auth_user and auth_pass and custom_token:
                try:
                    res = requests.post(f"{API_BASE_URL}/auth/register", json={
                        "team_username": auth_user, "password": auth_pass, "admin_token": custom_token.strip()
                    })
                    if res.status_code == 200: strl.success("🎉 Node Allocated! Toggle parameter above to Sign In.")
                except Exception as e: strl.error("💥 Network Anomaly.")
    strl.markdown("</div>", unsafe_allow_html=True)
    
    strl.markdown("<h4 style='text-align: center; margin-top: 2rem;'>💡 PUBLIC COMMUNITY DEPLOYMENTS</h4>", unsafe_allow_html=True)
    if strl.button("🌍 ACCESS GLOBAL COMMUNITY TERMINAL INTERFACE", use_container_width=True):
        open_public_community_dialog()
        
    # 📡 LIVE CROWDSOURCED DISPATCH LEDGER FEED
    strl.markdown("### 📡 Active Community Intelligence Ledger Feed")
    try:
        feed_res = requests.get(f"{API_BASE_URL}/public/community/all")
        if feed_res.status_code == 200:
            posts = feed_res.json().get("posts", [])
            if not posts:
                strl.info("ℹ️ Community ledger is currently empty. Be the first to broadcast a mechatronics issue mapping above!")
            for post in posts:
                with strl.expander(f"📦 MODULE ISSUE ID: {post['comment_id']} | Target MCU: {post['target_mcu']} ({post['timestamp']})"):
                    strl.markdown(f"**Student Hardware Scenario Description:**\n`{post['scrapped_component_text']}`")
                    strl.markdown("---")
                    strl.markdown(f"**Nexa Agentic Mentorship Output Solutions:**\n{post['mentor_guidance']}")
    except Exception as f_err: strl.error(f"Feed error: {str(f_err)}")

# ==========================================
# MODULE VIEWPORT AUTHENTICATED DOMAINS
# ==========================================
def run_client_dashboard_scope():
    strl.markdown("<h2>📋 TELEMETRY RECEPTOR: TEAM VIEWPORT</h2>", unsafe_allow_html=True)
    target_module = strl.sidebar.selectbox("CHOOSE SYSTEM SUBSYSTEM TARGET", ["Sumo Robot", "RC Car", "Robo Soccer"])
    
    if target_module == "Robo Soccer":
        strl.markdown("<div class='soccer-blueprint-arena'><div class='soccer-radar-line'></div><div class='soccer-omni-wheel sw-1'></div><div class='soccer-omni-wheel sw-2'></div><div class='soccer-omni-wheel sw-3'></div></div><p style='text-align:center; color:#00f0ff;'><b>OMNIDIRECTIONAL KINEMATICS ACTIVE</b></p>", unsafe_allow_html=True)
    elif target_module == "Sumo Robot":
        strl.markdown("<div class='sumo-combat-telemetry'><div class='sumo-laser-line'></div><div class='sumo-attack-wedge'></div></div><p style='text-align:center; color:#ff0055;'><b>COMBAT CHARGE ATTACK VECTOR ONLINE</b></p>", unsafe_allow_html=True)
    else: strl.markdown("<div class='robot-iris-portal'><div class='robot-iris-core'></div></div>", unsafe_allow_html=True)

    try:
        response = requests.get(f"{API_BASE_URL}/modules/{strl.session_state.team_id}/{target_module}")
        if response.status_code == 200:
            module_data = response.json()
            left_col, right_col = strl.columns([1, 1.2])
            with left_col:
                strl.markdown("### 🔌 CIRCUIT LAYOUT SCHEMATIC VECTOR")
                raw_url = str(module_data.get("circuit_diagram_url", "")).strip()
                if "http" in raw_url: strl.image(raw_url, use_container_width=True)
                if "specs" in module_data:
                    strl.markdown("#### ⚙️ SYSTEM ATTRIBUTES INGESTED")
                    for spec, val in module_data["specs"].items():
                        if val: strl.write(f"⚙️ **{spec}:** `{val}`")
            with right_col:
                strl.markdown("### 💰 ALLOCATED PKR SUPPLY BLOCK BALANCES")
                if module_data.get("budget"):
                    df = pd.DataFrame(module_data["budget"])
                    df['Total Subtotal (PKR)'] = df['quantity'].astype(int) * df['unit_cost_pkr'].astype(int)
                    df.columns = ['Subsystem Part Line', 'Quantity', 'Unit Value (PKR)', 'Total Subtotal (PKR)']
                    strl.dataframe(df, use_container_width=True, hide_index=True)
                    strl.metric(label="COMBINED PORTFOLIO VALUATION ASSET VALUE", value=f"{df['Total Subtotal (PKR)'].sum():,} PKR")
                if module_data.get("firmware"):
                    strl.markdown("### 💻 FIRMWARE LOGIC REGISTERS (C++)")
                    strl.code(module_data["firmware"], language="cpp")
    except Exception as e: strl.error(f"Sync Issue: {str(e)}")

def run_admin_portal_scope():
    strl.markdown("<h2>🔒 ADMINISTRATIVE CORE WRITE MODULE</h2>", unsafe_allow_html=True)
    admin_token_input = strl.text_input("ENTER VAULT SECURE WRITE AUTHORIZATION TOKEN", type="password")
    
    if admin_token_input == strl.session_state.team_admin_token and strl.session_state.team_admin_token != "":
        strl.success("🔓 Cryptographic Write Token Match. Access Pipeline Enabled.")
        mod_name = strl.selectbox("SELECT SUBSYSTEM MEMORY BUFFER RECEPTACLE", ["Sumo Robot", "RC Car", "Robo Soccer"])
        
        c_u1, c_u2 = strl.columns([2, 1])
        with c_u1: diag_url = strl.text_input("SCHEMATIC TOPOLOGY LINK (URL)")
        with c_u2: uploaded_pdf = strl.file_uploader("📥 INGEST GROUNDING PDF DATA SHEET", type=["pdf"])
        
        cl1, cl2, cl3 = strl.columns(3)
        with cl1: chassis = strl.text_input("CHASSIS FRAME GEOMETRY")
        with cl2: mcu = strl.text_input("MCU SYSTEM ARCHITECTURE")
        with cl3: motors = strl.text_input("ACTUATOR DRIVETRAIN LINES")
        
        cl4, cl5 = strl.columns(2)
        with cl4: drivers = strl.text_input("H-BRIDGE MODULE PROFILE")
        with cl5: sensors = strl.text_input("TELEMETRY SENSOR ARRAYS")
        
        budget_list = []
        for i in range(strl.session_state.rows):
            col1, col2, col3 = strl.columns([2.5, 0.6, 1.2])
            with col1: it_name = strl.text_input(f"Item {i+1} Description", key=f"name_{i}")
            with col2: it_qty = strl.number_input(f"Qty", min_value=1, value=1, key=f"qty_{i}")
            with col3: it_cost = strl.number_input(f"Unit Cost (PKR)", min_value=0, step=50, key=f"ucost_{i}")
            if it_name.strip(): budget_list.append({"item": it_name.strip(), "quantity": int(it_qty), "unit_cost_pkr": int(it_cost)})
        
        if strl.button("➕ PROVISION ADDITIONAL COST COMPONENT LINE"):
            strl.session_state.rows += 1; strl.rerun()
            
        firmware_code = strl.text_area("C++ EMBEDDED MEMORY PROGRAM MACHINE CODES PUSH", height=180)
        
        if strl.button("🚀 BROADCAST STRUCTURAL BLUEPRINTS TO NODES", use_container_width=True):
            form_payload = {
                "team_id": strl.session_state.team_id, "module_name": mod_name, "circuit_diagram_url": diag_url.strip(),
                "chassis": chassis, "mcu": mcu, "motors": motors, "drivers": drivers, "sensors": sensors,
                "firmware": firmware_code, "budget_json": json.dumps(budget_list)
            }
            files_bundle = {"file": (uploaded_pdf.name, uploaded_pdf.getvalue(), "application/pdf")} if uploaded_pdf else None
            with strl.spinner("Parsing RAG technical text bytes and syncing Atlas documents..."):
                res = requests.post(f"{API_BASE_URL}/modules/add", data=form_payload, files=files_bundle)
                if res.status_code == 200: strl.success("🎉 Transmission approved! Subsystem architecture synchronized.")
    elif admin_token_input != "": strl.error("🛑 ACCESS VIOLATION: Secure key vector alignment discrepancy.")

def run_agentic_planner_scope():
    strl.markdown("<h2>🧠 AGENTIC SPRINT CONTEXT ORCHESTRATION HIVE</h2>", unsafe_allow_html=True)
    
    col_l, col_r = strl.columns([2, 1])
    with col_l: strl.markdown("### 📋 ACTIVE CORE TRACKER OPERATORS")
    with col_r:
        if strl.button("📟 ACTIVATE DIAGNOSTIC TERMINAL HUD", use_container_width=True):
            open_hardware_diagnostics_dialog()

    strl.markdown("### 👥 1. HUMAN RESOURCE ASSETS & SKILLS MATRIX")
    team_members_list = []
    for k in range(strl.session_state.member_count):
        strl.markdown(f"##### Asset Node #{k+1}")
        col_name, col_role = strl.columns([1, 1])
        with col_name: m_name = strl.text_input(f"OPERATOR NAME", key=f"mem_name_{k}", value="Muhammad Hassaan Awais" if k==0 else ("Ali" if k==1 else ("Roshaan" if k==2 else "")))
        with col_role: m_role = strl.text_input(f"DESIGNATION", key=f"mem_role_{k}", value="Lead Systems Architect" if k==0 else ("Mechatronics Engineer" if k==1 else ("Supply Specialist" if k==2 else "")))
        m_skills = strl.text_area(f"SKILLS MATRIX LAYER PROFILE", key=f"mem_skills_{k}", value="Low-level firmware optimization, hardware interrupt C++ mapping, async logic core nodes." if k==0 else ("CAD mechanical modeling layout engineering, high-velocity kinematics design profiles." if k==1 else ("Inventory ledger processing, scarcity tracking variables and budget monitoring." if k==2 else ""))[:100])
        if m_name.strip(): team_members_list.append({"name": m_name.strip(), "role": m_role.strip(), "skills": m_skills.strip()})
    
    btn_col1, btn_col2 = strl.columns(2)
    with btn_col1:
        if strl.button("➕ ONBOARD TEAM ASSET"): strl.session_state.member_count += 1; strl.rerun()
    with btn_col2:
        if strl.button("➖ OFFBOARD TEAM ASSET") and strl.session_state.member_count > 1: strl.session_state.member_count -= 1; strl.rerun()
            
    strl.markdown("---")
    strl.markdown("### 📅 2. COMPETITION VECTOR MILESTONES & SCHEDULING")
    c_e1, c_e2 = strl.columns(2)
    with c_e1: event_name = strl.text_input("TARGET EVENT MISSION DESCRIPTION", value="UET Robocom Hackathon")
    with c_e2: event_date = strl.date_input("TARGET EVALUATION DATE INDEX", value=datetime.today())
    modules_selected = strl.multiselect("BLUEPRINT TRACKING CONSTRAINTS LOADED", ["Sumo Robot", "RC Car", "Robo Soccer"], default=["Sumo Robot"])

    date_str = event_date.strftime("%Y%m%d")
    ics_data = f"BEGIN:VCALENDAR\nVERSION:2.0\nBEGIN:VEVENT\nDTSTART;VALUE=DATE:{date_str}\nSUMMARY:🏁 Target: {event_name}\nEND:VEVENT\nEND:VCALENDAR"

    strl.download_button(
        label="📅 INJECT ACTIVE MILESTONES DIRECTLY INTO PERSONAL DEVICE CALENDAR (.ics)",
        data=ics_data, file_name=f"nexa_target_{strl.session_state.team_id}.ics", mime="text/calendar", use_container_width=True
    )

    strl.markdown("### 📦 3. HOSTEL LAB ROOM INVENTORY COUNTS")
    if "inv_rows" not in strl.session_state: strl.session_state.inv_rows = 3
    inventory_pool = []
    for j in range(strl.session_state.inv_rows):
        col_i1, col_i2 = strl.columns([3, 1])
        with col_i1: inv_name = strl.text_input(f"Stock Component {j+1} String Name", key=f"inv_name_{j}")
        with col_i2: inv_qty = strl.number_input(f"Stock Volume", min_value=0, value=0, key=f"inv_qty_{j}")
        if inv_name.strip(): inventory_pool.append({"item": inv_name.strip(), "available_qty": int(inv_qty)})
    if strl.button("➕ EXPAND INVENTORY QUANTITY LEDGER MATRIX INDEX"): strl.session_state.inv_rows += 1; strl.rerun()

    strl.markdown("---")
    if strl.button("🚀 INITIATE WEB-GROUNDED CONCURRENT CRITIC-ACTOR STRATEGY SEQUENCE", use_container_width=True):
        if not team_members_list: strl.error("❌ Array Empty: Cannot execute with no tracked personnel.")
        else:
            with strl.spinner("Parallel sub-agents tracking data vectors concurrently..."):
                try:
                    agent_res = requests.post(f"{API_BASE_URL}/agent/sprint", json={
                        "team_id": strl.session_state.team_id, "current_inventory": inventory_pool,
                        "event_details": {"event_name": event_name, "date": str(event_date), "categories": modules_selected}, "team_members": team_members_list
                    }, timeout=45)
                    if agent_res.status_code == 200:
                        strl.session_state.cached_plan = agent_res.json()["sprint_plan"]
                        strl.success("🎯 Parallel Concurrency Strategy Cycle Complete!")
                        strl.rerun()
                except Exception as ex: strl.error(f"💥 Ground Link Down: {str(ex)}")

    if strl.session_state.cached_plan:
        strl.markdown("---")
        strl.markdown("<h2>📋 COLLABORATIVE AGENT CONTEXT INSTRUCTIONS</h2>", unsafe_allow_html=True)
        raw_output = strl.session_state.cached_plan
        if "=== PROCUREMENT PROFILE ===" in raw_output:
            parts = raw_output.split("=== PROCUREMENT PROFILE ===")
            main_content = parts[1]
            if "=== DEVELOPER SPRINT BLOCKS ===" in main_content:
                inventory_block, dev_block = main_content.split("=== DEVELOPER SPRINT BLOCKS ===")
            else: inventory_block = main_content; dev_block = ""
            strl.warning("🛍️ Web-Verified Supply Logistics: Shortage Market Ingestion Pricing")
            strl.markdown(inventory_block.strip())
            if dev_block:
                strl.info("👤 Active Target Task Milestones Assigned to Human Operators")
                strl.markdown(dev_block.strip())
        else: strl.markdown(raw_output)

# ==========================================
# CENTRAL ROUTER MANAGEMENT MATRIX
# ==========================================
if not strl.session_state.authenticated and not strl.session_state.trigger_community_broadcast:
    render_authentication_gate()
elif strl.session_state.trigger_community_broadcast:
    render_authentication_gate()
else:
    strl.sidebar.markdown(f"### 🪐 ACTIVE HUD NODE")
    app_mode = strl.sidebar.selectbox("CHOOSE SYSTEM DOMAIN ROUTE", ["📋 Client Module Dashboard", "🔒 Secure Admin Portal", "🧠 Agentic Sprint Planner"])
    strl.sidebar.markdown("---")
    if strl.sidebar.button("🚨 TERMINATE ACTIVE COMMAND DISPATCH NODE", use_container_width=True):
        strl.session_state.logout_sequence = True
        strl.rerun()
    if app_mode == "📋 Client Module Dashboard": run_client_dashboard_scope()
    elif app_mode == "🔒 Secure Admin Portal": run_admin_portal_scope()
    elif app_mode == "🧠 Agentic Sprint Planner": run_agentic_planner_scope()
