from pydantic import BaseModel, ValidationError


class MessageChat(BaseModel):
    ticket_id: int
    chat_message: str


class ChangeStatus(BaseModel):
    ticket_id: int
    status: str


class TicketId(BaseModel):
    ticket_id: int


class UpdateChat(BaseModel):
    ticket_id: int
    last_message_id: int


def json_check(json, model):
    try:
        json = model.parse_raw(json)
        return json
    except ValidationError as e:
        print(e.json())
