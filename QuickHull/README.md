# QuickHull Algorithm Animation

This is a comprehensive Manim animation that visualizes the QuickHull algorithm's divide-and-conquer approach with aggressive pruning.

## Video Output

The rendered 1080p60 animation is available as [`quickhull_animation.mp4`](./quickhull_animation.mp4).

## Installation

First, install Manim:

```bash
pip install manim
```

## Running the Animation

### Main Visualization (Full QuickHull with Pruning)
```bash
# Low quality (fast preview)
manim -pql quickhull_animation.py QuickHullVisualization

# High quality (for presentations)
manim -pqh quickhull_animation.py QuickHullVisualization

# 4K quality
manim -pqk quickhull_animation.py QuickHullVisualization
```
