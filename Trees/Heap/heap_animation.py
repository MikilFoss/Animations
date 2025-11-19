"""
Heap Visualization using Manim
Shows max-heap insertion, extraction, and heapify operations

Run with: manim -pql heap_animation.py HeapVisualization
For high quality: manim -pqh heap_animation.py HeapVisualization
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

class HeapVisualization(Scene):
    
    def construct(self):
        # Title - keep visible throughout
        title = create_title("Heaps")
        self.play(Write(title), run_time=0.2)
        self.wait(0.3)
        
        # Show heap property - keep this longer
        property_title = Text("Heap Property", font_size=32).to_corner(UL)
        self.play(Write(property_title))
        
        # Visual diagram - single parent-child example
        parent = create_circular_node(10, ORIGIN + UP * 1.5, color=GREEN)
        left_child = create_circular_node(5, ORIGIN + LEFT * 1.5 + DOWN * 0.5, color=BLUE)
        right_child = create_circular_node(7, ORIGIN + RIGHT * 1.5 + DOWN * 0.5, color=BLUE)
        
        edge1 = create_edge_circular_nodes(parent, left_child, color=GREEN)
        edge2 = create_edge_circular_nodes(parent, right_child, color=GREEN)
        
        label1 = Text("Max-Heap: parent >= children", font_size=24, color=GREEN).next_to(parent, UP, buff=0.3)
        label2 = Text("10 >= 5 and 10 >= 7", font_size=22, color=YELLOW).next_to(parent, DOWN, buff=0.5)
        label3 = Text("Complete binary tree structure", font_size=22, color=YELLOW).next_to(label2, DOWN, buff=0.2)
        
        self.play(Create(parent), run_time=0.4)
        self.wait(0.3)
        self.play(Write(label1), run_time=0.4)
        self.wait(0.4)
        self.play(Create(edge1), Create(edge2), run_time=0.4)
        self.wait(0.3)
        self.play(Create(left_child), Create(right_child), run_time=0.4)
        self.wait(0.3)
        self.play(Write(label2), run_time=0.4)
        self.wait(0.4)
        self.play(Write(label3), run_time=0.4)
        self.wait(2.0)  # Keep this explainer longer
        
        self.play(FadeOut(property_title), FadeOut(parent), FadeOut(left_child), 
                  FadeOut(right_child), FadeOut(edge1), FadeOut(edge2), 
                  FadeOut(label1), FadeOut(label2), FadeOut(label3))
        
        # Build max-heap from [4, 10, 3, 5, 1, 8, 7]
        insert_title = Text("Insertion: Building a max-heap", font_size=28).to_corner(UL)
        self.play(Write(insert_title))
        
        values = [4, 10, 3, 5, 1, 8, 7]
        heap = []
        nodes = {}  # {idx: node_mobject} - track by position index
        edges = []  # List of edge mobjects
        
        def get_position(idx):
            """Calculate position for node at index idx"""
            level = int(np.log2(idx + 1))
            pos_in_level = idx - (2 ** level - 1)
            total_in_level = 2 ** level
            x_offset = (pos_in_level - total_in_level / 2 + 0.5) * 1.8
            y_pos = 2.0 - level * 1.3
            return np.array([x_offset, y_pos, 0])
        
        def update_node_value(node, new_val):
            """Update the value displayed in a node"""
            text = node[1]
            new_text = Text(str(new_val), font_size=24, color=WHITE)
            new_text.move_to(text.get_center())
            return Transform(text, new_text)
        
        for val in values:
            insert_val_text = Text(f"Inserting: {val}", font_size=24, color=YELLOW).to_edge(DOWN)
            self.play(Write(insert_val_text), run_time=0.3)
            self.wait(0.2)
            
            # Add to heap
            heap.append(val)
            idx = len(heap) - 1
            
            # Calculate position and create node
            position = get_position(idx)
            node = create_circular_node(val, position, color=BLUE)
            nodes[idx] = node
            
            # Show node being added
            self.play(Create(node), run_time=0.4)
            self.wait(0.2)
            
            # Connect to parent and heapify up
            if idx > 0:
                parent_idx = (idx - 1) // 2
                
                # Create edge
                edge = create_edge_circular_nodes(nodes[parent_idx], node)
                edges.append(edge)
                self.play(Create(edge), run_time=0.3)
                self.wait(0.2)
                
                # Heapify up if needed
                current_idx = idx
                while current_idx > 0:
                    parent_idx = (current_idx - 1) // 2
                    if heap[parent_idx] < heap[current_idx]:
                        # Swap needed
                        self.play(
                            nodes[current_idx].animate.set_color(RED),
                            nodes[parent_idx].animate.set_color(RED),
                            run_time=0.3
                        )
                        self.wait(0.2)
                        
                        # Swap values in heap array
                        heap[parent_idx], heap[current_idx] = heap[current_idx], heap[parent_idx]
                        
                        # Update displayed values in nodes (nodes stay at their positions)
                        self.play(
                            update_node_value(nodes[parent_idx], heap[parent_idx]),
                            update_node_value(nodes[current_idx], heap[current_idx]),
                            run_time=0.4
                        )
                        
                        self.play(
                            nodes[current_idx].animate.set_color(BLUE),
                            nodes[parent_idx].animate.set_color(BLUE),
                            run_time=0.2
                        )
                        self.wait(0.2)
                        
                        current_idx = parent_idx
                    else:
                        break
            
            self.play(FadeOut(insert_val_text), run_time=0.2)
            self.wait(0.2)
        
        self.play(FadeOut(insert_title))
        self.wait(0.5)
        
        # Extract max operation
        extract_title = Text("Extraction: Removing maximum element", font_size=28).to_corner(UL)
        self.play(Write(extract_title))
        
        extract_text = Text("Extracting maximum (root)", font_size=24, color=YELLOW).to_edge(DOWN)
        self.play(Write(extract_text), run_time=0.3)
        
        # Find root (value at index 0)
        max_val = heap[0]
        max_node = nodes[0]
        
        # Highlight root
        self.play(max_node.animate.set_color(RED).scale(1.2), run_time=0.4)
        self.wait(0.5)
        
        # Move last element to root
        last_val = heap[-1]
        last_idx = len(heap) - 1
        last_node = nodes[last_idx]
        
        swap_text = Text(f"Moving last element ({last_val}) to root", font_size=22, color=YELLOW).to_edge(DOWN)
        self.play(Transform(extract_text, swap_text), run_time=0.3)
        
        # Update root value and fade out last node
        self.play(
            max_node.animate.set_opacity(0.3).scale(1/1.2),
            update_node_value(max_node, last_val),
            last_node.animate.set_opacity(0.3),
            run_time=0.6
        )
        self.wait(0.4)
        
        # Remove max from heap
        heap[0] = heap[-1]
        heap.pop()
        
        # Remove last node from tracking
        self.remove(nodes[last_idx])
        del nodes[last_idx]
        
        # Heapify down
        heapify_text = Text("Heapifying down to restore property", font_size=22, color=YELLOW).to_edge(DOWN)
        self.play(Transform(extract_text, heapify_text), run_time=0.3)
        
        current_idx = 0
        while True:
            left_idx = 2 * current_idx + 1
            right_idx = 2 * current_idx + 2
            largest_idx = current_idx
            
            if left_idx < len(heap) and heap[left_idx] > heap[largest_idx]:
                largest_idx = left_idx
            
            if right_idx < len(heap) and heap[right_idx] > heap[largest_idx]:
                largest_idx = right_idx
            
            if largest_idx != current_idx:
                # Swap needed
                self.play(
                    nodes[current_idx].animate.set_color(RED),
                    nodes[largest_idx].animate.set_color(RED),
                    run_time=0.3
                )
                self.wait(0.2)
                
                # Swap values in heap array
                heap[current_idx], heap[largest_idx] = heap[largest_idx], heap[current_idx]
                
                # Update displayed values in nodes (nodes stay at their positions)
                self.play(
                    update_node_value(nodes[current_idx], heap[current_idx]),
                    update_node_value(nodes[largest_idx], heap[largest_idx]),
                    run_time=0.4
                )
                
                self.play(
                    nodes[current_idx].animate.set_color(BLUE),
                    nodes[largest_idx].animate.set_color(BLUE),
                    run_time=0.2
                )
                self.wait(0.2)
                
                current_idx = largest_idx
            else:
                break
        
        self.play(FadeOut(extract_title), FadeOut(extract_text))
        self.wait(0.5)
        
        # Show array representation vs tree visualization
        array_title = Text("Array Representation", font_size=28).to_corner(UL)
        self.play(Write(array_title))
        
        array_label = Text("Heap stored as array: [parent, left_child, right_child, ...]", 
                          font_size=20, color=YELLOW).to_edge(DOWN, buff=0.5)
        self.play(Write(array_label), run_time=0.3)
        
        array_visual = VGroup(*[
            VGroup(
                Text(str(v), font_size=22),
                Rectangle(width=0.7, height=0.7, color=BLUE, stroke_width=2)
            ).arrange(IN)
            for v in heap
        ]).arrange(RIGHT, buff=0.15).next_to(array_label, UP, buff=0.3)
        
        self.play(Write(array_visual), run_time=0.6)
        self.wait(1.5)
        
        self.play(FadeOut(array_title), FadeOut(array_label), FadeOut(array_visual))
        self.wait(0.5)
        
        # Visual summary complete
    
    
