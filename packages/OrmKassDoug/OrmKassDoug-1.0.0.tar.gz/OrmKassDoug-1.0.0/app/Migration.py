
    
class Migration:
    
    __file__ = None
    __conn__ = None
    __type__ = None
    __table__ = None    
    __comment__ = None
    
    __rollback__ = False
    

    def __init__(self) -> None:       
        
        self.SQL = ''
        
        self.params = {}
        
        self.columns = []
        
        self.column = {}
        
        self.primary_key = None
                         
        
    def up(self):
        return self
    
    
    def down(self):        
        return self
     
     

      
    #  TIPOSS ------------------
    
    def add(self):
        self.columns.append(self.column)
        self.column = {}
        return
        
        
    def id(self):
        self.column['name'] = 'id'
        self.column['type'] = 'BIGINT'
        self.column['unsigned'] = 'UNSIGNED'
        self.column['isNull'] = 'NOT NULL'  
        self.column['autoIncrement'] = 'AUTO_INCREMENT'  
        self.column['primary_key'] = 'PRIMARY KEY'     
        
        return self    
        
      
    def string(self, name, qnt:int = 255):
        self.column['name'] = name
        self.column['type'] = f"VARCHAR({qnt})"
        self.column['isNull'] = 'NOT NULL'    
                
        return self    
    
    
    def bigInteger(self, name):
        self.column['name'] = name
        self.column['type'] = f"BIGINT"
        self.column['isNull'] = 'NOT NULL'    
                
        return self    
    
    
    def bigIntegerUnisigned(self, name):
        self.column['name'] = name
        self.column['type'] = f"BIGINT UNSIGNED"
        self.column['isNull'] = 'NOT NULL'    
                
        return self 
    
    
    def text(self, name):
        self.column['name'] = name
        self.column['type'] = f"TEXT"
        self.column['isNull'] = 'NOT NULL'    
                
        return self   
        
        
    def enum(self, name:str, values:list):    
        str_values = ', '.join(map(lambda x: f'"{x}"', values))
        
        self.column['name'] = name
        self.column['type'] = f"ENUM({str_values})"
        self.column['isNull'] = 'NOT NULL'
        
        return self
    
    
    def integer(self, name:str, qnt:int = None):        
        self.column['name'] = name
        
        if qnt!=None:
            self.column['type'] = f"INT({qnt}) ZEROFILL UNSIGNED"
        else:
            self.column['type'] = f"INT"
        self.column['isNull'] = 'NOT NULL'
        
        return self
       
       
    def datetime(self, name:str):
        self.column['name'] = name
        self.column['type'] = "DATETIME"
        self.column['isNull'] = 'NOT NULL'
        
        return self
       
    # TIPOSS-----------
    
    
    
    # TOOLS-----------
       
       
    def nullable(self):        
        self.column['isNull'] = 'NULL'
        
        return self
    
    
    def unsigned(self):        
        self.column['unsigned'] = 'UNSIGNED'
        
        return self
    
    
    def comment(self, comment:str):
        self.column['comment'] = f"COMMENT '{comment}' "
        return self
    
    
    def unique(self, columns:list=None, name=None):  
        
        if columns!=None or name!=None:      
            
            uniq = ''
            for col in columns:
                uniq += f"{col}, "
                
            uniq = uniq[:-2]                       
       
            self.column['unique_key'] = f" UNIQUE KEY {name} ()" 
            return self
        else:
        
            self.column['unique'] = f"UNIQUE"                
            return self
            
            
    def current_timestamp(self):
        self.column['current_timestamp'] = 'DEFAULT CURRENT_TIMESTAMP' 
        
        return self
    
    
    def update_timestamp(self):
        self.column['on_update_timestamp'] = 'ON UPDATE CURRENT_TIMESTAMP' 
        
        return self    
            
    # TOOLS-----------
    
    
    
    
    def addColumn(self):
        self.column['add'] = "ADD COLUMN "
        
        return self
    

    def dropColumn(self):
        print('dropColumn in dev')
        
        return self
    
    
    def after(self, column:string):
        self.column['after'] = f"AFTER {column}"
        return self
        
        
    def first(self, column:string):
        self.column['first'] = f"FIRST {column}"
        return self
        
                
        
    
    
    
    def generate_sql(self):
        
        
        if self.__type__ in ['create','alter']:
            self.up()
            
        elif self.__type__ == 'drop':
            self.down()

        

         
        if self.__type__ == 'create' and self.__rollback__ == False:
            self.SQL = f"CREATE TABLE IF NOT EXISTS {self.__table__} {'('}"
        
            for col in self.columns:   
                column = '' 
                for value in col.values():              
                    column += f"{value} "
                
                self.SQL += f"{column}, "
            
            
            
            if self.primary_key != None:
                self.SQL += f"PRIMARY KEY ({self.primary_key})"
                
            
            
            self.SQL = self.SQL[:-2] 
            self.SQL += ");"
            
            
            
        elif self.__type__ == 'alter' and self.__rollback__ == False:
            self.SQL = f"ALTER TABLE {self.__table__} "
            
            
            for col in self.columns:   
                column = '' 
                for value in col.values():              
                    column += f"{value} "
                
                self.SQL += f"{column}, "
            
            self.SQL = self.SQL[:-2]     
            
        else:
            print('DROP')
       
    
    def dropTableIfExists(self):
        self.SQL = f"DROP TABLE IF EXISTS {self.__table__};"
          
    
    def execute(self, rollback:bool = False):
        
        if rollback == False:
            self.generate_sql()     
        else:
            self.dropTableIfExists()
            
        try:
            db.get_engine(self.__conn__).connect().execute(statement=text(self.SQL),parameters=self.params)
            return True
        except Exception as err:       
            return err
              
       









            
        
    def toSql(self):
        self.generate_sql()
        
        print(self.SQL)
   
        return self.SQL    

        
    

    # def types(self):
        
    #     # Números Inteiros:
    #     TINYINT
    #     SMALLINT
    #     MEDIUMINT
    #     INT ou INTEGER
    #     BIGINT
        
        
    #     # Números Decimais/Floating-Point:
    #     FLOAT
    #     DOUBLE
    #     DECIMAL ou NUMERIC
        
        
    #     # Datas e Horas:
    #     DATE
    #     TIME
    #     DATETIME
    #     TIMESTAMP
    #     YEAR
        
        
    #     # Texto e Caracteres:
    #     CHAR
    #     VARCHAR
    #     TEXT
    #     TINYTEXT
    #     MEDIUMTEXT
    #     LONGTEXT
        
        
    #     # Binários:
    #     BINARY
    #     VARBINARY
    #     BLOB
    #     TINYBLOB
    #     MEDIUMBLOB
    #     LONGBLOB
        
        
    #     # Valores Booleanos:   
    #     BOOLEAN ou BOOL
    #     BIT
        
        
    #     # Outros Tipos Especiais:
    #     ENUM
    #     SET
        
    #     # Tipos Espaciais (para dados geoespaciais):
    #     GEOMETRY
    #     POINT
    #     LINESTRING
    #     POLYGON
    #     MULTIPOINT
    #     MULTILINESTRING
    #     MULTIPOLYGON
    #     GEOMETRYCOLLECTION