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

# Fast preview config (for development)
FAST_CONFIG = {
    'frame_rate': 30,
    'pixel_width': 1280,
    'pixel_height': 720
}

def apply_manim_config(fast=False):
    """
    Apply common Manim configuration to config object.
    
    Args:
        fast: If True, use fast preview settings (30fps, 720p). 
              If False, uses high quality defaults (60fps, 1080p).
              Note: When using manim quality flags (-ql, -qm, -qh), set fast=False
              to let manim handle quality, or use FAST_MODE=true for fastest preview.
    """
    if fast:
        # Force fast settings regardless of quality flags
        config.frame_rate = FAST_CONFIG['frame_rate']
        config.pixel_width = FAST_CONFIG['pixel_width']
        config.pixel_height = FAST_CONFIG['pixel_height']
    else:
        # Set high quality defaults
        # Note: These will be overridden by manim's -ql/-qm/-qh flags during rendering
        # To use manim's quality flags effectively, they should be set before this call
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
    text = Text(str(value), font_size=font_size, color=WHITE, disable_ligatures=True)
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
    return Text(title_text, font_size=font_size, disable_ligatures=True).to_edge(UP)


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


def calculate_binary_tree_position(parent_pos, level, is_left, base_spacing=2.0, level_spacing=1.2):
    """
    Calculate position for a binary tree node relative to its parent
    
    Args:
        parent_pos: Parent node position (numpy array)
        level: Level in the tree (0 = root)
        is_left: True if left child, False if right child
        base_spacing: Base horizontal spacing (default: 2.0)
        level_spacing: Vertical spacing between levels (default: 1.2)
    
    Returns:
        numpy array representing the new position
    """
    spacing = base_spacing / (2 ** level)
    direction = LEFT if is_left else RIGHT
    new_pos = parent_pos + direction * spacing + DOWN * level_spacing
    return np.array(new_pos)


def calculate_tree_level_position(idx, base_y=2.0, level_spacing=1.3, horizontal_spacing=1.8):
    """
    Calculate position for a node in a complete binary tree using array index
    
    Args:
        idx: Array index (0-based)
        base_y: Base Y position for root (default: 2.0)
        level_spacing: Vertical spacing between levels (default: 1.3)
        horizontal_spacing: Horizontal spacing between nodes (default: 1.8)
    
    Returns:
        numpy array representing the position
    """
    level = int(np.log2(idx + 1))
    pos_in_level = idx - (2 ** level - 1)
    total_in_level = 2 ** level
    x_offset = (pos_in_level - total_in_level / 2 + 0.5) * horizontal_spacing
    y_pos = base_y - level * level_spacing
    return np.array([x_offset, y_pos, 0])


def animate_search_path(scene, path, nodes_dict, highlight_color=YELLOW, 
                        default_color=BLUE, scale_factor=1.3, wait_time=0.15):
    """
    Animate highlighting a search path through nodes
    
    Args:
        scene: Manim Scene object
        path: List of node identifiers
        nodes_dict: Dictionary mapping identifiers to node data
        highlight_color: Color for highlighting (default: YELLOW)
        default_color: Default node color (default: BLUE)
        scale_factor: Scale factor for highlighting (default: 1.3)
        wait_time: Wait time between highlights (default: 0.15)
    """
    for i, node_id in enumerate(path):
        if node_id in nodes_dict:
            node_data = nodes_dict[node_id]
            if isinstance(node_data, dict) and 'node' in node_data:
                node = node_data['node']
            else:
                node = node_data
            
            scene.play(node.animate.set_color(highlight_color).scale(scale_factor), run_time=0.3)
            scene.wait(wait_time)
            
            if i < len(path) - 1:
                scene.play(node.animate.set_color(default_color).scale(1/scale_factor), run_time=0.2)

