# schemes

## Description
Schemes is a python package that allows you to easily create and manage data schemes for your data science projects.

## Installation
```bash
pip install model_schemes
```

## Usage
```python
from model_schemes.legal import petition
data = {...}
p= petition.PetitionSchema(**data)
p.model_dump()
p.model_dump_json()
```
## License
[MIT](https://choosealicense.com/licenses/mit/)

## Author
[Russell-AI](https://github.com/russell-ai)

