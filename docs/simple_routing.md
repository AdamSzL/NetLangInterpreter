# Example: Simple Routing

This example demonstrates a more complex network setup that includes:
- A single central router with 3 ports connected to 3 switches.
- Each switch is connected to two separate hosts.
- Routing is handled via static routes configured in the router.

The program uses:
- `define` statements to encapsulate logic for creating switches and hosts.
- Custom loops (`repeat x times`) to dynamically construct parts of the topology.
- Field access and list operations to properly assign and connect components.
- The `connect` instruction to establish links between ports.
- The `send` instruction to simulate packet transmission.

## Objective

The goal of this example is to demonstrate:
- The use of nested loops and abstractions to model repetitive structure.
- The role of the router in forwarding packets between subnets using defined routing rules.
- How subnets are allocated to different host pairs and connected via switches to the router.

## Highlights

- The router has three interfaces: `192.168.1.1`, `192.168.2.1`, and `192.168.3.1`, each for one subnet.
- A default route (`0.0.0.0/0`) is defined in the router’s routing table, pointing to `eth2`.
- Each switch connects to a different router port and serves two hosts.
- Hosts are configured dynamically using parameterized functions.
- One host sends a message to another host across subnets, requiring correct forwarding through the router.

See the source file for full implementation: [`examples/simple_routing.netlang`](../examples/simple_routing.netlang)
