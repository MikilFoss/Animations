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
from Trees.utils import apply_manim_config, create_circular_node, create_edge_circular_nodes, create_title

apply_manim_config()

class BSTVisualization(Scene):
    
    def construct(self):
        # Title - keep visible throughout
        title = create_title("Binary Search Trees")
        self.play(Write(title), run_time=0.2)
        self.wait(0.3)
        
        # Show BST property
        property_title = Text("BST Property: left < root < right", font_size=32).to_corner(UL)
        self.play(Write(property_title))
        
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
        
        self.play(FadeOut(property_title), FadeOut(root_demo), FadeOut(left_demo), 
                  FadeOut(right_demo), FadeOut(edge1), FadeOut(edge2), 
                  FadeOut(label_left), FadeOut(label_right))
        
        # Insert elements: [50, 30, 70, 20, 40, 60, 80, 10, 25]
        insert_sequence = [50, 30, 70, 20, 40, 60, 80, 10, 25]
        tree = {}  # {value: {'node': mobject, 'left': value or None, 'right': value or None, 'pos': position}}
        edges = []
        root_val = None
        
        for val in insert_sequence:
            if root_val is None:
                root_val = val
                root_pos = ORIGIN + UP * 2.5
                root_node = create_circular_node(val, root_pos)
                tree[val] = {'node': root_node, 'left': None, 'right': None, 'pos': root_pos}
                self.play(Create(root_node), run_time=0.3)
                self.wait(0.2)
            else:
                new_node, new_pos, parent_val, is_left = self.insert_bst(root_val, val, tree, 0, ORIGIN + UP * 2.5)
                if new_node:
                    tree[val] = {'node': new_node, 'left': None, 'right': None, 'pos': new_pos}
                    if is_left:
                        tree[parent_val]['left'] = val
                    else:
                        tree[parent_val]['right'] = val
                    # Create edge connecting parent and new node at circle boundaries
                    parent_node = tree[parent_val]['node']
                    edge = create_edge_circular_nodes(parent_node, new_node)
                    edges.append(edge)
                    self.play(Create(edge), Create(new_node), run_time=0.4)
                    self.wait(0.15)
        
        self.wait(0.5)
        
        # Search for 25
        search_title = Text("Searching for 25", font_size=32).to_corner(UL)
        self.play(Write(search_title))
        
        # Highlight search path
        search_path = self.search_path(root_val, 25, tree)
        for i, val in enumerate(search_path):
            if val in tree:
                self.play(tree[val]['node'].animate.set_color(YELLOW).scale(1.3), run_time=0.3)
                self.wait(0.15)
                if i < len(search_path) - 1:
                    self.play(tree[val]['node'].animate.set_color(BLUE).scale(1/1.3), run_time=0.2)
        
        # Keep 25 highlighted
        self.wait(0.5)
        self.play(tree[25]['node'].animate.set_color(GREEN).scale(1.2), run_time=0.3)
        self.wait(0.5)
        
        self.play(FadeOut(search_title))
        
        # Show complexity
        complexity = Text("Search Complexity: O(log n)", font_size=28).to_corner(DR)
        self.play(Write(complexity), run_time=0.3)
        self.wait(1)
        
        # Visual summary
        self.play(*[tree[v]['node'].animate.set_color(GOLD).scale(1.1) for v in tree], run_time=0.5)
        self.wait(1)
        
        # Visual summary complete
    
    def insert_bst(self, current_val, new_val, tree, level, current_pos):
        """Insert value into BST recursively"""
        if new_val < current_val:
            if tree[current_val]['left'] is None:
                # Insert as left child
                spacing = 2.0 / (2 ** level)
                new_pos = current_pos + LEFT * spacing + DOWN * 1.2
                new_node = create_circular_node(new_val, new_pos)
                return new_node, new_pos, current_val, True
            else:
                left_pos = tree[tree[current_val]['left']]['pos']
                return self.insert_bst(tree[current_val]['left'], new_val, tree, level + 1, left_pos)
        elif new_val > current_val:
            if tree[current_val]['right'] is None:
                # Insert as right child
                spacing = 2.0 / (2 ** level)
                new_pos = current_pos + RIGHT * spacing + DOWN * 1.2
                new_node = create_circular_node(new_val, new_pos)
                return new_node, new_pos, current_val, False
            else:
                right_pos = tree[tree[current_val]['right']]['pos']
                return self.insert_bst(tree[current_val]['right'], new_val, tree, level + 1, right_pos)
        return None, None, None, None
    
    def search_path(self, current_val, target, tree):
        """Get search path for target value"""
        path = [current_val]
        if current_val == target:
            return path
        if target < current_val and tree[current_val]['left']:
            path.extend(self.search_path(tree[current_val]['left'], target, tree))
        elif target > current_val and tree[current_val]['right']:
            path.extend(self.search_path(tree[current_val]['right'], target, tree))
        return path
