# nMapper

This network mapping tool designed to visualize connected devices and their relationships within a network. It provides a user-friendly interface for inputting network data and generating visual maps that accurately represent the layout of a network. The tool supports complex network structures and allows customization of the map's appearance.

# RECON WorkFlow Block
![FlowDiagram](https://github.com/zaidbinkokab/nMapper/assets/57888815/3590ca4b-77b5-40e0-8683-a8e0c1f923c2)

## Key Features:
## Network Discovery: 
Scan a subnet to discover connected devices and gather information about their IP and MAC addresses.
## Visual Mapping: 
Generate visual maps that display the connections between devices and their relationships in a clear and organized manner.
## Customization: 
Customize the appearance of the network map, including node colors, sizes, and labels.
## Export Functionality: 
Export the network map in various formats (e.g., PNG, PDF) for further analysis and documentation.
## Network Optimization: 
Identify potential vulnerabilities, optimize network performance, and troubleshoot connectivity issues using detailed device information.

# Installation
Follow these steps to set up and run the nMapper application on your local machine:

## Prerequisites
Python 3 installed on your system. You can download Python from the official Python website.

## Clone the Repository
Open your terminal (Command Prompt on Windows, Terminal on macOS/Linux).
Navigate to the directory where you want to clone the repository.

Run the following command to clone the repository:
``` git clone https://github.com/zaidbinkokab/nMapper.git ```

## Install Dependencies
Navigate to the cloned repository's directory:

``` cd nMapper ```

## Install the required Python dependencies using pip:
``` pip install -r requirements.txt ```

### Run the Application
After installing the dependencies, you can run the application using the following command:

``` python3 main.py ```

The application's GUI window should open, allowing you to interact with the nMapper tool.

## How to Use:
Input the subnet or IP address of the network you want to scan.<br>
Click the "Scan Subnet" button to discover connected devices.<br>
Visualize the network map to see device connections and relationships. <br>
Customize the map appearance and export it for further analysis and documentation.<br>

## Dependencies:

Python 3.x <br>
tkinter <br>
networkx <br>
matplotlib <br>
scapy <br>

## Usage:
Clone the repository and run the main.py file to launch the network mapping tool.

## Contributing:
Contributions are welcome! Feel free to open issues or pull requests for any enhancements or bug fixes you'd like to see in the project.

## License:
This project is licensed under the GNU GENERAL PUBLIC LICENSE - see the LICENSE file for details.
