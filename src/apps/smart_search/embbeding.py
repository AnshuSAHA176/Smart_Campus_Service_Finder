from sentence_transformers import SentenceTransformer


MODEL_NAME = "BAAI/bge-m3"

model = SentenceTransformer(
    MODEL_NAME,
    device="cpu",
)


def embedding_model(text: str) -> list[float]:
    """
    Generate a normalized embedding for the given text.
    """
    if not text or not text.strip():
        raise ValueError("Text cannot be empty.")

    embedding = model.encode(
        text.strip(),
        normalize_embeddings=True,
        convert_to_numpy=True,
    )

    return embedding.tolist()


def create_embedding(title: str, description: str,category:str) -> list[float]:
    """
    Create an embedding representing a place and its description and category.
    """

    text = (
        f"Place: {title.strip()}\n"
        f"Description: {description.strip()}"
        f"Category : {category}"
    )

    return embedding_model(text)




