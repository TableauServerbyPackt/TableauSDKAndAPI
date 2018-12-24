## import the libraries
import tableausdk.Extract as tde
import pandas as pd
import os

## bring in a sample Graduate School Admissions datasets
file_name = "http://www.ats.ucla.edu/stat/data/binary.csv"
df = pd.read_csv(file_name)
df.head()
df.shape

## create the extract name, but remove the extract if it already exists
fname = "example.tde"
try:  
    tdefile = tde.Extract(fname)
except:
    os.system('del ' + fname)
    os.system('del DataExtract.log')
    tdefile = tde.Extract(fname)


## define the table definition
tableDef = tde.TableDefinition()

## create a list of column names and types
colnames = df.columns
coltypes = df.dtypes

## create a dict for the field maps
## Caveat: I am not including all of the possibilities below
fieldMap = {
    'float64' :     tde.Types.Type.DOUBLE,
    'float32' :     tde.Types.Type.DOUBLE,
    'int64' :       tde.Types.Type.DOUBLE,
    'int32' :       tde.Types.Type.DOUBLE,
    'object':       tde.Types.Type.DOUBLE,
    'bool' :        tde.Types.Type.DOUBLE
}

## for each column, add the appropriate info the Table Definition
for i in range(0, len(colnames)):
    cname = colnames[i]
    ctype = fieldMap.get(str(coltypes[i]))
    tableDef.addColumn(cname, ctype)  


## create the extract from the Table Definition
## Super Hacky, but legible
## for each row, add the data to the table
## Again, not accounting for every type or errors
with tdefile as extract:
    table = extract.addTable("Extract", tableDef)
    for r in range(0, df.shape[0]):
        row = tde.Row(tableDef)
        for c in range(0, len(coltypes)):
            if str(coltypes[c]) == 'float64':
                row.setDouble(c, df.iloc[r,c])
            elif str(coltypes[c]) == 'float32':
                row.setDouble(c, df.iloc[r,c])
            elif str(coltypes[c]) == 'int64':
                row.setDouble(c, df.iloc[r,c])   
            elif str(coltypes[c]) == 'int32':
                row.setDouble(c, df.iloc[r,c])
            elif str(coltypes[c]) == 'object':
                row.setString(c, df.iloc[r,c])
            elif str(coltypes[c]) == 'bool':
                row.setBoolean(c, df.iloc[r,c])
            else:
                row.setNull(c)
        # insert the row
        table.insert(row)

## close the file
tdefile.close()