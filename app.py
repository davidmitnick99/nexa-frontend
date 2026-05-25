import streamlit as strl
import requests

strl.set_page_config(
    page_title="Nexa Core | Robotics Control Dashboard",
    page_icon="🤖",
    layout="wide"
)

# FIXED PERMANENT RENDER LINK
BACKEND_URL = "https://nexa-backend-tuhl.onrender.com"

strl.title("🤖 Nexa Core Gateway")
strl.subheader("Team Nexus Global Blueprint Ecosystem")
strl.markdown("---")

strl.sidebar.header("🕹️ Module Navigation")
target_module = strl.sidebar.selectbox(
    "Choose Robotics Blueprint:",
    ["Sumo Robot", "RC Car"]
)

strl.sidebar.markdown("---")
strl.sidebar.success("🟢 Connected Live to Render Cloud Node")

try:
    with strl.spinner(f"Querying cloud node for '{target_module}' matrices..."):
        api_endpoint = f"{BACKEND_URL}/modules/{target_module.replace(' ', '%20')}"
        response = requests.get(api_endpoint, timeout=15)
        
    if response.status_code == 200:
        module_data = response.json()
        
        col1, col2 = strl.columns(2)
        with col1:
            strl.metric(label="Active Module Profile", value=module_data.get("module_name"))
        with col2:
            raw_cost = str(module_data.get("estimated_total_pkr", "0"))
            formatted_cost = f"{int(raw_cost):,}" if raw_cost.isdigit() else raw_cost
            strl.metric(label="Estimated Allocation Cost", value=f"PKR {formatted_cost}")
            
        strl.markdown("### 🛠️ Required Hardware Components")
        components_list = module_data.get("required_components", [])
        if components_list:
            formatted_components = []
            for item in components_list:
                formatted_components.append({
                    "Component Designation": item.get("name", "Unknown Component"),
                    "Quantity Required": item.get("quantity", "1"),
                    "Est. Unit Cost (PKR)": f"{int(str(item.get('est_price_pkr', 0))):,}" if str(item.get('est_price_pkr', '')).isdigit() else "0"
                })
            strl.table(formatted_components)
        else:
            strl.warning("No discrete components allocations recorded.")
            
        strl.markdown("---")
        left_col, right_col = strl.columns([1, 1])
        
        with left_col:
            strl.markdown("### 🔌 System Circuit Topology")
            image_url = module_data.get("circuit_diagram_url")
            if image_url and image_url.startswith("http"):
                strl.image(image_url, caption=f"Official {target_module} Schematic Matrix", use_container_width=True)
            else:
                strl.info("No external schematic vector files linked.")
                
        with right_col:
            strl.markdown("### 💻 Embedded Firmware Blueprint")
            code_snippet = module_data.get("base_code_snippet", "")
            if code_snippet:
                strl.code(code_snippet, language="cpp")
            else:
                strl.info("No deployment microcontroller firmware uploaded.")
    else:
        strl.error(f"❌ Cloud Backend Alert: Returned Status Code {response.status_code}")
        
except requests.exceptions.RequestException as e:
    strl.error("⚠️ Communication Loop Interrupted")
    strl.markdown("Free cloud instances go to sleep when idle. Give Render 30 seconds to wake up and refresh your browser tab!")
