from tasks import app
from flask import render_template, request, url_for, redirect
from tasks.forms import TaskForm, ProccesTaskForm


import csv
from datetime import date

DATOS = './data/tareas.dat'
cabecera = ['title', 'description', 'date']

@app.route("/")
def index():
    fdatos = open(DATOS, 'r')
    csvreader = csv.reader(fdatos, delimiter=",", quotechar='"')

    registros = []
    for linea in csvreader:
        registros.append(linea)

  
    fdatos.close()
    return render_template("index.html", registros=registros) 


@app.route("/newtask", methods=['GET', 'POST'])
def newTask():
    form = TaskForm(request.form)

    if request.method == 'GET':
        return render_template("task.html", form=form)
    
    if form.validate():
        fdatos = open(DATOS, 'a')
        csvwriter = csv.writer(fdatos, delimiter=",", quotechar='"')

        title = request.values.get('title')
        desc = request.values.get('description')
        date = request.values.get('date')

        csvwriter.writerow([title, desc, date])

        fdatos.close()
        return redirect(url_for("index"))
    else:
        return render_template("task.html", form=form)
        
@app.route("/processtask", methods=['GET', 'POST'])
def processTask():
    form = ProccesTaskForm(request.form)

    if request.method == 'GET':

        fdatos = open(DATOS, 'r')
        csvreader = csv.reader(fdatos, delimiter=",", quotechar='"')

        registroAct = None
        ilinea = 1
        ix = int(request.values.get('ix'))
        for linea in csvreader:
            if ilinea == ix:
                registroAct = linea
                break
            ilinea += 1

        if registroAct:
            if registroAct[2]:
                fechaTarea = date(int(registroAct[2][:4]), int(registroAct[2][5:7]), int(registroAct[2][8:]))
            else:
                fechaTarea = None

            if 'btnModificar' in request.values:
                accion = 'M'

            if 'btnBorrar' in request.values:
                accion = 'B'


            form = ProccesTaskForm(data = {'ix': ix, 'title': registroAct[0], 'description': registroAct[1], 'date': fechaTarea, 'btn': accion})

            

        return render_template("processtask.html", form=form)
    
    if form.validate():
        print("Mofificar el fichero")

    return render_template("processtask.html", form=form)


   

