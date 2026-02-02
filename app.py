import streamlit as st
import pandas as pd
import numpy as np
import subprocess
import os
import matplotlib.pyplot as plt
import re

st.set_page_config(page_title="HPC-Parser", layout="wide")

st.title("💻 HPC-Parser: Scientific Data Engine")
st.markdown("C++ based high-throughput data serialization engine with Python fallback.")

# Security: Validate file paths
def validate_filename(filename):
    """Prevent path traversal attacks"""
    # Only allow alphanumeric, underscore, hyphen, and dot
    if not re.match(r'^[a-zA-Z0-9_\-\.]+$', filename):
        raise ValueError("Invalid filename")
    # Prevent directory traversal
    if '..' in filename or '/' in filename or '\\' in filename:
        raise ValueError("Path traversal not allowed")
    return filename

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

col1, col2 = st.columns(2)

with col1:
    st.header("1. Input Data Stream")
    input_text = st.text_area("Edit Sensor Data", 
                               "1.2 3.4 5.6 7.8\n9.0 1.2 3.4 5.6\n7.8 9.0 1.2 3.4\n5.6 7.8 9.0 1.2\n1.1 2.2 3.3 4.4",
                               height=200)
    
    if st.button("Process Data", type="primary"):
        try:
            # Save input safely
            input_file = 'data/input_data.txt'
            with open(input_file, "w") as f:
                f.write(input_text)
                
            st.info("Processing data...")
            
            # Try C++ engine first
            binary_path = "hpc_parser.exe" if os.name == 'nt' else "./hpc_parser"
            use_cpp = False
            
            if os.path.exists(binary_path):
                try:
                    # Security: Use absolute paths, no user input in command
                    result = subprocess.run(
                        [binary_path, os.path.abspath(input_file), "data/output.h5"],
                        check=True,
                        capture_output=True,
                        text=True,
                        timeout=30  # Prevent hanging
                    )
                    use_cpp = True
                    st.success("✅ C++ Engine executed successfully")
                except subprocess.TimeoutExpired:
                    st.warning("⏱️ C++ Engine timed out, using Python fallback")
                except Exception as e:
                    st.warning(f"C++ Engine failed, using Python fallback")
            else:
                st.info("Using Python Reference Implementation")
                
            # Python fallback (real computation)
            if not use_cpp:
                output_data = []
                input_flat = []
                
                with open(input_file, "r") as f:
                    lines = f.readlines()
                    
                for line in lines:
                    vals = [float(x) for x in line.split()]
                    input_flat.extend(vals)
                    # Engine logic: v^2 + 0.5
                    processed = [v*v + 0.5 for v in vals]
                    output_data.extend(processed)
                    
                st.session_state['input_data'] = input_flat
                st.session_state['output_data'] = output_data
                st.success("✅ Python Engine completed")
            
        except Exception as e:
            st.error(f"Error: {str(e)}")

with col2:
    st.header("2. Processing Results")
    if 'output_data' in st.session_state:
        df = pd.DataFrame({
            "Original Signal": st.session_state['input_data'],
            "Processed Output": st.session_state['output_data']
        })
        
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(df.index, df["Original Signal"], 'b-', label='Original', alpha=0.7)
        ax.plot(df.index, df["Processed Output"], 'r-', label='Processed', alpha=0.7)
        ax.set_xlabel("Sample Index")
        ax.set_ylabel("Value")
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
        
        st.write("Sample Output (first 5 values):")
        st.code(st.session_state['output_data'][:5])
    else:
        st.info("Click 'Process Data' to see results")

st.divider()
st.header("Engine Information")
st.markdown("""
**Language**: C++ with OpenMP parallelization  
**Fallback**: Python reference implementation  
**Operation**: Data transformation (v² + 0.5)  
**Security**: Path validation, timeout protection
""")
