1. Export original model from Zbrush to .obj file (export scale x1)
2. Project model to uv using Unfold3D (adapt tile size)
3. Export model with uv and uvin3D (use dimensions = tile size, and normalize uv coords in model)
4. Import model with uv and uvin3D back to Zbrush
5. Project polypaint of original model to model with uv
6. Export model with uv and polypaint to .obj file (export scale x100)
7. Remove irregularities from model
8. Export regular model with uv and polypaint to .obj file (export scale x100)
9. Call python script `apply_pattern.py` (adapt argument `s` such that it equals 100x tile size)
Example with tile size = 8:
	python path\to\apply_pattern.py path\to\regular\model.obj -p path\to\irregular\pattern.obj -s 800 -r 2 -g 4 -b 8 -d 0
