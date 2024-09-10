from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth import authenticate, login
from .models import Teachers,Students,Marks
from django.contrib.auth.models import User
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import pandas as pd
import openpyxl
from django.db.models import Avg, Sum

def home(request):
    return render(request, 'home.html')

def login_page(request):
    # if request.user.is_authenticated:
    if 1==2:
        print("yes")
        return redirect('/main')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                print("Authenticated")
                login(request, user)
                return redirect('main')
            else:
                print(user)
                err_msg = {"msg": "Username or password is wrong, please try again"}
                return render(request, 'registration/login.html', err_msg)
        else:
            return render(request, 'registration/login.html')
    
    
@login_required(login_url='/login')
def main(request):
    query = request.GET.get('q')
    if query:
        students = Students.objects.filter(student_name__exact=query)
    else:
        students = Students.objects.all()
    return render(request, 'main.html', {'students': students})

# def register_page(request):
#     user = User.objects.create_user(username='john',
#                                  email='jlennon@beatles.com',
#                                  password='glass onion')


@login_required(login_url='/login')
def add_student(request):
    if request.method == 'POST':
        supervisor_id = request.POST['supervisor_id']
        reg_no = request.POST['reg_no']
        student_name = request.POST['student_name']

        student = Students(supervisor_id=supervisor_id, reg_no=reg_no, student_name=student_name)
        student.save()
        return redirect('main')

    return render(request, 'add_student.html')
@login_required(login_url='/login')
def add_marks(request, reg_no):
    reg_no = int(reg_no)
    if request.method == 'POST':
        subject_id = request.POST['subject_id']
        subject_name = request.POST['subject_name']
        marks = request.POST['marks']
        mark = Marks(reg_no=reg_no, subject_id=subject_id, subject_name=subject_name, marks=marks)
        mark.save()
        return redirect('report', reg_no=reg_no,)
    else:
        return render(request, 'add_marks.html', {'reg_no': reg_no})
@login_required(login_url='/login')
def report(request, reg_no):
    student = Students.objects.get(reg_no=reg_no)
    marks = Marks.objects.filter(reg_no=reg_no)
    total_marks = 0
    result = " "
    subject_count = 0
    for mark in marks:
        total_marks += mark.marks
        subject_count += 1

    # Calculate average marks
    if subject_count > 0:
        average_marks = total_marks / subject_count
    else:
        average_marks = 0  # Handle case where no subjects exist
    if average_marks > 80:
        result = "Fast Learner"
    else:
        result = "Slow Learner"
    
    marks_data = Marks.objects.all()
    subjects = Marks.objects.values('subject_id').annotate(
            total_marks=Sum('marks'),
            average_marks=Avg('marks')
    )
    subject_average_marks = []
    for subject in subjects:
        subject_average_marks.append(subject['average_marks'])
    # Creating lists to store features and target variable
    X = []
    y = []
    all_marks = []
    # Extracting features and target variable from Django model instances
    for mark in marks_data:
        X.append([mark.marks])
        all_marks.append([mark.marks])
        
        if int(mark.marks)>80:
            mark.learner_type = "Fast Learner"
        else:
            mark.learner_type = "Slow Learner"
        y.append(mark.learner_type)
    print("ALL_MARKS->",all_marks)
    print("Average MARKS->",subject_average_marks)
    # Splitting the dataset into training and testing sets (80% training, 20% testing)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize the DecisionTreeClassifier
    clf = DecisionTreeClassifier()

    # Train the Decision Tree Classifier
    clf.fit(X_train, y_train)

    # Make predictions on the testing set
    y_pred = clf.predict(X_test)

    # Calculate the accuracy of the model
    accuracy = accuracy_score(y_test, y_pred)
    round(accuracy,2)
    marks_list = [mark.marks for mark in marks]
    print(marks_list)
    context = {
        'marks': marks,
        'marklist':marks_list,
        'student': student,
        'average_marks':average_marks,
        'subject_average_marks': subject_average_marks,
        'result':result,
        'accuracy':accuracy
    }
    return render(request, 'report.html', context)

@login_required(login_url='/login')
def upload_student(request):
    if request.method =="POST":
        if 'fileUpload' in request.FILES and request.FILES['fileUpload']:
            excel_file = request.FILES['fileUpload']
            flag = excel_file.name.lower().endswith(('.xlsx', '.xls'))
            if flag==True:
                print("read")
                df = pd.read_excel(excel_file,engine='openpyxl')
                for index, row in df.iterrows():
                    student = Students(supervisor_id=row['Supervisor ID'], reg_no=row['Reg_No'], student_name=row['Student Name'])
                    student.save()
                    mark = Marks(reg_no=row['Reg_No'], subject_id=row["Subject-ID"], subject_name=row["Subject Name"], marks=row["Marks"])
                    mark.save()
                print(df)
                success = {"msg":"File Uploaded successfully"}
                return render(request,'add_student.html',success)
            else:
                error = {"msg":"Please select excel file only"}
                return render(request,'add_student.html',error)
        else:
            error = {"msg":"No file selected"}
            return render(request,'add_student.html',error)
    return render(request,'add_student.html')

@login_required(login_url='/login')
def delete_student(request, reg_no):
    student = Students.objects.get(reg_no=reg_no)
    student.delete()
    return redirect('main')

@login_required(login_url='/login')
def delete_mark(request, subject_id,reg_no):
    mark = Marks.objects.get(subject_id=subject_id,reg_no=reg_no)
    mark.delete()
    return redirect('report', reg_no)


