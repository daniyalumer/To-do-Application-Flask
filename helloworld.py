#create, read, update and delete --- create and update can be under the same. if id given update else create
# id, description, date created, date updated, find the hash of the description to put in id.
#crud operations need to be done 

from flask import Flask, render_template, jsonify, request, redirect, url_for
from datetime import datetime
import hashlib

app = Flask(__name__)

todo_list=[]

def generatehash(description):
    return hashlib.md5(description.encode('utf-8')).hexdigest()


@app.route('/todo', methods=['POST'])
def create_or_update_todo():
    description=request.form.get('description')
    id=request.form.get('id')
    currenttime=str(datetime.now())[:-7]
    #update item
    if id:
        for todo in todo_list:
            if id == todo['id']:
                todo['description']=description
                todo['dateupdated']=currenttime
                return jsonify({'message': f'item {id} updated successfully', 'todo': todo}), 200
            return jsonify({'error': 'Todo item not found'}), 404
    #create item
    else:
        todo_id=generatehash(description)
        for todo in todo_list:
            if todo['id']==todo_id:
                return jsonify({'error': 'Item with the same description already exists'}), 400
        
        new_todo_item = {
            'id': todo_id,
            'description': description,
            'date_created': currenttime,
            'date_updated': currenttime,
            'date_completed': None,
            'completed': False
        }
        todo_list.append(new_todo_item)
        return jsonify({'message': 'New item created in to do list', 'todo': new_todo_item}), 201

@app.route('/completed/<string:todo_id>', methods=['POST'])
def completed_todo_by_id(todo_id):
    current_time=str(datetime.now())[0:7]
    for todo in todo_list:
        if todo['id']==todo_id:
            todo['completed']=True,
            todo['date_completed']=current_time
            return redirect(url_for('home'))
    return jsonify({'error': 'Todo item not found'}), 404

@app.route('/')
def home():
    return render_template('index.html', todos=todo_list)

if __name__ == '__main__':
    app.run(debug=True)
