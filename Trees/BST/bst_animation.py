"""
Binary Search Tree Visualization using Manim
Shows insertion and search operations

Run with: manim -pql bst_animation.py BSTVisualization
For high quality: manim -pqh bst_animation.py BSTVisualization
"""

from manim import *
import numpy as np
import sys
import os
# Add parent directory to path for utils import
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
from Trees.base_tree_visualization import BaseTreeVisualization
from Trees.tree_builder import BinaryTreeBuilder
from Trees.utils import create_circular_node, create_edge_circular_nodes

class BSTVisualization(BaseTreeVisualization):
    
    def construct(self):
        # Title - keep visible throughout
        title = self.create_title_section("Binary Search Trees")
        
        # Show BST property
        property_section = self.create_property_section(
            "BST Property: left < root < right",
            []
        )
        
        # Visual diagram showing property
        root_demo = create_circular_node(50, ORIGIN + UP * 1.5)
        left_demo = create_circular_node(30, ORIGIN + LEFT * 1.5 + DOWN * 0.5, color=GREEN)
        right_demo = create_circular_node(70, ORIGIN + RIGHT * 1.5 + DOWN * 0.5, color=GREEN)
        
        edge1 = create_edge_circular_nodes(root_demo, left_demo, color=GREEN)
        edge2 = create_edge_circular_nodes(root_demo, right_demo, color=GREEN)
        
        label_left = Text("30 < 50", font_size=20, color=GREEN).next_to(left_demo, DOWN, buff=0.2)
        label_right = Text("70 > 50", font_size=20, color=GREEN).next_to(right_demo, DOWN, buff=0.2)
        
        self.play(Create(root_demo), run_time=0.3)
        self.play(Create(edge1), Create(edge2), run_time=0.3)
        self.play(Create(left_demo), Create(right_demo), run_time=0.3)
        self.play(Write(label_left), Write(label_right), run_time=0.3)
        self.wait(1)
        
        self.fade_out_group(property_section, root_demo, left_demo, right_demo, 
                          edge1, edge2, label_left, label_right)
        
        # Insert elements: [50, 30, 70, 20, 40, 60, 80, 10, 25]
        insert_sequence = [50, 30, 70, 20, 40, 60, 80, 10, 25]
        tree = {}  # {value: {'node': mobject, 'left': value or None, 'right': value or None, 'pos': position}}
        edges = []
        root_val = None
        tree_builder = BinaryTreeBuilder()
        
        for val in insert_sequence:
            if root_val is None:
                root_val = val
                root_pos = ORIGIN + UP * 2.5
                root_node = create_circular_node(val, root_pos)
                tree[val] = {'node': root_node, 'left': None, 'right': None, 'pos': root_pos}
                self.play(Create(root_node), run_time=0.3)
                self.wait(0.2)
            else:
                new_node, new_pos, parent_val, is_left = tree_builder.insert_binary_node(
                    root_val, val, tree, 0, ORIGIN + UP * 2.5, root_pos=ORIGIN + UP * 2.5
                )
                if new_node:
                    tree[val] = {'node': new_node, 'left': None, 'right': None, 'pos': new_pos}
                    if is_left:
                        tree[parent_val]['left'] = val
                    else:
                        tree[parent_val]['right'] = val
                    # Create edge connecting parent and new node at circle boundaries
                    parent_node = tree[parent_val]['node']
                    edge = tree_builder.create_insertion_animation(self, new_node, parent_node)
                    edges.append(edge)
        
        self.wait(0.5)
        
        # Search for 25
        search_title = Text("Searching for 25", font_size=32).to_corner(UL)
        self.play(Write(search_title))
        
        # Highlight search path
        search_path = tree_builder.search_path(root_val, 25, tree)
        self.highlight_path(search_path, tree)
        
        # Keep 25 highlighted
        self.wait(0.5)
        self.play(tree[25]['node'].animate.set_color(GREEN).scale(1.2), run_time=0.3)
        self.wait(0.5)
        
        self.play(FadeOut(search_title))
        
        # Show complexity
        complexity = self.create_complexity_display("Search Complexity: O(log n)")
        self.wait(1)
        
        # Visual summary
        self.play(*[tree[v]['node'].animate.set_color(GOLD).scale(1.1) for v in tree], run_time=0.5)
        self.wait(1)
        
        # Visual summary complete
    
