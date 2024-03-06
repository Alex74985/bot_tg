from flask import redirect, url_for, render_template, request
from bot import create_app, db
from flask_admin.contrib.sqla import ModelView


app = create_app()


@app.route('/')
def main():
    return redirect(url_for('admin.admin_main'))
    # return redirect('/admin', 302)


if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True, port=5000)
