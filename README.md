# QuickHull Algorithm Animation

This is a comprehensive Manim animation that visualizes the QuickHull algorithm's divide-and-conquer approach with aggressive pruning.

## Video Output

The rendered 1080p60 animation is available as [`quickhull_animation.mp4`](./quickhull_animation.mp4).

## Installation

First, install Manim:

```bash
# On macOS
brew install py3cairo ffmpeg
pip install manim

# On Ubuntu/Debian
sudo apt-get install libcairo2-dev libpango1.0-dev ffmpeg
pip install manim

# On Windows (using Chocolatey)
choco install manimce
```

Or simply:
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

### Step-by-Step Explanation
```bash
manim -pql quickhull_animation.py QuickHullStepByStep
```

## What the Animation Shows

### Scene 1: QuickHullVisualization
1. **Setup**: Displays ~45 points (12 on outer hull, 33 interior)
2. **Step 0**: Finds and highlights LEFT (green) and RIGHT (green) extreme points
3. **Baseline**: Draws line between LEFT and RIGHT
4. **Partition**: Separates points into ABOVE (yellow) and BELOW (purple) baseline
5. **Upper Hull Recursion**:
   - Finds PMAX (red) - farthest point from baseline
   - Draws triangle (LEFT, PMAX, RIGHT)
   - **PRUNES** all interior points (fades them out)
   - Recursively solves left and right subproblems
6. **Lower Hull Recursion**: Same process for points below baseline
7. **Final Hull**: Shows complete convex hull in gold
8. **Statistics**: Displays total points, hull points, and pruned count

### Scene 2: QuickHullStepByStep
1. Shows key algorithmic ideas
2. Runtime analysis with Universal D&C Theorem
3. Comparison table with other convex hull algorithms

## Key Features

### Visual Elements
- **Green dots**: Extreme points (LEFT, RIGHT)
- **Red dots**: PMAX points (farthest from current baseline)
- **Yellow dots**: Points above baseline being processed
- **Purple dots**: Points below baseline being processed
- **Gold dots**: Final convex hull points
- **Faded dots**: Pruned interior points (the magic of QuickHull!)
- **Red triangles**: Current triangle being considered for pruning

### Animation Highlights
- Smooth transitions between recursion levels
- Clear visual distinction between kept vs pruned points
- Step-by-step labeling (PMAX, LEFT, RIGHT)
- Real-time statistics showing pruning efficiency

## Understanding the Algorithm Through Animation

Watch for these key moments:

1. **Initial Partition** (~5 seconds in): 
   - Notice how points are cleanly separated into upper/lower halves

2. **First PMAX** (~8 seconds in):
   - The algorithm finds the point farthest from baseline
   - Triangle forms showing the "cone" of influence

3. **First Prune** (~10 seconds in):
   - Watch points inside the triangle fade out
   - These points can NEVER be on the convex hull!
   - This is why QuickHull is fast!

4. **Recursion** (~12-20 seconds):
   - Notice how each recursive call works on fewer and fewer points
   - Most points get pruned early
   - Only a small fraction participates in deep recursion

5. **Final Hull** (~25 seconds):
   - All hull points light up in gold
   - Notice how few points actually matter!

## Customization

You can modify the animation by editing `quickhull_animation.py`:

### Change Point Distribution
In `generate_interesting_points()`:
```python
# More outer points (larger hull)
for angle in np.linspace(0, 2*np.pi, 20, endpoint=False):  # was 12

# More interior points (more pruning to show)
for _ in range(50):  # was 25
```

### Change Animation Speed
```python
# Faster recursion
self.play(Create(triangle), run_time=0.2)  # was 0.5

# Slower for teaching
self.wait(2)  # was 1
```

### Change Colors
```python
# Different color scheme
points[i].animate.set_color(TEAL)  # instead of YELLOW
```

## Output

The animation will be saved in:
```
media/videos/quickhull_animation/[quality]/QuickHullVisualization.mp4
```

The main 1080p60 output is also available as [`quickhull_animation.mp4`](./quickhull_animation.mp4) in the repository root.

Quality levels:
- `-ql`: 480p (low quality, fast render)
- `-qm`: 720p (medium quality)
- `-qh`: 1080p (high quality)
- `-qk`: 2160p (4K quality)

## Troubleshooting

### "Command not found: manim"
Make sure you installed manim and it's in your PATH:
```bash
python -m manim -pql quickhull_animation.py QuickHullVisualization
```

### "No module named 'manim'"
Install manim:
```bash
pip install manim
```

### Animation runs but points are off-screen
The `scale_points()` function should handle this, but if not, try:
```python
points_coords = self.scale_points(points_coords, target_width=8)  # was 10
```

### Recursion too fast to follow
Increase wait times:
```python
self.wait(2)  # increase from 1
```

Or render at higher frame rate and slow down playback.

## For Your Algorithms Exam

After watching this animation, you should understand:

1. **Why QuickHull is efficient**: The pruning! Most points get eliminated early
2. **The recursion structure**: How PMAX divides the problem into two smaller subproblems
3. **What gets pruned**: Any point inside the current triangle
4. **Runtime analysis**: Why aggressive pruning leads to Θ(N) average case

## Scene Ideas for Learning

You could create additional scenes:

### Scene 3: Compare with Quadrant Approach
Show how splitting by median x,y would keep all 4 quadrants active (no pruning!)

### Scene 4: Worst Case
Show points arranged in a circle where minimal pruning occurs (Θ(N²))

### Scene 5: Best Case
Show points where half are pruned each time (Θ(N))

## Questions for Understanding

After watching the animation, test yourself:

1. How many points were in the original set?
2. How many were on the final hull?
3. How many got pruned?
4. At what depth of recursion did most pruning occur?
5. Why can we safely prune points inside the triangle?

Answers:
1. ~45 points
2. ~20 points (outer ring)
3. ~25 points (interior)
4. First level (finds PMAX, eliminates large triangle)
5. Because they're "inside" the convex polygon we're building - they can't be on the outer boundary

## Next Steps

1. Watch the animation multiple times
2. Pause at key moments to understand what's happening
3. Read the DP guide for comparison with other algorithmic paradigms
4. Practice explaining QuickHull to someone else using the visualization

Good luck on your exam! 🚀
