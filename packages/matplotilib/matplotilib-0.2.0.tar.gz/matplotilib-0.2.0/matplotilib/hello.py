import nbformat
from IPython.display import display, HTML, FileLink

def hello():
    print("Hello from matplotilib!")

def CNN():
    # Load the notebook content
    notebook_path = 'notebook/CNN.ipynb'
    with open(notebook_path, 'r', encoding='utf-8') as notebook_file:
        notebook_content = nbformat.read(notebook_file, as_version=4)

    # Display a download link
    display(HTML(f'<a href="{notebook_path}" download></a>'))
