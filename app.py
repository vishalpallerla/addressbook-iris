from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, text
from flask.cli import with_appcontext, AppGroup
import click

app = Flask(__name__)

# Configure the database connection
engine = create_engine("iris://superuser:SYS@localhost:1972/DEVOCADO")
conn = engine.connect()

@app.route('/')
def index():
    query = 'SELECT * FROM AddressBook.Address'
    result = conn.exec_driver_sql(query)
    entries = [row for row in result]
    return render_template('index.html', entries=entries)

@app.route('/new', methods=['GET', 'POST'])
def new_entry():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        query = text("""
            INSERT INTO AddressBook.Address (Name, Address)
            VALUES (:name, :address)
        """)
        conn.execute(query, {'name': name, 'address': address})
        conn.commit()
        return redirect(url_for('index'))
    return render_template('new_entry.html')

@click.command('create-table')
@with_appcontext
def create_table():
    query = """
        CREATE TABLE AddressBook.Address (
            Id INTEGER IDENTITY PRIMARY KEY,
            Name VARCHAR(100) NOT NULL,
            Address VARCHAR(200) NOT NULL
        )
    """
    conn.exec_driver_sql(query)

app.cli.add_command(create_table)

if __name__ == '__main__':
    app.run(debug=True)