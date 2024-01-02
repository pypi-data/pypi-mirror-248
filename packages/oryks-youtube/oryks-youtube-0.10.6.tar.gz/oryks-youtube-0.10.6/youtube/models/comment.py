from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Author(BaseModel):
    display_name: str
    profile_image_url: str
    channel_url: Optional[str] = ''
    channel_id: Optional[str] = ''


class Snippet(BaseModel):
    author: Author
    channel_id: str
    video_id: str
    text_display: str
    text_original: str
    can_rate: bool
    viewer_rating: str
    like_count: int
    # moderation_status: str
    published_at: datetime
    updated_at: datetime
    parent_id: Optional[str] = None


class Comment(BaseModel):
    id: str
    snippet: Snippet
