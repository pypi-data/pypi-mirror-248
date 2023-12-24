# Interface w/ vector databases as virtual tables in SQLite
# Uses the APSW library to let us use the SQLite C API in Python
# refer to: https://rogerbinns.github.io/apsw/vtable.html

# Key concepts:
# - VTModule: a template for creating virtual tables
# - VT: a virtual table instance
# - VTCursor: a cursor instance (for iterating over rows in the virtual table)

class VTCursor:
    def __init__(self, embedder, index):
        self.rowid = 0
        self.query = ""
        self.ids = []
        self.similarities = []
        self.embedder = embedder
        self.index = index

    def Column(self, number):
        if number == 0:
            return self.ids[self.rowid]
        elif number == 1:
            return self.query
        elif number == 2:
            return self.similarities[self.rowid]

    def Eof(self):
        return self.rowid >= len(self.ids)
    
    def Filter(self, idxNum, idxStr, constraintArgs):
        self.query = constraintArgs[0]
        query_vector = self.embedder(self.query)
        self.ids, self.similarities = self.index.search(query_vector, top_k=10)
    
    def Next(self):
        self.rowid += 1

    def Rowid(self):  
        return self.rowid

    def Close(self):
        pass

class VT:
    def __init__(self, embedder, index):
        self.embedder = embedder
        self.index = index

    def BestIndex(self, constraints, orderbys):
        constraint_usage = [0 if c[0]==1 else None for c in constraints] # passed in argv to Filter
        # contraint_usage, idxNum, idxStr, sorted, estimatedCost
        return (constraint_usage, 0, '', True, 100)
    
    def Open(self):
        return VTCursor(self.embedder, self.index)

    def UpdateInsertRow(self, newrowid, newvalues):
        id, query, similarity = newvalues
        self.index.add(id, self.embedder(query))
        return 0  # TODO: return new rowid


class VectorVirtualTableModule:
    def __init__(self, embedder, index):
        self.embedder = embedder
        self.index = index

    def Create(self, connection, modulename, databasename, tablename, *args):
        create_stmt = f"CREATE TABLE x(id INTEGER, query TEXT, similarity REAL)"
        vtable = VT(self.embedder, self.index)
        return (create_stmt, vtable)
    Connect = Create 