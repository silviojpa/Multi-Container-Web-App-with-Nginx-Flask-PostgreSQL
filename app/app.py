from flask import Flask, render_template_string, request, redirect
import os
import psycopg2
import time
from prometheus_flask_exporter import PrometheusMetrics


app = Flask(__name__)

metrics = PrometheusMetrics(app)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        database=os.environ.get("DB_NAME", "usuarios_db"),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASSWORD", "postgres")
    )
    return conn

def init_db():
    connected = False
    retries = 10
    while not connected and retries > 0:
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id SERIAL PRIMARY KEY,
                    nome VARCHAR(100),
                    idade INT,
                    email VARCHAR(100),
                    cpf VARCHAR(14),
                    estado VARCHAR(2)
                );
            ''')
            conn.commit()
            cur.close()
            conn.close()
            connected = True
            print("Tabela 'usuarios' verificada/criada com sucesso!")
        except Exception as e:
            print(f"Aguardando o banco de dados... Erro: {e}")
            retries -= 1
            time.sleep(3)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome = request.form['nome']
        idade = request.form['idade']
        email = request.form['email']
        cpf = request.form['cpf']
        estado = request.form['estado']
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO usuarios (nome, idade, email, cpf, estado) VALUES (%s, %s, %s, %s, %s)",
            (nome, idade, email, cpf, estado)
        )
        conn.commit()
        cur.close()
        conn.close()
        return redirect('/')

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT nome, idade, email, cpf, estado FROM usuarios;")
    usuarios = cur.fetchall()
    cur.close()
    conn.close()

    html_template = '''
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <title>Lab DevOps - Cadastro de Usuários</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f4f4f9; color: #333; }
            h2 { color: #0275d8; }
            form { background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); max-width: 400px; margin-bottom: 20px; }
            input { display: block; width: 100%; margin-bottom: 10px; padding: 8px; box-sizing: border-box; }
            button { background: #0275d8; color: white; border: none; padding: 10px; width: 100%; border-radius: 4px; cursor: pointer; }
            button:hover { background: #025val; }
            table { width: 100%; border-collapse: collapse; background: #fff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            th, td { padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }
            th { background: #0275d8; color: white; }
        </style>
    </head>
    <body>
        <h2>Cadastro de Usuários (Lab DevOps)</h2>
        <form method="POST">
            <label>Nome:</label>
            <input type="text" name="nome" required>
            <label>Idade:</label>
            <input type="number" name="idade" required>
            <label>E-mail:</label>
            <input type="email" name="email" required>
            <label>CPF:</label>
            <input type="text" name="cpf" required>
            <label>Estado:</label>
            <input type="text" name="estado" maxlength="2" required placeholder="Ex: RJ">
            <button type="submit">Cadastrar</button>
        </form>

        <h2>Usuários Cadastrados</h2>
        <table>
            <tr><th>Nome</th><th>Idade</th><th>E-mail</th><th>CPF</th><th>Estado</th></tr>
            {% for u in usuarios %}
            <tr><td>{{ u[0] }}</td><td>{{ u[1] }}</td><td>{{ u[2] }}</td><td>{{ u[3] }}</td><td>{{ u[4] }}</td></tr>
            {% endfor %}
        </table>
    </body>
    </html>
    '''
    return render_template_string(html_template, usuarios=usuarios)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)