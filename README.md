# 💻 HPC-Parser: Scientific Data Engine

[![C++](https://img.shields.io/badge/C++-17-00599C.svg)](https://isocpp.org/)
[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg)](https://streamlit.io/)

High-throughput data serialization engine with C++/OpenMP parallelization and Python fallback.

## 🎯 Goal
Architect a high-throughput data serializer in C++ that converts raw, sparse sensor data into optimized formats. CERN deals with petabytes of data; this demonstrates the ability to build custom, high-speed data loaders that outperform standard Python libraries—a major differentiator for GSoC mentors.

## 🛠️ Technologies
- **C++17** - Core language for performance
- **OpenMP** - Shared-memory multi-processing for parallelization
- **HDF5** - Efficient hierarchical data format (optional)
- **Python** - Fallback implementation and GUI

## 🚀 Quick Start

### Installation
```bash
pip install -r requirements.txt
```

### Compile C++ Engine (Optional)
```bash
mkdir build
cd build
cmake ..
make
```

### Run App
```bash
streamlit run app.py
```

## 📊 Performance
- **Operation**: Data transformation (v² + 0.5)
- **Parallelization**: OpenMP multi-threading
- **Fallback**: Python reference implementation if binary unavailable

## 📁 Project Structure
```
HPC-Parser/
├── app.py                  # Streamlit web interface
├── src/
│   └── engine.cpp          # C++ implementation with OpenMP
├── include/
│   └── engine.h            # Header file
├── CMakeLists.txt          # Build configuration
├── dummy_data.txt          # Sample input data
├── requirements.txt        # Python dependencies
└── README.md
```

## 🔒 Security Features
- **Path Validation**: Prevents directory traversal attacks
- **Input Sanitization**: Regex validation for filenames
- **Subprocess Safety**: Timeout protection (30s limit)
- **No User Input in Commands**: Prevents injection attacks

## 🎨 Features
- Interactive data editing
- Real-time processing visualization
- C++ engine with automatic Python fallback
- Input vs. output signal comparison plot

## 🔬 How It Works
1. **Input**: User edits sensor data in text area
2. **Processing**: 
   - Attempts to run compiled C++ binary (if available)
   - Falls back to Python implementation (real computation, not mock)
3. **Transformation**: Applies v² + 0.5 to each value
4. **Visualization**: Plots original vs. processed signals

## 🔗 Relevance to ML4SCI/CERN
Demonstrates expertise in:
- High-performance C++ programming
- Parallel processing with OpenMP
- Data serialization and optimization
- Python/C++ integration
- Security-hardened code practices
