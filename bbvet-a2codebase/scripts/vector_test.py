from __future__ import annotations

import json
from pathlib import Path

import boto3

# This is just an initial test file, following the week 7 practical, to test one vector knowledge.


# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------

REGION = "ap-southeast-2"

QUT_USERNAME = "n12030511@qut.edu.au"

VECTOR_BUCKET = "n12030511-bbvet-vectors"
VECTOR_INDEX = "bbvet-knowledge"

TITAN_MULTIMODAL_MODEL_ID = "amazon.titan-embed-image-v1"
DIMENSION = 256

# vector_test.py is:
# bbvet-knowledge/bbvet-a2codebase/scripts/vector_test.py
#
# parents[2] therefore points back to bbvet-knowledge/
REPO_ROOT = Path(__file__).resolve().parents[2]

# Pick one known document for our first test.
TEST_DOCUMENT = REPO_ROOT / "product-info" / "clinic-health.md"

TEST_QUERY = "What is Clinic Health?"


# -------------------------------------------------------------------
# AWS setup
# -------------------------------------------------------------------

def ensure_index(client) -> None:
    """
    Create the S3 Vector bucket and index if they do not already exist.

    This follows the create-or-reuse pattern from the Week 7 practical.
    """

    tags = {
        "qut-username": QUT_USERNAME,
        "purpose": "assessment 2",
    }

    try:
        client.create_vector_bucket(
            vectorBucketName=VECTOR_BUCKET,
            tags=tags,
        )
        print(f"Created vector bucket: {VECTOR_BUCKET}")

    except client.exceptions.ConflictException:
        print(f"Using existing vector bucket: {VECTOR_BUCKET}")

    try:
        client.create_index(
            vectorBucketName=VECTOR_BUCKET,
            indexName=VECTOR_INDEX,
            dataType="float32",
            dimension=DIMENSION,
            distanceMetric="cosine",
            tags=tags,
        )
        print(f"Created vector index: {VECTOR_INDEX}")

    except client.exceptions.ConflictException:
        print(f"Using existing vector index: {VECTOR_INDEX}")


# -------------------------------------------------------------------
# Bedrock embeddings
# -------------------------------------------------------------------

def invoke_titan(client, payload: dict) -> list[float]:
    """
    Call Amazon Titan Multimodal Embeddings through Bedrock.
    """

    response = client.invoke_model(
        modelId=TITAN_MULTIMODAL_MODEL_ID,
        contentType="application/json",
        accept="application/json",
        body=json.dumps(payload),
    )

    response_body = json.loads(response["body"].read())

    return response_body["embedding"]


def embed_text(client, text: str) -> list[float]:
    """
    Convert text into a 256-dimensional embedding.
    """

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
# Store document
# -------------------------------------------------------------------

def store_document(s3vectors, bedrock, file_path: Path) -> None:
    """
    Read one Markdown file, embed it, and store the resulting vector.
    """

    text = file_path.read_text(encoding="utf-8")

    print(f"\nEmbedding document:")
    print(f"  {file_path.relative_to(REPO_ROOT)}")

    embedding = embed_text(bedrock, text)

    vector_key = file_path.relative_to(REPO_ROOT).as_posix()

    s3vectors.put_vectors(
        vectorBucketName=VECTOR_BUCKET,
        indexName=VECTOR_INDEX,
        vectors=[
            {
                "key": vector_key,
                "data": {
                    "float32": embedding,
                },
                "metadata": {
                    "kind": "document",
                    "source": vector_key,
                    "filename": file_path.name,
                },
            }
        ],
    )

    print(f"Stored vector:")
    print(f"  {vector_key}")


# -------------------------------------------------------------------
# Query
# -------------------------------------------------------------------

def query_vectors(s3vectors, bedrock, query_text: str) -> None:
    """
    Embed a query using the same model, then find the closest vectors.
    """

    query_embedding = embed_text(bedrock, query_text)

    result = s3vectors.query_vectors(
        vectorBucketName=VECTOR_BUCKET,
        indexName=VECTOR_INDEX,
        queryVector={
            "float32": query_embedding,
        },
        topK=3,
        returnDistance=True,
        returnMetadata=True,
    )

    print(f'\nResults for query: "{query_text}"')

    vectors = result.get("vectors", [])

    if not vectors:
        print("No matches returned.")
        return

    for i, vector in enumerate(vectors, start=1):
        print(f"\nResult {i}")
        print(f"  Key:      {vector.get('key')}")
        print(f"  Distance: {vector.get('distance')}")
        print(f"  Metadata: {vector.get('metadata')}")


# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------

def main() -> None:

    if not TEST_DOCUMENT.exists():
        raise FileNotFoundError(
            f"Could not find test document: {TEST_DOCUMENT}"
        )

    # Same two clients used in the Week 7 practical:
    # Bedrock creates embeddings.
    # S3 Vectors stores and searches them.
    bedrock = boto3.client(
        "bedrock-runtime",
        region_name=REGION,
    )

    s3vectors = boto3.client(
        "s3vectors",
        region_name=REGION,
    )

    ensure_index(s3vectors)

    store_document(
        s3vectors=s3vectors,
        bedrock=bedrock,
        file_path=TEST_DOCUMENT,
    )

    query_vectors(
        s3vectors=s3vectors,
        bedrock=bedrock,
        query_text=TEST_QUERY,
    )


if __name__ == "__main__":
    main()