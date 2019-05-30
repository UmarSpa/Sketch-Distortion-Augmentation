# Sketch Distortion / Augmentation
This code introduces distortion in SVG format sketches. It can be used for sketch data augmentation.

## Explanation

Input: sketches in TU Berlin style SVG format.

**dataAugN:** Number of distorted/augmented samples that are going to be generated.

**transXVar:** Translation along x axis

**transYVar:** Translation along y axis

**rotateVar:** Degrees of rotation

**scaleXVar:** Scale along x axis

**scaleYVar:** Scale along y axis

**skewXVar:** Skew along x axis

**skewYVar:** Skew along y axis

**pathXVar:** Path jittering along x axis

**pathYVar:** Path jittering along y axis

**curveXVar:** Bézier Curve jittering along x axis

**curveYVar:** Bézier Curve jittering along y axis

Output: distorted sketches in TUBerlin style svg format.