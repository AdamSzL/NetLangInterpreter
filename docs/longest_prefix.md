# Longest Prefix Matching Example

This example demonstrates how **longest prefix matching** is used when forwarding packets between networks. In this scenario, a single router is configured with multiple routing entries, and the packet forwarding logic must choose the route with the most specific match (i.e., the longest prefix).

## Purpose

The goal of this example is to showcase how the routing logic in NetLang prefers more specific CIDR routes over less specific ones, even if multiple entries match the destination.

## Concepts Covered

* Longest prefix match in routing
* Host and Router device configuration
* Dynamic list construction
* Packet sending and forwarding across multiple subnets

## Program Overview

* **Three hosts** are dynamically created, each with two ports (eth0 and eth1). Each port is assigned an IP and gateway.
* A **router** (`R1`) is defined with three ports, each connected to a different subnet.
* The router's `routingTable` contains two entries:

  * `172.16.0.0/16` via `eth1`
  * `172.16.1.0/24` via `eth2`
* Because `172.16.1.100` belongs to both subnets, the router should forward the packet via `eth2`, since `172.16.1.0/24` is more specific than `172.16.0.0/16`.

## Key Snippet

```netlang
send "Hello" from hosts<0>.ports<0> to 172.16.1.100
```

This line sends a packet that will match both routing entries, but should ultimately be routed via `eth2` due to longest prefix match logic.

## Features Used

* `repeat x times as index` loop
* List indexing (`hosts<0>`, `subnets<index>`, etc.)
* Object instantiation with parameters
* `add` expression to build lists
* `connect` and `send` networking instructions

## 🗂 Related File

The full source code can be found in [`examples/longest_prefix.netlang`](../examples/longest_prefix.netlang)