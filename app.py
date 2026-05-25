import streamlit as strl
import requests
import pandas as pd

strl.set_page_config(page_title="Nexa Core Production Gateway", layout="wide")
API_BASE_URL = "https://nexa-backend-tuhl.onrender.com"

strl.title("🤖 Nexa Core Production Gateway")
strl.markdown("---")

app_mode = strl.sidebar.selectbox("Select Workspace Domain", ["📋 Client Module Dashboard", "🔒 Secure Admin Portal"])

if app_mode == "📋 Client Module Dashboard":
    target_module = strl.sidebar.selectbox("Active Blueprint Filter", ["Sumo Robot", "RC Car", "Robo Soccer"])
    
    with strl.spinner("Synchronizing..."):
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
                            strl.write(f"**{spec}:** {val}")

                with right_col:
                    strl.markdown("### 💰 Component Budget Configuration")
                    if "budget" in module_data and module_data["budget"]:
                        # Convert to DataFrame and compute dynamic mathematical totals
                        df = pd.DataFrame(module_data["budget"])
                        df['Total (PKR)'] = df['quantity'].astype(int) * df['unit_cost_pkr'].astype(int)
                        
                        # Rename columns elegantly for presentation
                        df.columns = ['Component Item', 'Qty', 'Unit Cost (PKR)', 'Total Subtotal (PKR)']
                        strl.dataframe(df, use_container_width=True, hide_index=True)
                        
                        grand_total = df['Total Subtotal (PKR)'].sum()
                        strl.metric(label="Calculated Grand Production Cost", value=f"{grand_total:,} PKR")
                    
                    if "firmware" in module_data:
                        strl.markdown("### 💻 Embedded Architecture Code")
                        strl.code(module_data["firmware"], language="cpp")
        except Exception as e:
            strl.error(f"Cloud synchronization failure: {str(e)}")

elif app_mode == "🔒 Secure Admin Portal":
    strl.markdown("## 🔒 Secure Admin Portal")
    access_token = strl.text_input("Enter Production Authorization Token", type="password")
    
    if access_token == "NEXUS_ADMIN_2026":
        if "rows" not in strl.session_state:
            strl.session_state.rows = 4 # Starts with 4 slots for components

        mod_name = strl.text_input("Module Name")
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
                it_name = strl.text_input(f"Item {i+1} Description (e.g. N20 Motors, Chassis)", key=f"name_{i}")
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
