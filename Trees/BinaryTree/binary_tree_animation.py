"""
Binary Tree Visualization using Manim
Shows building a binary tree from a sequence

Run with: manim -pql binary_tree_animation.py BinaryTreeVisualization
For high quality: manim -pqh binary_tree_animation.py BinaryTreeVisualization
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

class BinaryTreeVisualization(BaseTreeVisualization):
    
    def construct(self):
        # Title - keep visible throughout
        title = self.create_title_section("Binary Trees")
        
        # Build tree from sequence [1,2,3,4,5,6,7] - shorter visualization
        sequence = [1, 2, 3, 4, 5, 6, 7]
        
        # Create tree structure level by level - position it higher and more compact
        nodes = {}
        edges = []
        
        # Level 0: Root
        root = create_circular_node(1, ORIGIN + UP * 1.5)
        nodes[1] = root
        
        # Level 1: Nodes 2, 3
        node2 = create_circular_node(2, ORIGIN + LEFT * 2 + UP * 0.2)
        node3 = create_circular_node(3, ORIGIN + RIGHT * 2 + UP * 0.2)
        nodes[2] = node2
        nodes[3] = node3
        
        edge1 = create_edge_circular_nodes(root, node2)
        edge2 = create_edge_circular_nodes(root, node3)
        edges.extend([edge1, edge2])
        
        # Level 2: Nodes 4, 5, 6, 7
        node4 = create_circular_node(4, ORIGIN + LEFT * 3 + DOWN * 0.8)
        node5 = create_circular_node(5, ORIGIN + LEFT * 1 + DOWN * 0.8)
        node6 = create_circular_node(6, ORIGIN + RIGHT * 1 + DOWN * 0.8)
        node7 = create_circular_node(7, ORIGIN + RIGHT * 3 + DOWN * 0.8)
        nodes[4] = node4
        nodes[5] = node5
        nodes[6] = node6
        nodes[7] = node7
        
        edge3 = create_edge_circular_nodes(node2, node4)
        edge4 = create_edge_circular_nodes(node2, node5)
        edge5 = create_edge_circular_nodes(node3, node6)
        edge6 = create_edge_circular_nodes(node3, node7)
        edges.extend([edge3, edge4, edge5, edge6])
        
        # Create properties text first (but don't show yet)
        properties_title = Text("Binary Tree Properties", font_size=28, disable_ligatures=True).to_corner(UL, buff=0.3)
        
        prop1 = VGroup(
            Dot(color=GREEN, radius=0.08),
            Text("Max 2 children per node", font_size=20, disable_ligatures=True)
        ).arrange(RIGHT, buff=0.2).next_to(properties_title, DOWN, aligned_edge=LEFT, buff=0.2)
        
        prop2 = VGroup(
            Dot(color=GREEN, radius=0.08),
            Text("Hierarchical structure", font_size=20, disable_ligatures=True)
        ).arrange(RIGHT, buff=0.2).next_to(prop1, DOWN, aligned_edge=LEFT, buff=0.15)
        
        prop3 = VGroup(
            Dot(color=GREEN, radius=0.08),
            Text("Root at top, leaves at bottom", font_size=20, disable_ligatures=True)
        ).arrange(RIGHT, buff=0.2).next_to(prop2, DOWN, aligned_edge=LEFT, buff=0.15)
        
        # Show tree and properties simultaneously
        self.play(
            Create(root), 
            Create(edge1), Create(edge2),
            Create(node2), Create(node3),
            Create(edge3), Create(edge4), Create(edge5), Create(edge6),
            Create(node4), Create(node5), Create(node6), Create(node7),
            Write(properties_title),
            Write(prop1), Write(prop2), Write(prop3),
            run_time=1.0
        )
        self.wait(1.0)
        
        # Show statistics
        stats = VGroup(
            Text(f"Height: 3", font_size=24, disable_ligatures=True),
            Text(f"Nodes: 7", font_size=24, disable_ligatures=True),
            Text(f"Leaves: 4", font_size=24, disable_ligatures=True)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(DR, buff=0.3)
        
        self.play(Write(stats), run_time=0.3)
        self.wait(0.5)
        
        # Fade out properties and stats to make room for balanced comparisons
        self.fade_out_group(
            properties_title, prop1, prop2, prop3, stats,
            root, node2, node3, node4, node5, node6, node7,
            edge1, edge2, edge3, edge4, edge5, edge6
        )
        
        # Show comprehensive balanced tree comparisons
        balanced_title = Text("Types of Tree Balance", font_size=36, disable_ligatures=True).to_edge(UP, buff=0.5).shift(DOWN * 0.8)
        self.play(Write(balanced_title), run_time=0.3)
        self.wait(0.3)
        
        # 4 trees in a horizontal line
        node_radius = 0.15
        
        # X positions for 4 trees evenly spaced
        x_positions = [LEFT * 5.2, LEFT * 1.7, RIGHT * 1.7, RIGHT * 5.2]
        tree_base_y = DOWN * 0.6
        title_y = UP * 1.6
        
        # Complete - color GREEN
        complete_header = VGroup(
            Text("Complete", font_size=16, color=GREEN, disable_ligatures=True),
            Text("All levels filled except", font_size=11, color=GREEN_A, disable_ligatures=True),
            Text("last, filled left to right", font_size=11, color=GREEN_A, disable_ligatures=True)
        ).arrange(DOWN, buff=0.08).move_to(x_positions[0] + title_y)
        complete_tree = self.create_complete_tree_example(x_positions[0] + tree_base_y, node_radius=node_radius, node_color=GREEN)
        
        # Full - color BLUE
        full_header = VGroup(
            Text("Full", font_size=16, color=BLUE, disable_ligatures=True),
            Text("Every node has 0 or 2", font_size=11, color=BLUE_A, disable_ligatures=True),
            Text("children, never 1", font_size=11, color=BLUE_A, disable_ligatures=True)
        ).arrange(DOWN, buff=0.08).move_to(x_positions[1] + title_y)
        full_tree = self.create_full_tree_example(x_positions[1] + tree_base_y, node_radius=node_radius, node_color=BLUE)
        
        # Height-balanced - color PURPLE
        height_header = VGroup(
            Text("Height-Balanced", font_size=16, color=PURPLE, disable_ligatures=True),
            Text("Left/right subtree heights", font_size=11, color=PURPLE_A, disable_ligatures=True),
            Text("differ by at most 1 (AVL)", font_size=11, color=PURPLE_A, disable_ligatures=True)
        ).arrange(DOWN, buff=0.08).move_to(x_positions[2] + title_y)
        height_tree = self.create_height_balanced_example(x_positions[2] + tree_base_y, node_radius=node_radius, node_color=PURPLE)
        
        # Balanced - color ORANGE
        balanced_header = VGroup(
            Text("Balanced", font_size=16, color=ORANGE, disable_ligatures=True),
            Text("Height is O(log n)", font_size=11, color=GOLD_A, disable_ligatures=True)
        ).arrange(DOWN, buff=0.08).move_to(x_positions[3] + title_y)
        balanced_tree = self.create_balanced_tree_example(x_positions[3] + tree_base_y, node_radius=node_radius, node_color=ORANGE)
        
        # Show headers
        self.play(
            Write(complete_header), Write(full_header),
            Write(height_header), Write(balanced_header),
            run_time=0.5
        )
        self.wait(0.2)
        
        # Show trees
        self.play(
            *[Create(mob) for mob in complete_tree],
            *[Create(mob) for mob in full_tree],
            *[Create(mob) for mob in height_tree],
            *[Create(mob) for mob in balanced_tree],
            run_time=1.2
        )
        self.wait(2.0)
    
    def create_complete_tree_example(self, base_position, node_radius=0.4, node_color=BLUE):
        """Create a complete tree - all levels filled except last, filled left to right"""
        edges = []
        
        # Root
        root = create_circular_node(1, base_position + UP * 0.8, radius=node_radius, font_size=16, color=node_color)
        
        # Level 1 - both children
        node2 = create_circular_node(2, base_position + LEFT * 0.7, radius=node_radius, font_size=16, color=node_color)
        node3 = create_circular_node(3, base_position + RIGHT * 0.7, radius=node_radius, font_size=16, color=node_color)
        
        edge1 = create_edge_circular_nodes(root, node2, radius=node_radius)
        edge2 = create_edge_circular_nodes(root, node3, radius=node_radius)
        edges.extend([edge1, edge2])
        
        # Level 2 - filled left to right (4, 5, 6 - missing 7)
        node4 = create_circular_node(4, base_position + LEFT * 1.1 + DOWN * 0.7, radius=node_radius, font_size=16, color=node_color)
        node5 = create_circular_node(5, base_position + LEFT * 0.3 + DOWN * 0.7, radius=node_radius, font_size=16, color=node_color)
        node6 = create_circular_node(6, base_position + RIGHT * 0.3 + DOWN * 0.7, radius=node_radius, font_size=16, color=node_color)
        
        edge3 = create_edge_circular_nodes(node2, node4, radius=node_radius)
        edge4 = create_edge_circular_nodes(node2, node5, radius=node_radius)
        edge5 = create_edge_circular_nodes(node3, node6, radius=node_radius)
        edges.extend([edge3, edge4, edge5])
        
        return [root, node2, node3, node4, node5, node6, edge1, edge2, edge3, edge4, edge5]
    
    def create_full_tree_example(self, base_position, node_radius=0.4, node_color=BLUE):
        """Create a full tree - every node has 0 or 2 children"""
        edges = []
        
        # Root
        root = create_circular_node(1, base_position + UP * 0.8, radius=node_radius, font_size=16, color=node_color)
        
        # Level 1 - both children
        node2 = create_circular_node(2, base_position + LEFT * 0.7, radius=node_radius, font_size=16, color=node_color)
        node3 = create_circular_node(3, base_position + RIGHT * 0.7, radius=node_radius, font_size=16, color=node_color)
        
        edge1 = create_edge_circular_nodes(root, node2, radius=node_radius)
        edge2 = create_edge_circular_nodes(root, node3, radius=node_radius)
        edges.extend([edge1, edge2])
        
        # Level 2 - left has 2 children, right has 0 (leaf)
        node4 = create_circular_node(4, base_position + LEFT * 1.1 + DOWN * 0.7, radius=node_radius, font_size=16, color=node_color)
        node5 = create_circular_node(5, base_position + LEFT * 0.3 + DOWN * 0.7, radius=node_radius, font_size=16, color=node_color)
        
        edge3 = create_edge_circular_nodes(node2, node4, radius=node_radius)
        edge4 = create_edge_circular_nodes(node2, node5, radius=node_radius)
        edges.extend([edge3, edge4])
        
        return [root, node2, node3, node4, node5, edge1, edge2, edge3, edge4]
    
    def create_height_balanced_example(self, base_position, node_radius=0.4, node_color=BLUE):
        """Create a height-balanced (AVL) tree - subtree heights differ by at most 1"""
        edges = []
        
        # Root
        root = create_circular_node(5, base_position + UP * 0.8, radius=node_radius, font_size=16, color=node_color)
        
        # Level 1
        node2 = create_circular_node(3, base_position + LEFT * 0.7, radius=node_radius, font_size=16, color=node_color)
        node3 = create_circular_node(7, base_position + RIGHT * 0.7, radius=node_radius, font_size=16, color=node_color)
        
        edge1 = create_edge_circular_nodes(root, node2, radius=node_radius)
        edge2 = create_edge_circular_nodes(root, node3, radius=node_radius)
        edges.extend([edge1, edge2])
        
        # Level 2 - left subtree has 2, right has 1 (height diff = 1)
        node4 = create_circular_node(2, base_position + LEFT * 1.1 + DOWN * 0.7, radius=node_radius, font_size=16, color=node_color)
        node5 = create_circular_node(4, base_position + LEFT * 0.3 + DOWN * 0.7, radius=node_radius, font_size=16, color=node_color)
        node6 = create_circular_node(8, base_position + RIGHT * 0.7 + DOWN * 0.7, radius=node_radius, font_size=16, color=node_color)
        
        edge3 = create_edge_circular_nodes(node2, node4, radius=node_radius)
        edge4 = create_edge_circular_nodes(node2, node5, radius=node_radius)
        edge5 = create_edge_circular_nodes(node3, node6, radius=node_radius)
        edges.extend([edge3, edge4, edge5])
        
        return [root, node2, node3, node4, node5, node6, edge1, edge2, edge3, edge4, edge5]
    
    def create_balanced_tree_example(self, base_position, node_radius=0.4, node_color=BLUE):
        """Create a balanced tree - height is O(log n), not strictly height-balanced"""
        edges = []
        
        # Root
        root = create_circular_node(4, base_position + UP * 0.8, radius=node_radius, font_size=16, color=node_color)
        
        # Level 1
        node2 = create_circular_node(2, base_position + LEFT * 0.7, radius=node_radius, font_size=16, color=node_color)
        node3 = create_circular_node(6, base_position + RIGHT * 0.7, radius=node_radius, font_size=16, color=node_color)
        
        edge1 = create_edge_circular_nodes(root, node2, radius=node_radius)
        edge2 = create_edge_circular_nodes(root, node3, radius=node_radius)
        edges.extend([edge1, edge2])
        
        # Level 2 - slightly uneven but still O(log n)
        node4 = create_circular_node(1, base_position + LEFT * 1.1 + DOWN * 0.7, radius=node_radius, font_size=16, color=node_color)
        node5 = create_circular_node(5, base_position + RIGHT * 0.3 + DOWN * 0.7, radius=node_radius, font_size=16, color=node_color)
        node6 = create_circular_node(7, base_position + RIGHT * 1.1 + DOWN * 0.7, radius=node_radius, font_size=16, color=node_color)
        
        edge3 = create_edge_circular_nodes(node2, node4, radius=node_radius)
        edge4 = create_edge_circular_nodes(node3, node5, radius=node_radius)
        edge5 = create_edge_circular_nodes(node3, node6, radius=node_radius)
        edges.extend([edge3, edge4, edge5])
        
        return [root, node2, node3, node4, node5, node6, edge1, edge2, edge3, edge4, edge5]

