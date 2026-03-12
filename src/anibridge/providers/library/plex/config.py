"""Plex provider configuration."""

from pydantic import BaseModel, Field


class PlexProviderConfig(BaseModel):
    """Configuration for the Plex provider."""

    url: str = Field(default=..., description="The base URL of the Plex server.")
    token: str = Field(
        default=..., description="The account API token of the Plex server admin."
    )
    user: str = Field(default=..., description="The Plex user to synchronize.")
    sections: list[str] = Field(
        default_factory=list,
        description=(
            "A list of Plex library section names to constrain synchronization to."
        ),
    )
    genres: list[str] = Field(
        default_factory=list,
        description="A list of genres to constrain synchronization to.",
    )
    strict: bool = Field(
        default=True,
        description="Whether to enforce strict matching when resolving mappings.",
    )
