from .base import BaseModel
from typing import Dict, Any, List
import json


class BaseMessage(BaseModel):
    role: str
    content: str
    kwargs: Dict[str, Any] = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.role = kwargs.pop("role", self.role)
        self.content = kwargs.pop("content", self.content)
        self.kwargs = kwargs

    def dump(self):
        return {"role": self.role, "content": self.content, **self.kwargs}


class SystemMessage(BaseMessage):
    role: str = "system"


class UserMessage(BaseMessage):
    role: str = "user"


class AIMessage(BaseMessage):
    role: str = "assistant"


class ToolMessage(BaseMessage):
    role: str = "tool"


def convert_messages_to_dicts(messages: List[BaseMessage]) -> List[Dict[str, Any]]:
    """Convert a list of messages to a list of dicts"""
    return [message.dump() for message in messages]


def convert_dicts_to_messages(dicts: List[Dict[str, Any]]) -> List[BaseMessage]:
    """Convert a list of dicts to a list of messages"""
    messages = []
    for d in dicts:
        if d["role"] == "system":
            messages.append(SystemMessage(**d))
        elif d["role"] == "user":
            messages.append(UserMessage(**d))
        elif d["role"] == "assistant":
            messages.append(AIMessage(**d))
        elif d["role"] == "tool":
            messages.append(ToolMessage(**d))
        else:
            messages.append(BaseMessage(**d))
    return messages
