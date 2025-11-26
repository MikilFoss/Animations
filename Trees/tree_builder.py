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

        # z-index layering: rect < labels
        rect.set_z_index(2)
        key_texts.set_z_index(3)

        self.add(rect, key_texts)
        self.rect = rect
        self.key_texts = key_texts
        self.set_z_index(2)


def build_btree_graph_from_state(
    state: BTreeState,
    vertex_spacing: Tuple[float, float] = (2.8, 1.5),
    layout_scale: float = 2.0,
    x_offset: float = 1.8,
) -> Tuple[VGroup, Dict[int, BTreeNode]]:
    """
    Build a Manim visualization from a pure BTreeState using tree layout.
    
    Args:
        state: BTreeState snapshot from BTreeBuilder
        vertex_spacing: (horizontal, vertical) spacing between nodes
        layout_scale: Overall scale of the layout
        x_offset: Horizontal offset to shift tree right (avoid overlap with UI)
    
    Returns:
        Tuple of (VGroup containing all nodes and edges, dict mapping node_id -> BTreeNode)
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

    # Create edges between BTreeNodes
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
        edge.set_z_index(1)
        edges.add(edge)

    # Combine into VGroup
    all_nodes = VGroup(*btree_nodes.values())
    result = VGroup(edges, all_nodes)
    
    # Shift entire group right to avoid overlap with side panel
    result.shift(RIGHT * x_offset)

    return result, btree_nodes


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
        key_rect.set_z_index(4)  # Above labels
        return key_rect
    return None


