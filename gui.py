import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from scapy.all import get_if_addr, get_if_hwaddr, ARP, Ether, srp
from tkinter import simpledialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class NetworkMappingApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.devices = {}  # Dictionary to store device information
        self.connections = []  # List to store connection information
        self.create_widgets()
        
    def create_widgets(self):
        # Welcome Banner with ASCII art
                welcome_ascii = """
        =================================================================;=========
        ##::: ##:'##::::'##::::'###::::'########::'########::'########:'########::
        ###:: ##: ###::'###:::'## ##::: ##.... ##: ##.... ##: ##.....:: ##.... ##:
        ####: ##: ####'####::'##:. ##:: ##:::: ##: ##:::: ##: ##::::::: ##:::: ##:
        ## ## ##: ## ### ##:'##:::. ##: ########:: ########:: ######::: ########::
        ##. ####: ##. #: ##: #########: ##.....::: ##.....::: ##...:::: ##.. ##:::
        ##:. ###: ##:.:: ##: ##.... ##: ##:::::::: ##:::::::: ##::::::: ##::. ##::
        ##::. ##: ##:::: ##: ##:::: ##: ##:::::::: ##:::::::: ########: ##:::. ##:
        ..::::..::..:::::..::..:::::..::..:::::::::..:::::::::........::..:::::..::
        ===============;============================================================
                                Designed and Developed by Zaid ©
        -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

        """
                welcome_label = tk.Label(self, text=welcome_ascii, font=("Courier", 10))
                welcome_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

                # Machine's IP and MAC Address
                ip_address = get_if_addr("eth0")  # Change "eth0" to the appropriate interface name
                mac_address = get_if_hwaddr("eth0")  # Change "eth0" to the appropriate interface name

                machine_info_label = tk.Label(self, text=f"Your IP Address: {ip_address}, MAC Address: {mac_address}")
                machine_info_label.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 10))

                # Subnet Input Field
                self.subnet_label = tk.Label(self, text="Enter Subnet or IP Address:")
                self.subnet_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
                self.subnet_entry = tk.Entry(self)
                self.subnet_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

                # Scan Button
                self.scan_button = tk.Button(self, text="Scan Subnet", command=self.scan_and_visualize)
                self.scan_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

                # Network Graph Canvas
                self.canvas = tk.Canvas(self, width=800, height=600)
                self.canvas.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

                # IP and MAC Address Table
                self.table_label = tk.Label(self, text="IP and MAC Address Table:")
                self.table_label.grid(row=5, column=0, columnspan=2, padx=10, pady=(20, 5))

                self.tree = ttk.Treeview(self, columns=("IP Address", "MAC Address"), show="headings")
                self.tree.heading("IP Address", text="IP Address")
                self.tree.heading("MAC Address", text="MAC Address")
                self.tree.grid(row=6, column=0, columnspan=2, padx=10, pady=(0, 20))

    def scan_and_visualize(self):
        # Get IP address from the entry field
        ip_address = self.subnet_entry.get()

        if ip_address:
            # Determine the subnet mask based on the IP address
            subnet = ip_address.split('.')
            subnet[-1] = '0'
            subnet = '.'.join(subnet) + '/24'  # Assuming a /24 subnet mask

            # Perform network scanning to discover hosts on the subnet
            hosts = self.scan_subnet(subnet)
            print("Discovered hosts:", hosts)  # Debug print

            # Add discovered hosts to the devices dictionary
            for host in hosts:
                self.devices[host] = {"ip_address": host, "mac_address": ""}
            print("Updated devices:", self.devices)  # Debug print

            # Visualize the updated network graph
            self.visualize_network(ip_address)

    def visualize_network(self, current_machine_ip):
        # Create a directed graph
        G = nx.DiGraph()

        # Add current machine as a node
        G.add_node(current_machine_ip, ip_address=current_machine_ip, device_type="Current Machine")

        # Add other devices as nodes
        for device, info in self.devices.items():
            if device != current_machine_ip and not device.endswith('.0') and not device.endswith('.255') and not device.endswith('.2') and not device.endswith('.254'):
                G.add_node(device, **info)

        # Add connections as edges
        for connection in self.connections:
            from_device, to_device, connection_type = connection
            if from_device in G.nodes and to_device in G.nodes:
                G.add_edge(from_device, to_device, connection_type=connection_type)

        # Calculate the positions of nodes
        pos = nx.spring_layout(G)

        # Set the position of the current machine
        pos[current_machine_ip] = [0, 0]  # Place the current machine at the center

        # Visualize the network graph
        nx.draw(G, pos, with_labels=True, node_color="skyblue", node_size=1000, font_size=10, font_weight="bold")
        plt.title("Network Topology")

        # Display the plot
        plt.show()


        # Update IP and MAC Address Table
        self.update_table()

    def update_table(self):
        # Clear the table
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Add IP and MAC addresses to the table
        for device, info in self.devices.items():
            ip_address = info.get("ip_address", "")
            mac_address = info.get("mac_address", "")
            self.tree.insert("", "end", values=(ip_address, mac_address))
            
        # Visualize the updated network graph
        self.visualize_network()
    def scan_subnet(self, subnet):
        arp = ARP(pdst=subnet)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether / arp
        result = srp(packet, timeout=3, verbose=False)[0]

        hosts = []
        for sent, received in result:
            ip_address = received.psrc
            mac_address = received.hwsrc
            hosts.append(ip_address)
            # Populate devices dictionary with MAC addresses
            self.devices[ip_address] = {"ip_address": ip_address, "mac_address": mac_address}
        return hosts
