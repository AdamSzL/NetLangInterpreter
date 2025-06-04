# ⭐ Star Topology Example

This example demonstrates how to build a **star topology** using NetLang, where a central switch is connected to multiple hosts.

## Program Description

The program constructs a hub-and-spoke network topology with the following components:

- **1 central switch** (`Hub`)
- **8 hosts** named `Host 1` to `Host 8`
- **Function** `createHost(index: int) => Host` for dynamic host generation
- **Loops** (`repeat`) for generating and connecting devices
- **Packet sending** from `Host 1` to `192.168.1.6`

## Concepts Used

- Function definitions and returns (`define`, `return`)
- Custom object initialization (`Host`, `CopperEthernetPort`, `Switch`)
- Loops: `repeat x times as index`
- Field access with list indexing (`hosts<0>.ports<0>`)
- List manipulation: `add`, indexed access
- Network instruction: `connect`, `send`

## Network Summary

Each of the 8 hosts gets assigned a unique IP address in the `192.168.1.0/24` subnet, and is connected to the central switch via dynamically created ports. Finally, a packet is sent from `Host 1` (`192.168.1.1`) to `192.168.1.6` (assumed to belong to `Host 6`).

## Code Location

You can find the full source in [`examples/star_topology.netlang`](../examples/star_topology.netlang).