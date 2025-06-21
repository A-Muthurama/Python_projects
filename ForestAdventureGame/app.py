from flask import Flask, render_template, request, redirect, session, url_for
from game import setup_game, process_action

app = Flask(__name__)
app.secret_key = 'forest-secret-key'  # Needed for session management

@app.route('/')
def index():
    session.clear()
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    name = request.form['name']
    session['player'] = setup_game(name)
    return redirect(url_for('town'))

@app.route('/town', methods=['GET', 'POST'])
def town():
    if 'player' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        result, next_page = process_action(session['player'], 'town', request.form['action'])
        session.modified = True  # Let Flask know session was updated
        if next_page != 'town':
            return redirect(url_for(next_page))
        return render_template('town.html', player=session['player'], result=result)

    return render_template('town.html', player=session['player'])

@app.route('/shop', methods=['GET', 'POST'])
def shop():
    if 'player' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        result, next_page = process_action(session['player'], 'shop', request.form['action'])
        session.modified = True
        if next_page != 'shop':
            return redirect(url_for(next_page))
        return render_template('shop.html', player=session['player'], result=result)

    return render_template('shop.html', player=session['player'])

@app.route('/forest', methods=['GET', 'POST'])
def forest():
    if 'player' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        result, next_page = process_action(session['player'], 'forest', request.form['action'])
        session.modified = True
        if 'Game Over' in result:
            return render_template('gameover.html', player=session['player'], result=result)
        if next_page != 'forest':
            return redirect(url_for(next_page))
        return render_template('forest.html', player=session['player'], result=result)

    return render_template('forest.html', player=session['player'])

@app.route('/quit')
def quit_game():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
