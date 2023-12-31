from dataclasses import dataclass, asdict
import json

@dataclass
class UserExchange:
  id: int
  email: str
  first_name: str
  last_name: str
  address: str
  city: str
  phone: str
  action: str = 'create'