import nbformat
from nbconvert import PythonExporter
import glob

for notebook_path in glob.glob("*.ipynb"):
    with open(notebook_path) as f:
        nb = nbformat.read(f, as_version=4)
    exporter = PythonExporter()
    source, _ = exporter.from_notebook_node(nb)
    
    py_path = notebook_path.replace(".ipynb", ".py")
    with open(py_path, "w") as f:
        f.write(source)
    print(f"✅ {notebook_path} -> {py_path}")
