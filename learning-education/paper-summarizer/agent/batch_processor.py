import os
from agent.pdf_parser import extract_text_from_pdf
from agent.summarizer import PaperSummarizer

class BatchProcessor:
    def __init__(self):
        self.summarizer = PaperSummarizer()

    def process_directory(self, directory_path: str) -> dict:
        """
        Processes all PDF files in a directory and generates summaries.

        Args:
            directory_path (str): Path to the directory containing PDFs.

        Returns:
            dict: A dictionary where keys are filenames and values are summary dictionaries.
        """
        results = {}
        if not os.path.exists(directory_path):
            print(f"Directory {directory_path} does not exist.")
            return results

        for filename in os.listdir(directory_path):
            if filename.lower().endswith(".pdf"):
                filepath = os.path.join(directory_path, filename)
                print(f"Processing {filename}...")
                text = extract_text_from_pdf(filepath)
                if text:
                    summary = self.summarizer.summarize_all(text)
                    results[filename] = summary
                else:
                    print(f"Could not extract text from {filename}")

        return results
