import subprocess
import os


class SphinxClient:
    @staticmethod
    def build_html(doc_folder_path: str):
        """
        Builds the HTML documentation using Sphinx.

        Args:
            doc_folder_path (str): The path to the folder containing the Sphinx documentation.

        Returns:
            CompletedProcess: The result of the Sphinx build command.
        """
        current_dir = doc_folder_path

        # Path to your Sphinx source directory (two directories up)
        sphinx_source_dir = doc_folder_path
        print(sphinx_source_dir)

        # Path to the directory to output the HTML files (two directories up and down to 'build')
        build_dir = os.path.abspath(os.path.join(current_dir, "build", "html"))
        print(build_dir)

        # Command to build Sphinx documentation
        command = ["sphinx-build", "-b", "html", sphinx_source_dir, build_dir]

        # Run the Sphinx build command
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return result
