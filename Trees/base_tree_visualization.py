"""
Base class for tree visualizations
Provides common initialization, setup, and utility methods
"""

from manim import *
import sys
import os
from Trees.utils import apply_manim_config, create_title

class BaseTreeVisualization(Scene):
    """Base class for tree visualizations with common setup and utilities"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_paths()
        self.setup_config()
    
    def setup_paths(self):
        """Set up import paths for utils"""
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if parent_dir not in sys.path:
            sys.path.insert(0, parent_dir)
    
    def setup_config(self):
        """Apply Manim configuration"""
        fast_mode = os.getenv('FAST_MODE', 'False').lower() == 'true'
        apply_manim_config(fast=fast_mode)
    
    def create_title_section(self, title_text, font_size=48):
        """Create and display title section"""
        title = create_title(title_text, font_size=font_size)
        self.play(Write(title), run_time=0.2)
        self.wait(0.3)
        return title
    
    def create_property_section(self, title_text, properties, position=UL, title_font_size=32):
        """
        Create a property explanation section
        
        Args:
            title_text: Title for the property section
            properties: List of property strings or tuples (text, color)
            position: Corner position (UL, UR, DL, DR)
            title_font_size: Font size for title
        
        Returns:
            VGroup containing all property elements
        """
        property_title = Text(title_text, font_size=title_font_size).to_corner(position)
        self.play(Write(property_title))
        
        property_items = []
        for prop in properties:
            if isinstance(prop, tuple):
                text, color = prop
            else:
                text, color = prop, WHITE
            
            prop_text = Text(text, font_size=24, color=color)
            property_items.append(prop_text)
        
        if property_items:
            prop_group = VGroup(*property_items).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            prop_group.next_to(property_title, DOWN, aligned_edge=LEFT, buff=0.3)
            self.play(*[Write(item) for item in property_items], run_time=0.5)
        
        return VGroup(property_title, *property_items)
    
    def create_complexity_display(self, complexity_text, position=DR, font_size=28):
        """
        Create complexity information display
        
        Args:
            complexity_text: Text to display
            position: Corner position
            font_size: Font size
        
        Returns:
            Text object
        """
        complexity = Text(complexity_text, font_size=font_size).to_corner(position)
        self.play(Write(complexity), run_time=0.3)
        return complexity
    
    def highlight_path(self, path, nodes_dict, highlight_color=YELLOW, 
                       default_color=BLUE, scale_factor=1.3, wait_time=0.15):
        """
        Highlight a path through nodes
        
        Args:
            path: List of node identifiers (values or IDs)
            nodes_dict: Dictionary mapping identifiers to node data
            highlight_color: Color for highlighting
            default_color: Default node color
            scale_factor: Scale factor for highlighting
            wait_time: Wait time between highlights
        """
        for i, node_id in enumerate(path):
            if node_id in nodes_dict:
                node_data = nodes_dict[node_id]
                if isinstance(node_data, dict) and 'node' in node_data:
                    node = node_data['node']
                else:
                    node = node_data
                
                self.play(node.animate.set_color(highlight_color).scale(scale_factor), run_time=0.3)
                self.wait(wait_time)
                
                if i < len(path) - 1:
                    self.play(node.animate.set_color(default_color).scale(1/scale_factor), run_time=0.2)
    
    def fade_out_group(self, *mobjects, run_time=0.3):
        """Fade out multiple mobjects"""
        self.play(*[FadeOut(mob) for mob in mobjects if mob is not None], run_time=run_time)


