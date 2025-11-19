"""
Shared utilities for tree visualizations
Provides common functions for creating nodes, edges, and configuring scenes
"""

from manim import *
import numpy as np

# Common configuration constants
MANIM_CONFIG = {
    'frame_rate': 60,
    'pixel_width': 1920,
    'pixel_height': 1080
}

def apply_manim_config():
    """Apply common Manim configuration to config object"""
    config.frame_rate = MANIM_CONFIG['frame_rate']
    config.pixel_width = MANIM_CONFIG['pixel_width']
    config.pixel_height = MANIM_CONFIG['pixel_height']


def create_circular_node(value, position, color=BLUE, radius=0.4, font_size=24, fill_opacity=0.3, stroke_width=2):
    """
    Create a circular tree node with a value
    
    Args:
        value: Value to display in the node
        position: Position (x, y, z) for the node
        color: Color of the circle (default: BLUE)
        radius: Radius of the circle (default: 0.4)
        font_size: Font size for the value text (default: 24)
        fill_opacity: Fill opacity of the circle (default: 0.3)
        stroke_width: Stroke width of the circle (default: 2)
    
    Returns:
        VGroup containing the circle and text
    """
    circle = Circle(radius=radius, color=color, fill_opacity=fill_opacity, fill_color=color, stroke_width=stroke_width)
    text = Text(str(value), font_size=font_size, color=WHITE)
    node = VGroup(circle, text).move_to(position)
    return node


def create_edge_circular_nodes(node1, node2, radius=0.4, stroke_width=3, color=WHITE):
    """
    Create an edge connecting two circular nodes at their boundaries
    
    Args:
        node1: First node (VGroup with circle as first element)
        node2: Second node (VGroup with circle as first element)
        radius: Radius of the circular nodes (default: 0.4)
        stroke_width: Width of the edge line (default: 3)
        color: Color of the edge (default: WHITE)
    
    Returns:
        Line object connecting the nodes at their boundaries
    """
    center1 = node1.get_center()
    center2 = node2.get_center()
    
    # Calculate direction vector
    direction = center2 - center1
    if np.linalg.norm(direction) == 0:
        return Line(center1, center2, stroke_width=stroke_width, color=color)
    
    direction_normalized = direction / np.linalg.norm(direction)
    
    # Calculate edge points on circle boundaries
    start_point = center1 + direction_normalized * radius
    end_point = center2 - direction_normalized * radius
    
    return Line(start_point, end_point, stroke_width=stroke_width, color=color)


def create_edge_rectangular_nodes(parent_node, child_node, stroke_width=2, color=WHITE):
    """
    Create an edge connecting two rectangular nodes (like B-tree nodes) at their boundaries
    
    Args:
        parent_node: Parent node (VGroup with Rectangle as first element)
        child_node: Child node (VGroup with Rectangle as first element)
        stroke_width: Width of the edge line (default: 2)
        color: Color of the edge (default: WHITE)
    
    Returns:
        Line object connecting the nodes at their boundaries
    """
    parent_rect = parent_node[0]  # Rectangle is first element
    child_rect = child_node[0]
    
    parent_center = parent_rect.get_center()
    child_center = child_rect.get_center()
    
    # Calculate direction
    direction = child_center - parent_center
    if np.linalg.norm(direction) == 0:
        return Line(parent_center, child_center, stroke_width=stroke_width, color=color)
    
    direction_normalized = direction / np.linalg.norm(direction)
    
    # Get rectangle dimensions (scaling is already applied to the rectangle)
    parent_height = parent_rect.get_height()
    child_height = child_rect.get_height()
    
    # Calculate edge points on rectangle boundaries
    parent_edge = parent_center + direction_normalized * (parent_height / 2)
    child_edge = child_center - direction_normalized * (child_height / 2)
    
    return Line(parent_edge, child_edge, stroke_width=stroke_width, color=color)


def create_title(title_text, font_size=48):
    """
    Create a title text positioned at the top edge
    
    Args:
        title_text: Text to display
        font_size: Font size (default: 48)
    
    Returns:
        Text object positioned at the top edge
    """
    return Text(title_text, font_size=font_size).to_edge(UP)


def create_edge_from_positions(pos1, pos2, radius=0.4, stroke_width=3, color=WHITE):
    """
    Create an edge connecting two positions (useful when nodes aren't created yet)
    
    Args:
        pos1: First position (numpy array or tuple)
        pos2: Second position (numpy array or tuple)
        radius: Radius to offset from positions (default: 0.4)
        stroke_width: Width of the edge line (default: 3)
        color: Color of the edge (default: WHITE)
    
    Returns:
        Line object connecting the positions
    """
    pos1 = np.array(pos1)
    pos2 = np.array(pos2)
    
    # Calculate direction vector
    direction = pos2 - pos1
    if np.linalg.norm(direction) == 0:
        return Line(pos1, pos2, stroke_width=stroke_width, color=color)
    
    direction_normalized = direction / np.linalg.norm(direction)
    
    # Calculate edge points offset by radius
    start_point = pos1 + direction_normalized * radius
    end_point = pos2 - direction_normalized * radius
    
    return Line(start_point, end_point, stroke_width=stroke_width, color=color)

