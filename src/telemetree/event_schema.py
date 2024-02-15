from pydantic import BaseModel
from typing import List, Optional
import datetime
from telemetree import entities_schema


class Update(BaseModel):
    update_id: int
    message: Optional[entities_schema.Message]
    edited_message: Optional[entities_schema.Message]
    inline_query: Optional[entities_schema.InlineQuery]
    chosen_inline_result: Optional[entities_schema.ChosenInlineResult]
    my_chat_member: Optional[entities_schema.MyChatMember]
