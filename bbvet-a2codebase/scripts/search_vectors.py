from __future__ import annotations
import json
import boto3

# The file allows for search through the indexed bbvet knowledge repo.

# The users question is coverted to an embedding, the same way it is in index_repository.py,
# and that query is compared against the already existing embeddings in S3 vectors.

# S3 then returns the closest matching document chunks based on the semantic similarity.


# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------

REGION = "ap-southeast-2"
VECTOR_BUCKET = "n12030511-bbvet-vectors"
VECTOR_INDEX = "bbvet-knowledge"
TITAN_MULTIMODAL_MODEL_ID = "amazon.titan-embed-image-v1"
DIMENSION = 256


# -------------------------------------------------------------------
# Embeddings
# -------------------------------------------------------------------

def invoke_titan(client, payload: dict) -> list[float]:
    response = client.invoke_model(
        modelId=TITAN_MULTIMODAL_MODEL_ID,
        contentType="application/json",
        accept="application/json",
        body=json.dumps(payload),
    )

    return json.loads(
        response["body"].read()
    )["embedding"]


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
# Search
# -------------------------------------------------------------------

def search(
    s3vectors,
    bedrock,
    query: str,
    top_k: int = 5,
) -> None:

    query_embedding = embed_text(
        bedrock,
        query,
    )

    result = s3vectors.query_vectors(
        vectorBucketName=VECTOR_BUCKET,
        indexName=VECTOR_INDEX,
        queryVector={
            "float32": query_embedding,
        },
        topK=top_k,
        returnDistance=True,
        returnMetadata=True,
    )

    vectors = result.get("vectors", [])

    print()
    print("=" * 70)
    print(f'QUERY: "{query}"')
    print("=" * 70)

    if not vectors:
        print("No results.")
        return

    for position, vector in enumerate(vectors, start=1):

        metadata = vector.get("metadata", {})

        print()
        print(f"RESULT {position}")
        print("-" * 70)

        print(f"Key:      {vector.get('key')}")
        print(f"Distance: {vector.get('distance')}")
        print(f"Source:   {metadata.get('source')}")
        print(f"Kind:     {metadata.get('kind')}")
        print(
            f"Chunk:    "
            f"{metadata.get('chunk_index')}"
        )

        print()
        print("Text:")
        print(metadata.get("text", "[no text stored]"))


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

    print("BBVet Repo Search")
    print("Type 'quit' to exit.")

    while True:

        query = input("\nSearch > ").strip()

        if not query:
            continue

        if query.lower() in {
            "quit",
            "exit",
            "q",
        }:
            break

        search(
            s3vectors=s3vectors,
            bedrock=bedrock,
            query=query,
        )


if __name__ == "__main__":
    main()

# ChatGPT was used to assist writing this code. 
# The code was reviewed and tested by myself.