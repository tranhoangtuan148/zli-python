import enum

from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel
from utils import get_uid


class TAttachmentContent(BaseModel):
    title: str
    description: str
    href: str
    thumb: str
    childnumber: int
    action: str
    params: str
    type: str

class TOtherContent(BaseModel):
    __root__: Dict[str, Any]

class TQuote(BaseModel):
    ownerId: int
    cliMsgId: int
    globalMsgId: int
    cliMsgType: int
    ts: int
    msg: str
    attach: str
    fromD: str
    ttl: int

class TMention(BaseModel):
    uid: str
    pos: int
    len: int
    type: Union[0, 1]

class TMessage(BaseModel):
    actionId: str
    msgId: str
    cliMsgId: str
    msgType: str
    uidFrom: str
    idTo: str
    dName: str
    ts: str
    status: int
    content: Union[str, TAttachmentContent, TOtherContent]
    notify: str
    ttl: int
    userId: str
    uin: str
    topOut: str
    topOutTimeOut: str
    topOutImprTimeOut: str
    propertyExt: Optional[Dict[str, Union[int, str]]]
    paramsExt: Dict[str, int]
    cmd: int
    st: int
    at: int
    realMsgId: str
    quote: Optional[TQuote]

class TGroupMessage(TMessage):
    mentions: Optional[List[TMention]]

class MessageType(enum.Enum):
    DIRECT = 1
    GROUP = 2

class Message(BaseModel):
    type: MessageType = MessageType.DIRECT
    data: TMessage
    threadId: str
    isSelf: bool

    def __init__(self, data: TMessage):
        super().__init__()
        self.data = data
        self.threadId = data.uidFrom if data.uidFrom != "0" else data.idTo
        self.isSelf = data.uidFrom == "0"
        uid = get_uid()
        if data.idTo == "0":
            data.idTo = uid
        if data.uidFrom == "0":
            data.uidFrom = uid

class GroupMessage(BaseModel):
    type: MessageType = MessageType.GroupMessage
    data: TGroupMessage
    threadId: str
    isSelf: bool

    def __init__(self, data: TGroupMessage):
        super().__init__()
        self.data = data
        self.threadId = data.idTo
        self.isSelf = data.uidFrom == "0"
        if data.uidFrom == "0":
            data.uidFrom = get_uid()
