# cliente/db_router.py
class EpmapasRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'cliente':
            return 'epmapas'
        return 'default'

    def db_for_write(self, model, **hints):
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._state.db == 'epmapas' or obj2._state.db == 'epmapas':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == 'epmapas':
            return app_label == 'cliente'
        return True