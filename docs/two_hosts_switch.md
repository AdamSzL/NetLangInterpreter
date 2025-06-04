# Example: Two Hosts and a Switch

This example demonstrates a very simple local network setup using NetLang. It includes two hosts connected to a single switch. Each host uses a different Ethernet port type to illustrate type constraints in port connectivity.

---

## Purpose

This program showcases:
- Basic object instantiation (`Host`, `Switch`, `OpticalEthernetPort`, `CopperEthernetPort`)
- Port type compatibility checks
- Connecting devices using `connect`
- Sending a packet using `send`
- Minimal local communication scenario

---

## Code Structure

- **Host A** is equipped with an `OpticalEthernetPort` and assigned IP `192.168.1.0/24`.
- **Host B** uses a `CopperEthernetPort` and is also assigned `192.168.1.1/24`.
- **Switch** includes two ports, one optical and one copper.

The switch connects each host on its respective port, and Host A sends a message to Host B via IP `192.168.1.1`.

---

## Key Language Features Used

- Object initialization with required fields
- Mixing different port types (to test compatibility)
- Field access via dot and list indexing
- The `connect` instruction
- The `send` instruction to simulate packet transmission and trigger visualization

---

## Sample Output

Running this program in the interpreter should:
- Connect devices only if port types match (optical to optical, copper to copper)
- Show the packet being sent from Host A to Host B
- Animate the flow on the network graph
- Display logs with connection and delivery status