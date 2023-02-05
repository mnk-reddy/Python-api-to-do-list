from flask import Flask,request,jsonify
import csv
app = Flask(__name__)


@app.route('/delete')           #Delete Api
def delete():

    file=open('tasks.csv','r',newline='')       #read csv File
    read=csv.reader(file)
    next(read)

    task=request.args['Task']   # Task to be deleted
    
    updated_tasks=[]            #store updated tasks
    flag=0                      # to check if task exists
    
    
    for row in read:            #iterate through existing tasks
        if task==row[0]:
            flag=1
            continue
        else:
            updated_tasks.append(row)
    file.close()


    if flag!=1:                 #If no Task
        return task+' Does not exist in to-do list'
    
    file=open('tasks.csv','w',newline='')       #Open file and write new tasks
    write=csv.writer(file)
    head=['Task','Status']
    write.writerow(head)
    write.writerows(updated_tasks)
    file.close()


    return task+' Deleted successfully'

@app.route('/update')
def change_status():                        #Api to change status
    
    file=open('tasks.csv','r',newline='')
    read=csv.reader(file)
    next(read)
    
    task=request.args['Task']
    updated_tasks=[]
    flag=0                              # To check if task exists

    for row in read:
        if task==row[0]:
            status=(int(row[1])+1)%2      #change status 
            update=[task,status]
            updated_tasks.append(update)
            flag=1
        else:
            updated_tasks.append(row)
    file.close()
    
    if flag!=1:
        return task+' Does not Exist'
    
    file=open('tasks.csv','w',newline='')
    write=csv.writer(file)
    head=['Task','Status']
    write.writerow(head)
    write.writerows(updated_tasks)
    file.close()
    return update[0]+' Updated Successfully to '+str(update[1])     #update message

@app.route('/create')
def create():

    # read all tasks from request
    new_task=request.args.to_dict(flat=False)
    tasks=new_task['Task']
    
    #check if tasks already present
    previous_task=set()
    file=open('tasks.csv','r',newline='')
    read=csv.reader(file)
    next(read)

    for i in read:
        previous_task.add(i[0])
    for i in tasks:
        if i in previous_task:
            tasks.remove(i)
    file.close()

    # add only unique tasks into file
    file=open('tasks.csv','a',newline='')
    write=csv.writer(file)
    for i in tasks:
        write.writerow([i,0])
    file.close()
    return 'success'

@app.route('/tasks')
def tasks():                # get all tasks from file

    file=open('tasks.csv','r',newline='')
    read=csv.reader(file)
    next(read)

    tasks={'Tasks':[]} 
    for i in read:
        tasks['Tasks'].append({'Task':i[0],'Status':i[1]})
    file.close()

    return jsonify(tasks)

if __name__ == '__main__':
    app.run(debug=True)