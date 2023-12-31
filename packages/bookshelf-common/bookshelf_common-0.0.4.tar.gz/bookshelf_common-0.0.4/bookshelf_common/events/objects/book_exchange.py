from dataclasses import dataclass, asdict
import json

@dataclass
class BookExchange:
  id: int
  title: str
  slug: str
  novelist: str
  description: str
  price: int
  status: str
  genre: str
  user_id: int
  version: int
  action: str = 'create'

  @property
  def subject(self) -> str:
    return 'book_exchange'
  
  @property
  def message_body(self) -> str:
    return json.dumps(asdict(self))

  # @subject.setter
  # def subject(self, subject: str):
  #       self._subject = subject