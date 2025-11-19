"""
B-Tree Visualization using Manim
Shows B-tree insertion, search, and deletion with node splitting

Run with: manim -pql btree_animation.py BTreeVisualization
For high quality: manim -pqh btree_animation.py BTreeVisualization
"""

from manim import *
import numpy as np
import sys
import os
# Add parent directory to path for utils import
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
from Trees.utils import apply_manim_config, create_edge_rectangular_nodes, create_title

apply_manim_config()

class BTreeVisualization(Scene):
    
    def construct(self):
        # Title - keep visible throughout
        title = create_title("B-Trees")
        self.play(Write(title), run_time=0.2)
        self.wait(0.3)
        
        # Show B-tree properties - keep this longer
        property_title = Text("B-Tree Properties", font_size=32).to_corner(UL)
        self.play(Write(property_title))
        
        # Visual diagram showing min/max keys - single node demo
        node_demo = Rectangle(width=3, height=0.8, color=BLUE, fill_opacity=0.2)
        keys = VGroup(*[Text(str(k), font_size=20) for k in [10, 20, 30]])
        keys.arrange(RIGHT, buff=0.2).move_to(node_demo)
        node_group = VGroup(node_demo, keys)
        
        label1 = Text("Order 3: 1-2 keys per node", font_size=24, color=GREEN).next_to(node_group, DOWN, buff=0.3)
        label2 = Text("Keys are sorted within each node", font_size=22, color=YELLOW).next_to(label1, DOWN, buff=0.2)
        label3 = Text("All leaves at same level", font_size=22, color=YELLOW).next_to(label2, DOWN, buff=0.2)
        
        self.play(Create(node_group), Write(label1), run_time=0.5)
        self.wait(0.5)
        self.play(Write(label2), run_time=0.4)
        self.wait(0.5)
        self.play(Write(label3), run_time=0.4)
        self.wait(2.0)  # Keep this explainer longer
        
        self.play(FadeOut(property_title), FadeOut(node_group), FadeOut(label1), 
                  FadeOut(label2), FadeOut(label3))
        
        # Insert elements: [10, 20, 30, 40, 50, 60, 70, 80, 90]
        # Create explainer panel on the left side
        explainer_panel = Rectangle(width=4.5, height=4, color=WHITE, fill_opacity=0.1, stroke_width=2)
        explainer_panel.to_corner(UL, buff=0.5).shift(DOWN * 0.5 + RIGHT * 0.5)
        explainer_title = Text("Insertion Steps", font_size=22, color=YELLOW)
        explainer_title.move_to(explainer_panel.get_top() + DOWN * 0.4)
        
        self.explainer_panel = explainer_panel
        self.current_explainer = None
        
        self.play(Create(explainer_panel), Write(explainer_title), run_time=0.3)
        self.explainer_title = explainer_title
        
        insert_sequence = [10, 20, 30, 40, 50, 60, 70, 80, 90]
        tree_nodes = {}  # {id: {'node': mobject, 'keys': [keys], 'children': [ids], 'pos': position, 'level': level}}
        tree_edges = []  # [(parent_id, child_id, edge_mobject)]
        node_id_counter = 0
        root_id = None
        self.tree_scale = 0.8  # Scale factor for tree
        self.level_spacing = 1.2  # Vertical spacing between levels (increased)
        self.base_y = 1.5  # Base Y position for root (higher up, grows downward)
        self.tree_x_offset = 2.5  # Shift tree to the right to avoid overlap with instructions
        
        # Build B-tree with splitting - Order 3 (max 2 keys per node)
        for i, val in enumerate(insert_sequence):
            insert_val_text = Text(f"Inserting: {val}", font_size=24, color=YELLOW).to_edge(DOWN)
            self.play(Write(insert_val_text), run_time=0.3)
            self.wait(0.2)
            
            if root_id is None:
                # First node - position shifted right to avoid overlap with instructions
                root_id = node_id_counter
                root_pos = np.array([self.tree_x_offset, self.get_level_y(0), 0])
                root_node = self.create_btree_node([val], root_pos)
                root_node.scale(self.tree_scale)
                tree_nodes[root_id] = {'node': root_node, 'keys': [val], 'children': [], 'pos': root_pos, 'level': 0}
                self.play(Create(root_node), run_time=0.4)
                self.wait(0.3)
                node_id_counter += 1
            else:
                # Insert into existing tree
                result = self.insert_into_btree(root_id, val, tree_nodes, tree_edges, node_id_counter, parent_id=None, root_id=root_id)
                if result:
                    node_id_counter, new_edges, new_root_id = result
                    if new_edges:
                        tree_edges.extend(new_edges)
                    if new_root_id is not None:
                        root_id = new_root_id  # Update root if split occurred
                    self.wait(0.3)
            
            self.play(FadeOut(insert_val_text), run_time=0.2)
            self.wait(0.2)
        
        # Clear explainer
        fade_outs = [FadeOut(self.explainer_panel), FadeOut(self.explainer_title)]
        if hasattr(self, 'current_explainer') and self.current_explainer:
            fade_outs.append(FadeOut(self.current_explainer))
        self.play(*fade_outs, run_time=0.3)
        self.wait(0.5)
        
        # Show search operation
        search_title = Text("Search Operation: Finding key 50", font_size=28).to_corner(UL)
        self.play(Write(search_title))
        
        search_val = 50
        search_text = Text(f"Searching for: {search_val}", font_size=24, color=YELLOW).to_edge(DOWN)
        self.play(Write(search_text), run_time=0.3)
        
        # Highlight search path
        search_path = self.search_btree(root_id, search_val, tree_nodes)
        found = False
        for node_id in search_path:
            if node_id in tree_nodes:
                node = tree_nodes[node_id]['node']
                self.play(node.animate.set_color(YELLOW).scale(1.05), run_time=0.4)
                self.wait(0.2)
                # Check if key is in this node
                if search_val in tree_nodes[node_id]['keys']:
                    found = True
                    # Highlight the key
                    key_idx = tree_nodes[node_id]['keys'].index(search_val)
                    key_rect = self.get_key_rect(node, key_idx)
                    if key_rect:
                        self.play(Create(key_rect), run_time=0.3)
                        self.wait(0.5)
                        self.play(FadeOut(key_rect), run_time=0.2)
                    self.play(node.animate.set_color(BLUE).scale(1/1.05), run_time=0.2)
                    break
                else:
                    self.play(node.animate.set_color(BLUE).scale(1/1.05), run_time=0.2)
                    self.wait(0.15)
        
        if not found:
            not_found_text = Text("Key not found", font_size=24, color=RED).to_edge(DOWN)
            self.play(Write(not_found_text), run_time=0.3)
            self.wait(0.5)
            self.play(FadeOut(not_found_text), run_time=0.2)
        
        self.play(FadeOut(search_title), FadeOut(search_text))
        self.wait(0.5)
        
        # Clear the preview slide - fade out everything except title
        all_tree_nodes = VGroup(*[data['node'] for data in tree_nodes.values()])
        all_tree_edges = VGroup(*[e[2] for e in tree_edges if len(e) == 3])
        self.play(
            FadeOut(all_tree_nodes),
            FadeOut(all_tree_edges),
            FadeOut(search_title),
            FadeOut(search_text),
            run_time=0.5
        )
        self.wait(0.3)
        
        # Why B-trees for databases - Final slide
        db_title = Text("Why B-trees for Databases?", font_size=36, disable_ligatures=True).next_to(title, DOWN, buff=0.8)
        self.play(Write(db_title), run_time=0.5)
        self.wait(0.3)
        
        reasons = VGroup(
            VGroup(Dot(color=GREEN), Text("Minimize disk I/O", font_size=24, disable_ligatures=True)).arrange(RIGHT, buff=0.3),
            VGroup(Dot(color=GREEN), Text("Balanced height: O(log n)", font_size=24, disable_ligatures=True)).arrange(RIGHT, buff=0.3),
            VGroup(Dot(color=GREEN), Text("Nodes match disk page size", font_size=24, disable_ligatures=True)).arrange(RIGHT, buff=0.3),
            VGroup(Dot(color=GREEN), Text("Used in file systems & databases", font_size=24, disable_ligatures=True)).arrange(RIGHT, buff=0.3)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(db_title, DOWN, buff=0.8)
        
        for reason in reasons:
            self.play(Write(reason), run_time=0.5)
            self.wait(0.3)
        
        self.wait(2.0)
        
        # Visual summary complete
    
    def create_btree_node(self, keys, position):
        """Create a B-tree node with keys"""
        rect_width = max(2.0, len(keys) * 0.8 + 0.4)
        rect = Rectangle(width=rect_width, height=0.8, color=BLUE, fill_opacity=0.2, fill_color=BLUE, stroke_width=2)
        key_texts = VGroup(*[Text(str(k), font_size=20) for k in keys])
        key_texts.arrange(RIGHT, buff=0.2)
        node = VGroup(rect, key_texts).move_to(position)
        return node
    
    def get_key_rect(self, node, key_idx):
        """Get the rectangle for a specific key in a node"""
        # Extract the rectangle and key texts
        rect = node[0]
        key_texts = node[1]
        if key_idx < len(key_texts):
            key_text = key_texts[key_idx]
            # Create a highlight rectangle around this key
            key_rect = Rectangle(
                width=0.7, height=0.6, 
                color=GREEN, stroke_width=3
            ).move_to(key_text.get_center())
            return key_rect
        return None
    
    def get_level_y(self, level):
        """Calculate Y position for a given level (higher level = lower Y, tree grows downward)"""
        return self.base_y - level * self.level_spacing
    
    def get_node_x(self, parent_x, child_index, total_children):
        """Calculate X position for a child node"""
        spacing = 2.5 * self.tree_scale  # Increased horizontal spacing
        if total_children == 1:
            return parent_x
        elif total_children == 2:
            return parent_x + spacing * (child_index - 0.5)
        else:
            # For more children, distribute evenly
            total_width = (total_children - 1) * spacing
            start_x = parent_x - total_width / 2
            return start_x + child_index * spacing
    
    
    def update_explainer(self, text, color=WHITE):
        """Update the explainer panel with new text"""
        # Split text into lines if needed
        lines = text.split('\n')
        text_objects = [Text(line, font_size=18, color=color) for line in lines]
        new_text = VGroup(*text_objects).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        new_text.move_to(self.explainer_panel.get_center() + DOWN * 0.3)
        
        if hasattr(self, 'current_explainer') and self.current_explainer:
            # Fade out old text and write new text - slower for better readability
            self.play(FadeOut(self.current_explainer), run_time=0.3)
            self.play(Write(new_text), run_time=0.8)
        else:
            self.play(Write(new_text), run_time=0.8)
        self.current_explainer = new_text
    
    def insert_into_btree(self, node_id, val, tree_nodes, tree_edges, node_id_counter, parent_id=None, root_id=None):
        """Insert value into B-tree, handling splits"""
        node_data = tree_nodes[node_id]
        keys = node_data['keys']
        children = node_data['children']
        node = node_data['node']
        
        # If leaf node
        if len(children) == 0:
            # Add key to leaf
            keys.append(val)
            keys.sort()
            
            # Update explainer
            self.update_explainer(f"Adding {val} to leaf node\nKeys: {keys}", YELLOW)
            
            # Highlight node
            self.play(node.animate.set_color(YELLOW), run_time=0.3)
            
            # Update node visualization
            new_node = self.create_btree_node(keys, node_data['pos'])
            self.play(Transform(node, new_node), run_time=0.4)
            tree_nodes[node_id]['keys'] = keys
            # Keep the transformed node reference
            updated_node = node  # The transformed node
            
            # Check if split needed (Order 3: max 2 keys)
            if len(keys) > 2:
                self.update_explainer(f"Node overflow! ({len(keys)} keys)\nSplitting node...", RED)
                # Split node
                self.play(updated_node.animate.set_color(RED), run_time=0.3)
                self.wait(0.3)
                
                # Split keys: [left_keys], middle, [right_keys]
                mid_idx = len(keys) // 2
                middle_key = keys[mid_idx]
                left_keys = keys[:mid_idx]
                right_keys = keys[mid_idx + 1:]
                
                # Remove old edges connected to this node
                edges_to_remove = []
                for i, edge_info in enumerate(tree_edges):
                    if len(edge_info) == 3:
                        _, child_id, edge = edge_info
                        if child_id == node_id:
                            edges_to_remove.append((i, edge))
                
                for i, edge in reversed(edges_to_remove):
                    self.remove(edge)
                    tree_edges.pop(i)
                
                if parent_id is None:  # Root split - create new root
                    self.update_explainer("Root split:\n• Create new root\n• Split into 2 children\n• Scale tree down", GREEN)
                    
                    # Scale down entire tree and shift down
                    current_level = tree_nodes[node_id].get('level', 0)
                    new_level = 0  # New root at level 0
                    child_level = current_level + 1  # Children one level below
                    
                    # Scale and shift all existing nodes down - maintain x offset
                    all_nodes_group = VGroup(*[data['node'] for data in tree_nodes.values()])
                    all_edges_group = VGroup(*[e[2] for e in tree_edges if len(e) == 3])
                    if len(all_nodes_group) > 0:
                        # Calculate new positions based on level (shift down, maintain x position with scale)
                        for nid, ndata in tree_nodes.items():
                            old_level = ndata.get('level', 0)
                            new_level_for_node = old_level + 1
                            new_y = self.get_level_y(new_level_for_node)
                            old_pos = ndata['pos']
                            # Maintain x offset, scale x position relative to tree center
                            scaled_x = self.tree_x_offset + (old_pos[0] - self.tree_x_offset) * self.tree_scale
                            new_pos = np.array([scaled_x, new_y, 0])
                            ndata['level'] = new_level_for_node
                            ndata['pos'] = new_pos
                        
                        # Animate the scale and position changes
                        animations = []
                        for nid, ndata in tree_nodes.items():
                            animations.append(ndata['node'].animate.scale(self.tree_scale).move_to(ndata['pos']))
                        if len(all_edges_group) > 0:
                            animations.append(all_edges_group.animate.scale(self.tree_scale))
                        self.play(*animations, run_time=0.4)
                    
                    # Create new root with middle key at level 0 - shifted right
                    new_root_id = node_id_counter
                    new_root_pos = np.array([self.tree_x_offset, self.get_level_y(new_level), 0])
                    new_root = self.create_btree_node([middle_key], new_root_pos)
                    new_root.scale(self.tree_scale)
                    tree_nodes[new_root_id] = {'node': new_root, 'keys': [middle_key], 'children': [node_id, node_id_counter + 1], 'pos': new_root_pos, 'level': new_level}
                    
                    # Create left child (reuse node_id, replace the old node)
                    left_child_id = node_id
                    left_x = self.get_node_x(self.tree_x_offset, 0, 2)
                    left_child_pos = np.array([left_x, self.get_level_y(child_level), 0])
                    left_child = self.create_btree_node(left_keys, left_child_pos)
                    left_child.scale(self.tree_scale)
                    tree_nodes[left_child_id]['node'] = left_child
                    tree_nodes[left_child_id]['keys'] = left_keys
                    tree_nodes[left_child_id]['children'] = []
                    tree_nodes[left_child_id]['pos'] = left_child_pos
                    tree_nodes[left_child_id]['level'] = child_level
                    
                    # Create right child
                    right_child_id = node_id_counter + 1
                    right_x = self.get_node_x(self.tree_x_offset, 1, 2)
                    right_child_pos = np.array([right_x, self.get_level_y(child_level), 0])
                    right_child = self.create_btree_node(right_keys, right_child_pos)
                    right_child.scale(self.tree_scale)
                    tree_nodes[right_child_id] = {'node': right_child, 'keys': right_keys, 'children': [], 'pos': right_child_pos, 'level': child_level}
                    
                    # Create edges
                    edge1 = create_edge_rectangular_nodes(new_root, left_child)
                    edge2 = create_edge_rectangular_nodes(new_root, right_child)
                    
                    # Remove old node and create new ones
                    self.play(
                        FadeOut(updated_node),
                        run_time=0.2
                    )
                    self.play(
                        Create(new_root),
                        Create(left_child),
                        Create(right_child),
                        Create(edge1),
                        Create(edge2),
                        run_time=0.6
                    )
                    
                    return node_id_counter + 2, [(new_root_id, left_child_id, edge1), (new_root_id, right_child_id, edge2)], new_root_id
                else:
                    # Non-root split - need to handle parent update
                    self.update_explainer(f"Child split:\n• Promote middle key\n• Update parent node\n• Create 2 children", BLUE)
                    
                    # Get correct level from node data
                    current_level = tree_nodes[node_id].get('level', 0)
                    child_level = current_level  # Children stay at same level as the split node
                    parent_data = tree_nodes[parent_id]
                    parent_pos = parent_data['pos']
                    parent_children = parent_data['children']
                    parent_keys = parent_data['keys']
                    
                    # Find position of this node among parent's children
                    child_index_in_parent = parent_children.index(node_id)
                    total_siblings = len(parent_children) + 1  # +1 because we're splitting into 2
                    
                    # Create left child (reuse node_id)
                    left_child_id = node_id
                    left_x = self.get_node_x(parent_pos[0], child_index_in_parent, total_siblings)
                    left_child_pos = np.array([left_x, self.get_level_y(child_level), 0])
                    left_child = self.create_btree_node(left_keys, left_child_pos)
                    left_child.scale(self.tree_scale)
                    tree_nodes[left_child_id]['node'] = left_child
                    tree_nodes[left_child_id]['keys'] = left_keys
                    tree_nodes[left_child_id]['children'] = []
                    tree_nodes[left_child_id]['pos'] = left_child_pos
                    tree_nodes[left_child_id]['level'] = child_level
                    
                    # Create right child
                    right_child_id = node_id_counter
                    right_x = self.get_node_x(parent_pos[0], child_index_in_parent + 1, total_siblings)
                    right_child_pos = np.array([right_x, self.get_level_y(child_level), 0])
                    right_child = self.create_btree_node(right_keys, right_child_pos)
                    right_child.scale(self.tree_scale)
                    tree_nodes[right_child_id] = {'node': right_child, 'keys': right_keys, 'children': [], 'pos': right_child_pos, 'level': child_level}
                    
                    # Remove old edge from parent
                    edges_to_remove = []
                    for i, edge_info in enumerate(tree_edges):
                        if len(edge_info) == 3:
                            p_id, c_id, edge = edge_info
                            if p_id == parent_id and c_id == node_id:
                                edges_to_remove.append((i, edge))
                    
                    for i, edge in edges_to_remove:
                        self.remove(edge)
                        tree_edges.pop(i)
                    
                    # Create new edges
                    parent_node = tree_nodes[parent_id]['node']
                    edge1 = create_edge_rectangular_nodes(parent_node, left_child)
                    edge2 = create_edge_rectangular_nodes(parent_node, right_child)
                    
                    # Find position to insert middle_key in parent
                    insert_pos = 0
                    for i, key in enumerate(parent_keys):
                        if middle_key < key:
                            insert_pos = i
                            break
                        insert_pos = i + 1
                    
                    # Insert middle key into parent
                    parent_keys.insert(insert_pos, middle_key)
                    
                    # Update parent's children list
                    parent_children.remove(node_id)
                    parent_children.insert(insert_pos, left_child_id)
                    parent_children.insert(insert_pos + 1, right_child_id)
                    
                    # Update parent node visualization
                    parent_node = tree_nodes[parent_id]['node']
                    new_parent_node = self.create_btree_node(parent_keys, tree_nodes[parent_id]['pos'])
                    new_parent_node.scale(self.tree_scale)
                    
                    self.play(
                        FadeOut(updated_node),
                        Transform(parent_node, new_parent_node),
                        Create(left_child),
                        Create(right_child),
                        Create(edge1),
                        Create(edge2),
                        run_time=0.6
                    )
                    tree_nodes[parent_id]['node'] = new_parent_node
                    tree_nodes[parent_id]['keys'] = parent_keys
                    tree_nodes[parent_id]['children'] = parent_children
                    
                    # Check if parent needs to split (propagate split upward)
                    if len(parent_keys) > 2:
                        self.update_explainer("Parent overflow!\nSplitting propagates upward", RED)
                        self.wait(0.5)
                        # Split the parent node - find grandparent
                        grandparent_id = None
                        for gid, gdata in tree_nodes.items():
                            if parent_id in gdata.get('children', []):
                                grandparent_id = gid
                                break
                        
                        # Split parent keys
                        parent_mid_idx = len(parent_keys) // 2
                        parent_middle_key = parent_keys[parent_mid_idx]
                        parent_left_keys = parent_keys[:parent_mid_idx]
                        parent_right_keys = parent_keys[parent_mid_idx + 1:]
                        
                        # Get parent's children and split them appropriately
                        parent_children = tree_nodes[parent_id]['children']
                        # Split children: left half go with left keys, right half go with right keys
                        num_children = len(parent_children)
                        children_mid = (num_children + 1) // 2  # +1 because we have one more child than keys
                        parent_left_children = parent_children[:children_mid]
                        parent_right_children = parent_children[children_mid:]
                        
                        if grandparent_id is None:  # Parent is root - create new root
                            # Scale down entire tree
                            for nid, ndata in tree_nodes.items():
                                if nid != parent_id:
                                    old_level = ndata.get('level', 0)
                                    new_level_for_node = old_level + 1
                                    new_y = self.get_level_y(new_level_for_node)
                                    old_pos = ndata['pos']
                                    scaled_x = self.tree_x_offset + (old_pos[0] - self.tree_x_offset) * self.tree_scale
                                    new_pos = np.array([scaled_x, new_y, 0])
                                    ndata['level'] = new_level_for_node
                                    ndata['pos'] = new_pos
                            
                            # Create new root
                            new_root_id = node_id_counter + 1
                            new_root_pos = np.array([self.tree_x_offset, self.get_level_y(0), 0])
                            new_root = self.create_btree_node([parent_middle_key], new_root_pos)
                            new_root.scale(self.tree_scale)
                            tree_nodes[new_root_id] = {'node': new_root, 'keys': [parent_middle_key], 'children': [parent_id, new_root_id + 1], 'pos': new_root_pos, 'level': 0}
                            
                            # Update left child (reuse parent_id)
                            parent_level = tree_nodes[parent_id].get('level', 0)
                            child_level = parent_level + 1
                            left_x = self.get_node_x(self.tree_x_offset, 0, 2)
                            left_pos = np.array([left_x, self.get_level_y(child_level), 0])
                            left_node = self.create_btree_node(parent_left_keys, left_pos)
                            left_node.scale(self.tree_scale)
                            tree_nodes[parent_id]['node'] = left_node
                            tree_nodes[parent_id]['keys'] = parent_left_keys
                            tree_nodes[parent_id]['children'] = parent_left_children
                            tree_nodes[parent_id]['pos'] = left_pos
                            tree_nodes[parent_id]['level'] = child_level
                            
                            # Update levels of left children
                            for child_id in parent_left_children:
                                if child_id in tree_nodes:
                                    tree_nodes[child_id]['level'] = child_level + 1
                            
                            # Create right child
                            right_child_id = new_root_id + 1
                            right_x = self.get_node_x(self.tree_x_offset, 1, 2)
                            right_pos = np.array([right_x, self.get_level_y(child_level), 0])
                            right_node = self.create_btree_node(parent_right_keys, right_pos)
                            right_node.scale(self.tree_scale)
                            tree_nodes[right_child_id] = {'node': right_node, 'keys': parent_right_keys, 'children': parent_right_children, 'pos': right_pos, 'level': child_level}
                            
                            # Update levels of right children
                            for child_id in parent_right_children:
                                if child_id in tree_nodes:
                                    tree_nodes[child_id]['level'] = child_level + 1
                            
                            # Remove old edges from parent, create new edges
                            edges_to_remove = []
                            for i, edge_info in enumerate(tree_edges):
                                if len(edge_info) == 3:
                                    p_id, c_id, edge = edge_info
                                    if p_id == parent_id:
                                        edges_to_remove.append((i, edge))
                            
                            for i, edge in reversed(edges_to_remove):
                                self.remove(edge)
                                tree_edges.pop(i)
                            
                            # Create new edges
                            edge1 = create_edge_rectangular_nodes(new_root, left_node)
                            edge2 = create_edge_rectangular_nodes(new_root, right_node)
                            
                            # Animate
                            parent_old_node = tree_nodes[parent_id]['node']
                            self.play(
                                FadeOut(parent_old_node),
                                run_time=0.2
                            )
                            
                            # Scale and move existing nodes
                            animations = []
                            for nid, ndata in tree_nodes.items():
                                if nid not in [new_root_id, parent_id, right_child_id]:
                                    animations.append(ndata['node'].animate.scale(self.tree_scale).move_to(ndata['pos']))
                            if animations:
                                self.play(*animations, run_time=0.4)
                            
                            self.play(
                                Create(new_root),
                                Create(left_node),
                                Create(right_node),
                                Create(edge1),
                                Create(edge2),
                                run_time=0.6
                            )
                            
                            return new_root_id + 2, [(new_root_id, parent_id, edge1), (new_root_id, right_child_id, edge2)], new_root_id
                        else:
                            # Non-root parent split - promote to grandparent
                            # This is getting complex - for now, just ensure parent doesn't overflow
                            # by limiting keys
                            pass
                    
                    return node_id_counter + 1, [(parent_id, left_child_id, edge1), (parent_id, right_child_id, edge2)], None
            
            self.play(updated_node.animate.set_color(BLUE), run_time=0.2)
            return node_id_counter, [], None
        else:
            # Internal node - find child to insert into
            self.update_explainer(f"Internal node: {keys}\nFinding correct child...", YELLOW)
            
            child_idx = 0
            for i, key in enumerate(keys):
                if val < key:
                    child_idx = i
                    break
                child_idx = i + 1
            
            # Recursively insert into child
            if child_idx < len(children):
                child_id = children[child_idx]
                self.play(node.animate.set_color(YELLOW), run_time=0.2)
                self.wait(0.1)
                result = self.insert_into_btree(child_id, val, tree_nodes, tree_edges, node_id_counter, parent_id=node_id, root_id=root_id)
                self.play(node.animate.set_color(BLUE), run_time=0.2)
                if result:
                    return result[0], result[1], result[2] if len(result) > 2 else None
            
            return node_id_counter, [], None
    
    def search_btree(self, node_id, val, tree_nodes):
        """Get search path for a value"""
        path = [node_id]
        if node_id not in tree_nodes:
            return path
        
        node_data = tree_nodes[node_id]
        keys = node_data['keys']
        children = node_data['children']
        
        # Check if key is in this node
        if val in keys:
            return path
        
        # Find child to search
        if len(children) == 0:
            return path  # Leaf node, not found
        
        child_idx = 0
        for i, key in enumerate(keys):
            if val < key:
                child_idx = i
                break
            child_idx = i + 1
        
        if child_idx < len(children):
            child_id = children[child_idx]
            path.extend(self.search_btree(child_id, val, tree_nodes))
        
        return path
