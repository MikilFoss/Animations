"""
B-Tree Visualization using Manim
Shows B-tree insertion and search with node splitting

Run with: manim -pql btree_animation.py BTreeVisualization
For high quality: manim -pqh btree_animation.py BTreeVisualization
"""

from manim import *
import sys
import os

# Add parent directory to path for imports
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from Trees.base_tree_visualization import BaseTreeVisualization
from Trees.tree_builder import BTreeBuilder, BTreeNode, build_btree_graph_from_state, get_btree_key_rect


class BTreeVisualization(BaseTreeVisualization):
    
    def construct(self):
        # 1. Title section (use self.create_title_section from base class)
        title = self.create_title_section("B-Trees")
        
        # 2. Property section showing B-tree properties
        property_section = self.create_property_section(
            "B-Tree Properties",
            [
                ("Order 3: 1-2 keys per node", GREEN),
                ("Keys are sorted within each node", YELLOW),
                ("All leaves at same level", YELLOW)
            ]
        )
        
        # 3. Visual node demo (similar to original but simplified)
        # Show a single B-tree node with keys and explain properties
        node_demo = BTreeNode([10, 20])
        node_demo.scale(1.2)
        
        label1 = Text("Order 3: 1-2 keys per node", font_size=24, color=GREEN, disable_ligatures=True)
        label1.next_to(node_demo, DOWN, buff=0.3)
        label2 = Text("Keys are sorted within each node", font_size=22, color=YELLOW, disable_ligatures=True)
        label2.next_to(label1, DOWN, buff=0.2)
        label3 = Text("All leaves at same level", font_size=22, color=YELLOW, disable_ligatures=True)
        label3.next_to(label2, DOWN, buff=0.2)
        
        self.play(Create(node_demo), Write(label1), run_time=0.5)
        self.wait(0.5)
        self.play(Write(label2), run_time=0.4)
        self.wait(0.5)
        self.play(Write(label3), run_time=0.4)
        self.wait(2.0)
        
        self.fade_out_group(property_section, node_demo, label1, label2, label3)
        
        # 4. Create explainer panel on the left (smaller)
        explainer_panel = Rectangle(width=3.0, height=2.5, color=WHITE, fill_opacity=0.1, stroke_width=2)
        explainer_panel.to_corner(UL, buff=0.2).shift(DOWN * 0.2)
        explainer_title = Text("Insertion Steps", font_size=16, color=YELLOW, disable_ligatures=True)
        explainer_title.move_to(explainer_panel.get_top() + DOWN * 0.25)
        
        self.play(Create(explainer_panel), Write(explainer_title), run_time=0.3)
        
        # Store for later cleanup
        self.explainer_panel = explainer_panel
        self.explainer_title = explainer_title
        self.current_explainer = None
        
        # 5. Build B-tree with insertions using BTreeBuilder
        builder = BTreeBuilder(order=3)
        current_tree_group = None
        current_nodes = None
        
        insert_sequence = [10, 20, 30, 40, 50, 60, 70, 80, 90]
        
        for val in insert_sequence:
            insert_val_text = Text(f"Inserting: {val}", font_size=22, color=YELLOW, disable_ligatures=True)
            insert_val_text.to_edge(DOWN)
            self.play(Write(insert_val_text), run_time=0.3)
            self.wait(0.2)
            
            # Get tree state before insert to detect splits
            old_node_count = len(builder._nodes) if builder._root_id is not None else 0
            
            # If tree exists, show step-by-step traversal to find insertion point
            if current_tree_group is not None and current_nodes is not None:
                # Get the path we'll traverse to insert
                insertion_path = builder.get_insertion_path(val)
                
                # Step 1: Highlight traversal path
                self.update_explainer(f"Finding where\nto insert {val}...", ORANGE)
                
                for i, nid in enumerate(insertion_path):
                    if nid in current_nodes:
                        node_mobj = current_nodes[nid]
                        is_leaf = (i == len(insertion_path) - 1)
                        
                        # Highlight current node being examined
                        self.play(
                            node_mobj.rect.animate.set_color(ORANGE),
                            node_mobj.animate.scale(1.08),
                            run_time=0.25,
                        )
                        
                        if is_leaf:
                            self.update_explainer(f"Found leaf!\nInsert {val} here", GREEN)
                        else:
                            # Show comparison
                            node_keys = builder._nodes[nid].keys
                            if val < node_keys[0]:
                                self.update_explainer(f"{val} < {node_keys[0]}\nGo left", WHITE)
                            elif len(node_keys) > 1 and val > node_keys[-1]:
                                self.update_explainer(f"{val} > {node_keys[-1]}\nGo right", WHITE)
                            else:
                                self.update_explainer(f"Compare keys\nGo to child", WHITE)
                        
                        self.wait(0.2)
                        
                        # Reset color (keep scale for leaf)
                        if not is_leaf:
                            self.play(
                                node_mobj.rect.animate.set_color(BLUE),
                                node_mobj.animate.scale(1/1.08),
                                run_time=0.2,
                            )
            
            # Insert and get new state
            new_state, inserted_leaf_id = builder.insert_and_snapshot(val)
            new_tree_group, new_nodes = build_btree_graph_from_state(new_state)
            
            # Check if split occurred
            new_node_count = len(new_state.nodes)
            split_occurred = new_node_count > old_node_count and old_node_count > 0
            
            # Update explainer based on what happened
            if split_occurred:
                self.update_explainer(f"Node overflow!\nSplit: middle key\ngoes to parent", RED)
            else:
                self.update_explainer(f"Inserted {val}", GREEN)
            
            # Animate transition
            if current_tree_group is None:
                self.play(Create(new_tree_group), run_time=0.7)
            else:
                self.play(
                    TransformMatchingShapes(
                        current_tree_group,
                        new_tree_group,
                        fade_transform_mismatches=True,
                    ),
                    run_time=0.6,
                )
                self.remove(current_tree_group)
            
            current_tree_group = new_tree_group
            current_nodes = new_nodes
            
            # Highlight the node where the key was inserted (green flash)
            if inserted_leaf_id in current_nodes:
                inserted_node = current_nodes[inserted_leaf_id]
                self.play(
                    inserted_node.rect.animate.set_color(GREEN),
                    inserted_node.animate.scale(1.1),
                    run_time=0.25,
                )
                self.wait(0.15)
                self.play(
                    inserted_node.rect.animate.set_color(BLUE),
                    inserted_node.animate.scale(1/1.1),
                    run_time=0.25,
                )
            
            self.play(FadeOut(insert_val_text), run_time=0.2)
            self.wait(0.15)
        
        # 6. Clear explainer
        fade_outs = [FadeOut(explainer_panel), FadeOut(explainer_title)]
        if self.current_explainer:
            fade_outs.append(FadeOut(self.current_explainer))
        self.play(*fade_outs, run_time=0.3)
        self.wait(0.5)
        
        # 7. Search operation
        search_title = Text("Search Operation: Finding key 50", font_size=28, disable_ligatures=True)
        search_title.to_corner(UL)
        self.play(Write(search_title))
        
        search_val = 50
        search_text = Text(f"Searching for: {search_val}", font_size=24, color=YELLOW, disable_ligatures=True)
        search_text.to_edge(DOWN)
        self.play(Write(search_text), run_time=0.3)
        
        # Use builder's search_path
        path_node_ids = builder.search_path(search_val)
        found = False
        
        for nid in path_node_ids:
            # Get the BTreeNode from our nodes dict
            node_mobj = current_nodes[nid]
            
            # Highlight node
            self.play(
                node_mobj.rect.animate.set_color(YELLOW),
                node_mobj.animate.scale(1.05),
                run_time=0.4,
            )
            self.wait(0.2)
            
            # Check if key is in this node
            node_keys = builder._nodes[nid].keys
            if search_val in node_keys:
                found = True
                key_idx = node_keys.index(search_val)
                key_rect = get_btree_key_rect(node_mobj, key_idx)
                if key_rect:
                    self.play(Create(key_rect), run_time=0.3)
                    self.wait(0.5)
                    self.play(FadeOut(key_rect), run_time=0.2)
                
                # Reset highlight
                self.play(
                    node_mobj.rect.animate.set_color(BLUE),
                    node_mobj.animate.scale(1/1.05),
                    run_time=0.2,
                )
                break
            else:
                # Reset and continue
                self.play(
                    node_mobj.rect.animate.set_color(BLUE),
                    node_mobj.animate.scale(1/1.05),
                    run_time=0.2,
                )
                self.wait(0.15)
        
        if not found:
            not_found_text = Text("Key not found", font_size=24, color=RED, disable_ligatures=True)
            not_found_text.to_edge(DOWN)
            self.play(Write(not_found_text), run_time=0.3)
            self.wait(0.5)
            self.play(FadeOut(not_found_text), run_time=0.2)
        
        # 8. Fade out tree and search UI
        self.fade_out_group(current_tree_group, search_title, search_text)
        self.wait(0.3)
        
        # 9. Why B-trees for databases - Final slide
        db_title = Text("Why B-trees for Databases?", font_size=36, disable_ligatures=True)
        db_title.next_to(title, DOWN, buff=0.8)
        self.play(Write(db_title), run_time=0.5)
        self.wait(0.3)
        
        reasons = VGroup(
            VGroup(Dot(color=GREEN), Text("Minimize disk I/O", font_size=24, disable_ligatures=True)).arrange(RIGHT, buff=0.3),
            VGroup(Dot(color=GREEN), Text("Balanced height: O(log n)", font_size=24, disable_ligatures=True)).arrange(RIGHT, buff=0.3),
            VGroup(Dot(color=GREEN), Text("Nodes match disk page size", font_size=24, disable_ligatures=True)).arrange(RIGHT, buff=0.3)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(db_title, DOWN, buff=0.8)
        
        for reason in reasons:
            self.play(Write(reason), run_time=0.5)
            self.wait(0.3)
        
        self.wait(2.0)
    
    def update_explainer(self, text, color=WHITE):
        """Update the explainer panel with new text"""
        lines = text.split('\n')
        text_objects = [Text(line, font_size=14, color=color, disable_ligatures=True) for line in lines]
        new_text = VGroup(*text_objects).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        new_text.move_to(self.explainer_panel.get_center())
        
        if self.current_explainer:
            self.play(
                FadeOut(self.current_explainer),
                FadeIn(new_text),
                run_time=0.2
            )
        else:
            self.play(FadeIn(new_text), run_time=0.2)
        
        self.current_explainer = new_text
