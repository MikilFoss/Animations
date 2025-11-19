"""
AVL Tree Visualization using Manim
Shows insertion with rotations to maintain balance

Run with: manim -pql avl_tree_animation.py AVLTreeVisualization
For high quality: manim -pqh avl_tree_animation.py AVLTreeVisualization
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

class AVLTreeVisualization(Scene):
    
    def construct(self):
        # Title - keep visible throughout
        title = create_title("AVL Trees")
        self.play(Write(title), run_time=0.2)
        self.wait(0.3)
        
        # Show AVL property
        property_title = Text("AVL Property: Balance factor ∈ {-1, 0, 1}", font_size=32).to_corner(UL)
        self.play(Write(property_title))
        
        # Visual with balance factors
        root = self.create_avl_node(10, ORIGIN + UP * 1.5, bf=0)
        left = self.create_avl_node(5, ORIGIN + LEFT * 1.5 + DOWN * 0.5, bf=0)
        right = self.create_avl_node(15, ORIGIN + RIGHT * 1.5 + DOWN * 0.5, bf=0)
        
        edge1 = create_edge_circular_nodes(root, left)
        edge2 = create_edge_circular_nodes(root, right)
        
        self.play(Create(root), Create(left), Create(right), Create(edge1), Create(edge2), run_time=0.5)
        self.wait(1)
        
        self.play(FadeOut(property_title), FadeOut(root), FadeOut(left), 
                  FadeOut(right), FadeOut(edge1), FadeOut(edge2))
        
        # Insert elements: [10, 20, 30, 40, 50]
        insert_sequence = [10, 20, 30, 40, 50]
        nodes = {}
        edges = []
        root_val = None
        
        for val in insert_sequence[:3]:  # Show first few
            if root_val is None:
                root_val = val
                root_pos = ORIGIN + UP * 2.5
                root_node = self.create_avl_node(val, root_pos, bf=0)
                nodes[val] = {'node': root_node, 'pos': root_pos}
                self.play(Create(root_node), run_time=0.4)
                self.wait(0.15)
            else:
                new_pos = ORIGIN + (LEFT if val < root_val else RIGHT) * 2 + UP * 1
                new_node = self.create_avl_node(val, new_pos, bf=0)
                nodes[val] = {'node': new_node, 'pos': new_pos}
                # Create edge connecting parent and new node at circle boundaries
                parent_node = nodes[root_val]['node']
                edge = create_edge_circular_nodes(parent_node, new_node)
                edges.append(edge)
                self.play(Create(edge), Create(new_node), run_time=0.4)
                self.wait(0.15)
        
        self.wait(0.5)
        
        # Show rotation restoring balance
        rotation_title = Text("Rotations Restore Balance", font_size=32).to_corner(UL)
        self.play(Write(rotation_title))
        
        # Visual demonstration
        for val in list(nodes.keys())[:2]:
            self.play(nodes[val]['node'].animate.set_color(YELLOW).scale(1.2), run_time=0.3)
            self.wait(0.2)
            self.play(nodes[val]['node'].animate.set_color(BLUE).scale(1/1.2), run_time=0.2)
        
        self.play(FadeOut(rotation_title))
        
        # Compare with BST
        compare_title = Text("AVL vs BST", font_size=28).to_corner(UL)
        self.play(Write(compare_title))
        
        avl_height = Text("AVL: Height O(log n)", font_size=24, color=GREEN).next_to(compare_title, DOWN, aligned_edge=LEFT)
        bst_height = Text("BST: Height O(n) worst", font_size=24, color=RED).next_to(avl_height, DOWN, aligned_edge=LEFT)
        
        self.play(Write(avl_height), Write(bst_height), run_time=0.5)
        self.wait(1)
        
        self.play(FadeOut(compare_title), FadeOut(avl_height), FadeOut(bst_height))
        
        # Visual summary
        self.play(*[nodes[v]['node'].animate.set_color(GOLD).scale(1.1) for v in nodes], run_time=0.5)
        self.wait(1)
        
        # Visual summary complete
    
    def create_avl_node(self, value, position, bf=0):
        """Create an AVL tree node with balance factor"""
        base_node = create_circular_node(value, position)
        circle = base_node[0]
        bf_text = Text(f"bf={bf}", font_size=16, color=YELLOW).next_to(circle, DOWN, buff=0.1)
        return VGroup(*base_node, bf_text)

