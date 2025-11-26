"""
QuickHull Algorithm Visualization using Manim
Shows the divide-and-conquer approach with pruning

Run with: manim -pql quickhull_animation.py QuickHullVisualization
For high quality: manim -pqh quickhull_animation.py QuickHullVisualization
"""

from manim import *
import numpy as np
import sys
import os
# Add root directory to path for typography import
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)
from typography import DocText

# Set to True for faster rendering during development (30fps, 720p)
FAST_MODE = os.getenv('FAST_MODE', 'False').lower() == 'true'
if FAST_MODE:
    config.frame_rate = 30
    config.pixel_width = 1280
    config.pixel_height = 720
else:
    config.frame_rate = 60
    config.pixel_width = 1920
    config.pixel_height = 1080

class QuickHullVisualization(Scene):
    
    def construct(self):
        # Title
        title = DocText("QuickHull Algorithm", font_size=48).to_edge(UP)
        subtitle = DocText("Divide & Conquer with Aggressive Pruning", font_size=28).next_to(title, DOWN)
        self.play(Write(title), Write(subtitle))
        self.wait(0.165)
        self.play(FadeOut(title), FadeOut(subtitle))
        
        # Create a nice set of points that will show pruning well
        points_coords = self.generate_interesting_points()
        
        # Scale and center points
        points_coords = self.scale_points(points_coords)
        
        # Create point objects
        points = VGroup(*[
            Dot(point=np.array([x, y, 0]), radius=0.08, color=BLUE)
            for x, y in points_coords
        ])
        
        self.play(Create(points), run_time=0.335)
        self.wait(0.165)
        
        # Add title for this step
        step_title = DocText("Step 0: Find Extreme Points", font_size=32).to_corner(UL)
        self.play(Write(step_title))
        
        # Find and highlight LEFT and RIGHT
        left_idx = np.argmin([p[0] for p in points_coords])
        right_idx = np.argmax([p[0] for p in points_coords])
        
        left_point = points[left_idx]
        right_point = points[right_idx]
        
        left_label = DocText("LEFT", font_size=24, color=GREEN).next_to(left_point, DOWN)
        right_label = DocText("RIGHT", font_size=24, color=GREEN).next_to(right_point, DOWN)
        
        self.play(
            left_point.animate.set_color(GREEN).scale(1.5),
            right_point.animate.set_color(GREEN).scale(1.5),
            Write(left_label),
            Write(right_label)
        )
        self.wait(0.165)
        
        # Draw baseline
        baseline = Line(
            left_point.get_center(),
            right_point.get_center(),
            color=GREEN,
            stroke_width=4
        )
        baseline_label = DocText("Baseline", font_size=20, color=GREEN).move_to(
            (left_point.get_center() + right_point.get_center()) / 2 + DOWN * 0.5
        )
        self.play(Create(baseline), Write(baseline_label))
        self.wait(0.165)
        
        # Partition into above and below
        self.play(FadeOut(step_title))
        partition_title = DocText("Partition: Above & Below Baseline", font_size=32).to_corner(UL)
        self.play(Write(partition_title))
        
        above_points = []
        below_points = []
        
        for i, (x, y) in enumerate(points_coords):
            if i == left_idx or i == right_idx:
                continue
            
            if self.point_above_line(
                (x, y),
                points_coords[left_idx],
                points_coords[right_idx]
            ) > 0:
                above_points.append((i, x, y))
                self.play(points[i].animate.set_color(YELLOW), run_time=0.017)
            else:
                below_points.append((i, x, y))
                self.play(points[i].animate.set_color(PURPLE), run_time=0.017)
        
        self.wait(0.165)
        
        # Now solve upper hull recursively
        self.play(FadeOut(partition_title))
        upper_title = DocText("Solving Upper Hull (Above Baseline)", font_size=32).to_corner(UL)
        self.play(Write(upper_title))
        
        # Fade out below points temporarily
        below_indices = [i for i, _, _ in below_points]
        self.play(*[points[i].animate.set_opacity(0.2) for i in below_indices])
        self.wait(0.085)
        
        # Recursively solve upper hull with animation
        hull_points = [left_idx, right_idx]
        hull_points_upper = self.animated_quickhull(
            points, points_coords, above_points,
            left_idx, right_idx,
            points_coords[left_idx], points_coords[right_idx],
            depth=0, color=YELLOW, is_upper_hull=True
        )
        hull_points.extend(hull_points_upper)
        
        self.wait(0.165)
        
        # Now solve lower hull
        self.play(FadeOut(upper_title))
        lower_title = DocText("Solving Lower Hull (Below Baseline)", font_size=32).to_corner(UL)
        self.play(Write(lower_title))
        
        # Fade out above points, restore below
        above_indices = [i for i, _, _ in above_points]
        self.play(
            *[points[i].animate.set_opacity(0.2) for i in above_indices],
            *[points[i].animate.set_opacity(1.0) for i in below_indices]
        )
        self.wait(0.085)
        
        hull_points_lower = self.animated_quickhull(
            points, points_coords, below_points,
            right_idx, left_idx,  # Note: reversed for lower hull
            points_coords[right_idx], points_coords[left_idx],
            depth=0, color=PURPLE
        )
        hull_points.extend(hull_points_lower)
        
        self.wait(0.165)
        
        # Show final convex hull
        self.play(FadeOut(lower_title), FadeOut(baseline_label))
        final_title = DocText("Final Convex Hull", font_size=36, color=GOLD).to_corner(UL)
        self.play(Write(final_title))
        
        # Restore all points visibility
        self.play(*[points[i].animate.set_opacity(1.0) for i in range(len(points))])
        self.wait(0.085)
        
        # Highlight hull points
        self.play(*[
            points[i].animate.set_color(GOLD).scale(1.3)
            for i in hull_points
        ])
        
        # Draw hull polygon
        hull_coords_ordered = self.order_hull_points(
            [points_coords[i] for i in hull_points],
            points_coords[left_idx]
        )
        
        hull_polygon = Polygon(
            *[np.array([x, y, 0]) for x, y in hull_coords_ordered],
            color=GOLD,
            stroke_width=6,
            fill_opacity=0.1,
            fill_color=GOLD
        )
        
        self.play(Create(hull_polygon), run_time=0.335)
        self.wait(0.165)
        
        # Show statistics
        stats = VGroup(
            DocText(f"Total Points: {len(points_coords)}", font_size=24),
            DocText(f"Hull Points: {len(hull_points)}", font_size=24),
            DocText(f"Pruned: {len(points_coords) - len(hull_points)}", font_size=24, color=RED)
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(DR)
        
        self.play(Write(stats))
        self.wait(0.335)
        
        # Fade out everything
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        
        # Final message
        end_text = DocText("QuickHull: Θ(N log N) average case", font_size=36)
        self.play(Write(end_text))
        self.wait(0.5)
    
    def animated_quickhull(self, points, points_coords, point_list, 
                          p1_idx, p2_idx, p1_coord, p2_coord, 
                          depth=0, color=YELLOW, is_upper_hull=False):
        """
        Recursively solve QuickHull with animation
        Returns list of hull point indices
        """
        if not point_list:
            return []
        
        # Speed multiplier based on depth - animations get faster as we go deeper
        base_speed_multiplier = 0.6 ** depth
        
        # Adjust speed for upper hull: depth 0 = 8x slower, depth 1 = 8x slower, depth 2 = 1.5x slower
        if is_upper_hull:
            if depth == 0:
                speed_multiplier = base_speed_multiplier * 8.0
            elif depth == 1:
                speed_multiplier = base_speed_multiplier * 8.0
            elif depth == 2:
                speed_multiplier = base_speed_multiplier * 1.5
            else:
                speed_multiplier = base_speed_multiplier
        else:
            speed_multiplier = base_speed_multiplier
        
        # Minimum wait time to avoid frame rate issues (60 FPS = 0.0167s minimum)
        min_wait = 0.017
        
        # Find PMAX (farthest from line)
        max_dist = -1
        pmax_idx = None
        pmax_coord = None
        
        for i, x, y in point_list:
            dist = abs(self.point_above_line((x, y), p1_coord, p2_coord))
            if dist > max_dist:
                max_dist = dist
                pmax_idx = i
                pmax_coord = (x, y)
        
        if pmax_idx is None:
            return []
        
        # Highlight PMAX
        pmax_point = points[pmax_idx]
        pmax_label = DocText("PMAX", font_size=20, color=RED).next_to(pmax_point, UP, buff=0.2)
        
        self.play(
            pmax_point.animate.set_color(RED).scale(1.4),
            Write(pmax_label),
            run_time=max(0.085 * speed_multiplier, min_wait)
        )
        self.wait(max(0.05 * speed_multiplier, min_wait))
        
        # Draw triangle (P1, PMAX, P2)
        triangle = Polygon(
            np.array([p1_coord[0], p1_coord[1], 0]),
            np.array([pmax_coord[0], pmax_coord[1], 0]),
            np.array([p2_coord[0], p2_coord[1], 0]),
            color=RED,
            stroke_width=3,
            fill_opacity=0.1,
            fill_color=RED
        )
        self.play(Create(triangle), run_time=max(0.085 * speed_multiplier, min_wait))
        self.wait(max(0.05 * speed_multiplier, min_wait))
        
        # Partition points: find those outside triangle
        outside_left = []
        outside_right = []
        inside_indices = []
        
        for i, x, y in point_list:
            if i == pmax_idx:
                continue
            
            # Check if point is inside triangle
            if self.point_in_triangle((x, y), p1_coord, pmax_coord, p2_coord):
                inside_indices.append(i)
            else:
                # Determine which side of PMAX
                if self.point_above_line((x, y), p1_coord, pmax_coord) > 0:
                    outside_left.append((i, x, y))
                elif self.point_above_line((x, y), pmax_coord, p2_coord) > 0:
                    outside_right.append((i, x, y))
                else:
                    inside_indices.append(i)
        
        # Animate pruning (fade out inside points)
        if inside_indices:
            prune_text = DocText(f"Prune {len(inside_indices)} interior points", 
                            font_size=20, color=RED).to_edge(DOWN)
            self.play(Write(prune_text), run_time=max(0.05 * speed_multiplier, min_wait))
            self.play(
                *[points[i].animate.set_opacity(0.2).scale(0.7) for i in inside_indices],
                run_time=max(0.085 * speed_multiplier, min_wait)
            )
            self.play(FadeOut(prune_text), run_time=max(0.05 * speed_multiplier, min_wait))
        
        self.wait(max(0.05 * speed_multiplier, min_wait))
        
        # Clean up triangle and label for recursion
        self.play(FadeOut(triangle), FadeOut(pmax_label), run_time=max(0.05 * speed_multiplier, min_wait))
        
        # Recurse on left side
        hull_left = []
        if outside_left:
            hull_left = self.animated_quickhull(
                points, points_coords, outside_left,
                p1_idx, pmax_idx, p1_coord, pmax_coord,
                depth + 1, color, is_upper_hull
            )
        
        # Recurse on right side
        hull_right = []
        if outside_right:
            hull_right = self.animated_quickhull(
                points, points_coords, outside_right,
                pmax_idx, p2_idx, pmax_coord, p2_coord,
                depth + 1, color, is_upper_hull
            )
        
        # Return all hull points found
        return hull_left + [pmax_idx] + hull_right
    
    def generate_interesting_points(self):
        """Generate a set of points that shows pruning well"""
        np.random.seed(42)
        points = []
        
        # Outer ring (will be on hull)
        for angle in np.linspace(0, 2*np.pi, 16, endpoint=False):
            r = 3 + np.random.uniform(-0.2, 0.2)
            x = r * np.cos(angle)
            y = r * np.sin(angle)
            points.append((x, y))
        
        # Inner points (will be pruned)
        for _ in range(40):
            r = np.random.uniform(0.5, 2.5)
            angle = np.random.uniform(0, 2*np.pi)
            x = r * np.cos(angle)
            y = r * np.sin(angle)
            points.append((x, y))
        
        # A few more on outer ring
        for angle in np.linspace(0.1, 2*np.pi, 12, endpoint=False):
            r = 3.2
            x = r * np.cos(angle)
            y = r * np.sin(angle)
            points.append((x, y))
        
        # Additional scattered points
        for _ in range(20):
            r = np.random.uniform(1.5, 2.8)
            angle = np.random.uniform(0, 2*np.pi)
            x = r * np.cos(angle)
            y = r * np.sin(angle)
            points.append((x, y))
        
        return points
    
    def scale_points(self, points, target_width=7):
        """Scale points to fit in scene"""
        points = np.array(points)
        
        # Center at origin
        center = points.mean(axis=0)
        points = points - center
        
        # Scale to target width
        max_extent = np.max(np.abs(points))
        scale = (target_width / 2) / max_extent
        points = points * scale
        
        return points.tolist()
    
    def point_above_line(self, point, line_start, line_end):
        """
        Compute signed distance from point to line
        Positive = above, Negative = below, 0 = on line
        """
        x, y = point
        x1, y1 = line_start
        x2, y2 = line_end
        
        return (x2 - x1) * (y - y1) - (y2 - y1) * (x - x1)
    
    def point_in_triangle(self, point, v1, v2, v3):
        """Check if point is inside triangle using barycentric coordinates"""
        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
        
        d1 = sign(point, v1, v2)
        d2 = sign(point, v2, v3)
        d3 = sign(point, v3, v1)
        
        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
        
        return not (has_neg and has_pos)
    
    def order_hull_points(self, hull_coords, start_point):
        """Order hull points counterclockwise from start_point"""
        # Compute centroid
        centroid = np.mean(hull_coords, axis=0)
        
        # Compute angles from centroid
        def angle_from_centroid(point):
            return np.arctan2(point[1] - centroid[1], point[0] - centroid[0])
        
        # Sort by angle
        hull_with_angles = [(p, angle_from_centroid(p)) for p in hull_coords]
        hull_with_angles.sort(key=lambda x: x[1])
        
        return [p for p, _ in hull_with_angles]


class QuickHullStepByStep(Scene):
    """Alternative scene with more detailed step-by-step breakdown"""
    
    def construct(self):
        # Title
        title = DocText("QuickHull: Step-by-Step", font_size=48).to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # Show key idea
        idea = VGroup(
            DocText("Key Idea:", font_size=32, color=YELLOW),
            DocText("• Find extreme points (LEFT, RIGHT)", font_size=24),
            DocText("• Find PMAX (farthest from baseline)", font_size=24),
            DocText("• Prune interior points aggressively", font_size=24, color=RED),
            DocText("• Recurse on remaining points", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        
        self.play(Write(idea))
        self.wait(3)
        
        self.play(FadeOut(title), FadeOut(idea))
        
        # Show complexity analysis
        complexity_title = DocText("Runtime Analysis", font_size=36).to_edge(UP)
        self.play(Write(complexity_title))
        
        analysis = VGroup(
            DocText("Recurrence: T(N) = 2·T(N/3) + Θ(N)", font_size=28),
            DocText("(assuming 2/3 of points pruned each time)", font_size=20, color=GRAY),
            DocText("", font_size=10),
            DocText("A = 2 (two recursive calls)", font_size=24),
            DocText("B = 3 (problem size divided by 3)", font_size=24),
            DocText("D = 1 (linear work per level)", font_size=24),
            DocText("", font_size=10),
            DocText("A < B^D  →  2 < 3^1", font_size=28, color=YELLOW),
            DocText("Case 1 of Universal D&C Theorem", font_size=24, color=GREEN),
            DocText("", font_size=10),
            DocText("Runtime: Θ(N) average case!", font_size=32, color=GREEN)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).shift(DOWN * 0.5)
        
        self.play(Write(analysis), run_time=4)
        self.wait(4)
        
        # Comparison with other approaches
        self.play(FadeOut(complexity_title), FadeOut(analysis))
        
        comparison_title = DocText("Comparison with Other Approaches", font_size=36).to_edge(UP)
        self.play(Write(comparison_title))
        
        table_data = [
            ["Algorithm", "Approach", "Runtime"],
            ["QuickHull", "D&C + Pruning", "Θ(N log N) avg"],
            ["Graham Scan", "Sort + Scan", "Θ(N log N)"],
            ["Jarvis March", "Greedy", "Θ(Nh)"],
            ["Quadrant Split", "D&C (bad)", "Θ(N log N) + high constants"]
        ]
        
        # Create table
        table = VGroup()
        for i, row in enumerate(table_data):
            row_group = VGroup()
            for j, cell in enumerate(row):
                if i == 0:
                    cell_text = DocText(cell, font_size=24, color=YELLOW)
                elif cell == "Θ(N log N) avg":
                    cell_text = DocText(cell, font_size=20, color=GREEN)
                else:
                    cell_text = DocText(cell, font_size=20)
                
                if j == 0:
                    cell_text.move_to(LEFT * 4 + UP * (1.5 - i * 0.5))
                elif j == 1:
                    cell_text.move_to(ORIGIN + UP * (1.5 - i * 0.5))
                else:
                    cell_text.move_to(RIGHT * 4 + UP * (1.5 - i * 0.5))
                
                row_group.add(cell_text)
            table.add(row_group)
        
        self.play(Write(table), run_time=3)
        self.wait(3)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        
        end_text = DocText("QuickHull wins on average!", font_size=48, color=GREEN)
        self.play(Write(end_text))
        self.wait(2)


# Render both scenes
# Run with: manim -pql quickhull_animation.py QuickHullVisualization
# Or: manim -pql quickhull_animation.py QuickHullStepByStep