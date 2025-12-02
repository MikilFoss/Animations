"""
Binary Search Tree Visualization using Manim
Shows BST properties, insertion, deletion (all 3 cases), and search operations

Run with: manim -pql bst_animation.py BSTVisualization
For high quality: manim -pqh bst_animation.py BSTVisualization
"""

from manim import *
import sys
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from Trees.base_tree_visualization import BaseTreeVisualization
from Trees.tree_builder import BSTBuilder, BSTState, build_bst_graph_from_state, animate_bst_transition
from Trees.utils import create_circular_node, create_edge_circular_nodes


class BSTVisualization(BaseTreeVisualization):
    
    def construct(self):
        # 1. Title section
        title = self.create_title_section("Binary Search Trees")
        
        # 2. Property section with BST properties demo
        property_section = self.create_property_section(
            "BST Property",
            [("left < root < right", GREEN)]
        )
        
        # Visual demo with root (50), left (30), right (70)
        root_demo = create_circular_node(50, ORIGIN + UP * 1.5)
        left_demo = create_circular_node(30, ORIGIN + LEFT * 1.5 + DOWN * 0.5, color=GREEN)
        right_demo = create_circular_node(70, ORIGIN + RIGHT * 1.5 + DOWN * 0.5, color=GREEN)
        
        edge1 = create_edge_circular_nodes(root_demo, left_demo, color=GREEN)
        edge2 = create_edge_circular_nodes(root_demo, right_demo, color=GREEN)
        
        label_left = Text("30 < 50", font_size=20, color=GREEN, disable_ligatures=True).next_to(left_demo, DOWN, buff=0.2)
        label_right = Text("70 > 50", font_size=20, color=GREEN, disable_ligatures=True).next_to(right_demo, DOWN, buff=0.2)
        
        self.play(Create(root_demo), run_time=0.3)
        self.play(Create(edge1), Create(edge2), run_time=0.3)
        self.play(Create(left_demo), Create(right_demo), run_time=0.3)
        self.play(Write(label_left), Write(label_right), run_time=0.3)
        self.wait(1.5)
        
        self.fade_out_group(property_section, root_demo, left_demo, right_demo,
                           edge1, edge2, label_left, label_right)
        
        # 3. Create explainer panel on the left
        explainer_panel = Rectangle(width=3.0, height=2.5, color=WHITE, fill_opacity=0.1, stroke_width=2)
        explainer_panel.to_corner(UL, buff=0.2).shift(DOWN * 0.2)
        explainer_title = Text("Insertion Steps", font_size=16, color=YELLOW, disable_ligatures=True)
        explainer_title.move_to(explainer_panel.get_top() + DOWN * 0.25)
        
        self.play(Create(explainer_panel), Write(explainer_title), run_time=0.3)
        
        self.explainer_panel = explainer_panel
        self.explainer_title = explainer_title
        self.current_explainer = None
        
        # 4. Build BST with insertions using BSTBuilder
        builder = BSTBuilder()
        prev_state = None
        prev_nodes = None
        prev_edges = None
        
        insert_sequence = [50, 30, 70, 20, 40, 60, 10, 5, 80, 25]
        
        for val in insert_sequence:
            insert_val_text = Text(f"Inserting: {val}", font_size=22, color=YELLOW, disable_ligatures=True)
            insert_val_text.to_edge(DOWN)
            self.play(Write(insert_val_text), run_time=0.3)
            self.wait(0.2)
            
            # If tree exists, show step-by-step traversal to find insertion point
            if prev_state is not None and prev_nodes is not None:
                insertion_path = builder.get_insertion_path(val)
                
                self.update_explainer(f"Finding where\nto insert {val}...", ORANGE)
                
                for i, nid in enumerate(insertion_path):
                    if nid in prev_nodes:
                        node_mobj = prev_nodes[nid]
                        is_leaf_position = (i == len(insertion_path) - 1)
                        node_key = builder._nodes[nid].key
                        
                        # Highlight current node
                        self.play(
                            node_mobj[0].animate.set_color(ORANGE),
                            run_time=0.5,
                        )
                        
                        if is_leaf_position:
                            if val < node_key:
                                self.update_explainer(f"{val} < {node_key}\nInsert as left child", GREEN)
                            else:
                                self.update_explainer(f"{val} > {node_key}\nInsert as right child", GREEN)
                        else:
                            if val < node_key:
                                self.update_explainer(f"{val} < {node_key}\nGo left", WHITE)
                            else:
                                self.update_explainer(f"{val} > {node_key}\nGo right", WHITE)
                        
                        self.wait(0.5)
                        
                        if not is_leaf_position:
                            self.play(
                                node_mobj[0].animate.set_color(BLUE),
                                run_time=0.4,
                            )
                
                # Reset last node color
                if insertion_path:
                    last_id = insertion_path[-1]
                    if last_id in prev_nodes:
                        self.play(
                            prev_nodes[last_id][0].animate.set_color(BLUE),
                            run_time=0.3,
                        )
            
            # Insert and get new state
            new_state, inserted_node_id = builder.insert_and_snapshot(val)
            
            self.update_explainer(f"Inserted {val}", GREEN)
            
            # Animate transition
            if prev_state is None:
                tree_group, prev_nodes, prev_edges = build_bst_graph_from_state(new_state)
                self.play(Create(tree_group), run_time=1.0)
            else:
                prev_nodes, prev_edges = animate_bst_transition(
                    self, prev_state, new_state, prev_nodes, prev_edges, run_time=1.0
                )
            
            prev_state = new_state
            
            self.play(FadeOut(insert_val_text), run_time=0.3)
            self.wait(0.3)
        
        # 5. Deletion operation showing all 3 cases
        self.update_explainer_title("Deletion Steps")
        
        # Case 1: Delete 5 (leaf node - deepest on left side)
        prev_state, prev_nodes, prev_edges = self.perform_deletion(
            builder, 5, prev_state, prev_nodes, prev_edges,
            "Leaf node\nRemove directly")
        self.wait(0.3)
        
        # Case 2: Delete 10 (one child - after deleting 5, node 10 has no children but 20 has child 25)
        # Actually delete 20 which now has only child 25 (since 10 has no children after 5 is gone)
        prev_state, prev_nodes, prev_edges = self.perform_deletion(
            builder, 10, prev_state, prev_nodes, prev_edges,
            "Leaf node\nRemove directly")
        self.wait(0.3)
        
        # Case 2b: Delete 20 (one child - has only 25)
        prev_state, prev_nodes, prev_edges = self.perform_deletion(
            builder, 20, prev_state, prev_nodes, prev_edges,
            "One child\nPromote child 25")
        self.wait(0.3)
        
        # Case 3: Delete 30 (two children)
        prev_state, prev_nodes, prev_edges = self.perform_deletion(
            builder, 30, prev_state, prev_nodes, prev_edges,
            "Two children\nUse inorder successor",
            show_successor=True)
        self.wait(0.5)
        
        # 6. Search operation
        self.update_explainer_title("Search Steps")
        
        search_val = 60
        search_text = Text(f"Searching for: {search_val}", font_size=22, color=YELLOW, disable_ligatures=True)
        search_text.to_edge(DOWN)
        self.play(Write(search_text), run_time=0.3)
        
        search_path = builder.search_path(search_val)
        
        for i, nid in enumerate(search_path):
            if nid in prev_nodes:
                node_mobj = prev_nodes[nid]
                node_key = builder._nodes[nid].key
                is_found = (node_key == search_val)
                
                self.play(
                    node_mobj[0].animate.set_color(ORANGE),
                    run_time=0.5,
                )
                
                if is_found:
                    self.update_explainer(f"Found {search_val}!", GREEN)
                    self.play(
                        node_mobj[0].animate.set_color(GREEN),
                        run_time=0.5,
                    )
                else:
                    if search_val < node_key:
                        self.update_explainer(f"{search_val} < {node_key}\nGo left", WHITE)
                    else:
                        self.update_explainer(f"{search_val} > {node_key}\nGo right", WHITE)
                    self.wait(0.5)
                    self.play(
                        node_mobj[0].animate.set_color(BLUE),
                        run_time=0.4,
                    )
        
        self.wait(1.0)
        self.play(FadeOut(search_text), run_time=0.3)
        
        # Reset found node color
        for nid in search_path:
            if nid in prev_nodes and builder._nodes[nid].key == search_val:
                self.play(prev_nodes[nid][0].animate.set_color(BLUE), run_time=0.3)
        
        # 7. Complexity summary
        fade_outs = [FadeOut(self.explainer_panel), FadeOut(self.explainer_title)]
        if self.current_explainer:
            fade_outs.append(FadeOut(self.current_explainer))
        self.play(*fade_outs, run_time=0.3)
        
        # Fade out tree
        all_tree_mobjects = list(prev_nodes.values()) + list(prev_edges.values())
        self.play(*[FadeOut(m) for m in all_tree_mobjects], run_time=0.5)
        self.wait(0.3)
        
        # Show complexity summary
        complexity_title = Text("BST Time Complexity", font_size=36, disable_ligatures=True)
        complexity_title.next_to(title, DOWN, buff=0.8)
        self.play(Write(complexity_title), run_time=0.5)
        self.wait(0.3)
        
        complexity_items = VGroup(
            VGroup(Dot(color=GREEN), Text("Average: O(log n)", font_size=24, disable_ligatures=True)).arrange(RIGHT, buff=0.3),
            VGroup(Dot(color=YELLOW), Text("Worst (skewed): O(n)", font_size=24, disable_ligatures=True)).arrange(RIGHT, buff=0.3),
            VGroup(Dot(color=BLUE), Text("Height determines performance", font_size=24, disable_ligatures=True)).arrange(RIGHT, buff=0.3)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(complexity_title, DOWN, buff=0.8)
        
        for item in complexity_items:
            self.play(Write(item), run_time=0.5)
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
    
    def update_explainer_title(self, new_title):
        """Update the explainer panel title"""
        new_title_text = Text(new_title, font_size=16, color=YELLOW, disable_ligatures=True)
        new_title_text.move_to(self.explainer_panel.get_top() + DOWN * 0.25)
        self.play(Transform(self.explainer_title, new_title_text), run_time=0.3)
    
    def perform_deletion(self, builder, val, prev_state, prev_nodes, prev_edges, 
                        case_explanation, show_successor=False):
        """Perform and animate a deletion operation.
        
        Returns:
            Tuple of (new_state, new_nodes, new_edges)
        """
        delete_text = Text(f"Deleting: {val}", font_size=22, color=RED, disable_ligatures=True)
        delete_text.to_edge(DOWN)
        self.play(Write(delete_text), run_time=0.3)
        
        # Show traversal to find node
        search_path = builder.search_path(val)
        
        self.update_explainer(f"Finding {val}...", ORANGE)
        
        for i, nid in enumerate(search_path):
            if nid in prev_nodes:
                node_mobj = prev_nodes[nid]
                node_key = builder._nodes[nid].key
                is_target = (node_key == val)
                
                self.play(
                    node_mobj[0].animate.set_color(ORANGE),
                    run_time=0.5,
                )
                
                if is_target:
                    self.update_explainer(f"Found {val}\n{case_explanation}", RED)
                    self.play(
                        node_mobj[0].animate.set_color(RED),
                        run_time=0.5,
                    )
                    
                    # If showing successor (two children case), highlight it
                    if show_successor:
                        # Find inorder successor (leftmost in right subtree)
                        target_node = builder._nodes[nid]
                        if target_node.right is not None:
                            successor_id = target_node.right
                            successor = builder._nodes[successor_id]
                            while successor.left is not None:
                                successor_id = successor.left
                                successor = builder._nodes[successor_id]
                            
                            if successor_id in prev_nodes:
                                successor_text = Text(f"Successor: {successor.key}", font_size=14, color=GREEN, disable_ligatures=True)
                                successor_text.next_to(prev_nodes[successor_id], RIGHT, buff=0.2)
                                self.play(
                                    prev_nodes[successor_id][0].animate.set_color(GREEN),
                                    Write(successor_text),
                                    run_time=0.5,
                                )
                                self.wait(0.5)
                                self.play(FadeOut(successor_text), run_time=0.3)
                else:
                    if val < node_key:
                        self.update_explainer(f"{val} < {node_key}\nGo left", WHITE)
                    else:
                        self.update_explainer(f"{val} > {node_key}\nGo right", WHITE)
                    self.wait(0.3)
                    self.play(
                        node_mobj[0].animate.set_color(BLUE),
                        run_time=0.3,
                    )
        
        self.wait(0.5)
        
        # Perform deletion
        new_state, case = builder.delete_and_snapshot(val)
        
        # Animate transition
        new_nodes, new_edges = animate_bst_transition(
            self, prev_state, new_state, prev_nodes, prev_edges, run_time=1.0
        )
        
        self.update_explainer(f"Deleted {val}", GREEN)
        
        self.play(FadeOut(delete_text), run_time=0.3)
        
        return new_state, new_nodes, new_edges
