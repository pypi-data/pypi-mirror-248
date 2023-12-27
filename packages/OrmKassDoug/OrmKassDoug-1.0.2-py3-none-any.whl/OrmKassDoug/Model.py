from Querier import Querier

class Model():
    
    __conn__ = None    
    __table__ = None    
    
    
    def __init__(self) -> None:
        self.query = Querier(self.__conn__).table(self.__table__) 
        
        self.__objects = [] 
        
        self.__has = []
    
    
    def all(self):        
        data = self.query.get()              
        return data
    
    
    def first(self):        
        data = self.query.first()              
        return data
    
    
    def select(self, columns:list):
        self.query.select(columns)
        return self
    
    
    def get(self, data=None):
        
        # print(self.__has)
        
        if data == None:
            data = self.query.get()
            
            
            
        # separação dos dados raiz dos objetos    
        # data_objs = []
        # data_root = []
        # for index, row in enumerate(data):
        #     com_underscore = {'__rawindex__':index}
        #     sem_underscore = {'__rawindex__':index}

        #     for key, value in row.items():
        #         if '___' in key:
        #             com_underscore[key] = value
        #         else:
        #             sem_underscore[key] = value

        #     data_objs.append(com_underscore)
        #     data_root.append(sem_underscore)



        # data_objs:::: consolidadção dos objetos
        # DAT_OBJS = []
        # for index, row in enumerate(data_objs):
        #     consolidado = {}
        #     for key in row.keys():
                               
        #         if key != '__rawindex__':
                    
        #             splited = key.split("___")
        #             keyMaster = splited[0]
        #             col = splited[1]
                    
        #             dated = {col:row[key]}
                    
        #             if keyMaster not in consolidado:
        #                 consolidado[keyMaster] = dated
        #             else:
        #                 consolidado[keyMaster].update(dated)                       
                
        #         else:
        #             consolidado['__rawindex__'] = row['__rawindex__']
             
             
        #     for key in consolidado.keys():
        #         if key != '__rawindex__':
        #             if all(value is None for value in consolidado[key].values()) : consolidado[key] = {}       
                    
        #     DAT_OBJS.append(consolidado)
            

        # ajuntadoooooo
        # for index, row in enumerate(data):
        #     data_root[index]['related'] = DAT_OBJS[index]

        # data = data_root
        
        
        
        
        # mesclar dados repetidos dentro de related -----verificadrrrrr
        # newdata = []
        # keyy = 'id'
        
        # consolidado = {}

        # for item in data:
        #     item_id = item[keyy]

        #     if item_id not in consolidado:
        #         consolidado[item_id] = item
        #     else:
        #         for relatedkey in consolidado[item_id]["related"].keys():
        #             if relatedkey != '__rawindex__':
        #                 before = consolidado[item_id]["related"][relatedkey]
        #                 consolidado[item_id]["related"][relatedkey] = []
        #                 consolidado[item_id]["related"][relatedkey].append(before)
        #                 consolidado[item_id]["related"][relatedkey].append(item['related'][relatedkey])                    


        # # Converter de volta para a lista
        # data = list(consolidado.values())
        
        
        
        
        
        return data
        
        
        # # data_root:::: consolidadção dos root
        # from json import dumps
        # consolidado = {}

        # for item in data_root:
        #     print(item['__rawindex__'])
        #     item.pop('__rawindex__')
        #     # Convertendo o item em uma string JSON para ser usado como chave do dicionário
        #     chave = dumps(item, sort_keys=True)
            
        #     if chave not in consolidado:
        #         consolidado[chave] = item
        #     else:
        #         # Se a chave já existir, você pode decidir como consolidar os itens repetidos
        #         # Neste exemplo, estamos apenas mantendo o primeiro item encontrado
        #         pass

        # # Convertendo os valores do dicionário de volta para uma lista
        # consolidado = list(consolidado.values())
        
        
        
        # return consolidado
          
          
          
          
          
          
          
          
        # cria os objetos de relacionamento nos dados
        for index, reg in enumerate(data):  
            for obj in self.__objects:     
                data[index][obj] = {key.replace(f"{obj}___",""): value for key, value in data[index].items() if key.startswith(f"{obj}___")}                 
                if all(value is None for value in data[index][obj].values()) : data[index][obj] = {}        
                    
                data[index] = {key: value for key, value in data[index].items() if not key.startswith(f'{obj}___')}
                
        
                
        #remove as cols objetos--------
        keys_to_remove = []
        guard = []

        for index, row in enumerate(data[:]):
            for key, value in row.items():
                if isinstance(value, (dict, list)):
                    keys_to_remove.append((index, key))
                    guard.append({key:row[key]})   
        # Remover as chaves após o loop
        for index, key in reversed(keys_to_remove):
            data[index].pop(key, None)
                
                
                
                
        

        #retira da raiz os repetidos--------
        from json import dumps
        consolidado = {}

        for item in data:
            # Convertendo o item em uma string JSON para ser usado como chave do dicionário
            chave = dumps(item, sort_keys=True)
            
            if chave not in consolidado:
                consolidado[chave] = item
            else:
                # Se a chave já existir, você pode decidir como consolidar os itens repetidos
                # Neste exemplo, estamos apenas mantendo o primeiro item encontrado
                pass

        # Convertendo os valores do dicionário de volta para uma lista
        data = list(consolidado.values())




                
        print('\n\n\n')
        print( guard)
        print('\n\n\n')
        
        return data
        

        consolidado = {}

        for index, obj in enumerate(guard):
            for key in obj.keys():
                guard[index][key]
                
                if key not in consolidado:
                    consolidado[key] = guard[index][key]
                else:
                    
                    if type(consolidado[key]) == dict:                    
                        x = consolidado[key]
                        
                        if x['id'] != guard[index][key]['id']:                            
                            consolidado[key] = []                        
                            consolidado[key].append(x)
                            consolidado[key].append(guard[index][key])
                        else:
                            consolidado[key] = x
                    else:
                        consolidado[key].append(guard[index][key])
                    
        print(consolidado)
        
        # for index, row in enumerate(data):
        #     print('\n\n\n')
        #     print(index)
        #     print(consolidado[index])
        #     # row.append(consolidado[index])
            
            


            
        return data
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    def toSql(self):        
        return  self.query.toSql()
    
    
    def where(self,  where: dict|list[dict] ):
        self.query.where(where)
        return self
    
    
    def whereIn(self, column:str, values:list):
        self.query.whereIn(column, values)
        return self
    
    
    def has(self, model, model_key, local_key, type):
        method_name = __name__        
        rela_table = model.__table__        
        
        data = Querier(self.__conn__).getColumnsNames(rela_table, rela_table) 
               
        self.query.upColumns(data)
        
        self.query.join(rela_table, model_key, local_key)
        
        self.__objects.append(rela_table)
        
        for x in self.__has:
            for a in x.values():
                check = len(a)
                if check == 0:
                    key = list(x)[0]
                    x[key] = {"type":type,"key":local_key}
                
    
    def hasOne(self, model, model_key, local_key): 
        self.has( model, model_key, local_key, 'one')
                    
       
    def hasMany(self, model, model_key, local_key):
        self.has( model, model_key, local_key, 'many')
       
        
           
    def withModel(self, model:list|str):   
        
        def x(d):               
            method = getattr(self, d)       
            self.__has.append({method.__name__:{}})             
            method()  
            
        
        if type(model) == str:
            x(model)
        else:
            for i in model:
                x(i)
                
        return self
    
    