# 01. Networks: Definition and Why We Study Them

## Types

- Social Networks
- Transportation and Mobility Networks
- Information Networks
- Biological Networks

- .....

## Why to Study

> Study the structure of a network can allow us to answer questions about complex phenomena

- rumor spread in network
- the most influential person
- how will a network split to two group
- virus spread
- places which are hard to reach

## What to Learn

Basic techniques to study networks

# 02. Network Definition and Vocabulary

## Network / Graph

> a representation of connections among a set of items

## Nodes / Vertices

The items

## Edges / Link / Ties

The connections

## Types of Networks

### Undirected Networks

symmetric relationships

```python
G = nx.Graph()
```

### Directed Networks

asymmetric relationships

```python
G = nx.DiGraph()
```

### Weighted Networks

### Signed Networks

### Other Edge Attributes

Edges can carry many other labels or attributes

### Multigraphs

A network where multiple edges can connect the same nodes (parallel edges).

```python
G = nx.MultiGraph()
```

# 03. Node and Edge Attributes

About using `NetworkX` library to add and get edge/node attributes.

# 04. Bipartite Graphs

## Bipartite Graphs

> A graph whose nodes can be split into two sets L and R and every edge connects an node in L with a node in R

```python
import networkx as nx
from networkx.algorithms import bipartite
B = nx.Graph()
B.add_nodes_from(['A', 'B', 'C', 'D', 'E'], bipartite=0)
B.add_nodes_from([1, 2, 3, 4], bipartite=1)
# add_edge ...
```

### Operations

Check if a gragh is bipartite

```python
bipartite.is_bipartite(B)
```

Check if a set of nodes is a bipartition of grash

```python
X = set([1,2,3,4])
bipartite.is_bipartite_node_set(B, X)
```

Getting each set of nodes of a bipartite graph

```python
bipartite.sets(B)
```

## Projected Graphs

> **L-Bipartite graph projection**: Network of nodes in group L, where a pair of nodes is connected if they have a common neighbor in R in the bipartite graph.

```python
P = bipartite.projected_graph(B, X)
```

> **L-Bipartite weighted graph projection**: An L-Bipartite graph projection with weights on the edges that are proportional to the number of common neighbors between the nodes.

```python
P = bipartite.weighted_projected_graph(B, X)
```

## Summary

- No separate class for bipartite graphs in NetworkX. Use ```Graph(), Digraph(), MultiGraph()```, etc.
- Use ```from networkx.algorithms import bipartite``` for bipartite related algorithms.
