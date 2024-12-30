class User:
    def __init__(self, user_id, name, email):
        self.id = user_id
        self.name = name
        self.email = email

    def save(self):
        # Logic to save the user to the database
        pass

    def delete(self):
        # Logic to delete the user from the database
        pass