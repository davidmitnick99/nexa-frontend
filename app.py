import streamlit as strl
import requests

strl.set_page_config(page_title="Nexa Core Production Gateway", layout="wide")

API_BASE_URL = "https://nexa-backend-tuhl.onrender.com"

strl.title("🤖 Nexa Core Production Gateway")
strl.caption("Autonomous Systems Management Interface | Team Nexus Cloud Network")
strl.markdown("---")

app_mode = strl.sidebar.selectbox("Select Workspace Domain", ["📋 Client Module Dashboard", "🔒 Secure Admin Portal"])

if app_mode == "📋 Client Module Dashboard":
    strl.sidebar.header("Module Navigation")
    target_module = strl.sidebar.selectbox("Active Blueprint Filter", ["Sumo Robot", "RC Car", "Robo Soccer"])
    
    if strl.sidebar.button("Fetch Live Cluster Data"):
        strl.rerun()

    with strl.spinner(f"Synchronizing with Render cloud node for '{target_module}'..."):
        try:
            response = requests.get(f"{API_BASE_URL}/modules/{target_module}", timeout=7)
            if response.status_code == 200:
                module_data = response.json()
                
                left_col, right_col = strl.columns([1, 1.2])
                
                with left_col:
                    strl.markdown("### 🔌 System Circuit Topology")
                    image_url = module_data.get("circuit_diagram_url")
                    if image_url and image_url.startswith("http"):
                        strl.image(image_url, caption=f"Official {target_module} Schematic Matrix", use_container_width=True)
                    else:
                        strl.info("No external schematic vector files linked.")
                    
                    if "specs" in module_data:
                        strl.markdown("#### ⚙️ Hardware Specifications")
                        for spec, val in module_data["specs"].items():
                            if val: # Only show if not blank
                                strl.write(f"**{spec}:** {val}")

                with right_col:
                    strl.markdown("### 💰 Component Budget Configuration")
                    if "budget" in module_data and module_data["budget"]:
                        # Filter out empty entries from display
                        clean_budget = [item for item in module_data["budget"] if item.get('item')]
                        if clean_budget:
                            total_pkr = sum(int(item['cost_pkr']) for item in clean_budget if item['cost_pkr'].isdigit())
                            strl.dataframe(clean_budget, use_container_width=True)
                            strl.metric(label="Calculated Modules Production Cost", value=f"{total_pkr:,} PKR")
                        else:
                            strl.info("No components listed for this module.")
                    
                    if "firmware" in module_data:
                        strl.markdown("### 💻 Embedded Architecture Code")
                        strl.code(module_data["firmware"], language="cpp")
            else:
                strl.error(f"⚠️ Error {response.status_code}: Unable to load profile parameters.")
        except Exception as e:
            strl.error(f"❌ Cloud synchronization failure: {str(e)}")

elif app_mode == "🔒 Secure Admin Portal":
    strl.markdown("## 🔒 Nexus Core Management Administration Console")
    
    access_token = strl.text_input("Enter Production Authorization Token", type="password")
    
    if access_token == "NEXUS_ADMIN_2026":
        strl.success("🔐 Security Handshake Approved.")
        strl.markdown("---")
        
        # Initialize component list in session state if it doesn't exist
        if "component_count" not in strl.session_state:
            strl.session_state.component_count = 3  # Starts with 3 rows by default

        mod_name = strl.text_input("Module Name (e.g., Robo Soccer, Drone)")
        diag_url = strl.text_input("Raw GitHub Image URL (circuit_diagram_url)")
        
        strl.markdown("#### ⚙️ Core Technical Specifications")
        chassis = strl.text_input("Chassis / Frame Body")
        mcu = strl.text_input("Microcontroller Model")
        motors = strl.text_input("Actuators / Motors Array")
        drivers = strl.text_input("Motor Driver Modules")
        sensors = strl.text_input("Sensors Array Configuration")
        
        strl.markdown("#### 💰 Dynamic Budget Parameters")
        
        budget_list = []
        # Dynamically loop and build input rows
        for i in range(strl.session_state.component_count):
            c1, c2 = strl.columns([2, 1])
            with c1:
                item_name = strl.text_input(f"Component {i+1} Name", key=f"item_{i}")
            with c2:
                item_cost = strl.number_input(f"Cost (PKR)", min_value=0, step=50, key=f"cost_{i}")
            
            if item_name:
                budget_list.append({"item": item_name.strip(), "cost_pkr": str(int(item_cost))})

        # Buttons to dynamically add/remove items rows instantly
        b1, b2, _ = strl.columns([1, 1, 3])
        with b1:
            if strl.button("➕ Add Component Row"):
                strl.session_state.component_count += 1
                strl.rerun()
        with b2:
            if strl.button("➖ Remove Row") and strl.session_state.component_count > 1:
                strl.session_state.component_count -= 1
                strl.rerun()

        strl.markdown("#### 💻 Target Firmware Microcode Block")
        firmware_code = strl.text_area("Paste C++ Arduino/ESP32 Script Memory Matrix", height=200)
        
        # Final Broadcast submission button
        if strl.button("🚀 Broadcast Module Blueprint to Cloud"):
            if not mod_name or not diag_url:
                strl.error("❌ Critical fields missing: Module Name and Diagram URL are strictly required.")
            else:
                payload_package = {
                    "module_name": mod_name.strip(),
                    "circuit_diagram_url": diag_url.strip(),
                    "specs": {
                        "Chassis": chassis,
                        "Microcontroller": mcu,
                        "Motors": motors,
                        "Motor Driver": drivers,
                        "Sensors": sensors
                    },
                    "budget": budget_list,
                    "firmware": firmware_code
                }
                
                with strl.spinner("Transmitting encrypted stream to cloud data center..."):
                    try:
                        write_response = requests.post(f"{API_BASE_URL}/modules/add", json=payload_package, timeout=10)
                        if write_response.status_code == 200:
                            strl.success(f"🎉 Success! {write_response.json()['message']}")
                        else:
                            strl.error(f"❌ Write operation rejected: {write_response.json().get('detail', 'Error parsing fields.')}")
                    except Exception as write_err:
                        strl.error(f"💥 Network transport execution failure: {str(write_err)}")
                        
    elif access_token != "":
        strl.error("🛑 ACCESS DENIED: Invalid Security Authorization Token.")
