from flask_admin.contrib.sqla import ModelView


class PlayerView(ModelView):
    column_display_pk = False
    column_labels = {
        'draw_id': 'ID розыгрыша',
        'user_id': 'ID участника',
        'user_name': 'Ник участника',
    }

    column_sortable_list = ('draw_id', 'user_id', 'user_name')

    can_edit = False
    can_create = False
    can_export = True
    can_delete = False

    export_types = ['csv']
    export_max_rows = 20000

    column_searchable_list = ['user_id', 'user_name']

    edit_modal = False
