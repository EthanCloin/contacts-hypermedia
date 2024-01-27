class Contact:
    contacts = ["john", "jane", "bill", "jill"]

    def search(self, pattern: str) -> list[str]:
        return [c for c in self.contacts if pattern in c]
