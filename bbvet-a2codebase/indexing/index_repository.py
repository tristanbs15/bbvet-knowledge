from __future__ import annotations

import json
from pathlib import Path

import boto3

# This file is for understanding semantic meaning in the bbvet-knowledge repo.

# It splits the markdown files into bit sized chunks, and coverts those 
# chunks into numerical embeddings in vector space (256 dimensions as seen in prac 7) 
# using Amazon Titan through Bedrock.

# These embeddings are stored in Amazons S3 Vectors with some other extra metadata that 
# will be important for referencing (filename, doc type, chunk number).

# Configuration

REGION = "ap-southeast-2"

QUT_USERNAME = "n12030511@qut.edu.au"
VECTOR_BUCKET = "n12030511-bbvet-vectors"
VECTOR_INDEX = "bbvet-knowledge"

TITAN_MULTIMODAL_MODEL_ID = "amazon.titan-embed-image-v1"
DIMENSION = 256

# index_repository.py is:
# bbvet-knowledge/bbvet-a2codebase/indexing/index_repository.py
#
# parents[2] points back to bbvet-knowledge/
REPO_ROOT = Path(__file__).resolve().parents[2]

KNOWLEDGE_FOLDERS = [
    REPO_ROOT / "weekly-meetings",
    REPO_ROOT / "extra-meetings",
    REPO_ROOT / "product-info",
]

# Simple character-based chunking.
CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200


# -------------------------------------------------------------------
# Bedrock embeddings
# -------------------------------------------------------------------

def invoke_titan(client, payload: dict) -> list[float]:
    response = client.invoke_model(
        modelId=TITAN_MULTIMODAL_MODEL_ID,
        contentType="application/json",
        accept="application/json",
        body=json.dumps(payload),
    )

    response_body = json.loads(response["body"].read())

    return response_body["embedding"]


def embed_text(client, text: str) -> list[float]:
    return invoke_titan(
        client,
        {
            "inputText": text,
            "embeddingConfig": {
                "outputEmbeddingLength": DIMENSION,
            },
        },
    )


# -------------------------------------------------------------------
# Discover documents
# -------------------------------------------------------------------

def discover_markdown_files() -> list[Path]:
    """
    Find all Markdown files in the configured knowledge folders.
    """

    files: list[Path] = []

    for folder in KNOWLEDGE_FOLDERS:
        if not folder.exists():
            print(f"Warning: folder does not exist: {folder}")
            continue

        files.extend(folder.rglob("*.md"))

    return sorted(files)


# -------------------------------------------------------------------
# Chunking
# -------------------------------------------------------------------

def chunk_text(
    text: str,
    chunk_size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP,
) -> list[str]:
    """
    Split a document into overlapping text chunks.

    The overlap helps preserve context that falls across chunk boundaries.
    """

    text = text.strip()

    if not text:
        return []

    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))

        chunk = text[start:end]

        # If possible, stop at a paragraph boundary rather than
        # cutting directly through a paragraph.
        if end < len(text):
            paragraph_break = chunk.rfind("\n\n")

            if paragraph_break > chunk_size // 2:
                end = start + paragraph_break
                chunk = text[start:end]

        chunk = chunk.strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = max(end - overlap, start + 1)

    return chunks


# -------------------------------------------------------------------
# Metadata helpers
# -------------------------------------------------------------------

def document_kind(file_path: Path) -> str:
    """
    Determine the document type based on its top-level repository folder.
    """

    relative = file_path.relative_to(REPO_ROOT)

    return relative.parts[0]


# -------------------------------------------------------------------
# Index one document
# -------------------------------------------------------------------

def index_document(
    s3vectors,
    bedrock,
    file_path: Path,
) -> int:
    """
    Read, chunk, embed and store one Markdown document.
    """

    relative_path = file_path.relative_to(REPO_ROOT).as_posix()

    print(f"\nIndexing: {relative_path}")

    text = file_path.read_text(encoding="utf-8")

    chunks = chunk_text(text)

    if not chunks:
        print("  Skipping empty document.")
        return 0

    vectors = []

    for chunk_index, chunk in enumerate(chunks):

        print(
            f"  Embedding chunk "
            f"{chunk_index + 1}/{len(chunks)}..."
        )

        embedding = embed_text(
            bedrock,
            chunk,
        )

        vector_key = f"{relative_path}#chunk-{chunk_index}"

        vectors.append(
            {
                "key": vector_key,
                "data": {
                    "float32": embedding,
                },
                "metadata": {
                    "source": relative_path,
                    "kind": document_kind(file_path),
                    "filename": file_path.name,
                    "chunk_index": chunk_index,
                    "text": chunk,
                },
            }
        )

    # Store every chunk from this document.
    s3vectors.put_vectors(
        vectorBucketName=VECTOR_BUCKET,
        indexName=VECTOR_INDEX,
        vectors=vectors,
    )

    print(f"  Stored {len(vectors)} chunks.")

    return len(vectors)


# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------

def main() -> None:

    bedrock = boto3.client(
        "bedrock-runtime",
        region_name=REGION,
    )

    s3vectors = boto3.client(
        "s3vectors",
        region_name=REGION,
    )

    files = discover_markdown_files()

    print("BBVet repository indexer")
    print("------------------------")
    print(f"Repository root: {REPO_ROOT}")
    print(f"Markdown documents found: {len(files)}")

    if not files:
        print("\nNo Markdown files found.")
        return

    total_chunks = 0

    for file_path in files:
        total_chunks += index_document(
            s3vectors=s3vectors,
            bedrock=bedrock,
            file_path=file_path,
        )

    print("\nIndexing complete.")
    print(f"Documents indexed: {len(files)}")
    print(f"Vectors stored:    {total_chunks}")


if __name__ == "__main__":
    main()

# ChatGPT was used to assist (not completely generate) writing this code. 
# The code was reviewed and tested by myself.