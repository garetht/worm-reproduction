import enum


class EmbeddingsType(enum.Enum):
  OpenAI = "vector_store"
  GTESmall = "gte-small"
  GTEBase = "gte-base"
  GTELarge = "gte-large"
