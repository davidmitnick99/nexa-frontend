import streamlit as strl
import requests

# 🎨 Match branding styles with custom page layout configuration
strl.set_page_config(page_title="Nexa Core Production Gateway", layout="wide")

API_BASE_URL = "https://nexa-backend-tuhl.onrender.com"

strl.title("🤖 Nexa Core Production Gateway")
strl.caption("Autonomous Systems Management Interface | Team Nexus Cloud Network")
strl.markdown("---")

# 🧭 High-level application navigation tabs
app_mode = strl.sidebar.selectbox("Select Workspace Domain", ["📋 Client Module Dashboard", "🔒 Secure Admin Portal"])

if app_mode == "📋 Client Module Dashboard":
    strl.sidebar.header("Module Navigation")
    target_module = strl.sidebar.selectbox("Active Blueprint Filter", ["Sumo Robot", "RC Car"])
    
    if strl.sidebar.button("Fetch Live Cluster Data"):
        strl.rerun()

    with strl.spinner(f"Synchronizing with Render cloud node for '{target_module}'..."):
        try:
            response = requests.get(f"{API_BASE_URL}/modules/{target_module}", timeout=7)
            if response.status_code == 200:
                module_data = response.json()
                
                # Split workspace cleanly into 2 columns
                left_col, right_col = strl.columns([1, 1.2])
                
                with left_col:
                    strl.markdown("### 🔌 System Circuit Topology")
                    image_url = module_data.get("circuit_diagram_url")
                    if image_url and image_url.startswith("http"):
                        strl.image(image_url, caption=f"Official {target_module} Schematic Matrix", use_container_width=True)
                    else:
                        strl.info("No external schematic vector files linked.")
                    
                    # Technical specification parameters parsing
                    if "specs" in module_data:
                        strl.markdown("#### ⚙️ Hardware Specifications")
                        for spec, val in module_data["specs"].items():
                            strl.write(f"**{spec}:** {val}")

                with right_col:
                    strl.markdown("### 💰 Component Budget Configuration")
                    if "budget" in module_data:
                        total_pkr = sum(int(item['cost_pkr']) for item in module_data['budget'])
                        strl.dataframe(module_data["budget"], use_container_width=True)
                        strl.metric(label="Calculated Modules Production Cost", value=f"{total_pkr:,} PKR")
                    
                    # Code Blocks Compilation
                    if "firmware" in module_data:
                        strl.markdown("### 💻 Embedded Architecture Code")
                        strl.code(module_data["firmware"], language="cpp")
            else:
                strl.error(f"⚠️ Error {response.status_code}: Unable to load profile parameters.")
        except Exception as e:
            strl.error(f"❌ Cloud synchronization failure: {str(e)}")

elif app_mode == "🔒 Secure Admin Portal":
    strl.markdown("## 🔒 Nexus Core Management Administration Console")
    
    # 🔐 Protection Security Gate
    access_token = strl.text_input("Enter Production Authorization Token", type="password")
    
    if access_token == "NEXUS_ADMIN_2026":
        strl.success("🔐 Security Handshake Approved. Input parameters below to write data:")
        strl.markdown("---")
        
        with strl.form("new_module_form", clear_on_submit=True):
            mod_name = strl.text_input("Module Name (e.g., Robo Soccer, Drone)")
            diag_url = strl.text_input("Raw GitHub Image URL (circuit_diagram_url)")
            
            strl.markdown("#### ⚙️ Core Technical Specifications")
            chassis = strl.text_input("Chassis / Frame Body")
            mcu = strl.text_input("Microcontroller Model")
            motors = strl.text_input("Actuators / Motors Array")
            drivers = strl.text_input("Motor Driver Modules")
            sensors = strl.text_input("Sensors Array Configuration")
            
            strl.markdown("#### 💰 Budget Parameters (Top 3 Essential Core Items)")
            item1 = strl.text_input("Component Item 1 Description")
            cost1 = strl.number_input("Item 1 Cost (PKR)", min_value=0, value=0, step=50)
            
            item2 = strl.text_input("Component Item 2 Description")
            cost2 = strl.number_input("Item 2 Cost (PKR)", min_value=0, value=0, step=50)
            
            item3 = strl.text_input("Component Item 3 Description")
            cost3 = strl.number_input("Item 3 Cost (PKR)", min_value=0, value=0, step=50)
            
            strl.markdown("#### 💻 Target Firmware Microcode Block")
            firmware_code = strl.text_area("Paste C++ Arduino/ESP32 Script Memory Matrix", height=200)
            
            submit_btn = strl.form_submit_button("🚀 Broadcast Module Blueprint to Cloud")
            
            if submit_btn:
                if not mod_name or not diag_url:
                    strl.error("❌ Critical fields missing: Module Name and Diagram URL are strictly required.")
                else:
                    # Constructing the payload schema mapping directly to Pydantic requirements
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
                        "budget": [
                            {"item": item1, "cost_pkr": str(cost1)},
                            {"item": item2, "cost_pkr": str(cost2)},
                            {"item": item3, "cost_pkr": str(cost3)}
                        ],
                        "firmware": firmware_code
                    }
                    
                    with strl.spinner("Transmitting encrypted stream to cloud data center..."):
                        try:
                            write_response = requests.post(f"{API_BASE_URL}/modules/add", json=payload_package, timeout=10)
                            if write_response.status_code == 200:
                                strl.success(f"🎉 Success! {write_response.json()['message']}")
                            else:
                                strl.error(f"❌ Write operation rejected: {write_response.json().get('detail', 'Unknown database constraint violation.')}")
                        except Exception as write_err:
                            strl.error(f"💥 Network transport execution failure: {str(write_err)}")
    elif access_token != "":
        strl.error("🛑 ACCESS DENIED: Invalid Security Authorization Token.")
