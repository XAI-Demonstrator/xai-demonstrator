import couchdb

from .config import settings

couch = couchdb.Server(f"http://{settings.db_user}:{settings.db_password}"  # noqa
                       f"@{settings.db_host}:{settings.db_port}")


class Repository:

    def __init__(self):
        self.db = None

    @property
    def database(self) -> couchdb.Database:
        if self.db is None:
            try:
                self.db = couch.create(settings.db_name)
            except couchdb.PreconditionFailed:
                self.db = couch[settings.db_name]
        return self.db

    def __getitem__(self, identifier: str):
        return self.database[identifier]

    def __setitem__(self, identifier: str, value):
        self.database[identifier] = value

    def __iter__(self):
        for doc_id in self.database:
            yield doc_id


repo = Repository()
