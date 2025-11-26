"""
Red-Black Tree Visualization using Manim
Shows insertion with color changes and rotations

Run with: manim -pql redblack_tree_animation.py RedBlackTreeVisualization
For high quality: manim -pqh redblack_tree_animation.py RedBlackTreeVisualization
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
from Trees.utils import create_circular_node, create_edge_circular_nodes

class RedBlackTreeVisualization(BaseTreeVisualization):
    
    def construct(self):
        # Title - keep visible throughout
        title = self.create_title_section("Red-Black Trees")
        
        # Show RB properties
        property_section = self.create_property_section(
            "Red-Black Properties",
            [("Black height balanced", GREEN)]
        )
        
        # Visual with colored nodes
        root = Circle(radius=0.4, color=BLACK, fill_opacity=1, fill_color=BLACK)
        root_text = Text("7", font_size=24, color=WHITE).move_to(root)
        root_node = VGroup(root, root_text).move_to(ORIGIN + UP * 1.5)
        
        left = Circle(radius=0.4, color=RED, fill_opacity=1, fill_color=RED)
        left_text = Text("3", font_size=24, color=WHITE).move_to(left)
        left_node = VGroup(left, left_text).move_to(ORIGIN + LEFT * 1.5 + DOWN * 0.5)
        
        edge = create_edge_circular_nodes(root_node, left_node)
        
        label = Text("Black height balanced", font_size=20, color=GREEN).next_to(root_node, UP)
        
        self.play(Create(root_node), Create(left_node), Create(edge), Write(label), run_time=0.5)
        self.wait(1)
        
        self.fade_out_group(property_section, root_node, left_node, edge, label)
        
        # Insert elements: [7, 3, 18, 10, 22, 8, 11, 26]
        insert_sequence = [7, 3, 18, 10, 22, 8, 11, 26]
        nodes = {}
        edges = []
        root_val = None
        
        for val in insert_sequence[:4]:  # Show first few insertions
            if root_val is None:
                root_val = val
                root_pos = ORIGIN + UP * 2.5
                root_node = self.create_rb_node(val, root_pos, is_red=False)
                nodes[val] = {'node': root_node, 'pos': root_pos}
                self.play(Create(root_node), run_time=0.4)
                self.wait(0.15)
            else:
                # Simple insertion visualization
                new_pos = ORIGIN + (LEFT if val < root_val else RIGHT) * 2 + UP * 1
                new_node = self.create_rb_node(val, new_pos, is_red=True)
                nodes[val] = {'node': new_node, 'pos': new_pos}
                # Create edge connecting parent and new node at circle boundaries
                parent_node = nodes[root_val]['node']
                edge = create_edge_circular_nodes(parent_node, new_node)
                edges.append(edge)
                self.play(Create(edge), Create(new_node), run_time=0.4)
                self.wait(0.15)
        
        self.wait(0.5)
        
        # Show rotation maintaining balance
        balance_title = Text("Rotations Maintain Balance", font_size=32).to_corner(UL)
        self.play(Write(balance_title))
        
        # Visual demonstration
        for val in list(nodes.keys())[:2]:
            self.play(nodes[val]['node'].animate.set_color(YELLOW).scale(1.2), run_time=0.3)
            self.wait(0.2)
            self.play(nodes[val]['node'].animate.set_color(BLUE).scale(1/1.2), run_time=0.2)
        
        self.play(FadeOut(balance_title))
        
        # Show complexity
        complexity = self.create_complexity_display("Worst-case height: O(log n)")
        self.wait(1)
        
        # Visual summary
        self.play(*[nodes[v]['node'].animate.set_color(GOLD).scale(1.1) for v in nodes], run_time=0.5)
        self.wait(1)
        
        # Visual summary complete
    
    def create_rb_node(self, value, position, is_red=True):
        """Create a red-black tree node"""
        color = RED if is_red else BLACK
        return create_circular_node(value, position, color=color, fill_opacity=1)

