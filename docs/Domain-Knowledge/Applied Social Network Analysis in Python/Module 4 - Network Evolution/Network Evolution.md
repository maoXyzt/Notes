# 01. Preferential Attachment Model

## Degree Distributions

The probability distribution of the degrees over the entire network.

```python
G.degree()
```

In-Degree Distributions

```python
G.in_degree()
```

### Degree Distributions in Real Networks

Degree distribution look like a straight line when on a log-log scale.

Power law:
$$
P(k) = Ck^{-\alpha},\ \text{where}\ C\ \text{and}\ \alpha\ \text{are constants}
$$

## Preferential Attachment Model

- Start with two nodes connected by an edge.

- At each time step, add a new node with an edge connecting it to an existing node.

- Choose the node to connect to at random with probability proportional to each node's degree.

- The probability of connecting to a node u of degree $k_u$ is
  $$
  k_u/\sum_{j}k_j
  $$

```python
nx.barabasi_albert_graph(n, m)
# returns a network with n nodes. Each new node attches to m existing nodes according to the Preferential Attachment Model.
```

# 02. Small World Networks

Real social networks appear to have **small shortest paths** between nodes and **high clustering coefficient**.

The preferential attachment model produces networks with **small shortest paths** but **very small clustering coefficient**.

## Small World Model

- Start with a ring of n nodes, where each node is connected to its k nearest neighbors.
- Fix a parameter $p \in [0, 1]$
- Consider each edge (u, v). With probability p, select a node w at random and rewire the edge (u, v) so it becomes (u, w).

**Regular Lattice** (p=0): no edge is rewired.

**Random Network** (p=1): all edges are rewired.

**Small World Network** (0<p<1): Some edges are rewired. Network conserves some local structure but has some randomness.

As p increases:

- average shortest path decreases rapidly.
- average clustering coefficient decreases slowly.

For small values of p, small world networks have **small average shortest path** and **high clustering coefficient**, matching what we observe in real networks.

**However, the degree distribution of small world networks is not a power law.**

```python
nx.watts_strogatz_graph(n, k, p)
# returns a small world network
```

### Variants

Small world network can be disconnected,** which is sometimes undesirable.

```python
nx.connected_watts_strogatz_graph(n, k, p, t)
# runs nx.watts_strogatz_graph(n, k, p) up to t times until it returns a connected small world network.
```

```python
nx.newman_watts_strogatz_graph(n, k, p)
# runs a model simalar to the small world model, but rather than rewiring edges, new edges are added with probability p.
```

# 03. Link Prediction

Link prediction problem: Given a network, predict which edges will be formed in the future.

5 basic measures:

- Number of Common Neighbors
- Jaccard Coefficient
- Resource Allocation Index
- Adamic-Adar Index
- Preferential Attachment Score

2 measures that require community information:

- Common Neighbor Soundarajan-Hopcroft Score
- Resource Allocation Soundarajan-Hopcroft Score

Use these measures as features to train a classifier in order to make the prediction.

## Measure 1: Common Neighbors

**Triadic closure**: the tendency for people who share connections in a social network to become connected.

The number of common neighbors of nodes X and Y is
$$
\text{comm\_neigh}(X, Y) = |N(X)\cap N(Y)|
$$
where N(X) is the set of neighbors of node X.

```python
# nx.non_edges(graph): Returns the non-existent edges in the graph.
common_neigh = [
    (e[0], e[1], len(list(nx.common_neighbors(G, e[0], e[1]))))
    for e in nx.non_edges(G)
]
```

## Measure 2: Jaccard Coefficient

Number of common neighbors normalized by the total number of neighbors.

The Jaccard coefficient of nodes X and Y is
$$
\text{jacc\_coeff}(X, Y)=\frac{|N(X)\cap N(Y)|}{|N(X)\cup N(Y)|}
$$

```python
nx.jaccard_coefficient(G)
```

## Measure 3: Resource Allocation

Fraction of a "resource" that a node can send to another through their common neighbors.

The Resource Allocation index of nodes X and Y is
$$
\text{res\_allot}(X, Y)=\sum\nolimits_{u\in N(X)\cap N(Y)}\frac{1}{|N(u)|}
$$

```python
nx.resource_allocation_index(G)
```

## Measure 4: Adamic-Adar Index

Similar to resource allocation index, but with log in the denominator.

The Adamic-Adar index of nodes X and Y is
$$
\text{adamic\_adar}(X, Y)=\sum\nolimits_{u\in N(X)\cap N(Y)}\frac{1}{\log(|N(u)|)}
$$

```python
nx.adamic_adar_index(G)
```

## Measure 5: Pref. Attachment

In the preferential attachment model, nodes with high degree get more neighbors.

Product of the nodes' degree

The preferential attachment score of nodes X and Y is
$$
\text{pref\_attach}(X, Y)=|N(X)||N(Y)|
$$

```python
nx.preferential_attachment(G)
```

## Community Structure

Assume the nodes in this network belong to different communities (sets of nodes).

Pairs of nodes who belong to the same community and have many common neighbors in their community are likely to form an edge.

## Measure 6: Community Common Neighbors

Number of common neighbors with bonus for neighbors in same community.

The common Neighbor Soundarajan-Hopcroft score of nodes X and Y is:
$$
\begin{aligned}
 & \text{cn\_soundarajan\_hopcroft}(X, Y) = |N(X)\cap N(Y)| + \sum\nolimits_{u\in N(X)\cap N(Y)}f(u) \\
 & \text{where} f(u) =
     \left\{
         \begin{array}{lr}
             1,\ u\ \text{in same comm. as X and Y} \\
             0,\ \text{otherwise}
         \end{array}
     \right.
\end{aligned}
$$

```python
# Assign nodes to communities with attribute node "community"
G.node['A']['community'] = 0
G.node['B']['community'] = 0
...
G.node['E']['community'] = 1
G.node['F']['community'] = 1
...
#
nx.cn_soundarajan_hopcroft(G)
```

## Measure 7: Community Resource Allocation

Similar to resource allocation index, but only considering nodes in the same community.

The Resource Allocation Soundarajan-Hopcroft score of nodes X and Y is:
$$
\text{ra\_soundarajan\_hopcroft}(X, Y) = \sum\nolimits_{u\in N(X)\cap N(Y)}\frac{f(u)}{|N(u)|'}
$$

```python
nx.ra_index_soundarajan_hopcroft(G)
```
