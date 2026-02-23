import argparse
import os
import json
from agent.pdf_parser import extract_text_from_pdf
from agent.summarizer import PaperSummarizer
from agent.visualizer import Visualizer
from agent.reading_list import ReadingListGenerator
from agent.batch_processor import BatchProcessor

def main():
    parser = argparse.ArgumentParser(description="Paper Summarizer Agent")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Summarize single file
    parser_summarize = subparsers.add_parser("summarize", help="Summarize a single PDF file")
    parser_summarize.add_argument("filepath", type=str, help="Path to the PDF file")
    parser_summarize.add_argument("--visual", action="store_true", help="Generate visual summary (Mermaid.js)")

    # Batch process
    parser_batch = subparsers.add_parser("batch", help="Batch process a directory of PDFs")
    parser_batch.add_argument("directory", type=str, help="Path to the directory")

    # Reading list
    parser_reading_list = subparsers.add_parser("reading-list", help="Generate a reading list")
    parser_reading_list.add_argument("topic", type=str, help="Topic for the reading list")

    args = parser.parse_args()

    if args.command == "summarize":
        filepath = args.filepath
        if not os.path.exists(filepath):
            print(f"File not found: {filepath}")
            return

        print(f"Extracting text from {filepath}...")
        text = extract_text_from_pdf(filepath)
        if not text:
            print("Failed to extract text.")
            return

        print("Generating summary...")
        summarizer = PaperSummarizer()
        summary = summarizer.summarize_all(text)

        print("\n=== Summary ===")
        print(json.dumps(summary, indent=2))

        if args.visual:
            print("\nGenerating visual summary...")
            visualizer = Visualizer()
            visual_summary = visualizer.generate_visual_summary(text)
            print("\n=== Visual Summary (Mermaid.js) ===")
            print(visual_summary)

    elif args.command == "batch":
        directory = args.directory
        print(f"Processing directory: {directory}...")
        processor = BatchProcessor()
        results = processor.process_directory(directory)

        print("\n=== Batch Results ===")
        print(json.dumps(results, indent=2))

        # Save to file
        output_file = os.path.join(directory, "summaries.json")
        try:
            with open(output_file, "w") as f:
                json.dump(results, f, indent=2)
            print(f"Results saved to {output_file}")
        except Exception as e:
            print(f"Error saving results: {e}")

    elif args.command == "reading-list":
        topic = args.topic
        print(f"Generating reading list for topic: {topic}...")
        generator = ReadingListGenerator()
        reading_list = generator.generate_reading_list(topic)

        print("\n=== Reading List ===")
        print(reading_list)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
