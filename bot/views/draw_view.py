from flask_admin.contrib.sqla import ModelView


class DrawView(ModelView):
    column_display_pk = True
    column_labels = {
        'id': 'ID розыгрыша',
        'user_id': 'ID создателя',
        'chanel_id': 'Канал публикации',
        'text': 'Текст',
        'winers_count': 'Количество победителей',
        'predicted_winners': 'ID нужных победителей',
        'post_time': 'Время начала',
        'end_time': 'Время конца'
    }

    column_list = ['id', 'user_id', 'chanel_id', 'text', 'winers_count', 'predicted_winners', 'post_time', 'end_time']
    column_sortable_list = ('id', 'user_id', 'chanel_id', 'post_time', 'end_time')

    can_edit = True
    can_create = False
    can_export = False
    can_delete = False

    export_types = ['csv']
    export_max_rows = 20000

    column_searchable_list = ['user_id', 'chanel_id']

    column_editable_list = ['predicted_winners']

    edit_modal = True

    form_excluded_columns = ['id', 'user_id', 'chanel_id', 'text', 'winers_count', 'post_time', 'end_time', 'message_id', 'chanel_name', 'file_type', 'file_id']
