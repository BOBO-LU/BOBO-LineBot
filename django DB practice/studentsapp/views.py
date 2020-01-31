from django.shortcuts import render
from studentsapp.models import student

def listone(request): 
	try: 
		unit = student.objects.get(cName="v") #讀取一筆資料
	except:
  		errormessage = " (讀取錯誤!)"
	return render(request, "listone.html", locals())

def listall(request):  
    try:
        students = student.objects.all().order_by('id')  #讀取資料表, 依 id 遞增排序
    except:
        errormessage = " (listall 出現錯誤)"
    return render(request, "listall.html", locals())


def insert(request):  #新增資料
    try:

        cName = 'melody'
        cSex =  'F'
        cBirthday =  '1997-12-26'
        cEmail = 'bear@superstar.com'
        cPhone =  '0963245612'
        cAddr =  '台北市信義路'
        unit = student.objects.create(cName=cName, cSex=cSex, cBirthday=cBirthday, cEmail=cEmail,cPhone=cPhone, cAddr=cAddr) 
        unit.save()  #寫入資料庫
        students = student.objects.all().order_by('-id')  #讀取資料表, 依 id 遞減排序
    except:
        errormessage = "error insert"
    return render(request, "listall.html", locals())
	
def modify(request):  #刪除資料
    try:
        unit = student.objects.get(id=5)
        unit.cName = '張四平'
        unit.cAddr = '台北市信義路234號'
        unit.save()  #寫入資料庫
        students = student.objects.all().order_by('-id')
    except:
        errormessage = "error modify"
    return render(request, "listall.html", locals())
	
def delete(request,id=None):  #刪除資料
    try:
        unit = student.objects.get(id=5)
        unit.delete()
        students = student.objects.all().order_by('-id')
    except:
        errormessage = "error delete"
    return render(request, "listall.html", locals())


