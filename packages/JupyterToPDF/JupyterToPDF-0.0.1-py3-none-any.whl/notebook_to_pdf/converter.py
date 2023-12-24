import os
import pdfkit

def convert_notebook_to_pdf(notebook_path, output_folder=None):
    if output_folder and not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Convert to HTML
    html_output = notebook_path.replace('.ipynb', '.html')
    os.system(f"jupyter nbconvert --to html \"{notebook_path}\"")

    # Define PDF output path
    if output_folder:
        pdf_output = os.path.join(output_folder, os.path.basename(notebook_path).replace('.ipynb', '.pdf'))
    else:
        pdf_output = notebook_path.replace('.ipynb', '.pdf')

    # Convert HTML to PDF
    pdfkit.from_file(html_output, pdf_output)

    return pdf_output
