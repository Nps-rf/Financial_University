# -*- coding: utf-8 -*-
# noinspection SpellCheckingInspection
"""
◈ P4MTD -> Package For Manipulating Tabular Data
◈ Created on 18.12.2021 by Nikolai Pikalov
◈ @author: Nikolai Pikalov <ya.pikus@gmail.com>
◈ Changed on 21.12.2021 by Nikolai Pikalov
"""
import csv
from Exceptions import *
from Objects import *


class Util:
    """
    Works with 'Table' type
    """
    class Basics:
        """
        Basic save-load operations
        """
        @staticmethod
        def load_table(path: str, encoding: str = 'utf-8') -> dict:
            """
            :param path: path to file.
             Indication possibilities:
             ◈ Absolute path
             ◈ Path name
            :param encoding: unnecessary argument, sets an encoding for file, default: 'utf-8'
            :return: Dictionary
            """
            with open(path, 'r', encoding=encoding) as table:
                import_dict = dict(csv.reader(table))
                table = Table()
                for key in import_dict.keys():
                    table.header.append(key)
                for key in table.header:
                    table.append(import_dict[key])
                return table

        @staticmethod
        def save_table(table: Table, path: str, encoding: str = 'utf-8') -> None:
            """
            Works only with .csv
            :rtype: None
            :param table:  Table-object
            :param path: path to file.
             Indication possibilities:
             ◈ Absolute path
             ◈ Path name
            :param encoding: unnecessary argument, sets an encoding for file, default: 'utf-8'
            """
            type = path.split('.')[-1].replace('\\', '')
            with open(path, 'w', encoding=encoding) as file:
                if type == 'csv':
                    writer = csv.DictWriter(file, fieldnames=table.header, lineterminator="\r", delimiter=",")
                    writer.writeheader()
                    writer.writerows(table.fields)
                elif type == 'txt':
                    print(*table.header, file=file, sep=',')
                    for field in table.fields:
                        for head in table.header:
                            print(field.setdefault(head), file=file, end=',')
                        print(file=file)
                else:
                    raise TypeError(f'Unsupported type "{type}')

    class Operations:
        """
        Advanced operations with Table-type objects
        Methods:
            ◈ get_rows_by_number
            ◈ get_rows_by_index
            ◈ get_column_types
            ◈ set_column_types
            ◈ get_values
            ◈ set_values
            ◈ print_table
        """
        @staticmethod
        def get_rows_by_number(table: Table, start: int, stop: int, copy_table: bool = False) -> Table or staticmethod:
            """
            :rtype: Table
            :param table: Table-object, method works with table.fields
            :param start: Start of range
            :param stop:  End of range
            :param copy_table: if False, edits the source table, if True, return copy of new table
            :return: Table object
            """
            if not copy_table:
                for row in range(stop + 1, start, -1):
                    try:
                        del table.fields[row]
                    except IndexError:
                        pass
                for row in range(start - 1, -1, -1):
                    try:
                        del table.fields[row]
                    except IndexError:
                        pass

                return Util.Operations.get_rows_by_number

            else:
                ret_table = Table(header=table.header)
                for row in table.fields[start:stop + 1]:
                    ret_table.append(row)

                return ret_table

        @staticmethod
        def get_rows_by_index(table: Table, indexes: list or tuple, copy_table: bool = False) -> Table or staticmethod:
            """
            :rtype: Table
            :param table: Table-object, method works with table.fields
            :param indexes: values that should only be in table
            ◈ Example:
                                         TABLE
                        ___________________________________________
                        ||  user,password,email                  ||
                        ||  Nikolai,12345678,ya.pikus@gmail.com  ||
                        ||  Alex,423426719,example.yahoo.com     ||
                        ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
               [..] creating table
               >>> your_table : Table
               >>> Util.Operations.get_rows_by_index(table=your_table, indexes=('user', 'password'), copy_table=True)
               OUT[0]:
                                          TABLE
                                ___________________________
                                ||  user,password        ||
                                ||  Nikolai,12345678     ||
                                ||  Alex,423426719       ||
                                ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
            :param copy_table: if False, edits the source table, if True, return copy of new table
            :return: Table object
            """
            if not copy_table:
                for row in range(len(table.fields)):
                    old_field = table.fields[row]
                    table.fields[row] = dict()
                    for ind in indexes:
                        try:
                            table.fields[row].setdefault(ind, old_field[ind])
                        except KeyError:
                            pass

                return Util.Operations.get_rows_by_index
            else:
                ret_table = Table()
                ret_table.set_header(table.header)
                for row in range(len(table.fields)):
                    old_field = table.fields[row]
                    ret_table.fields.append(dict())
                    for ind in indexes:
                        try:
                            ret_table.fields[row].setdefault(ind, old_field[ind])
                        except KeyError:
                            pass

                return ret_table

        @staticmethod
        def get_column_types(table: Table, by_number=True, index=None):
            """

            :param table:
            :param by_number:
            :param index:
            :return:
            """
            if by_number and index.isalpha():
                raise IncorrectIndex()
            if index is None and by_number:
                ind = len(table.fields)
            else:
                ind = index

            if by_number and index is not None:
                types = []
                head = table.header[ind]
                types.append((head, [type(field[head]) for field in table.fields]))

                return types

            elif index is None:
                types = []
                for head in table.header:
                    types.append(['head', []])
                    for field in table.fields:
                        types[-1][0] = head
                        try:
                            types[-1][1].append(type(field[head]))
                        except KeyError:
                            types[-1][1].append(type(None))

                return types

            elif not by_number:
                types = [['head', []]]
                for field in table.fields:
                    types[-1][0] = ind
                    try:
                        types[-1][1].append(type(field[ind]))
                    except KeyError:
                        types[-1][1].append(type(None))
                return types

        @staticmethod
        def set_column_types(table: Table, index, types='str', by_number=False) -> staticmethod:
            """
            :param index:
            :param table: Table-object
            :param types: str
            :param by_number: bool
            """
            if (by_number and str(index).isalpha()) or (not by_number and str(index).isdigit()):
                raise IncorrectIndex()
            if by_number:
                index = table.header[index]
            if types == 'str':
                for field in range(len(table.fields)):
                    table.fields[field][index] = str(table.fields[field][index])
            elif types == 'int':
                for field in range(len(table.fields)):
                    table.fields[field][index] = int(table.fields[field][index])
            elif types == 'list':
                for field in range(len(table.fields)):
                    table.fields[field][index] = list(table.fields[field][index])
            elif types == 'float':
                for field in range(len(table.fields)):
                    table.fields[field][index] = float(table.fields[field][index])
            else:
                raise UnsupportedType(case=types)
            return Util.Operations.get_column_types

        @staticmethod
        def get_values(table: Table, column=0, by_number=True):
            """

            :param by_number: boll
            :param table: Table-object
            :param column: int or str
            """
            if by_number:
                head = table.header[column]
            else:
                head = column

            ret_table = [head, []]
            for field in range(len(table.fields)):
                ret_table[1].append(table.fields[field][head])
            return ret_table

        @staticmethod
        def set_values(table: Table, values, column=0):
            """

            :param table:
            :param values:
            :param column:
            """
            raise WorkInProgress()

        @staticmethod
        def print_table(table: Table):
            """
            Analog of Pretty Print, but for 'Table'
            :param table: Table-object, method works with table.fields and table.header
            """
            print('◈', *table.header, '◈', sep='  ')
            for field in table.fields:
                print('◈ ', end='')
                for head in table.header:
                    try:
                        print(field[head] + ',', end=' ')
                    except KeyError:
                        print('None' + ',', end=' ')
                print('◈')


if __name__ == '__main__':
    '''
    Improvised debug :)
    '''
    new_table = Table(header=['user', 'password', 'email'])
    new_table.append(field={'password': '5965478', 'user': 'Nikolai', 'email': 'ya.pikus@gmail.com'})
    new_table.append(field={'password': '123456787', 'user': 'Nikola', 'email': 'Soft@ya.ru'})
    new_table.append(field={'password': '42342671', 'user': 'Alex'})
    new_table.append(field={'password': 'QWERTY21', 'user': 'Смит'})
    Util.Operations.print_table(new_table)


if __name__ == '__init__':
    pass
