from flask_admin.contrib.sqla import ModelView


class TokenView(ModelView):
    column_display_pk = False
    column_labels = {
        'bot_id': 'Token бота'
    }

    can_edit = True
    can_create = False
    can_export = False
    can_delete = False

