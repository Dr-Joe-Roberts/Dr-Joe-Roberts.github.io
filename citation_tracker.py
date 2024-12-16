#!/usr/bin/env python3
import os
from pathlib import Path
import logging
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scholarly import scholarly

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_citations_per_year(author_id):
    """Fetch citations per year for the given scholar author."""
    author_data = scholarly.search_author_id(author_id)
    author_data = scholarly.fill(author_data)

    # Extract citations per year
    citations_per_year = author_data.get('cites_per_year', {})

    return citations_per_year

def create_citations_plot(citations_dict, output_path):
    """Create a simple bar plot of citations per year."""
    years = sorted(citations_dict.keys(), key=lambda x: int(x))
    citations = [citations_dict[year] for year in years]
    x_positions = np.arange(len(years))

    plt.figure(figsize=(10,5), dpi=150)
    bars = plt.bar(x_positions, citations, color='blue', alpha=0.7)
    plt.title('Citations per Year', fontsize=12)
    plt.xlabel('Year', fontsize=10)
    plt.ylabel('Citations', fontsize=10)
    plt.xticks(x_positions, years, rotation=45, fontsize=8)
    plt.yticks(fontsize=8)
    plt.grid(axis='y', alpha=0.3)

    # Add value labels
    for bar, val in zip(bars, citations):
        plt.text(bar.get_x() + bar.get_width()/2., val, f'{val}',
                 ha='center', va='bottom', fontsize=8)

    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, bbox_inches='tight', facecolor='white', transparent=False)
    plt.close()

def main(author_id, output_dir="./data"):
    logging.info("Starting citation plot update")
    if not author_id:
        logging.error("No author ID provided.")
        return

    citations_per_year = fetch_citations_per_year(author_id)
    if not citations_per_year:
        logging.warning("No citation data found.")
        return

    output_dir = Path(output_dir)
    plot_path = output_dir / 'citations_plot.png'
    create_citations_plot(citations_per_year, plot_path)
    logging.info(f"Plot saved to {plot_path}")

if __name__ == "__main__":
    # Pass your author_id here or set via environment variable
    author_id = os.getenv('GOOGLE_SCHOLAR_ID', 'YOUR_SCHOLAR_ID_HERE')
    main(author_id)
