class KeyValue:
    class Exceptions:
        class KeyAlreadyExists(Exception):
            pass
        class KeyError(Exception):
            pass

    def __init__(self):
        self.connections = []
        self.keys = []
        self.values = []
        self.exceptions = self.Exceptions()

    def __repr__(self):
        current_repr_string = "<"
        for x in self.connections:
            current_repr_string += f"\"{str(self.keys[x[0]])}\": \"{str(self.values[x[1]])}\", "
        current_repr_string = current_repr_string.removesuffix(", ") + ">"
        return current_repr_string
    
    def __str__(self):
        return self.__repr__()

    def insert(self, key, value):
        if key in self.keys:
            raise self.exceptions.KeyAlreadyExists(f"Key already exists: {key}")
        new_indexing = (len(self.keys), len(self.values))
        self.keys.append(key)
        self.values.append(value)
        self.connections.append(new_indexing)

    def remove(self, key):
        if not key in self.keys:
            raise self.exceptions.KeyError(f"Key doesn't exist: {key}")
        index_k = self.keys.index(key)
        for connection in self.connections:
            if connection[0] == index_k:
                index_v = connection[1]
        connection = (index_k, index_v)
        self.keys.remove(key)
        self.values.remove(self.values[index_v])
        self.connections.remove(connection)

    def get_at(self, key):
        if not key in self.keys:
            raise self.exceptions.KeyError(f"Key doesn't exist: {key}")
        index_k = self.keys.index(key)
        for connection in self.connections:
            if connection[0] == index_k:
                index_v = connection[1]
        return self.values[index_v]
    
    def edit_at(self, key, new_value):
        if not key in self.keys:
            raise self.exceptions.KeyError(f"Key doesn't exist: {key}")
        index_k = self.keys.index(key)
        for connection in self.connections:
            if connection[0] == index_k:
                index_v = connection[1]
        self.values[index_v] = new_value