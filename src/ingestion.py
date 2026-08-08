from Bio import SeqIO
import os

def ingest_genomic_file(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Genomic file not found at: {file_path}")
    print(f"[Ingestion] Parsing genomic file: {os.path.basename(file_path)}")
    for record in SeqIO.parse(file_path, "fasta"):
        sequence_length = len(record.seq)
        print(f"[Ingestion] Success. Ingested ID: {record.id}")
        print(f"[Ingestion] Total Base Pairs: {sequence_length}")
        return record.id, record.seq
