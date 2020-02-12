from operator import itemgetter
import math
from collections import defaultdict

def mutex_test(tasks,semaph):  
    items = defaultdict(list)
    for row in semaph:
        items[row['sem']].append(row['task'])  #make a list of 'id' values for each 'un' key
    tmp=[d['sem'] for d in semaph]
    tmp1 = sorted(set(tmp))
    sem={}
    for el in tmp1:
        prio=0        
        if len(items[el])==0:
            sem[el]=0
            continue
        for i in range(len(items[el])):
            atask=items[el][i]
            tmp2=list(filter(lambda task: task['name'] == atask, tasks))
            prio2=tmp2[0]['P'] 
            if prio<prio2: prio=prio2
        sem[el]=prio
    #print(sem)
    lista=sorted(tasks, key=itemgetter('P'),reverse=False)
    for x in lista:
        new_lista=[d for d in lista if d['P'] < x['P']]
        # if not have any task with lower priority result is zero
        if len(new_lista)==0:
            x['B']=0
        else:
            set_mp = set()
            set_sem = set()
            for item in new_lista:
                set_mp.add(item['name'])
                tmp_name=item['name']
                tmp3=[d for d in semaph if d['task'] == tmp_name]
                for item1 in tmp3:
                    set_sem.add(item1['sem'])
            # print(x['name'])
            # print(set_mp)
            vb_list=[]
            for val in set_sem:
                if sem[val]>=x['P']:
                    #print("We test "+val)
                    for z in set_mp:
                        # print("Testing " + val + " en " + z)
                        item2=[d for d in semaph if d['task'] == z and d['sem'] == val]
                        # if empty set we not test it
                        if len(item2)==0: continue
                        #print(item2)
                        vb_list.append(item2[0]['C'])
                # else: print("Skipping "+ val)
            # if empty set blocking zero
            if len(vb_list)==0: vb=0
            # if serveral take maximun value
            else: vb=max(vb_list)
            # print("B=" + str(vb))
            x['B']=vb
    for x in tasks:
        x['RB']=x['R']+x['B']
    return tasks



def schedulable_test(lista,tipo):
    print("Sorting type: " + tipo)
    if tipo=='DMF':
        newlist=sorted(lista, key=itemgetter('D'),reverse=True)
        i=1
        for x in newlist:
            x['P']=i
            i=i+1
    elif tipo=='EMF':
        newlist=sorted(lista, key=itemgetter('T'),reverse=True)
        i=1
        for x in newlist:
            x['P']=i
            i=i+1    
    UL=0
    for x in newlist:
        UL=UL+x['C']/x['T']
    UL=UL*100.0
    tam=len(newlist)
    limit=tam*(2**(1/tam)-1)*100.0
    print("CPU Utilization: " + "{:5.2f}".format(UL) + "%")
    print("Liu and Layland test limit: " + "{:5.2f}".format(limit)+ "%")
    if UL>limit:
        print("We cannot know if system is schedulable from Liu and Layland test.")
    else:
        print("System is guaranteed schedulable by Liu and Layland test.")
    lista=sorted(newlist, key=itemgetter('P'),reverse=True)
    for x in lista:
        # if maximun priority anyone interrupts the task
        if x['P']==tam:
            x['R']=x['C']
        else:
            vr=x['C']
            vd=x['D']          
            priority=tam-x['P']
            ant=0             
            while vr<vd and vr!=ant:
                ant=vr
                nvr=x['C']
                for i in range(priority):
                    tmp=[d for d in lista if d['P'] == tam-i]
                    ele=tmp[0]
                    nvr=nvr+int(math.ceil(vr/ele['T']))*ele['C']
                vr=nvr
            x['R']=vr
    return lista

def print_list(lista):
    newlist=sorted(lista, key=itemgetter('name'),reverse=False)           
    print("Task   T    D     C    P    R    B   RB")
    planificable=True
    m_planificable=True    
    for x in newlist:
        print(x['name']+"{:8d}".format(x['T'])+"{:5d}".format(x['D'])+"{:5d}".format(x['C'])+"{:5d}".format(x['P'])+"{:5d}".format(x['R'])+"{:5d}".format(x['B'])+"{:5d}".format(x['RB']))
        if x['R']>x['D']: planificable=False
        if x['RB']>x['D']: m_planificable=False
    if planificable:
        print("System is schedulable.")
    else:
        print("System is not schedulable.")

    if m_planificable:
        print("System with mutex is schedulable.")
    else:
        print("System with mutex is not schedulable.")  
            
task1={}
task2={}
task3={}
task4={}
task5={}
task6={}
task7={}
task_list=[]
task1['name']='A'
task1['T']=1000
task1['D']=20
task1['C']=3
task_list.append(task1)
task2['name']='B'
task2['T']=100
task2['D']=100
task2['C']=10
task_list.append(task2)
task3['name']='C'
task3['T']=50
task3['D']=50
task3['C']=20
task_list.append(task3)
task4['name']='D'
task4['T']=57
task4['D']=10
task4['C']=5
task_list.append(task4)
task5['name']='E'
task5['T']=33
task5['D']=33
task5['C']=1
task_list.append(task5)
task6['name']='F'
task6['T']=7
task6['D']=7
task6['C']=1
task_list.append(task6)
task7['name']='G'
task7['T']=30
task7['D']=5
task7['C']=2
task_list.append(task7)
task_list=schedulable_test(task_list,'DMF')
mutex_list=[]
mutex1={}
mutex1['task']='A'
mutex1['sem']='S1'
mutex1['C']=2
mutex_list.append(mutex1)
mutex2={}
mutex2['task']='A'
mutex2['sem']='S3'
mutex2['C']=2
mutex_list.append(mutex2)
mutex3={}
mutex3['task']='B'
mutex3['sem']='S2'
mutex3['C']=7
mutex_list.append(mutex3)
mutex4={}
mutex4['task']='B'
mutex4['sem']='S3'
mutex4['C']=5
mutex_list.append(mutex4)
mutex5={}
mutex5['task']='B'
mutex5['sem']='S4'
mutex5['C']=2
mutex_list.append(mutex5)
mutex6={}
mutex6['task']='D'
mutex6['sem']='S1'
mutex6['C']=2
mutex_list.append(mutex6)
mutex7={}
mutex7['task']='C'
mutex7['sem']='S2'
mutex7['C']=1
mutex_list.append(mutex7)
mutex8={}
mutex8['task']='G'
mutex8['sem']='S1'
mutex8['C']=1
mutex_list.append(mutex8)
task_list=mutex_test(task_list,mutex_list)
print_list(task_list)