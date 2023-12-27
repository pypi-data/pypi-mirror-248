import json

class Querier:
    
    def __init__(self, conn) -> None:
    
        self.__conn = conn
        
        self.__params = {}    
        
        self.__columns = [{"name":"*"}]
        
        self.__table = None
        
        self.__table_alias = None
        
        self.__limit = None
        
        self.__offset = None
    
        self.__group = None        
        
        self.__conditional = []
        
        self.__SQL = ""
        
        
        self.__values_update = None
        
        self.__last_method = None
        
        self.__join = []
    
       
    
    
    #select-------------------------------------------------------------
    
    def select(self, columns:list[str|dict]):
        """Informar quais colunas buscar""" 
        
        self.__columns = []
    
        for col in columns:
            
            if type(col) == dict:
                self.__columns.append(col) 
            else:
                self.__columns.append({"name":col}) 
            
        return self
        
    
    def table(self, table:str, alias:str = None):
        """Informa a table e seu alias se houver"""
                
        self.__table = table
        
        self.__table_alias = alias
        
        self.__columns = self.getColumnsNames(self.__table, alias)
        
        return self
    
    
    
    
    
    #joins-------------------------------------------------------------
        
    def join(self, table, model_key, local_key):
        self.__join.append(f" LEFT JOIN {table} ON ({table}.{model_key} = {self.__table}.{local_key}) ")    
        return self
    
    
    
    
    # condicional-------------------------------------------------------------
        
    def where(self, values:dict, conector:str = 'AND'):
                
        where = ""     
               
        for col, value in values.items():
            keyParamValue, keyParam = self.paramKey(col)
            self.__params[keyParamValue] = value
            
            where += f" {col} = {keyParam} AND "
            
        where = where[:-4]    
            
        self.__conditional.append({"where":where, "conector":conector})    
        return self
            
    
    def whereIn(self, column:str, values:list[str], conector:str = "AND", type:str = ''):
        
        where = f"{column} {type} IN "
        
        vals = ''
        for index, val in enumerate(values):
            keyParamValue, keyParam = self.paramKey(f"{column}in{index}")
            self.__params[keyParamValue] = val
        
            vals += f"'{keyParam}', "
            
        where += f"({vals[:-2]})"        
    
        self.__conditional.append({"where":where, "conector":conector})    
        return self
    
    
    def whereNotIn(self, column:str, values:list[str], conector = 'AND'):
        
        return self.whereIn(column=column, values=values, type="NOT", conector=conector)  
    
    
    def orWhere(self, values:dict):
        
        return self.where(values, "OR")
    
    
    def orWhereIn(self, column:str, values:list[str]):
        
        return self.whereIn(column, values, "OR")
            
    
    def whereIsNull(self, col, conector:str = 'AND', type:str=""):        

        where = f" {col} IS {type} NULL "    
        self.__conditional.append({"where":where, "conector":conector})    
        return self
    
    
    def whereIsNotNull(self, col, conector:str = 'AND'):
        
        return self.whereIsNull(col, conector, type="NOT")
    
    
    def whereLike(self, col:str, value:str, conector:str="AND"):
        
        keyParamValue, keyParam = self.paramKey(f"like{col}")
        self.__params[keyParamValue] = value
        
        where = f" {col} LIKE {keyParam} " 
            
        self.__conditional.append({"where":where, "conector":conector})    
        return self
    
    
       
    # pos condicional   -------------------------------------------------------------         
    
    def limit(self, limit:int):
        self.__limit = limit
        return self
    
    
    def offset(self, offset:int):
        self.__offset = offset
        return self
    
    
    def groupBy(self, group:str|list[str]):  
        
        if type(group) == str:    
            grouped = group
            
        else:            
            grouped = ""
            for gr in group:
                grouped += f"{gr}, "
            grouped = grouped[:-2] 
            
        
        self.__group = grouped
            
        return self
    
    
     
    

    
    
        
    # insert update delete-------------------------------------------------------------
    def insert(self, data:dict):    
        
        self.__last_method = 'insert'    
        
        cols = ""         
        values = ""         
        for col, value in data.items():
            cols += f"{col}, "
            values += f"?, "
        cols = cols[:-2]        
        values = values[:-2]      
            
                
        sql = f"INSERT INTO {self.__table} ({cols}) VALUES ({values})"     
            

    def update(self, data):   
        
        self.__last_method = 'update'                 
    
        values = ""
        for key, value in data.items():
            keyParam = self.paramKey(key)
            self.__params[keyParam] = value
            
            values += f"{key} = {keyParam}, "  
                 
        
        values = values[:-2]   
        self.__values_update = values        
        
        self.construct_update_query()
        return self


    def delete(self):
        
        self.__last_method = 'delete'
        self.construct_delete_query()
        return self  
            
    



    
    # finalização-------------------------------------------------------------    
    
    def get(self):
        
        self.construct_select_query()
        
        data = db.get_engine(self.__conn).connect().execute(statement=text(self.__SQL),parameters=self.__params) 
        
        result_dicts = [dict(row._mapping) for row in data]
        json_result = json.dumps(result_dicts, default=str)            
        return json.loads(json_result)
    
    
    def first(self):
        pass
    
    
    def toSql(self):
        
        if self.__last_method == None:   
            self.__last_method = 'select'     
            self.construct_select_query()
            
        return {'conn':self.__conn, 'type':self.__last_method, 'query':self.__SQL, 'params':self.__params}
    
    
    def exec(self):        
        with db.get_engine(self.conn).connect() as cursor:
            cursor.execute(text(self.__SQL),parameters=self.__params)  
            cursor.commit()  
    
    
    
    
    
    
    # misc-------------------------------------------------------------
    
    
    def construct_select_query(self):        
        
        #alias       
        tableAlias = "" if self.__table_alias == None else self.__table_alias
        tableColAlias = "" if self.__table_alias == None else self.__table_alias + "."
        
        
        
        #colunas
        columns = ""
        for col in self.__columns:
            
            colAlias = ''
            if 'alias' in col:
                if col['alias'] != '':
                    colAlias = f" AS {col['alias']}"
            
            columns += f"{tableColAlias}{col['name']}{colAlias}, "             
        columns = columns[:-2]        
        
        
        
        #condicional
        where = ""
        for wheres in self.__conditional: 
            queryWhere = wheres['where']      
            where += f" {wheres['conector']} ({queryWhere})"            
        if where != '' :
            where = f" WHERE {where} "  
        where = where.replace("WHERE  AND","WHERE").replace("WHERE  OR","WHERE")
        
        
        
        #limit and offset               
        limit = f" LIMIT {self.__limit}" if self.__limit != None else ""
        offset = f" OFFSET {self.__offset}" if self.__offset != None else ""
         
         
         
        #group
        groupby = "" if self.__group == None else f" GROUP BY {self.__group}"
        
        
        #join
        join = "" 
        for jn in self.__join:
            join += jn
        
        
         
        self.__SQL = f"SELECT {columns} FROM {self.__table} {tableAlias} {join} {where} {limit} {offset} {groupby}"
    
    
    def construct_insert_query(self):
        pass
    
    
    def construct_update_query(self):
        
        #condicional
        where = ""
        for wheres in self.__conditional: 
            queryWhere = wheres['where']      
            where += f" {wheres['conector']} ({queryWhere})"            
        if where != '' :
            where = f" WHERE {where} "  
        where = where.replace("WHERE  AND","WHERE").replace("WHERE  OR","WHERE")
        
        self.__SQL = f"UPDATE {self.__table} SET {self.__values_update} {where}"     
    
    
    def construct_delete_query(self):
        
        #condicional
        where = ""
        for wheres in self.__conditional: 
            queryWhere = wheres['where']      
            where += f" {wheres['conector']} ({queryWhere})"            
        if where != '' :
            where = f" WHERE {where} "  
        where = where.replace("WHERE  AND","WHERE").replace("WHERE  OR","WHERE")
        
        self.__SQL = f"DELETE FROM {self.__table} {where}"     
                  
    
    def lenParams(self):
        return len(self.__params)
    
    
    def paramKey(self, key):
        pIndex = self.lenParams()
        keyparam = f"p{self.__table}_{key}_{pIndex}".replace('.',"_")
        return f"{keyparam}", f":{keyparam}"
    
   
    def getColumnsNames(self, table:str, alias:str = None):
        
        sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = 'nuvem_flask_api' AND TABLE_NAME = :ptable ORDER BY ORDINAL_POSITION"
        
        data = db.get_engine(self.__conn).connect().execute(statement=text(sql),parameters={'ptable':table}) 
        result_dicts = [row._mapping for row in data.fetchall()]
        
        
        data = []
        for col in result_dicts:
            if alias == None:
                data.append({"name":f"{table}.{col['COLUMN_NAME']}"})  
            else:
                data.append({"name":f"{table}.{col['COLUMN_NAME']}", "alias":f"{alias}___{col['COLUMN_NAME']}"})  
                    
        return data
    
    
    def upColumns(self, data):
        self.__columns = self.__columns + (data)