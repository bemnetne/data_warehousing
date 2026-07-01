from pydantic import BaseModel, Field
from typing import List


class TopProductResponse(BaseModel):
    message_text: str = Field(
        description="The Telegram message that was posted."
    )

    mentions: int = Field(
        description="Number of times the exact message appears across the dataset."
    )


class ChannelActivityResponse(BaseModel):
    full_date: str = Field(
        description="Date on which the messages were posted."
    )

    posts: int = Field(
        description="Total number of messages published on the specified date."
    )

    average_views: float = Field(
        description="Average number of views received by messages posted on that date."
    )



class MessageSearchResponse(BaseModel):
    message_id: int = Field(
        description="Unique identifier of the Telegram message."
    )

    message_text: str = Field(
        description="Content of the Telegram message matching the search query."
    )

    view_count: int | None = Field(
        default=None,
        description="Total number of views recorded for the message."
    )

    forward_count: int | None = Field(
        default=None,
        description="Total number of times the message was forwarded."
    )


class VisualContentResponse(BaseModel):
    channel_name: str = Field(
        description="Telegram channel name."
    )

    image_category: str = Field(
        description="Detected image category."
    )

    total_posts: int = Field(
        description="Number of image posts."
    )

    average_views: float = Field(
        description="Average number of views."
    )