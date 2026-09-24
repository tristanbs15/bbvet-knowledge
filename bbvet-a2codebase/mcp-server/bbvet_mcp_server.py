from __future__ import annotations
import json
import boto3
from fastmcp import FastMCP


# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------

REGION = "ap-southeast-2"
VECTOR_BUCKET = "n12030511-bbvet-vectors"
VECTOR_INDEX = "bbvet-knowledge"
EMBEDDING_MODEL_ID = "amazon.titan-embed-image-v1"
DIMENSION = 256


# -------------------------------------------------------------------
# MCP server
# -------------------------------------------------------------------

mcp = FastMCP("BBVet Knowledge Toolset")

# -------------------------------------------------------------------
# AWS clients
# -------------------------------------------------------------------

bedrock = boto3.client(
    "bedrock-runtime",
    region_name=REGION,
)

s3vectors = boto3.client(
    "s3vectors",
    region_name=REGION,
)

# -------------------------------------------------------------------
# Embedding helpers
# -------------------------------------------------------------------

def invoke_titan(payload: dict) -> list[float]:
    """
    Send text to Titan and return a 256-dimensional embedding.
    """

    response = bedrock.invoke_model(
        modelId=EMBEDDING_MODEL_ID,
        contentType="application/json",
        accept="application/json",
        body=json.dumps(payload),
    )

    response_body = json.loads(
        response["body"].read()
    )

    return response_body["embedding"]


def embed_text(text: str) -> list[float]:
    """
    Convert text into the same embedding format used
    when the BBVet repository was indexed.
    """

    return invoke_titan(
        {
            "inputText": text,
            "embeddingConfig": {
                "outputEmbeddingLength": DIMENSION,
            },
        }
    )

# -------------------------------------------------------------------
# MCP Tools
# -------------------------------------------------------------------

@mcp.tool
def search_bbvet_knowledge(query: str) -> dict:
    """
    Search the BBVet knowledge repository for information relevant
    to a natural-language query.
    """

    query = query.strip()

    if not query:
        raise ValueError("query must not be empty")

    query_embedding = embed_text(query)

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

    matches = []

    for vector in result.get("vectors", []):
        metadata = vector.get("metadata", {})

        matches.append(
            {
                "source": metadata.get("source"),
                "chunk_index": metadata.get("chunk_index"),
                "text": metadata.get("text", ""),
                "distance": vector.get("distance"),
            }
        )

    return {
    "query": query,
    "matches": matches,
    }


# -------------------------------------------------------------------
# Run server
# -------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run()

# ChatGPT was used to assist writing this code. 
# The code was reviewed and tested by myself.