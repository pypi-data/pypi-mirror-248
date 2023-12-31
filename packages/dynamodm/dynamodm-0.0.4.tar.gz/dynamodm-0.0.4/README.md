# DynamoDB Object Document Mapper (ODM) for Python

## Installation

```bash
pip install dynamodm
```

## Usage

```python

from dynamodm import DynaModel, Field

class User(DynaModel):
	sub: str = Field(pk=True)
	name: str = Field(sk=True)
	age: int

user = User(sub="user", name="John Doe", age=42)

async def main():
	await user.put()
	# User(sub='user', name='John Doe', age=42)
	await User.get(pk="user", sk="John Doe")
	# User(sub='user', name='John Doe', age=42)
	await User.query(pk="user", sk="John Doe",operator="begins_with")
	# [User(sub='user', name='John Doe', age=42)]
	await User.delete(pk="user", sk="John Doe")
	# None
	
```

## Features

- [x] Type hints
- [x] Automatic schema generation
- [x] Automatic table creation
- [x] Automatic table updates
- [x] Automatic table deletion
