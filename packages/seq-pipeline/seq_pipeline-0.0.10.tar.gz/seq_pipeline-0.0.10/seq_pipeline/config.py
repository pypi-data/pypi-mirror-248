import os


PIPELINES_DIR = os.path.join(os.path.dirname(__file__), "pipelines")
VERSION = "2023-12-19"

INPUT_TYPES = {
    "paired_fastq": [".r1.fastq.gz", ".r2.fastq.gz"],
    "single_fastq": [".fastq.gz"],
    "indexed_bam": [".bam", ".bam.bai"],
    "bigwig": [".bigwig"]}
