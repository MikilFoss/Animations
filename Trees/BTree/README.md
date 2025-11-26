# B-Tree Animation

This Manim animation visualizes B-tree insertion with node splitting.

## Video Output

The rendered 1080p60 animation will be available as `btree_animation.mp4` after rendering.

## Installation

First, install Manim:

```bash
pip install manim
```

## Running the Animation

```bash
# Low quality (fast preview) - RECOMMENDED for development
manim -pql btree_animation.py BTreeVisualization

# High quality (for presentations)
manim -pqh btree_animation.py BTreeVisualization

# 4K quality
manim -pqk btree_animation.py BTreeVisualization
```

## Speed Optimization Tips

To make compilation faster:

1. **Use low quality flag** (`-pql`): Already 3-4x faster than high quality
2. **Disable caching for small changes**: `manim -pql --disable_caching btree_animation.py BTreeVisualization`
3. **Use fast mode**: Set environment variable for even faster preview:

   ```bash
   FAST_MODE=true manim -pql btree_animation.py BTreeVisualization
   ```

   This uses 30fps and 720p instead of 60fps and 1080p.

4. **Render specific scenes**: If you have multiple scenes, render only one:

   ```bash
   manim -pql btree_animation.py BTreeVisualization --scene_names BTreeVisualization
   ```

5. **Skip preview**: Remove `-p` flag if you don't need auto-playback:
   ```bash
   manim -ql btree_animation.py BTreeVisualization
   ```
