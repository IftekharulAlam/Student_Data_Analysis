from django.shortcuts import render
from django.db import connection
import calc.ml_code as ml_code


def home(request):
    return render(request, 'index.html')

def revenue(request):
      if request.method == 'POST':
          input_School_ID = request.POST["School_ID"]
          input_semester_name1 = request.POST["Semester1"]
          input_year1 = request.POST["Year1"]
          input_semester_name2 = request.POST["Semester2"]
          input_year2 = request.POST["Year2"]
          sql_query1="select SCHOOL_ID, SUM(ENROLLED*CREDIT_HOUR) from SECTION INNER JOIN COURSE ON SECTION.COURSE_ID = COURSE.COURSE_ID INNER JOIN DEPARTMENT ON COURSE.MAJOR_ID = DEPARTMENT.DEPARTMENT_ID where SEMESTER_NAME='"+str(input_semester_name1) +"' and SM_YEAR="+str(input_year1) + " and SCHOOL_ID ='"+str(input_School_ID) +"'"
          

          with connection.cursor() as cursor_1:
            cursor_1.execute("select SCHOOL_ID from SCHOOL")
            row1 = cursor_1.fetchall()

          with connection.cursor() as cursor_4:
            cursor_4.execute("select distinct SEMESTER_NAME from SECTION")
            row4 = cursor_4.fetchall()
          with connection.cursor() as cursor_5:
            cursor_5.execute("select distinct SM_YEAR from SECTION")
            row5 = cursor_5.fetchall()

          with connection.cursor() as cursor_2:
            cursor_2.execute(sql_query1)
            row2 = cursor_2.fetchall()
            


          my_list = []
          my_list2 = []
          data_list=[]
          data_list1=[]


          for r in row4:
            for n in r:
              my_list.append(n)
        
          for r in row5:
            for n in r:
              my_list2.append(n)
          check_point = 0 
          for r in my_list2:
            for n in my_list:
              cus_query = "select concat(SEMESTER_NAME, SM_YEAR), SUM(ENROLLED*CREDIT_HOUR) from SECTION INNER JOIN COURSE ON SECTION.COURSE_ID = COURSE.COURSE_ID INNER JOIN DEPARTMENT ON COURSE.MAJOR_ID = DEPARTMENT.DEPARTMENT_ID where SEMESTER_NAME='"+str(n)+"' and SM_YEAR="+str(r) +" and SCHOOL_ID='"+str(input_School_ID) +"'"
              with connection.cursor() as cursor_my:
                cursor_my.execute(cus_query)
                myrow = cursor_my.fetchall()
              for re in myrow:
                  if re[0]==input_semester_name1+input_year1:
                      check_point=1
                  if check_point == 1:
                      data_list.append(re)
                  if re[0]==input_semester_name2+input_year2:
                      check_point=0

          for r in range(len(my_list2)):
              for n in range(len(my_list)):
                if n+1 < len(my_list) :
                  cus_query="select concat(t1.sem_name,t2.sem_name),round(((t2.t - t1.t) / t2.t * 100)) from (select concat(SEMESTER_NAME, SM_YEAR) as sem_name , SUM(ENROLLED*CREDIT_HOUR) as t from SECTION INNER JOIN COURSE ON SECTION.COURSE_ID = COURSE.COURSE_ID INNER JOIN DEPARTMENT ON COURSE.MAJOR_ID = DEPARTMENT.DEPARTMENT_ID where SEMESTER_NAME='"+str(my_list[n])+"' and SM_YEAR="+str(my_list2[r]) +" and SCHOOL_ID='"+str(input_School_ID) +"') as t1 join (select concat(SEMESTER_NAME, SM_YEAR) as sem_name, SUM(ENROLLED*CREDIT_HOUR) as t from SECTION INNER JOIN COURSE ON SECTION.COURSE_ID = COURSE.COURSE_ID INNER JOIN DEPARTMENT ON COURSE.MAJOR_ID = DEPARTMENT.DEPARTMENT_ID where SEMESTER_NAME='"+str(my_list[n+1])+"' and SM_YEAR="+str(my_list2[r]) +" and SCHOOL_ID='"+str(input_School_ID) +"') as t2"
                  with connection.cursor() as cursor_my:
                    cursor_my.execute(cus_query)
                    myrow2 = cursor_my.fetchall()
                    
              
                  for re in myrow2:
                      data_list1.append(re)
                      
            
        

          label_data =[]
          show_data = []
          label_data1 =[]
          show_data1 = []
          for r in data_list:
            label_data.append(r[0])
            show_data.append(r[1])
          
          for r in data_list1:
            label_data1.append(r[0])
            show_data1.append(r[1])
         
        
          return render(request, 'revenue.html',{"chart_labels1":label_data1,"chart_data1":show_data1,"summary_data":data_list1,"chart_labels":label_data,"chart_data":show_data,"data1":data_list,"school_id":row1,"input_school_id":input_School_ID,"data3":row4,"data4":row5})
      with connection.cursor() as cursor_4: 
          cursor_4.execute("select distinct SEMESTER_NAME from SECTION")
          row4 = cursor_4.fetchall()
      with connection.cursor() as cursor_5:
          cursor_5.execute("select distinct SM_YEAR from SECTION")
          row5 = cursor_5.fetchall() 


      with connection.cursor() as cursor_6:
        cursor_6.execute("select SCHOOL_ID from SCHOOL")
        row6 = cursor_6.fetchall()
      return render(request, 'revenue.html',{"school_id":row6,"data3":row4,"data4":row5})

def resources(request):
      if request.method == 'POST':
          input_semester_name = request.POST["Semester"]
          input_year = request.POST["Year"]
          sql_query="select SCHOOL_ID, sum(ENROLLED),avg(ENROLLED) ,avg(ROOM.CAPACITY), (avg(ROOM.CAPACITY)-avg(ENROLLED)) from SECTION INNER JOIN COURSE ON SECTION.COURSE_ID = COURSE.COURSE_ID INNER JOIN DEPARTMENT ON COURSE.MAJOR_ID = DEPARTMENT.DEPARTMENT_ID INNER JOIN ROOM ON SECTION.ROOM_ID = ROOM.ROOM_ID WHERE SEMESTER_NAME='"+str(input_semester_name) +"' and SM_YEAR="+str(input_year)+" group by SCHOOL_ID"
        
          with connection.cursor() as cursor_2:
            cursor_2.execute("select distinct SEMESTER_NAME from SECTION")
            row2 = cursor_2.fetchall()

          with connection.cursor() as cursor_3:
            cursor_3.execute("select distinct SM_YEAR from SECTION")
            row3 = cursor_3.fetchall()
          with connection.cursor() as cursor_4:
            cursor_4.execute(sql_query)
            row4 = cursor_4.fetchall()
            

          ch_d1 = [item[0] for item in row4]
          ch_d2 = [item[1] for item in row4]
          
          return render(request, 'resources.html',{"chart_labels":ch_d1,"chart_data":ch_d2,"data2":row2,"data3":row3,"data":row4,"sem_name":input_semester_name,"year":input_year})
      with connection.cursor() as cursor_2:
        cursor_2.execute("select distinct SEMESTER_NAME from SECTION")
        row2 = cursor_2.fetchall()
      with connection.cursor() as cursor_3:
        cursor_3.execute("select distinct SM_YEAR from SECTION")
        row3 = cursor_3.fetchall()
        
      
      ch_d1 = ""
      ch_d2 = ""

      return render(request, 'resources.html',{"data2":row2,"data3":row3,"chart_labels":ch_d1,"chart_data":ch_d2,})

def enrollment(request):
    if request.method == 'POST':
      input_semester_name = request.POST["Semester"]
      input_year = request.POST["Year"]
      input_choice1 = request.POST["Option"]
      if(input_choice1 == "1-10"):
          sql_query= "select DEPARTMENT_ID, count(SECTION_ID) as summary from SECTION INNER JOIN COURSE ON SECTION.COURSE_ID = COURSE.COURSE_ID INNER JOIN DEPARTMENT ON COURSE.MAJOR_ID = DEPARTMENT.DEPARTMENT_ID where SEMESTER_NAME='"+str(input_semester_name) +"' and SM_YEAR="+str(input_year)+" and ENROLLED BETWEEN 1 and 10 and SCHOOL_ID='SETS' group by DEPARTMENT_ID"
     
      if(input_choice1 == "11-20"):
          sql_query= "select DEPARTMENT_ID, count(SECTION_ID) as summary from SECTION INNER JOIN COURSE ON SECTION.COURSE_ID = COURSE.COURSE_ID INNER JOIN DEPARTMENT ON COURSE.MAJOR_ID = DEPARTMENT.DEPARTMENT_ID where SEMESTER_NAME='"+str(input_semester_name) +"' and SM_YEAR="+str(input_year)+" and ENROLLED BETWEEN 11 and 20 and SCHOOL_ID='SETS' group by DEPARTMENT_ID"
     
      if(input_choice1 == "21-30"):
          sql_query= "select DEPARTMENT_ID, count(SECTION_ID) as summary from SECTION INNER JOIN COURSE ON SECTION.COURSE_ID = COURSE.COURSE_ID INNER JOIN DEPARTMENT ON COURSE.MAJOR_ID = DEPARTMENT.DEPARTMENT_ID where SEMESTER_NAME='"+str(input_semester_name) +"' and SM_YEAR="+str(input_year)+" and ENROLLED BETWEEN 21 and 30 and SCHOOL_ID='SETS' group by DEPARTMENT_ID"
     
      if(input_choice1 == "31-35"):
          sql_query= "select DEPARTMENT_ID, count(SECTION_ID) as summary from SECTION INNER JOIN COURSE ON SECTION.COURSE_ID = COURSE.COURSE_ID INNER JOIN DEPARTMENT ON COURSE.MAJOR_ID = DEPARTMENT.DEPARTMENT_ID where SEMESTER_NAME='"+str(input_semester_name) +"' and SM_YEAR="+str(input_year)+" and ENROLLED BETWEEN 31 and 35 and SCHOOL_ID='SETS' group by DEPARTMENT_ID"
     
      if(input_choice1 == "41-50"):
          sql_query= "select DEPARTMENT_ID, count(SECTION_ID) as summary from SECTION INNER JOIN COURSE ON SECTION.COURSE_ID = COURSE.COURSE_ID INNER JOIN DEPARTMENT ON COURSE.MAJOR_ID = DEPARTMENT.DEPARTMENT_ID where SEMESTER_NAME='"+str(input_semester_name) +"' and SM_YEAR="+str(input_year)+" and ENROLLED BETWEEN 41 and 50 and SCHOOL_ID='SETS' group by DEPARTMENT_ID"
     
      if(input_choice1 == "51-55"):
          sql_query= "select DEPARTMENT_ID, count(SECTION_ID) as summary from SECTION INNER JOIN COURSE ON SECTION.COURSE_ID = COURSE.COURSE_ID INNER JOIN DEPARTMENT ON COURSE.MAJOR_ID = DEPARTMENT.DEPARTMENT_ID where SEMESTER_NAME='"+str(input_semester_name) +"' and SM_YEAR="+str(input_year)+" and ENROLLED BETWEEN 51 and 55 and SCHOOL_ID='SETS' group by DEPARTMENT_ID"
     
      if(input_choice1 == "56-60"):
          sql_query= "select DEPARTMENT_ID, count(SECTION_ID) as summary from SECTION INNER JOIN COURSE ON SECTION.COURSE_ID = COURSE.COURSE_ID INNER JOIN DEPARTMENT ON COURSE.MAJOR_ID = DEPARTMENT.DEPARTMENT_ID where SEMESTER_NAME='"+str(input_semester_name) +"' and SM_YEAR="+str(input_year)+" and ENROLLED BETWEEN 56 and 60 and SCHOOL_ID='SETS' group by DEPARTMENT_ID"
     
      if(input_choice1 == "60+"):
          sql_query= "select DEPARTMENT_ID, count(SECTION_ID) as summary from SECTION INNER JOIN COURSE ON SECTION.COURSE_ID = COURSE.COURSE_ID INNER JOIN DEPARTMENT ON COURSE.MAJOR_ID = DEPARTMENT.DEPARTMENT_ID where SEMESTER_NAME='"+str(input_semester_name) +"' and SM_YEAR="+str(input_year)+" and ENROLLED > 60 and SCHOOL_ID='SETS' group by DEPARTMENT_ID"
     
      
      sql_query_total = "select 'Total', sum(summary) from ("+sql_query+") as dadao"

      with connection.cursor() as cursor_1:
        cursor_1.execute(sql_query)
        row1 = cursor_1.fetchall()
        
      with connection.cursor() as cursor_4:
        cursor_4.execute(sql_query_total)
        row4 = cursor_4.fetchall()

      with connection.cursor() as cursor_2:
        cursor_2.execute("select distinct SEMESTER_NAME from SECTION")
        row2 = cursor_2.fetchall()
      with connection.cursor() as cursor_3:
        cursor_3.execute("select distinct SM_YEAR from SECTION")
        row3 = cursor_3.fetchall()
      return render(request, 'enrollment.html',{"data":row1,"data2":row2,"data3":row3,"data4":row4,"sem_name":input_semester_name,"year":input_year,"for":input_choice1})
    
    with connection.cursor() as cursor_2:
        cursor_2.execute("select distinct SEMESTER_NAME from SECTION")
        row2 = cursor_2.fetchall()
    with connection.cursor() as cursor_3:
        cursor_3.execute("select distinct SM_YEAR from SECTION")
        row3 = cursor_3.fetchall()
   
        
    return render(request, 'enrollment.html',{"data2":row2,"data3":row3})

def classroom_req(request):
    if request.method == 'POST':
      input_semester_name = request.POST["Semester"]
      input_year = request.POST["Year"]
      input_choice1 = request.POST["Option"]
      if(input_choice1 == "1-20"):
          sql_query = "select * from SECTION where SEMESTER_NAME='"+str(input_semester_name) +"' and SM_YEAR="+str(input_year)+" and ENROLLED BETWEEN 1 and 20"
      
      if(input_choice1 == "21-30"):
          sql_query = "select * from SECTION where SEMESTER_NAME='"+str(input_semester_name) +"' and SM_YEAR="+str(input_year)+" and ENROLLED BETWEEN 21 and 30"
      
      if(input_choice1 == "31-35"):
          sql_query = "select * from SECTION where SEMESTER_NAME='"+str(input_semester_name) +"' and SM_YEAR="+str(input_year)+" and ENROLLED BETWEEN 31 and 35"
      
      if(input_choice1 == "36-40"):
          sql_query = "select * from SECTION where SEMESTER_NAME='"+str(input_semester_name) +"' and SM_YEAR="+str(input_year)+" and ENROLLED BETWEEN 36 and 40"
      
      if(input_choice1 == "41-50"):
          sql_query = "select * from SECTION where SEMESTER_NAME='"+str(input_semester_name) +"' and SM_YEAR="+str(input_year)+" and ENROLLED BETWEEN 41 and 50"
      
      if(input_choice1 == "51-54"):
          sql_query = "select * from SECTION where SEMESTER_NAME='"+str(input_semester_name) +"' and SM_YEAR="+str(input_year)+" and ENROLLED BETWEEN 51 and 54"
      
      if(input_choice1 == "55-64"):
          sql_query = "select * from SECTION where SEMESTER_NAME='"+str(input_semester_name) +"' and SM_YEAR="+str(input_year)+" and ENROLLED BETWEEN 55 and 64"
      
      if(input_choice1 == "65-124"):
          sql_query = "select * from SECTION where SEMESTER_NAME='"+str(input_semester_name) +"' and SM_YEAR="+str(input_year)+" and ENROLLED BETWEEN 65 and 124"
      
      if(input_choice1 == "125-168"):
          sql_query = "select * from SECTION where SEMESTER_NAME='"+str(input_semester_name) +"' and SM_YEAR="+str(input_year)+" and ENROLLED BETWEEN 125 and 168"
      
      sql_query_total="SELECT COUNT(*) AS ""Sections"",ROUND((COUNT(*)/14.0),2) AS ""Slot_of_7"", ROUND((COUNT(*)/16.0),2) AS ""Slot_of_8"" from ("+sql_query+") as dadao"
     
        
      with connection.cursor() as cursor_4:
        cursor_4.execute(sql_query_total)
        row4 = cursor_4.fetchall()

      with connection.cursor() as cursor_2:
        cursor_2.execute("select distinct SEMESTER_NAME from SECTION")
        row2 = cursor_2.fetchall()
      with connection.cursor() as cursor_3:
        cursor_3.execute("select distinct SM_YEAR from SECTION")
        row3 = cursor_3.fetchall()
      return render(request, 'classroom_req.html',{"data2":row2,"data3":row3,"data4":row4,"sem_name":input_semester_name,"year":input_year,"for":input_choice1})
    
    with connection.cursor() as cursor_2:
        cursor_2.execute("select distinct SEMESTER_NAME from SECTION")
        row2 = cursor_2.fetchall()
    with connection.cursor() as cursor_3:
        cursor_3.execute("select distinct SM_YEAR from SECTION")
        row3 = cursor_3.fetchall()
    return render(request, 'classroom_req.html',{"data2":row2,"data3":row3})



def data_input(request):
    if request.method == 'POST':
      input_enrollment = request.POST["input"]
      if input_enrollment == "":
        print("cliked")
      else:
        input_semester_name = request.POST["Semester"]
        input_year = request.POST["Year"]
        sql_query = "select SCHOOL_ID, count(SECTION_ID) as t from COURSE inner join SECTION on COURSE.COURSE_ID=SECTION.COURSE_ID INNER JOIN DEPARTMENT ON COURSE.MAJOR_ID = DEPARTMENT.DEPARTMENT_ID and SEMESTER_NAME= '"+str(input_semester_name) +" ' and SM_YEAR="+str(input_year) +" and ENROLLED between 1 and "+str(input_enrollment)+" and BLOCKED = 0 group by SCHOOL_ID"
        with connection.cursor() as cursor_1:
          cursor_1.execute(sql_query)
          row1 = cursor_1.fetchall()
        sql_query_total = "select 'Total', sum(t) from (" + sql_query +") as dadao" 

        with connection.cursor() as cursor_total:
          cursor_total.execute(sql_query_total)
          row_total = cursor_total.fetchall()
        with connection.cursor() as cursor_2:
          cursor_2.execute("select distinct SEMESTER_NAME from SECTION")
          row2 = cursor_2.fetchall()
        with connection.cursor() as cursor_3:
          cursor_3.execute("select distinct SM_YEAR from SECTION")
          row3 = cursor_3.fetchall()
        return render(request, 'data_input.html',{"data_total":row_total,"data1":row1,"data2":row2,"data3":row3,"sem_name":input_semester_name,"year":input_year})
      
    with connection.cursor() as cursor_2:
        cursor_2.execute("select distinct SEMESTER_NAME from SECTION")
        row2 = cursor_2.fetchall()
    with connection.cursor() as cursor_3:
        cursor_3.execute("select distinct SM_YEAR from SECTION")
        row3 = cursor_3.fetchall()
    return render(request, 'data_input.html',{"data2":row2,"data3":row3,"data4":row2,"data5":row3})

def data_input_2(request):
    my_list = []
    with connection.cursor() as cursor_2:
        cursor_2.execute("select distinct SEMESTER_NAME from SECTION")
        row2 = cursor_2.fetchall()
    with connection.cursor() as cursor_3:
        cursor_3.execute("select distinct SM_YEAR from SECTION")
        row3 = cursor_3.fetchall()
    if request.method == 'POST':
      for i in range(1,61):
        input_semester_name = request.POST["Semester"]
        input_year = request.POST["Year"]
        sql_all_query_q = "select SCHOOL_ID, count(SECTION_ID) as t from COURSE inner join SECTION on COURSE.COURSE_ID=SECTION.COURSE_ID INNER JOIN DEPARTMENT ON COURSE.MAJOR_ID = DEPARTMENT.DEPARTMENT_ID and SEMESTER_NAME= '"+str(input_semester_name) +" ' and SM_YEAR="+str(input_year) +" and ENROLLED ="+str(i)+" group by SCHOOL_ID"
        with connection.cursor() as cursor_2:
          cursor_2.execute(sql_all_query_q)
          row_all = cursor_2.fetchall()
          my_list.append(row_all)
      
    return render(request, 'data_input.html',{"data_list":my_list,"data2":row2,"data3":row3,"data4":row2,"data5":row3})



def course_infos(request):
    if request.method == 'POST':
      input_school_id = request.POST["School_ID"]
      sql_query = "select distinct SECTION.COURSE_ID from SECTION INNER JOIN COURSE ON SECTION.COURSE_ID = COURSE.COURSE_ID INNER JOIN DEPARTMENT ON COURSE.MAJOR_ID = DEPARTMENT.DEPARTMENT_ID where SCHOOL_ID='"+str(input_school_id) +"'"
      with connection.cursor() as cursor_1:
        cursor_1.execute(sql_query)
        row1 = cursor_1.fetchall()
      with connection.cursor() as cursor_2:
        cursor_2.execute("select distinct SCHOOL_ID from SCHOOL")
        row2 = cursor_2.fetchall()
 
      return render(request, 'course_infos.html',{"data":row1,"data2":row2})
  
    with connection.cursor() as cursor_2:
        cursor_2.execute("select distinct SCHOOL_ID from SCHOOL")
        row2 = cursor_2.fetchall()

    return render(request, 'course_infos.html',{"data2":row2})

def course_infos_2(request):
    if request.method == 'POST':
      input_course_id = request.POST["Course_ID"]
      with connection.cursor() as cursor_2:
        cursor_2.execute("select distinct SCHOOL_ID from SCHOOL")
        row2 = cursor_2.fetchall()
      with connection.cursor() as cursor_3:
        cursor_3.execute("select concat(SEMESTER_NAME,SM_YEAR), sum(ENROLLED) from SECTION where COURSE_ID='"+str(input_course_id) +"' group by SEMESTER_NAME , SM_YEAR")
        row3 = cursor_3.fetchall()
      with connection.cursor() as cursor_2:
        cursor_2.execute("select distinct SEMESTER_NAME from SECTION")
        sem_names = cursor_2.fetchall()
      with connection.cursor() as cursor_3:
        cursor_3.execute("select distinct SM_YEAR from SECTION")
        year_names = cursor_3.fetchall()
      
        my_list_sem = []
        my_list_year = []
        data_list=[]
        for r in sem_names:
          for n in r:
            my_list_sem.append(n)
        
        for r in year_names:
          for n in r:
            my_list_year.append(n)
        check_point = 0 
        for r in my_list_year:
          for n in my_list_sem:
            cus_query = "select concat(SEMESTER_NAME,SM_YEAR),sum(ENROLLED) from SECTION where SEMESTER_NAME='"+str(n)+"' and SM_YEAR="+str(r)+" and COURSE_ID='"+str(input_course_id) +"'"
            with connection.cursor() as cursor_my:
              cursor_my.execute(cus_query)
              myrow = cursor_my.fetchall()
            for re in myrow:
                data_list.append(re)

        label_data =[]
        show_data = []
        for r in data_list:
          label_data.append(r[0])
          show_data.append(r[1])
        new_label = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39]
        
        # print(ml_code.train(new_label,show_data))
        chart_data2 = ml_code.train(new_label,show_data)

        
      
      return render(request, 'course_infos.html',{"course_name":input_course_id,"chart_data2":chart_data2,"chart_labels":label_data,"chart_data":show_data,"data2":row2, "data3":data_list})

    







