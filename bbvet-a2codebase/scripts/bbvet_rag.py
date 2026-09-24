from __future__ import annotations
import json
import boto3

# this takes the vector embeddings found to be relevant to the user questions and 
# converts the top 3 retrieved chunks into a readable answer using Nemotron chat model.

# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------

REGION = "ap-southeast-2"
VECTOR_BUCKET = "n12030511-bbvet-vectors"
VECTOR_INDEX = "bbvet-knowledge"
EMBEDDING_MODEL_ID = "amazon.titan-embed-image-v1"
DIMENSION = 256
TEXT_MODEL_ID = "nvidia.nemotron-super-3-120b"
TOP_K = 3


# -------------------------------------------------------------------
# Create embeddings
# -------------------------------------------------------------------

def invoke_titan(client, payload: dict) -> list[float]:
    """
    Send input to Titan and return its embedding vector.
    """

    response = client.invoke_model(
        modelId=EMBEDDING_MODEL_ID,
        contentType="application/json",
        accept="application/json",
        body=json.dumps(payload),
    )

    response_body = json.loads(
        response["body"].read()
    )

    return response_body["embedding"]


def embed_text(client, text: str) -> list[float]:
    """
    Convert text into the same 256-dimensional embedding format
    used when the repository was indexed.
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
# Retrieve knowledge
# -------------------------------------------------------------------

def retrieve_context(
    s3vectors,
    bedrock,
    query: str,
    top_k: int = TOP_K,
) -> list[dict]:
    """
    Find the document chunks that are semantically closest
    to user question.
    """

    query_embedding = embed_text(
        bedrock,
        query,
    )

    # Search the S3 Vector index for nearby vectors.
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

    return matches


# -------------------------------------------------------------------
# Build prompt context
# -------------------------------------------------------------------

def build_context(matches: list[dict]) -> str:
    """
    Turn retrieved vector results into readable context
    that can be supplied to the language model.
    """

    context_parts = []

    for number, match in enumerate(matches, start=1):

        context_parts.append(
            f"""
            SOURCE {number}
            File: {match["source"]}
            Chunk: {match["chunk_index"]}

            {match["text"]}
            """.strip()
                    )

    return "\n\n---\n\n".join(context_parts)


# -------------------------------------------------------------------
# Generate answer
# -------------------------------------------------------------------

def generate_answer(
    bedrock,
    question: str,
    matches: list[dict],
) -> str:
    """
    Ask Nemotron to answer the question using only
    the retrieved BBVet knowledge.
    """

    context = build_context(matches)

    prompt = f"""
        Answer the user's question using only the BBVet knowledge provided below.

        If the supplied knowledge does not contain enough information to answer the
        question, say that the available BBVet knowledge does not provide the answer.

        Do not invent facts.

        When useful, mention which source file contained the information.

        BBVET KNOWLEDGE:

{context}

USER QUESTION:

{question}
""".strip()

    response = bedrock.converse(
        modelId=TEXT_MODEL_ID,

        system=[
            {
                "text": (
                    "You are the BBVet Knowledge Custodian. "
                    "Answer questions accurately and concisely using only "
                    "the supplied BBVet repository context."
                )
            }
        ],

        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "text": prompt,
                    }
                ],
            }
        ],

        inferenceConfig={
            "maxTokens": 400,
            "temperature": 0.2,
        },
    )

    blocks = response["output"]["message"]["content"]

    return "".join(
        block["text"]
        for block in blocks
        if "text" in block
    )


# -------------------------------------------------------------------
# Display retrieval evidence
# -------------------------------------------------------------------

def print_retrieval(matches: list[dict]) -> None:
    """
    Show what S3 Vectors retrieved before the LLM generates
    its final answer.
    """

    print("\nRetrieved knowledge:")

    for number, match in enumerate(matches, start=1):

        print(
            f"  {number}. {match['source']} "
            f"(chunk {match['chunk_index']}, "
            f"distance {match['distance']:.3f})"
        )


# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------

def main() -> None:

    # The same Bedrock Runtime client handles both:
    # -- Titan embedding requests
    # -- Nemotron text-generation requests
    bedrock = boto3.client(
        "bedrock-runtime",
        region_name=REGION,
    )

    s3vectors = boto3.client(
        "s3vectors",
        region_name=REGION,
    )

    print("BBVet RAG test")
    print("Type 'quit' to exit.")

    while True:

        question = input("\nQuestion > ").strip()

        if not question:
            continue

        if question.lower() in {
            "quit",
            "exit",
            "q",
        }:
            break

        # Step 1: retrieve relevant BBVet knowledge.
        matches = retrieve_context(
            s3vectors=s3vectors,
            bedrock=bedrock,
            query=question,
        )

        print_retrieval(matches)

        # Step 2: give the retrieved knowledge to the LLM.
        answer = generate_answer(
            bedrock=bedrock,
            question=question,
            matches=matches,
        )

        print("\nAnswer:")
        print(answer)


if __name__ == "__main__":
    main()

# ChatGPT was used to assist writing this code. 
# The code was reviewed and tested by myself.