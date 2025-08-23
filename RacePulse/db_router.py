class DatabaseRouter:
    """
    Route some models to MySQL, others to Postgres
    """

    def db_for_read(self, model, **hints):
        if getattr(model, 'f1_db', False):
            return "f1_db"
        return "default"

    def db_for_write(self, model, **hints):
        if getattr(model, 'f1_db', False):
            return "f1_db"
        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        # Allow relations if both models use the same DB
        if obj1._state.db == obj2._state.db:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # Only migrate Postgres (default)
        if db == "default":
            return True
        return False
