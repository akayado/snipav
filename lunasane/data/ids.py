"""
DomainNotFoundErrors are raised whenever a instance corresponding to a
domain could not be found or the class is not properly defined for domain
handling.
"""

class DomainNotFoundError(Exception):
    def __init__(self, cls, dom):
        self.cls, self.dom = cls, dom
    def __str__(self):
        return repr(self.cls) + ', ' + repr(self.dom)

"""
Classes that hold domains must inherit the DomainHolder class and initialize count and domain_dict.
Each instance of subclasses will then have a domain.
To obtain an instance from by a domain number, one must call from_domain.
Domain numbers are generated dynamically and are not saved into any file.
"""

class DomainHolder:
    def __init__(self, cls=None):
        if cls==None:
            cls = self.__class__
        self.domain = cls.count
        cls.domain_dict[self.domain] = self
        cls.count += 1

    @classmethod
    def from_domain(cls, domain):
        if domain in cls.domain_dict:
            return cls.domain_dict[domain]
        else:
            raise DomainNotFoundError(cls, domain)

class IDNotFoundError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

"""
new_id_classes returns a pair of an ID class and an ID holder class.
IDs have domains, and IDs are unique within a domain.
An ID class can have multiple domains, thus, for example, items with the same ID in 
different Projects are permitted.

Full IDs can be used to identify a logical/visual item among multiple Projects and processes.
Full IDs can be uniquely generated by traversing item posessions using IDs and their domains.
"""

def new_id_classes(_default_prefix, digits=4):
    class AbstractID(str):
        ids = {} # dictionary of used ids of each domain.
        default_prefix = _default_prefix # prefix for ids generated by new_id.

        def __new__(cls, domain, idobj=None):
            if domain not in cls.ids:
                cls.ids[domain] = []
            if (idobj not in cls.ids[domain]) and (idobj != None):
                cls.register_id(domain, idobj)
                return super().__new__(cls, idobj)
            else:
                idobj = cls.new_id(domain)
                cls.register_id(domain, idobj)
                return super().__new__(cls, idobj)

        def serializable(self): # for JSON export
            return str(self)

        @classmethod
        def register_id(cls, domain, idobj):
            if domain in cls.ids:
                cls.ids[domain] += [idobj]
            else:
                cls.ids[domain] = [idobj]

        @classmethod
        def unregister_id(cls, domain, idobj):
            if domain in cls.ids:
                cls.ids[domain].pop(idobj)

        @classmethod
        def new_id(cls, domain):
            if domain not in cls.ids:
                cls.ids[domain] = []
            cnt = 0
            while True:
                idobj = cls.default_prefix + str(cnt).zfill(digits)
                if idobj not in cls.ids[domain]:
                    return idobj
                cnt += 1

    class AbstractIDHolder:
        def __init__(self, domain, idobj=None):
            if idobj == None:
                self.id = AbstractID(domain)
            elif idobj.__class__ == AbstractID:
                self.id = idobj
            else:
                self.id = AbstractID(domain, idobj)

    return AbstractID, AbstractIDHolder

