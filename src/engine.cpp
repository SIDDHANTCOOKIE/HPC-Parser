#include "engine.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <omp.h>
#include <vector>

// Mock HDF5 includes if not present, but structure assumes they would be used
// #include "H5Cpp.h" 

DataEngine::DataEngine(const std::string& input_file, const std::string& output_file) 
    : input_path(input_file), output_path(output_file) {}

std::vector<double> DataEngine::parse_line(const std::string& line) {
    std::vector<double> values;
    std::stringstream ss(line);
    double val;
    while (ss >> val) {
        values.push_back(val);
    }
    // Simulate complex calculation
    for(auto& v : values) {
        v = v * v + 0.5; 
    }
    return values;
}

void DataEngine::save_batch(const std::vector<std::vector<double>>& data) {
    // In a real scenario, H5Cpp calls would go here.
    // e.g. H5::H5File file(output_path, H5F_ACC_TRUNC);
    std::cout << "[HDF5] Saving batch of size " << data.size() << " to " << output_path << std::endl;
}

void DataEngine::run() {
    std::ifstream file(input_path);
    std::vector<std::string> lines;
    std::string line;
    
    // 1. Read Raw Data
    if (file.is_open()) {
        while (getline(file, line)) {
            lines.push_back(line);
        }
        file.close();
    } else {
        std::cerr << "Unable to open file" << std::endl;
        return;
    }

    std::cout << "Read " << lines.size() << " lines. Processing with OpenMP..." << std::endl;

    std::vector<std::vector<double>> processed_data(lines.size());

    // 2. Parallel Processing
    #pragma omp parallel for schedule(dynamic)
    for (size_t i = 0; i < lines.size(); ++i) {
        processed_data[i] = parse_line(lines[i]);
        
        // Debug info from threads
        // #pragma omp critical
        // std::cout << "Thread " << omp_get_thread_num() << " processed line " << i << std::endl;
    }

    // 3. Serialize
    save_batch(processed_data);
    std::cout << "Processing Complete." << std::endl;
}

int main(int argc, char** argv) {
    if (argc < 3) {
        std::cout << "Usage: ./hpc_parser <input.txt> <output.h5>" << std::endl;
        return 1;
    }
    
    DataEngine engine(argv[1], argv[2]);
    engine.run();
    
    return 0;
}
