"""
Tree building utilities for common binary tree operations
Provides helpers for insertion, positioning, and tree construction
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import copy

from manim import *
import numpy as np
from Trees.utils import create_circular_node, create_edge_circular_nodes, calculate_binary_tree_position


@dataclass
class BTreeNodeData:
    id: int
    keys: List[int] = field(default_factory=list)
    children: List[int] = field(default_factory=list)  # child node IDs


@dataclass
class BTreeState:
    """Immutable snapshot of a B-tree at a given step."""
    nodes: Dict[int, BTreeNodeData]
    root_id: int


@dataclass
class BTreeDiff:
    """Diff between two B-tree states for localized animations."""
    new_nodes: set          # node IDs in new_state only
    removed_nodes: set      # node IDs in old_state only  
    modified_nodes: set     # node IDs in both but keys differ
    unchanged_nodes: set    # node IDs in both with identical keys


def diff_btree_states(old: BTreeState, new: BTreeState) -> BTreeDiff:
    """Compute structural diff between two B-tree states."""
    old_ids = set(old.nodes.keys())
    new_ids = set(new.nodes.keys())

    common = old_ids & new_ids
    new_nodes = new_ids - old_ids
    removed_nodes = old_ids - new_ids

    modified_nodes = set()
    unchanged_nodes = set()
    for nid in common:
        if old.nodes[nid].keys == new.nodes[nid].keys:
            unchanged_nodes.add(nid)
        else:
            modified_nodes.add(nid)

    return BTreeDiff(
        new_nodes=new_nodes,
        removed_nodes=removed_nodes,
        modified_nodes=modified_nodes,
        unchanged_nodes=unchanged_nodes,
    )


class BinaryTreeBuilder:
    """Helper class for binary tree building operations"""
    
    def __init__(self, base_spacing=2.0, level_spacing=1.2, root_y=2.5):
        """
        Initialize tree builder
        
        Args:
            base_spacing: Base horizontal spacing between nodes
            level_spacing: Vertical spacing between levels
            root_y: Y position for root node
        """
        self.base_spacing = base_spacing
        self.level_spacing = level_spacing
        self.root_y = root_y
    
    def calculate_position(self, parent_pos, level, is_left):
        """
        Calculate position for a child node
        
        Args:
            parent_pos: Parent node position
            level: Current level in tree
            is_left: True for left child, False for right
        
        Returns:
            numpy array position
        """
        return calculate_binary_tree_position(parent_pos, level, is_left, 
                                            self.base_spacing, self.level_spacing)
    
    def insert_binary_node(self, current_val, new_val, tree, level, current_pos, 
                          node_creator=None, root_pos=None):
        """
        Insert a value into a binary tree structure (BST-style)
        
        Args:
            current_val: Current node value
            new_val: Value to insert
            tree: Tree dictionary {val: {'node': mobject, 'left': val, 'right': val, 'pos': pos}}
            level: Current level
            current_pos: Current node position
            node_creator: Optional function to create nodes (default: create_circular_node)
            root_pos: Root position for calculating absolute positions
        
        Returns:
            Tuple (new_node, new_pos, parent_val, is_left) or None if duplicate
        """
        if node_creator is None:
            node_creator = create_circular_node
        
        if root_pos is None:
            root_pos = current_pos
        
        if new_val < current_val:
            if tree[current_val]['left'] is None:
                new_pos = self.calculate_position(current_pos, level, is_left=True)
                new_node = node_creator(new_val, new_pos)
                return new_node, new_pos, current_val, True
            else:
                left_val = tree[current_val]['left']
                left_pos = tree[left_val]['pos']
                return self.insert_binary_node(left_val, new_val, tree, level + 1, 
                                             left_pos, node_creator, root_pos)
        elif new_val > current_val:
            if tree[current_val]['right'] is None:
                new_pos = self.calculate_position(current_pos, level, is_left=False)
                new_node = node_creator(new_val, new_pos)
                return new_node, new_pos, current_val, False
            else:
                right_val = tree[current_val]['right']
                right_pos = tree[right_val]['pos']
                return self.insert_binary_node(right_val, new_val, tree, level + 1, 
                                             right_pos, node_creator, root_pos)
        
        return None, None, None, None
    
    def create_insertion_animation(self, scene, new_node, parent_node, edge=None, 
                                  run_time=0.4, wait_time=0.15):
        """
        Create animation for inserting a node
        
        Args:
            scene: Manim Scene object
            new_node: New node mobject
            parent_node: Parent node mobject
            edge: Edge mobject (will be created if None)
            run_time: Animation run time
            wait_time: Wait time after animation
        """
        if edge is None:
            edge = create_edge_circular_nodes(parent_node, new_node)
        
        scene.play(Create(edge), Create(new_node), run_time=run_time)
        scene.wait(wait_time)
        return edge
    
    def search_path(self, current_val, target, tree):
        """
        Get search path for a target value in binary tree
        
        Args:
            current_val: Current node value
            target: Target value to find
            tree: Tree dictionary
        
        Returns:
            List of values in search path
        """
        path = [current_val]
        if current_val == target:
            return path
        
        if target < current_val and tree[current_val]['left']:
            path.extend(self.search_path(tree[current_val]['left'], target, tree))
        elif target > current_val and tree[current_val]['right']:
            path.extend(self.search_path(tree[current_val]['right'], target, tree))
        
        return path


class BTreeBuilder:
    """Pure Python B-tree builder with no Manim dependencies."""
    
    def __init__(self, order: int = 3):
        self.order = order
        self.max_keys = order - 1
        self.reset()
    
    def reset(self):
        self._next_id = 0
        self._nodes: Dict[int, BTreeNodeData] = {}
        self._root_id: Optional[int] = None
    
    def insert_and_snapshot(self, key: int) -> Tuple[BTreeState, int]:
        """
        Insert a key and return (snapshot, leaf_node_id where key was inserted).
        """
        if self._root_id is None:
            root = self._new_node([key], [])
            self._root_id = root.id
            return self._snapshot(), root.id
        else:
            root_node = self._nodes[self._root_id]
            if len(root_node.keys) > self.max_keys:
                self._split_root()
            leaf_id = self._insert_non_full(self._root_id, key)
            # Check if root needs split after insert
            root_node = self._nodes[self._root_id]
            if len(root_node.keys) > self.max_keys:
                self._split_root()
            return self._snapshot(), leaf_id
    
    def search_path(self, target: int) -> List[int]:
        if self._root_id is None:
            return []
        path = []
        node_id = self._root_id
        while node_id is not None:
            path.append(node_id)
            node = self._nodes[node_id]
            if target in node.keys:
                break
            if not node.children:
                break
            idx = 0
            while idx < len(node.keys) and target > node.keys[idx]:
                idx += 1
            node_id = node.children[idx] if idx < len(node.children) else None
        return path
    
    def get_insertion_path(self, key: int) -> List[int]:
        """Get the path from root to where a key would be inserted (without inserting)."""
        if self._root_id is None:
            return []
        path = []
        node_id = self._root_id
        while node_id is not None:
            path.append(node_id)
            node = self._nodes[node_id]
            if not node.children:
                break  # Reached leaf
            idx = 0
            while idx < len(node.keys) and key > node.keys[idx]:
                idx += 1
            node_id = node.children[idx] if idx < len(node.children) else None
        return path
    
    def _snapshot(self) -> BTreeState:
        nodes_copy = {}
        for nid, node in self._nodes.items():
            nodes_copy[nid] = BTreeNodeData(
                id=node.id,
                keys=list(node.keys),
                children=list(node.children)
            )
        return BTreeState(nodes=nodes_copy, root_id=self._root_id)
    
    def _new_node(self, keys: List[int], children: List[int]) -> BTreeNodeData:
        node = BTreeNodeData(id=self._next_id, keys=list(keys), children=list(children))
        self._nodes[self._next_id] = node
        self._next_id += 1
        return node
    
    def _insert_non_full(self, node_id: int, key: int) -> int:
        """Insert key into subtree rooted at node_id. Returns leaf node id where key was inserted."""
        node = self._nodes[node_id]
        if not node.children:
            # Leaf node - insert here
            idx = 0
            while idx < len(node.keys) and key > node.keys[idx]:
                idx += 1
            node.keys.insert(idx, key)
            return node_id
        else:
            # Internal node - find child to recurse into
            idx = 0
            while idx < len(node.keys) and key > node.keys[idx]:
                idx += 1
            child_id = node.children[idx]
            leaf_id = self._insert_non_full(child_id, key)
            
            # After recursive insert, check if child overflowed and needs split
            child = self._nodes[child_id]
            if len(child.keys) > self.max_keys:
                self._split_child(node_id, idx)
            
            return leaf_id
    
    def _split_child(self, parent_id: int, child_index: int):
        parent = self._nodes[parent_id]
        child_id = parent.children[child_index]
        child = self._nodes[child_id]
        
        mid = len(child.keys) // 2
        mid_key = child.keys[mid]
        
        left_keys = child.keys[:mid]
        right_keys = child.keys[mid + 1:]
        
        if child.children:
            left_children = child.children[:mid + 1]
            right_children = child.children[mid + 1:]
        else:
            left_children = []
            right_children = []
        
        child.keys = left_keys
        child.children = left_children
        
        new_node = self._new_node(right_keys, right_children)
        
        parent.keys.insert(child_index, mid_key)
        parent.children.insert(child_index + 1, new_node.id)
    
    def _split_root(self):
        old_root = self._nodes[self._root_id]
        
        mid = len(old_root.keys) // 2
        mid_key = old_root.keys[mid]
        
        left_keys = old_root.keys[:mid]
        right_keys = old_root.keys[mid + 1:]
        
        if old_root.children:
            left_children = old_root.children[:mid + 1]
            right_children = old_root.children[mid + 1:]
        else:
            left_children = []
            right_children = []
        
        old_root.keys = left_keys
        old_root.children = left_children
        
        right_node = self._new_node(right_keys, right_children)
        new_root = self._new_node([mid_key], [self._root_id, right_node.id])
        self._root_id = new_root.id


class BTreeNode(VGroup):
    """Visual B-tree node with rectangular shape and key labels."""
    
    def __init__(self, keys, **kwargs):
        super().__init__(**kwargs)
        rect_width = max(2.0, len(keys) * 0.8 + 0.4)
        rect = Rectangle(
            width=rect_width,
            height=0.8,
            color=BLUE,
            fill_opacity=0.2,
            fill_color=BLUE,
            stroke_width=2,
        )
        key_texts = VGroup(*[
            Text(str(k), font_size=20, color=WHITE, disable_ligatures=True)
            for k in keys
        ]).arrange(RIGHT, buff=0.2)
        key_texts.move_to(rect)

        # z-index layering: nodes above edges (5), rect < labels
        rect.set_z_index(10)
        key_texts.set_z_index(11)

        self.add(rect, key_texts)
        self.rect = rect
        self.key_texts = key_texts
        self.set_z_index(10)


def _connect_edge_to_nodes(edge: Line, parent_node: 'BTreeNode', child_node: 'BTreeNode') -> None:
    """Attach an updater so the edge always connects the given parent/child nodes."""
    def update_edge(e: Line) -> None:
        e.put_start_and_end_on(
            parent_node.get_bottom(),
            child_node.get_top(),
        )
    edge.clear_updaters()
    edge.add_updater(update_edge)


def build_btree_graph_from_state(
    state: BTreeState,
    vertex_spacing: Tuple[float, float] = (2.8, 1.5),
    layout_scale: float = 2.0,
    x_offset: float = 1.8,
) -> Tuple[VGroup, Dict[int, BTreeNode], Dict[Tuple[int, int], Line]]:
    """
    Build a Manim visualization from a pure BTreeState using tree layout.
    
    Args:
        state: BTreeState snapshot from BTreeBuilder
        vertex_spacing: (horizontal, vertical) spacing between nodes
        layout_scale: Overall scale of the layout
        x_offset: Horizontal offset to shift tree right (avoid overlap with UI)
    
    Returns:
        Tuple of (VGroup containing all nodes and edges,
                  dict mapping node_id -> BTreeNode,
                  dict mapping (parent_id, child_id) -> Line edge)
    """
    nodes = state.nodes
    root = state.root_id

    vertices = list(nodes.keys())
    edges_list = []
    for nid, node in nodes.items():
        for child_id in node.children:
            edges_list.append((nid, child_id))

    # Create Graph just for layout calculation
    g = Graph(
        vertices,
        edges_list,
        layout="tree",
        layout_scale=layout_scale,
        layout_config={
            "root_vertex": root,
            "vertex_spacing": vertex_spacing,
        },
    )

    # Create BTreeNodes at calculated positions
    btree_nodes: Dict[int, BTreeNode] = {}
    for nid in vertices:
        node_data = nodes[nid]
        bt_node = BTreeNode(node_data.keys)
        bt_node.move_to(g[nid].get_center())
        btree_nodes[nid] = bt_node

    # Create edges between BTreeNodes with updaters
    edges_dict: Dict[Tuple[int, int], Line] = {}
    edges = VGroup()
    for parent_id, child_id in edges_list:
        parent_node = btree_nodes[parent_id]
        child_node = btree_nodes[child_id]
        edge = Line(
            parent_node.get_bottom(),
            child_node.get_top(),
            color=WHITE,
            stroke_width=2,
        )
        edge.set_z_index(5)  # Below nodes (10)
        _connect_edge_to_nodes(edge, parent_node, child_node)
        edges.add(edge)
        edges_dict[(parent_id, child_id)] = edge

    # Combine into VGroup
    all_nodes = VGroup(*btree_nodes.values())
    result = VGroup(edges, all_nodes)
    
    # Shift entire group right to avoid overlap with side panel
    result.shift(RIGHT * x_offset)

    return result, btree_nodes, edges_dict


def get_btree_key_rect(node: BTreeNode, key_idx: int) -> Optional[Rectangle]:
    """Create a highlight rectangle around a specific key in a BTreeNode."""
    if key_idx < len(node.key_texts):
        key_text = node.key_texts[key_idx]
        key_rect = Rectangle(
            width=0.7,
            height=0.6,
            color=GREEN,
            stroke_width=3,
        ).move_to(key_text.get_center())
        key_rect.set_z_index(20)  # Above node labels
        return key_rect
    return None


def animate_btree_transition(
    scene,
    prev_state: BTreeState,
    new_state: BTreeState,
    prev_nodes: Dict[int, 'BTreeNode'],
    prev_edges: Dict[Tuple[int, int], Line],
    x_offset: float = 1.8,
    run_time: float = 1.0,
) -> Tuple[Dict[int, 'BTreeNode'], Dict[Tuple[int, int], Line]]:
    """
    Animate transition between B-tree states with localized animations.
    Only animates nodes/edges that actually changed.
    
    Args:
        scene: Manim Scene object
        prev_state: Previous BTreeState
        new_state: New BTreeState after operation
        prev_nodes: Dict mapping node_id -> BTreeNode mobject
        prev_edges: Dict mapping (parent_id, child_id) -> Line mobject
        x_offset: Horizontal offset for tree positioning
        run_time: Animation duration
    
    Returns:
        Tuple of (new_nodes_dict, new_edges_dict) for next iteration
    """
    for node in prev_nodes.values():
        node.rect.set_color(BLUE)
        node.rect.set_fill(BLUE, opacity=0.2)
    
    # Build target layout to get positions
    target_group, target_nodes, target_edges = build_btree_graph_from_state(
        new_state, x_offset=x_offset
    )
    
    diff = diff_btree_states(prev_state, new_state)
    
    node_anims = []
    edge_anims = []
    new_nodes_dict: Dict[int, BTreeNode] = {}
    new_edges_dict: Dict[Tuple[int, int], Line] = {}
    
    # Handle unchanged nodes - reuse existing mobjects, move if position changed
    for nid in diff.unchanged_nodes:
        old_node = prev_nodes[nid]
        target_node = target_nodes[nid]
        new_nodes_dict[nid] = old_node
        
        old_pos = old_node.get_center()
        new_pos = target_node.get_center()
        
        if np.linalg.norm(new_pos - old_pos) > 0.01:
            node_anims.append(old_node.animate.move_to(new_pos))
    
    # Handle modified nodes - transform to show new keys
    for nid in diff.modified_nodes:
        old_node = prev_nodes[nid]
        target_node = target_nodes[nid]
        
        # Transform old node into new visual
        node_anims.append(Transform(old_node, target_node))
        new_nodes_dict[nid] = old_node
    
    # Handle new nodes - use FadeIn to preserve fill_opacity
    for nid in diff.new_nodes:
        target_node = target_nodes[nid].copy()
        new_nodes_dict[nid] = target_node
        node_anims.append(FadeIn(target_node))
    
    # Handle removed nodes - fade out
    for nid in diff.removed_nodes:
        old_node = prev_nodes[nid]
        node_anims.append(FadeOut(old_node))
    
    # Handle edges
    old_edge_keys = set(prev_edges.keys())
    new_edge_keys = set(target_edges.keys())
    
    kept_edges = old_edge_keys & new_edge_keys
    added_edges = new_edge_keys - old_edge_keys
    removed_edges = old_edge_keys - new_edge_keys
    
    # Kept edges - reattach updater so they follow moved/transformed nodes
    for ek in kept_edges:
        old_edge = prev_edges[ek]
        parent_id, child_id = ek
        parent_node = new_nodes_dict[parent_id]
        child_node = new_nodes_dict[child_id]
        new_edges_dict[ek] = old_edge
        
        # Updater will keep edge connected to nodes during animation
        _connect_edge_to_nodes(old_edge, parent_node, child_node)
    
    # New edges - create with updater and animate in
    for ek in added_edges:
        parent_id, child_id = ek
        parent_node = new_nodes_dict[parent_id]
        child_node = new_nodes_dict[child_id]
        new_edge = Line(
            ORIGIN, ORIGIN,  # Updater will set correct endpoints
            color=WHITE,
            stroke_width=2,
        )
        new_edge.set_z_index(5)  # Below nodes (10)
        _connect_edge_to_nodes(new_edge, parent_node, child_node)
        new_edges_dict[ek] = new_edge
        scene.add(new_edge)
        edge_anims.append(Create(new_edge))
    
    # Removed edges - clear updaters and fade out
    for ek in removed_edges:
        old_edge = prev_edges[ek]
        old_edge.clear_updaters()
        edge_anims.append(FadeOut(old_edge))
    
    # Play all animations together
    if node_anims or edge_anims:
        scene.play(
            AnimationGroup(*node_anims, *edge_anims, lag_ratio=0.0),
            run_time=run_time,
        )
    
    return new_nodes_dict, new_edges_dict



