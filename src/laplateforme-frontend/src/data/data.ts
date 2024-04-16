// data.ts
import { Nodes, Edges, Layouts } from 'v-network-graph'

const nodes: Nodes = {
  node1: { name: 'N1' },
  node2: { name: 'N2' },
  node3: { name: 'N3' },
  node4: { name: 'N4' },
  node5: { name: 'N5' },
  node6: { name: 'N6' }
}

const edges: Edges = {
  edge1: { source: 'node1', target: 'node2', isSourceWireless: true },
  edge2: { source: 'node2', target: 'node3', isTargetWireless: true },
  edge3: { source: 'node2', target: 'node4', isTargetWireless: true },
  edge4: { source: 'node4', target: 'node5', isTargetWireless: true },
  edge5: { source: 'node4', target: 'node6', isTargetWireless: true }
}

const layouts: Layouts = {
  nodes: {
    node1: { x: 0, y: 0 },
    node2: { x: 80, y: 60 },
    node3: { x: 0, y: 160 },
    node4: { x: 200, y: 160 },
    node5: { x: 320, y: 0 },
    node6: { x: 320, y: 160 }
  }
}

export default {
  nodes,
  edges,
  layouts
}
