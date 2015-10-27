# pg-magic

### Usage
You can load csv to table by using the copy to table function
```python
from pg-magic import csv_to_table

csv_path = 'path/to/csv'
table_name = 'desired_name'

copy_to_table(table_name, csv_path)
```
