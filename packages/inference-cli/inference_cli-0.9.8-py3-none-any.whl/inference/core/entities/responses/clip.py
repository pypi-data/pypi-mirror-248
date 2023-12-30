from typing import Dict, List, Optional, Union

from pydantic import Field

from inference.core.entities.responses.inference import InferenceResponse


class ClipEmbeddingResponse(InferenceResponse):
    """Response for CLIP embedding.

    Attributes:
        embeddings (List[List[float]]): A list of embeddings, each embedding is a list of floats.
        time (float): The time in seconds it took to produce the embeddings including preprocessing.
    """

    embeddings: List[List[float]] = Field(
        example="[[0.12, 0.23, 0.34, ..., 0.43]]",
        description="A list of embeddings, each embedding is a list of floats",
    )
    time: Optional[float] = Field(
        description="The time in seconds it took to produce the embeddings including preprocessing"
    )


class ClipCompareResponse(InferenceResponse):
    """Response for CLIP comparison.

    Attributes:
        similarity (Union[List[float], Dict[str, float]]): Similarity scores.
        time (float): The time in seconds it took to produce the similarity scores including preprocessing.
    """

    similarity: Union[List[float], Dict[str, float]]
    time: Optional[float] = Field(
        description="The time in seconds it took to produce the similarity scores including preprocessing"
    )
