# 🌐 Example: Complex Network

This program sets up a **multi-router network topology** using the NetLang language. It demonstrates:
- Creation of multiple routers and hosts
- Port assignment with IP addresses and gateways
- Definition of routing tables using `RoutingEntry`
- Establishing network connections with `connect`
- Sending a packet from one host to another using `send`

---

## 🧠 Description

The network consists of:
- Three routers: `r1` (central), `r2`, and `r3`
- Two hosts: `hostA` and `hostB`, each located in different subnets
- Connections between routers and hosts forming a multi-path topology

The routers use **routing tables** to forward packets across the network. `hostA` sends a message to `hostB`, and the system automatically routes it through the correct intermediary routers based on IP addressing.

---

## 🧰 Language Features Used

- Object initialization (e.g. `Router`, `Host`, `CopperEthernetPort`)
- Lists and field access (e.g. `ports<0>`)
- `connect` and `send` instructions for networking
- Static routing using `routingTable`
- IP and CIDR types

---

## 📤 Program Behavior

The following actions take place:

1. Three routers are created with two ports each, connecting three different subnets:
   - `r1`: 10.0.1.0/24 and 10.0.2.0/24
   - `r2`: 10.0.1.0/24 and 10.0.3.0/24
   - `r3`: 10.0.2.0/24 and 10.0.4.0/24

2. Hosts are assigned to:
   - `hostA` → subnet 10.0.3.0/24
   - `hostB` → subnet 10.0.4.0/24

3. Routers are connected and routing tables configured to allow cross-subnet communication.

4. The command:
   ```netlang
   send "Hello from Host A!" from hostA.ports<0> to 10.0.4.2
   ```
   triggers routing through multiple routers, ultimately delivering the message to `hostB`.

---

## 🗂 Related File

The full source code can be found in [`examples/complex_network.netlang`](../examples/complex_network.netlang)
