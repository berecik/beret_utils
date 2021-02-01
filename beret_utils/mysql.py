#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Table:
    """
    class for manual SQL table manipulation
    """

    def __init__(self, db, name):
        """class initialise
        arguments:
            db:     data base object
            name:   name of destination table
        modifies fields:
            fields: table's column list
            name:   name of destination table
            db:     database object
            id:     name of destination table's primary key
        """
        self.name = name
        self.db = db
        cl = self.db.cursor()
        sql = "describe `%s`;" % str(name)
        cl.execute(sql)
        self.fields = {}
        fields = cl.fetchall()
        for field in fields:
            if 'auto_increment' in field[-1]:
                self.id = field[0]
            self.fields[field[0]] = field

    def getValues(self, table_name, col_name=False, col_val=False, sql=False):
        """take data from another table
        arguments:
            table_name: source table name
            col_name:   name of column to filter records
            col_val:    filtered value
            sql:        custom query
        modifies fields:
            values:     data to insert to destination table
            columns:    column's names in destination table
        """
        if not sql:
            sql = "select * from `%s` "
        if table_name:
            sql = sql % str(table_name)
        if col_name and col_val:
            sql = sql + " where %s in (" % col_name
            a = ''
            for x in col_val:
                sql = sql + a + "'%s'" % str(x)
                a = ','
            sql = sql + ")"
        sql = sql + ";"
        #        print sql

        cl = self.db.cursor()
        cl.execute(sql)
        self.values = cl.fetchall()
        self.columns = map(lambda x: x[0], cl.description)

    def transValues(self, column, trans_dict):
        """
        translate value of given column by given dictionary
        arguments:
            column:        name of column to translation
            trans_dict:    translation dictionary
        modifies fields:
            values:        in given column change values by translation dictionary
        """
        new_values = []
        id_index = self.columns.index(self.id)
        trans_index = self.columns.index(column)
        self.fields = self.__excludeId(self.columns, id_index)
        for v in self.values:
            value = list(v)
            value[trans_index] = trans_dict[value[trans_index]]
            new_values.append(value)
        self.values = new_values

    def sqlInsert(self, table, values, fields=False):
        """create SQL query
        arguments:
            table:    table name
            values:   values
            fields:   field's names to insert values
        """
        sql = "insert into `%s` " % table
        if fields:
            sql = sql + "("
            for field in fields:
                sql = sql + "`%s`," % str(field)
            sql = sql[:-1] + ") "
        sql = sql + "values ("
        for value in values:
            sql = sql + "%s," % self.sqlValue(value)
        sql = sql[:-1]
        sql = sql + ");\n"
        return sql

    def sqlValue(self, value):
        """
        change value to SQL text format
        """
        if type(value) == type(None):
            return "NULL"
        else:
            return "'%s'" % self.db.escape_string(str(value))

    def insertValues(self, column=False, trans_dict=False):
        """
        insert new values to destination table
        arguments:
            column:        foregin key column to translation
            trans_dict:    translation dictionary
        """
        cl = self.db.cursor()
        self.ids = {}
        self.bads = []
        id_index = self.columns.index(self.id)
        if column:
            self.transValues(column, trans_dict)
        self.fields = self.__excludeId(self.columns, id_index)
        for value in self.values:
            sql = self.sqlInsert(self.name, self.__excludeId(value, id_index), self.fields)
            if cl.execute(sql):
                self.ids[value[id_index]] = cl.lastrowid
            else:
                self.bads.append(value)
                print(value)

    def __excludeId(self, old, index):
        new = list(old)
        new.pop(index)
        return new


def insert_value(table, values, fields=False):
    """generate SQL query to insert given values
    parametry:
        table:    table name
        values:   values to insert
        fields:   optionaly field's names
    """
    sql = "insert into `%s` " % table
    if fields:
        sql = sql + "("
        for field in fields:
            sql = sql + "`%s`," % str(field)
        sql = sql[:-1] + ") "
    sql = sql + "values ("
    for value in values:
        if type(value) == type(None):
            sql = sql + " NULL , "
        else:
            sql = sql + "'%s'," % str(value)
    sql = sql[:-1]
    sql = sql + ");\n"
    return sql
