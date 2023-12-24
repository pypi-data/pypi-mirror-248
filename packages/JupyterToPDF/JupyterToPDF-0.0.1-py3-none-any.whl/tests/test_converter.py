import unittest
import os
from JupyterToPDF.converter import convert_notebook_to_pdf

class TestJupyterToPDF(unittest.TestCase):
    def setUp(self):
        # Path to the test notebook
        self.notebook_path = 'test_notebook.ipynb'
        # Create a simple notebook for testing
        with open(self.notebook_path, 'w') as f:
            f.write("# Test Notebook\nprint('Hello World')")

    def test_conversion(self):
        # Convert the notebook
        pdf_path = convert_notebook_to_pdf(self.notebook_path)

        # Check if the PDF file exists
        self.assertTrue(os.path.exists(pdf_path))

    def tearDown(self):
        # Clean up: remove created files
        os.remove(self.notebook_path)
        os.remove(self.notebook_path.replace('.ipynb', '.pdf'))

if __name__ == '__main__':
    unittest.main()
