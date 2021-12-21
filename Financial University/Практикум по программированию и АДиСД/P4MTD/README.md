Package For Manipulating Tabular Data
=====================================
____
![https://img.shields.io/badge/Python-3.8-blue](https://img.shields.io/badge/Python-3.8-blue)
![https://img.shields.io/badge/Status-WIP-red](https://img.shields.io/badge/Status-WIP-red)
* This is a third task of the programming workshop
* The module is designed to work with tabular data using the csv library

## Basics
| Name | Arguments | Description |
|----:|:----:|:-----
| `load_table` | `path`, `encoding` | Loads data from a csv file and converts it to a Table object |
| `save_table` | `table`, `path`, `encoding` | Saves the Table object in csv or txt format |

## Operations
| Name | Arguments | Description |
|----:|:----:|:----
| `get_rows_by_number` | `table`, `start`, `stop`, `copy_table` | Getting a table
| | | from a single row or from rows from an interval by row number|
| `get_rows_by_index` | `table`, `indexes`, `copy_table` | Getting a table
| | | from a single row or from rows with values in the first column that|
| | | match the passed arguments |
|`get_column_types`| `table`, `by_number`, `index`| Getting a dictionary like >>> (Column name: [data types])|
|`set_column_types`| `table`, `index`, `types`, `by_number`| Changing the data type for a specific column |
|`get_values`| `table`, `column`, `by_number`| Getting a list of table values by column|
|`set_values`| `table`, `values`, `column`| Sets a single value for a column|
|`print_table`|`table`|Outputs a Table object in a readable form|

## Legend
* `table`: `Table-object`, contains fields and header
* `path`: `str`, path to the file
* `encoding`: `str`, encoding of the file
* `start`: `int`, start of range
* `stop`: `int`, end of range
* `copy_Table`: `bool`, A switch that indicates the operation of the method, if True, returns a copy of the table, if False, changes the original table
* `by_number`: `bool`, A switch that shows the way to specify the desired column
* `index`, `int` or `str`, It is specified in different ways depending on the value of by_number
* `indexes`, `list` or `tuple`, values that should only be in table
* `types`, `str`, specifies the required data type
* `column` = `index`
____
## Examples
#### Table
> #### Header
> >`header=['user', 'password', 'email']`  
> 
> #### Field
> > 1)`{'password': '5965478', 'user': 'Nikolai', 'email': 'ya.pikus@gmail.com'}`
> > 2)`{'password': '123456787', 'user': 'Nikola', 'email': 'Soft@ya.ru'}`  
> > 3)`{'password': '42342671', 'user': 'Alex'}`  
> > 4)`{'password': 'QWERTY21', 'user': 'Смит'}`  
#### Call
>`Util.Operations.print_table(new_table)`  
#### Result
>`◈  user  password  email  ◈`  
`◈ Nikolai, 5965478, ya.pikus@gmail.com, ◈`  
`◈ Nikola, 123456787, Soft@ya.ru, ◈`  
`◈ Alex, 42342671, None, ◈`  
`◈ Смит, QWERTY21, None, ◈`
____________
## TODO LIST


* **Refactor code**
* **Improve some methods**
* **Add new methods**
* **Expand the possibilities of working with tabular data**
* **Add support for JSON, XML, EXCEL**

