import json

PAGE_SIZE = 100


class Contact:
    """
    representation of the model of a Contact object. exposes methods to interact with a JSON file of Contacts.
    """

    db = {}

    def __init__(
        self, id_="", first: str = "", last: str = "", phone: str = "", email: str = ""
    ):
        self.id = id_
        self.first = first
        self.last = last
        self.phone = phone
        self.email = email
        self.errors = {}

    def save(self):
        if self.id is None:
            if len(Contact.db) == 0:
                max_id = 1
            else:
                max_id = max(contact.id for contact in Contact.db.values())
            self.id = max_id + 1
            Contact.db[self.id] = self
        Contact.save_db()
        return True

    @classmethod
    def search(cls, text):
        result = []
        for c in cls.db.values():
            match_first = c.first is not None and text in c.first
            match_last = c.last is not None and text in c.last
            match_email = c.email is not None and text in c.email
            match_phone = c.phone is not None and text in c.phone
            if match_first or match_last or match_email or match_phone:
                result.append(c)
        return result

    @classmethod
    def all(cls, page=1):
        page = int(page)
        start = (page - 1) * PAGE_SIZE
        end = start + PAGE_SIZE
        return list(cls.db.values())[start:end]

    @staticmethod
    def save_db():
        out_arr = [c.__dict__ for c in Contact.db.values()]
        with open("contacts.json", "w") as f:
            json.dump(out_arr, f, indent=2)

    @classmethod
    def load_db(cls):
        with open("contacts.json", "r") as contacts_file:
            contacts = json.load(contacts_file)
            cls.db.clear()
            for c in contacts:
                cls.db[c["id"]] = Contact(
                    c["id"], c["first"], c["last"], c["phone"], c["email"]
                )
