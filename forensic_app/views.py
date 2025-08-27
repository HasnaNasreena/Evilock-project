import datetime
import json
import smtplib
from email.mime.text import MIMEText

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.db.models import Count
from django.db.models.functions import ExtractYear
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from prophet import Prophet

from forensic_app.models import *
# Create your views here.





from web3 import Web3, HTTPProvider
# truffle development blockchain address
blockchain_address = 'http://127.0.0.1:7545'
# Client instance to interact with the blockchain
web3 = Web3(HTTPProvider(blockchain_address,{"timeout": 80}))
# Set the default account (so we don't need to set the "from" for every transaction call)
web3.eth.defaultAccount = web3.eth.accounts[0]
compiled_contract_path = r"C:\Users\hp\PycharmProjects\evilock\blockchain\node_modules\.bin\build\contracts\Structreq.json"
# Deployed contract address (see `migrate` command output: `contract address`)
deployed_contract_address = '0x47e7BC2e880d7Dd1C1126e6d2c9936c399Af11B9'
# Create your views here.









def login(request):
    return render(request,'index.html')
def admin_add_court(request):
    return render(request, 'admin/addcourt.html')
def logout(request):
    auth.logout(request)
    return render(request,'index.html')


@login_required(login_url='/')
def addcourtpost(request):
    name = request.POST['textfield']
    place = request.POST['textfield2']
    pin = request.POST['textfield3']
    post = request.POST['textfield9']
    district=request.POST['textfield4']
    phone = request.POST['textfield5']
    email = request.POST['textfield6']
    courttype=request.POST['type']
    username=request.POST['textfield7']
    password=request.POST['textfield8']

    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login('projectmsc25@gmail.com','otiy cfjj tuin fixp')
        print("login=======")
    except Exception as e:
        print("Couldn't setup email!!" + str(e))
    msg = MIMEText("Your new password id : " + str(password)+" And Username is :"+str(username))
    print(msg)
    msg['Subject'] = 'Password'
    msg['To'] = email
    msg['From'] = 'projectmsc25@gmail.com'

    print("ok====")

    try:
        gmail.send_message(msg)
    except Exception as e:
        print(e,"jjjjjjjjjjjjjjjjjj")
        data = {"status": "not"}
        r = json.dumps(data)
        print(r)
        return HttpResponse('''<script>alert(' Invalid');window.location='/'</script>''')
    ob1=logintbl()
    ob1.username=username
    ob1.password=password
    ob1.type="court"

    # gmail = smtplib.SMTP('smtp.gmail.com', 587)
    # gmail.ehlo()
    # gmail.starttls()
    # gmail.login('projectmsc25@gmail.com','otiy cfjj tuin fixp')
    # print("login=======pppppppppppppppppppppppppppppppppppppppppppppppp")
    # msg = MIMEText("Your new password id : " + str(password),"Your new User Name : " + str(username))
    # print(msg)
    # msg['Subject'] = 'Password'
    # msg['To'] = email
    # msg['From'] = 'projectmsc25@gmail.com'
    #
    # print("ok===0000000000000000000000000000000=")

    ob1.save()


    ob = courttbl()
    ob.LOGIN=ob1
    ob.name = name
    ob.place = place
    ob.pin = pin
    ob.post = post
    ob.district=district
    ob.phone = phone
    ob.email = email
    ob.type = courttype
    ob.save()
    return HttpResponse('''<script>alert(' succes');window.location='/admin_view_court'</script>''')

@login_required(login_url='/')
def admin_view_court(request):
    ob=courttbl.objects.all()
    return render(request, 'admin/view court.html',{'data':ob})


@login_required(login_url='/')
def admin_view_allocationhistory(request):
    ob = case_alloctbl.objects.all()
    return render(request, 'admin/view allocationhistroy.html',{'data':ob})


@login_required(login_url='/')
def searchallocationhistory(request):
    date=request.POST["textfield"]
    ob=case_alloctbl.objects.filter(date__contains=date)
    return render(request, 'admin/view allocationhistroy.html',{'data':ob,'dt':date})


@login_required(login_url='/')
def admin_view_casehistory(request):
    ob=casetbl.objects.all()
    return render(request, 'admin/view casehistory.html',{'data':ob})


@login_required(login_url='/')
def admin_view_evidance_history(request,id):
    ob=evidencetbl.objects.filter(CASEID__id=id)
    ob1=forensic_evidence.objects.filter(ALLOCID__CASEID__id=id)
    return render(request, 'admin/view_evidance.html',{'data':ob,"data1":ob1})


@login_required(login_url='/')
def searchcasehistory(request):
    date=request.POST["textfield"]
    ob=casetbl.objects.filter(date__contains=date)
    return render(request, 'admin/view casehistory.html',{'data':ob,'dt':date})


@login_required(login_url='/')
def admin_view_feedback(request):
    ob=feedbacktbl.objects.all()
    return render(request, 'admin/view feedback.html',{'data':ob})


@login_required(login_url='/')
def searchFeedback(request):
    date=request.POST["textfield"]
    ob=feedbacktbl.objects.filter(date__contains=date)
    return render(request, 'admin/view feedback.html',{'data':ob,'dt':date})

@login_required(login_url='/')
def admin_view_staff_verify(request):
    ob=forensicstafftbl.objects.all()
    return render(request, 'admin/view staff&verify.html',{'data':ob})

@login_required(login_url='/')
def acceptstaff(request,id):
    ob=logintbl.objects.get(id=id)
    ob.type='forensicstaff'
    ob.save()
    return HttpResponse('''<script>alert(' verified succes');window.location='/admin_view_staff_verify'</script>''')


@login_required(login_url='/')
def rejectstaff(request,id):
    ob=logintbl.objects.get(id=id)
    ob.type='blocked'
    ob.save()
    return HttpResponse('''<script>alert('rejected');window.location='/admin_view_staff_verify'</script>''')




@login_required(login_url='/')
def admin_view_policestation(request):
    ob=police_stationtbl.objects.all()
    return render(request, 'admin/viewpolicestation.html',{'data':ob})



@login_required(login_url='/')
def editcourt(request,id):
    request.session["id"]=id
    ob=courttbl.objects.get(id=id)
    return render(request,'admin/editcourt.html',{'data':ob})


@login_required(login_url='/')
def editcourtpost(request):
    name = request.POST["textfield"]
    place=request.POST["textfield2"]
    pin=request.POST["textfield3"]
    post=request.POST["textfield9"]
    district=request.POST["textfield4"]
    phone=request.POST["textfield5"]
    email=request.POST["textfield6"]
    type=request.POST['type']
    ob = courttbl.objects.get(id= request.session["id"])
    ob.name=name
    ob.place=place
    ob.pin = pin
    ob.post = post
    ob.district = district
    ob.phone = phone
    ob.email = email
    ob.type=type
    ob.save()
    return HttpResponse('''<script>alert('edited');window.location='/admin_view_court'</script>''')


@login_required(login_url='/')
def delete(request,id):
    ob = courttbl.objects.get(id=id)
    ob.delete()
    return HttpResponse('''<script>alert('deleted');window.location='/admin_view_court'</script>''')
    
    






def loginpost(request):
    uname=request.POST["textfield"]
    pwd=request.POST["textfield2"]
    ob=logintbl.objects.filter(username=uname,password=pwd)
    if ob.exists():
        l=logintbl.objects.get(username=uname,password=pwd)
        request.session['lid'] = l.id
        if l.type == 'admin':
            ob1=auth.authenticate(username='admin',password='admin')
            if ob1 is not None:
                auth.login(request,ob1)
            return HttpResponse('''<script>alert('Login success');window.location='/adminhome'</script>''')
        elif l.type=='court':
            ob1 = auth.authenticate(username='admin', password='admin')
            if ob1 is not None:
                auth.login(request, ob1)

            obx=courttbl.objects.get(LOGIN=l.id)
            request.session["c_dist"]=obx.district
            return HttpResponse('''<script>alert('Login success');window.location='/courthome'</script>''')
        elif l.type=="police":
            request.session['lid'] = l.id
            ob1 = auth.authenticate(username='admin', password='admin')
            if ob1 is not None:
                auth.login(request, ob1)

                xx=police_stationtbl.objects.filter(LOGIN=l.id)
                if len(xx)>0:

                    return HttpResponse('''<script>alert('Login success');window.location='/policestation'</script>''')
                else:
                    return HttpResponse('''<script>alert('Invalid user');window.location='/'</script>''')


        elif l.type == "forensicstaff":


            ob1 = auth.authenticate(username='admin', password='admin')
            if ob1 is not None:
                auth.login(request, ob1)

            x1 = forensicstafftbl.objects.filter(LOGIN=l.id)

            if len(x1)>0:
                return HttpResponse('''<script>alert('Login success');window.location='/forensichome'</script>''')
            else:
                return HttpResponse('''<script>alert('Invalid user');window.location='/'</script>''')

        else:
            return HttpResponse('''<script>alert('invalid');window.location='/'</script>''')
    else:
        return HttpResponse('''<script>alert('Invalid user');window.location='/'</script>''')

#
#
# @login_required(login_url='/')
# def adminhome(request):
#
#     cases_by_date = (
#         casetbl.objects.values("date")
#             .annotate(count=Count("id"))
#             .order_by("date")
#     )
#
#     # Extract labels (dates) and data (case counts)
#     labels = [entry["date"].strftime("%Y-%m-%d") for entry in cases_by_date]
#     data = [entry["count"] for entry in cases_by_date]
#
#     context = {
#         "labels": json.dumps(labels),
#         "data": json.dumps(data),
#     }
#     return render(request,'admin/index.html',context)
#



from django.shortcuts import render
from django.db.models import Count
from .models import casetbl, case_alloctbl
import json

def adminhome(request):

    ob=usertbl.objects.all()
    kk=ob.count()
    request.session['kk']=kk

    ab = casetbl.objects.all()
    kp = ab.count()
    request.session['kp'] = kp

    pp = casetbl.objects.filter(status='accepted')
    pp1 = casetbl.objects.filter(status='accept')
    pp=pp.union(pp1)
    pa = pp.count()
    request.session['pa'] = pa
    # Aggregating case count by date for casetbl
    # cases_by_date = (
    #     casetbl.objects.values("date")
    #     .annotate(count=Count("id"))
    #     .order_by("date")
    # )
    #
    # # Extract labels (dates) and data (case counts)
    # labels = [entry["date"].strftime("%Y-%m-%d") for entry in cases_by_date]
    # data = [entry["count"] for entry in cases_by_date]
    #
    # # Aggregating 'assigned' case count by date from case_alloctbl
    # assigned_cases_by_date = (
    #     case_alloctbl.objects.filter(status="assigned")
    #     .values("date")
    #     .annotate(count=Count("id"))
    #     .order_by("date")
    # )
    #
    # # Extract labels (dates) and data (assigned case counts)
    # assigned_data = [entry["count"] for entry in assigned_cases_by_date]
    #
    # context = {
    #     "labels": json.dumps(labels),
    #     "data": json.dumps(data),
    #     "assigned_data": json.dumps(assigned_data),
    # }

    return render(request, 'admin/index.html')






@login_required(login_url='/')
def courthome(request):
    return render(request,'court/index.html')
@login_required(login_url='/')
def court_staffassign_case(request):

    print(request.session["c_dist"])
    ob=casetbl.objects.filter(incident_district=request.session["c_dist"],status__in=['accepted','accept'])
    return render(request, 'court/staff assign tocase.html',{'data':ob})

@login_required(login_url='/')
def assign_staff(request,id):
    request.session['aid']=id

    ob=forensicstafftbl.objects.filter(district=request.session["c_dist"])
    p=case_alloctbl.objects.filter(CASEID_id=request.session['aid'])
    return render(request,'court/staff assign to case 2.html',{'data':ob,'p':p})


@login_required(login_url='/')
def assign_staff_post(request):
    staff=request.POST['select']
    p=case_alloctbl.objects.filter(STAFFID_id=staff,CASEID_id=request.session['aid'])
    if p.exists():
        return HttpResponse('''<script>alert(' case Already allocated to this staff');window.location='/court_staffassign_case'</script>''')
    else:

        ob=case_alloctbl()
        ob.CASEID=casetbl.objects.get(id=request.session['aid'])
        ob.STAFFID_id=staff
        ob.date=datetime.datetime.now()
        ob.status='assigned'
        ob.save()
        return HttpResponse('''<script>alert('assigned');window.location='/court_staffassign_case'</script>''')

@login_required(login_url='/')
def court_staff_assign_to_case_2(request):
    return render(request, 'court/staff assign to case 2.html')

@login_required(login_url='/')
def verify_evidence_request(request):
    # kk=courttbl.objects.get(LOGIN_id=request.session['lid'])
    ob=evidence_requesttbl.objects.filter(COURT__LOGIN=request.session["lid"])

    print(ob,"============",request.session["lid"])

    return render(request, 'court/verify evidence request.html',{'data':ob})


@login_required(login_url='/')
def acceptevidence(request,id):
    ob=evidence_requesttbl.objects.get(id=id)
    ob.status='accepted'
    ob.save()
    return HttpResponse('''<script>alert('accept');window.location='/verify_evidence_request'</script>''')



@login_required(login_url='/')
def rejectevidence(request,id):
    ob=evidence_requesttbl.objects.get(id=id)
    ob.status='rejected'
    return HttpResponse('''<script>alert('rejected');window.location='/verify_evidence_request'</script>''')



@login_required(login_url='/')
def court_verify_policestation(request):
    ob=police_stationtbl.objects.filter(district=request.session["c_dist"])
    return render(request, 'court/verify policestation.html',{'data':ob})


@login_required(login_url='/')
def acceptpolicestation(request,id):
    ob=logintbl.objects.get(id=id)
    ob.type='police'
    ob.save()
    return HttpResponse('''<script>alert('accept');window.location='/court_verify_policestation'</script>''')


@login_required(login_url='/')
def rejectpolicestation(request,id):
    ob=logintbl.objects.get(id=id)
    ob.delete()
    return HttpResponse('''<script>alert('rejected');window.location='/court_verify_policestation'</script>''')




@login_required(login_url='/')
def policestation(request):
    # return render(request,'policestation/policestation.html')
    return render(request,'policestation/index.html')

@login_required(login_url='/')
def policestation_addnewevidence(request):
    p=casetbl.objects.filter(POLICE__LOGIN=request.session["lid"])
    ob=evidencetbl.objects.all()
    return render(request,'policestation/addnewevidence.html',{'data':p})














@login_required(login_url='/')
def policestation_addnewevidencepost(request):
    case=request.POST["sel"]
    evidencename=request.POST["textfield2"]
    image=request.FILES["file"]
    description=request.POST["textfield3"]
    date=datetime.date.today()
    fs=FileSystemStorage()
    fp=fs.save(image.name,image)
    ob=evidencetbl()
    ob.CASEID_id=case
    ob.POLICE=police_stationtbl.objects.get(LOGIN_id=request.session["lid"])
    ob.photo=fp
    ob.evidencename=evidencename
    ob.descripition=description
    ob.date=date
    ob.save()
    kk=request.session['lid']
    type="e"
    res = uploadfileblockchain(ob.CASEID.id,ob.id,kk,ob.CASEID.case,evidencename,fp,description,type)
    return HttpResponse('''<script>alert('Added');window.location='/policestation_addnewevidence'</script>''')



@login_required(login_url='/')
def editpolicestation(request,id):
    request.session["id"]=id
    case=casetbl.objects.all()
    ob=evidencetbl.objects.get(id=id)
    return render(request,'policestation/editpolicestation.html',{'data':case,'evidence':ob})

@login_required(login_url='/')
def editpolicestationpost(request):
    evidencename = request.POST["textfield2"]
    descripition=request.POST["textfield3"]
    date=request.POST["textfield"]
    ob = evidencetbl.objects.get(id= request.session["id"])

    if 'file' in request.FILES:
        photo = request.FILES["file"]
        fs=FileSystemStorage()
        fp=fs.save(photo.name,photo)
        ob.photo = fp
        ob.save()
    ob.evidencename=evidencename
    ob.descripition = descripition
    ob.date = date
    ob.save()
    return HttpResponse('''<script>alert('edited');window.location='/policestation_manageevidence'</script>''')


@login_required(login_url='/')
def delete_manageevidence(request, id):
    ob = evidencetbl.objects.get(id=id)
    ob.delete()
    return HttpResponse('''<script>alert('deleted');window.location='/policestation_manageevidence'</script>''')



@login_required(login_url='/')
# def policestation_case_reg(request):
#     station = police_stationtbl.objects.get(LOGIN=request.session['lid'])
#     # district = station.district
#     # cases = casetbl.objects.filter(incident_district=district)
#
#
#     lat1 = float(station.latitude)
#
#     lon1 = float(station.longitude)
#     from math import sin, cos, sqrt, atan2, radians
#     # ob = location_table.objects.filter(LOGIN__type="rescue")
#     ob = casetbl.objects.all()
#     r = []
#     for i in ob:
#         lat2 = float(i.latitude)
#         lon2 = float(i.longitude)
#
#         print("lat=", lat2, "lon", lon1)
#         # Approximate radius of earth in km
#         R = 6373.0
#
#         # lat1 = radians(lat1)
#         # lon1 = radians(lon1)
#         # lat2 = radians(lat2)
#         # lon2 = radians(lon2)
#
#         dlon = lon2 - lon1
#         dlat = lat2 - lat1
#
#         a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
#         c = 2 * atan2(sqrt(a), sqrt(1 - a))
#
#         distance = R * c
#         if distance < 1000:
#             data = {'USER': i.USER, 'POLICE': i.POLICE, 'case': i.case, 'details': i.details,
#                     'date': i.date, 'status': i.status, 'incident_place': i.incident_place, 'incident_pin': i.incident_pin,'incident_post': i.incident_post,'incident_district': i.incident_district,'latitude': i.latitude,'longitude': i.longitude,
#                     'id': i.id}
#             r.append(data)
#
#     return render(request,'policestation/case reg.html',{'data':r})
def policestation_case_reg(request):
    station = police_stationtbl.objects.get(LOGIN=request.session['lid'])

    lat1 = float(station.latitude)  # Ensure it's a float
    lon1 = float(station.longitude)  # Ensure it's a float



    print(lat1,"============",lon1)

    from math import sin, cos, sqrt, atan2, radians

    ob = casetbl.objects.filter(USER__LOGIN__type="user",status="pending").exclude(type='amonymous')
    r = []
    R = 6373.0  # Approximate radius of Earth in km

    for i in ob:
        try:
            lat2 = float(i.latitude)  # Convert to float
            lon2 = float(i.longitude)  # Convert to float
        except ValueError:
            print(f"Skipping invalid coordinates: {i.latitude}, {i.longitude}")
            continue  # Skip this case if there's an invalid value

        # lat2 = float(i.lat)
        # lon2 = float(i.lon)

        print("lat=", lat2, "lon", lon2)
        # Approximate radius of earth in km
        R = 6373.0

        # lat1 = radians(lat1)
        # lon1 = radians(lon1)
        # lat2 = radians(lat2)
        # lon2 = radians(lon2)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c

        print(distance, "----------------------")

        # Only include cases within 1000 km
        if distance < 400:
            data = {
                'USER': i.USER,
                'POLICE': i.POLICE,
                'case': i.case,
                'details': i.details,
                'date': i.date,
                'status': i.status,
                'incident_place': i.incident_place,
                'incident_pin': i.incident_pin,
                'incident_post': i.incident_post,
                'incident_district': i.incident_district,
                'latitude': lat2,  # Now it's a float
                'longitude': lon2,  # Now it's a float
                'id': i.id
            }
            r.append(data)

    return render(request, 'policestation/case reg.html', {'data': r})



@login_required(login_url='/')
def acceptcasereg(request,id):
    request.session['cid']=id
    ob=casetbl.objects.get(id=id)
    ob.status='accept'
    ob.POLICE=police_stationtbl.objects.get(LOGIN=request.session['lid'])
    ob.save()

    return HttpResponse('''<script>alert('accept');window.location='/policestation_case_reg'</script>''')



@login_required(login_url='/')
def rejectcasereg(request,id):
    ob=casetbl.objects.get(id=id)

    ob.delete()
    return HttpResponse('''<script>alert('rejected');window.location='/policestation_case_reg'</script>''')



@login_required(login_url='/')
def policestation_evidence_requ_forwa_to_court(request):
    print(request.session["lid"])
    ob = evidence_requesttbl.objects.filter(CASEID__POLICE__LOGIN=request.session["lid"])

    # ob = evidence_requesttbl.objects.filter(status="accept",CASEID__POLICE__LOGIN=request.session["lid"])
    return render(request,'policestation/evidence requ forwa to court.html',{'data':ob})


@login_required(login_url='/')
def acceptrequestcase(request,id):
    ob=evidence_requesttbl.objects.get(id=id)
    ob.status = 'accepted'
    ob.save()
    return HttpResponse('''<script>alert('accept');window.location='/policestation_evidence_requ_forwa_to_court'</script>''')


@login_required(login_url='/')
def rejectreuestevidence(request,id):
    ob=evidence_requesttbl.objects.get(id=id)
    ob.delete()
    return HttpResponse('''<script>alert('rejected');window.location='/policestation_evidence_requ_forwa_to_court'</script>''')


@login_required(login_url='/')
def forwardcourt(request):
    court=request.POST["court"]

    ob=evidence_requesttbl.objects.get(id=request.session["e_reqid"])
    ob.COURT_id=court
    ob.status='forward'
    ob.save()
    return HttpResponse('''<script>alert('forward');window.location='/policestation_evidence_requ_forwa_to_court'</script>''')

@login_required(login_url='/')
def forwardcourtpost(request,id):

    request.session["e_reqid"]=id

    obx=police_stationtbl.objects.get(LOGIN=request.session["lid"])


    obxx=courttbl.objects.filter(district=obx.district)


    return render(request, 'policestation/forwardcase.html', {"court":obxx})


@login_required(login_url='/')
def policestation_manageevidence(request):
    ob=evidencetbl.objects.filter(POLICE__LOGIN_id=request.session['lid'])

    # ob1=forensic_evidence.objects.filter(POLICE__LOGIN_id=request.session['lid'])
    ids = []
    obc = casetbl.objects.filter(POLICE__LOGIN__id=request.session['lid'])
    for i in obc:
        ids.append(i.id)
    ob1 = forensic_evidence.objects.filter(ALLOCID__CASEID__id__in=ids)
    return render(request,'policestation/manageevidence.html',{'data':ob,"data1":ob1})

    return render(request, 'admin/view_evidance.html',{'data':ob,"data1":ob1})



@login_required(login_url='/')
def viewverifiedcase(request):
    cases = casetbl.objects.filter(POLICE__LOGIN=request.session["lid"])  # Fetch all case records
    return render(request, 'policestation/view verified case.html', {'cases': cases})

def fir(request):

    return render(request, 'policestation/fir.html')




def firrequest(request):
    file=request.FILES['firFile']
    fs=FileSystemStorage()
    fp=fs.save(file.name,file)

    ob=firtbl()
    ob.fir = fp
    ob.CASEID=casetbl.objects.get(id=request.session['ccid'])
    ob.save()
    # return render(request, 'policestation/fir.html')
    return HttpResponse('''<script>alert('upload');window.location='/viewverifiedcase'</script>''')

def firview(request,id):
    request.session['ccid'] = id
    ob = firtbl.objects.filter(CASEID=request.session['ccid'])
    return render(request, 'policestation/firview.html',{'data':ob})


# @login_required(login_url='/')
# def policestation_view_anonymous_report(request):
#     lid=request.session['lid']
#
#     res=police_stationtbl.objects.filter(LOGIN=lid)
#     lat1=res[0].latitude
#     lon1=res[0].longitude
#
#     print("lllat",lat1)
#     print("longg",lon1)
#     # Convert the user's latitude and longitude from degrees to radians
#     lat1 = float(radians(lat1))
#     lon1 = float(radians(lon1))
#
#     # Initialize a list to store the nearby police stations
#     r = []
#
#     # Assuming police_stationtbl is the table where the police stations are stored
#     ob = casetbl.objects.all()
#
#     # Approximate radius of the Earth in kilometers (mean radius)
#     R = 6373.0
#
#     # Loop through each police station
#     for i in ob:
#         # Get the police station's latitude and longitude
#         lat2 = float(i.latitude)
#         lon2 = float(i.longitude)
#
#         # Convert police station's latitude and longitude from degrees to radians
#         lat2 = radians(lat2)
#         lon2 = radians(lon2)
#
#         # Calculate the differences between latitudes and longitudes
#         dlat = lat2 - lat1
#         dlon = lon2 - lon1
#
#         # Apply the Haversine formula to calculate the distance
#         a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
#         c = 2 * atan2(sqrt(a), sqrt(1 - a))
#
#         # Distance in kilometers
#         distance = R * c
#
#         # Convert the distance from kilometers to meters (since we're interested in 1000 meters)
#         distance_in_meters = distance * 1000
#
#         # Check if the police station is within 1000 meters
#         if distance_in_meters < 1000:
#             # Append the police station data to the result list
#             data = {
#                 'case': i.case,
#                 'details': i.details,
#                 'incident_place': i.incident_place,
#                 'incident_pin': i.incident_pin,
#                 'incident_post': i.incident_post,
#                 'incident_district': i.incident_district,
#             #     'email': i.email,
#             #     'landmark': i.landmark,
#                 'id': i.LOGIN.id,
#             #     'distance': distance_in_meters  # Include the distance for reference
#              }
#             r.append(data)
#     print(r, "rrrrrrrrrrr")
#     return render(request,'policestation/view anonymous report.html',{"data":r})



from math import sin, cos, sqrt, atan2, radians
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from math import sin, cos, sqrt, atan2, radians
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='/')
def policestation_view_anonymous_report(request):
    lid = request.session['lid']

    res = police_stationtbl.objects.filter(LOGIN=lid)
    lat1 = res[0].latitude
    lon1 = res[0].longitude

    print("lat", lat1)
    print("lon", lon1)

    # Ensure lat1 and lon1 are float values, handle potential empty values
    try:
        lat1 = float(lat1)
        lon1 = float(lon1)
    except ValueError:
        # Handle the case when latitude or longitude is invalid (empty string, etc.)
        return render(request, 'policestation/view_anonymous_report.html', {"error": "Invalid user location data."})

    # Convert the user's latitude and longitude from degrees to radians
    lat1 = radians(lat1)
    lon1 = radians(lon1)

    # Initialize a list to store the nearby police stations
    r = []

    # Assuming casetbl contains the case data (police stations)
    ob = casetbl.objects.filter(type = "amonymous",status='pending')

    # Approximate radius of the Earth in kilometers (mean radius)
    R = 6373.0

    # Loop through each police station
    for i in ob:
        # Get the police station's latitude and longitude
        lat2 = i.latitude
        lon2 = i.longitude

        # Check if latitude or longitude are valid numbers
        try:
            lat2 = float(lat2)
            lon2 = float(lon2)
        except ValueError:
            # Skip this police station if latitude or longitude is invalid
            continue

        # Convert police station's latitude and longitude from degrees to radians
        lat2 = radians(lat2)
        lon2 = radians(lon2)

        # Calculate the differences between latitudes and longitudes
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        # Apply the Haversine formula to calculate the distance
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        # Distance in kilometers
        distance = R * c

        # Convert the distance from kilometers to meters (since we're interested in 1000 meters)
        distance_in_meters = distance * 1000
        print(distance_in_meters,"============++++++++++++")
        # Check if the police station is within 1000 meters
        if distance_in_meters < 2000:
            # Append the police station data to the result list
            data = {
                'case': i.case,
                'details': i.details,
                'incident_place': i.incident_place,
                'incident_pin': i.incident_pin,
                'incident_post': i.incident_post,
                'incident_district': i.incident_district,
                'latitude': i.latitude,
                'longitude': i.longitude,
                'date': i.date,
                'id': i.id,
                'status': i.status,
                # 'id': i.LOGIN.id,
            }
            r.append(data)

    print(r, "rrrrrrrrrrr")
    return render(request, 'policestation/view anonymous report.html', {"data": r})



def approve_case(request,id):
    ob=casetbl.objects.get(id = id)
    ob.status = "accept"
    ob.POLICE = police_stationtbl.objects.get(LOGIN__id= request.session['lid'])
    ob.save()

    return HttpResponse('''<script>alert('approved');window.location='/policestation_view_anonymous_report'</script>''')



def reject_case(request,id):
    casetbl.objects.filter(id = id).update(status = "rejected")
    return HttpResponse('''<script>alert('rejected');window.location='/policestation_view_anonymous_report'</script>''')
























def registration(request):
    return render(request,'policeindex.html')


def registrationpost(request):
    stationname = request.POST["textfield"]
    place = request.POST["textfield2"]
    pin = request.POST["textfield3"]
    post = request.POST["textfield4"]
    district = request.POST["textfield5"]
    email = request.POST["textfield6"]
    phone = request.POST["textfield7"]
    landmark=request.POST['textfield8']
    username=request.POST["textfield9"]
    password=request.POST["textfield10"]
    lat="0"#request.POST["lat"]
    lon="0"#request.POST["lon"]
    p=logintbl()
    p.username=username
    p.password=password
    p.type='pending'
    p.save()
    ob = police_stationtbl()
    ob.LOGIN=p
    ob.stationname = stationname
    ob.place = place
    ob.pin = pin
    ob.post = post
    ob.district = district
    ob.email = email
    ob.phone = phone
    ob.landmark=landmark
    ob.latitude=lat
    ob.longitude=lon

    ob.save()
    request.session['pid']=ob.id
    return render(request,"map_start.html")
def policeloc(request):
    lat = request.POST["lat"]
    lon = request.POST["lon"]
    ob=police_stationtbl.objects.get(id=request.session['pid'])
    ob.latitude = lat
    ob.longitude = lon

    ob.save()
    return HttpResponse('''<script>alert('register');window.location='/'</script>''')




@login_required(login_url='/')
def forensichome(request):
    return render(request, 'forensicstaff/index.html')



def forensicstaff_forensicreg(request):
    ob=forensicstafftbl.objects.all()
    return render(request, 'forensicstaff/regindex.html', {'data': ob})


def forensicregpost(request):
    name = request.POST["textfield"]
    email = request.POST["textfield2"]
    photo = request.FILES["file"]
    regno = request.POST["textfield6"]
    forensicplace = request.POST["textfield3"]
    forensicpin = request.POST["textfield4"]
    forensicpost = request.POST["textfield5"]
    district=request.POST["district"]
    username = request.POST["textfield7"]
    password = request.POST["textfield8"]
    p=logintbl()
    p.username = username
    p.password = password
    p.type = 'pending'
    p.save()
    ob = forensicstafftbl()
    fs=FileSystemStorage()
    fp=fs.save(photo.name,photo)
    ob.LOGIN = p
    ob.name = name
    ob.email = email
    ob.photo = fp
    ob.regno = regno
    ob.forensicplace = forensicplace
    ob.forensicpin = forensicpin
    ob.forensicpost = forensicpost
    ob.district=district
    ob.save()
    return HttpResponse('''<script>alert('register');window.location='/'</script>''')


@login_required(login_url='/')
def forensicstaff_uploadevidence(request,id):
    request.session["cid"]=id
    ob=forensic_evidence.objects.filter(ALLOCID__CASEID_id=id)
    return render(request, 'forensicstaff/upload evidence.html',{'data':ob})


@login_required(login_url='/')
def forensicstaff_view_uploadevidence_police(request,id):

    ob=evidencetbl.objects.filter(CASEID__id=id)
    return render(request, 'forensicstaff/view_evidance.html',{'data':ob})












@login_required(login_url='/')
def forensic_addevidence(request):
    return render(request, 'forensicstaff/addevidence3.html', )


@login_required(login_url='/')
def forensic_addnewevidencepost(request):
    evidencename=request.POST["textfield"]
    file=request.FILES["file"]
    descripition=request.POST["textfield3"]
    date=datetime.date.today()
    fs=FileSystemStorage()
    fp=fs.save(file.name,file)
    ob=forensic_evidence()
    ob.ALLOCID=case_alloctbl.objects.filter(CASEID_id=request.session["cid"])[0]
    ob.file=fp
    ob.evidencename=evidencename
    ob.descripition=descripition
    ob.date=date
    ob.save()
    pp=case_alloctbl.objects.filter(CASEID_id=request.session["cid"])[0]
    kk=request.session['lid']
    type="f"
    res = uploadfileblockchain(pp.CASEID.id,ob.id,kk,pp.CASEID.case,evidencename,fp,descripition,type)

    return HttpResponse('''<script>alert('Added');window.location='/forensic_addevidence'</script>''')











def uploadfileblockchain(cid,eid,sid,case,evd,fn,details,type):
    print(cid,eid,sid,case,evd,fn,details,type,"kkkkkkkkkkkkkkkkkkkkkkkkkkk")
    try:

        with open(compiled_contract_path) as file:
            contract_json = json.load(file)  # load contract info as JSON
            contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
        contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)

        blocknumber = web3.eth.get_block_number()
        message2 = contract.functions.addreq(blocknumber + 1, str(cid), str(eid)+type, str(sid), str(case),  str(evd),  str(fn), str(details),

                                             str(datetime.datetime.today().date().strftime("%Y-%m-%d"))
                                             ).transact({'from': web3.eth.accounts[0]})

        print(message2)

        return "ok"
    except Exception as e:
        print(e,"kkkkkkkkkkkkkkkkkkkkkk")
        print("==================")
        print("==================")
        print("==================")
        return str(e)


@login_required(login_url='/')
def forensicstaff_view_alloc_case(request):
    print(request.session['lid'])
    ob=case_alloctbl.objects.filter(STAFFID_id=forensicstafftbl.objects.get(LOGIN_id=request.session["lid"]))
    return render(request, 'forensicstaff/view alloc case.html',{'data':ob})

@login_required(login_url='/')
def profilestaff(request):
    ob = forensicstafftbl.objects.get(LOGIN_id=request.session['lid'])
    return render(request,"forensicstaff/profile.html",{'staff':ob})



@login_required(login_url='/')
def chatwithuser(request):
    ob=forensicstafftbl.objects.get(LOGIN__id=request.session['lid'])
    ob = police_stationtbl.objects.filter(district=ob.district)
    return render(request,"forensicstaff/fur_chat.html",{'val':ob})


@login_required(login_url='/')
def chatview(request):
    ob = forensicstafftbl.objects.get(LOGIN__id=request.session['lid'])
    ob = police_stationtbl.objects.filter(district=ob.district)
    # ob = police_stationtbl.objects.all()
    d=[]
    for i in ob:
        r={"name":i.stationname,'photo':i.stationname,'email':i.email,'loginid':i.LOGIN.id}
        d.append(r)
    return JsonResponse(d, safe=False)



@login_required(login_url='/')
def coun_insert_chat(request,msg,id):
    from datetime import datetime
    print("===",msg,id)
    ob=chattbl()
    ob.FROM_ID=logintbl.objects.get(id=request.session['lid'])
    ob.TO_ID=logintbl.objects.get(id=id)
    ob.message=msg
    ob.date=datetime.now().strftime("%Y-%m-%d")
    ob.status="pending"
    ob.save()

    return JsonResponse({"task":"ok"})
    # refresh messages chatlist


@login_required(login_url='/')
def coun_msg(request,id):

    ob1=chattbl.objects.filter(FROM_ID__id=id,TO_ID_id=request.session['lid'])
    ob2=chattbl.objects.filter(FROM_ID__id=request.session['lid'],TO_ID__id=id)
    combined_chat = ob1.union(ob2)
    combined_chat=combined_chat.order_by('id')
    res=[]
    for i in combined_chat:
        res.append({"from_id":i.FROM_ID.id,"msg":i.message,"date":i.date,"chat_id":i.id})

    obu=police_stationtbl.objects.get(LOGIN__id=id)


    return JsonResponse({"data":res,"name":obu.stationname,"photo":obu.stationname,"user_lid":obu.LOGIN.id})

@login_required(login_url='/')
def chatwithfstaff(request):
    ob = forensicstafftbl.objects.all()
    return render(request,"policestation/policechat.html",{'val':ob})


@login_required(login_url='/')
def chatfstaffview(request):

    ob=police_stationtbl.objects.get(LOGIN__id=request.session['lid'])
    ob = forensicstafftbl.objects.filter(district=ob.district)
    d=[]
    for i in ob:
        r={"name":i.name,'photo':i.photo.url,'email':i.email,'loginid':i.LOGIN.id}
        d.append(r)
    return JsonResponse(d, safe=False)


    
@login_required(login_url='/')
def chatfuserview_load(request):
    return render(request,'policestation/chatwith_user.html')
@login_required(login_url='/')
def chatfuserview(request):
    ob = police_stationtbl.objects.get(LOGIN__id=request.session['lid'])
    ob = usertbl.objects.filter(district=ob.district)
    d=[]
    for i in ob:
        r={"name":i.name,'photo':i.photo.url,'email':i.email,'loginid':i.LOGIN.id}
        d.append(r)
    return JsonResponse(d, safe=False)





@login_required(login_url='/')
def coun_insert_fstaff(request,msg,id):
    from datetime import datetime
    print("===",msg,id)
    ob=chattbl()
    ob.FROM_ID=logintbl.objects.get(id=request.session['lid'])
    ob.TO_ID=logintbl.objects.get(id=id)
    ob.message=msg
    ob.date=datetime.now().strftime("%Y-%m-%d")
    ob.status="pending"
    ob.save()

    return JsonResponse({"task":"ok"})
    # refresh messages chatlist


@login_required(login_url='/')
def coun_fmsg(request,id):

    ob1=chattbl.objects.filter(FROM_ID__id=id,TO_ID_id=request.session['lid'])
    ob2=chattbl.objects.filter(FROM_ID__id=request.session['lid'],TO_ID__id=id)
    combined_chat = ob1.union(ob2)
    combined_chat=combined_chat.order_by('id')
    res=[]
    for i in combined_chat:
        res.append({"from_id":i.FROM_ID.id,"msg":i.message,"date":i.date,"chat_id":i.id})

    obu=forensicstafftbl.objects.get(LOGIN__id=id)


    return JsonResponse({"data":res,"name":obu.name,"photo":obu.photo.url,"user_lid":obu.LOGIN.id})

@login_required(login_url='/')
def coun_fmsg2(request,id):

    ob1=chattbl.objects.filter(FROM_ID__id=id,TO_ID_id=request.session['lid'])
    ob2=chattbl.objects.filter(FROM_ID__id=request.session['lid'],TO_ID__id=id)
    combined_chat = ob1.union(ob2)
    combined_chat=combined_chat.order_by('id')
    res=[]
    for i in combined_chat:
        res.append({"from_id":i.FROM_ID.id,"msg":i.message,"date":i.date,"chat_id":i.id})

    obu=usertbl.objects.get(LOGIN__id=id)


    return JsonResponse({"data":res,"name":obu.name,"photo":obu.photo.url,"user_lid":obu.LOGIN.id})



def forgotpassword(request):
     return render(request, 'forgot password.html', )


from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from django.conf import settings  # For email configuration


# def forgotpasswordpost(request):
#     if request.method == "POST":
#         email = request.POST.get("email")  # Use `get` to avoid KeyError
#         try:
#             # Attempt to fetch the user
#             s = logintbl.objects.get(username=email)
#
#             # Generate a password reset message (plain-text passwords should not be sent!)
#             subject = "Password Recovery"
#             message = f"Hello, here is your password: {s.password}"  # Replace with a reset link in production
#             from_email = 'jaseeljazck6@gmail.com'  # Set in settings.py
#
#             send_mail(subject, message, from_email, [email])
#             return JsonResponse({"status": "success", "message": "Password sent to your email."})
#         except ObjectDoesNotExist:
#             return JsonResponse({"status": "error", "message": "Invalid username"})
#         except Exception as e:
#             return JsonResponse({"status": "error", "message": f"An error occurred: {str(e)}"})
#     return JsonResponse({"status": "error", "message": "Invalid request method"})
#
#




def forgotpasswordpost(request):
    print(request.POST)
    try:
        print("1")
        print(request.POST)
        email = request.POST['email']
        print(email)
        s = logintbl.objects.get(username=email)
        # qry = "SELECT login.password FROM student  JOIN login ON login.L_id = student.L_id WHERE email=%s"
        # s = selectone(qry, email)
        print(s, "=============")
        if s is None:
            data = {"status": "not"}
            r = json.dumps(data)

            print(r)
            # return HttpResponse
            return HttpResponse('''<script>alert(' Invalid');window.location='/'</script>''')

            # return jsonify({'task': 'invalid email'})
        else:
            try:
                gmail = smtplib.SMTP('smtp.gmail.com', 587)
                gmail.ehlo()
                gmail.starttls()
                gmail.login('hasnareena90@gmail.com', 'vtiq xdzy froo dqsy')
                print("login=======")
            except Exception as e:
                print("Couldn't setup email!!" + str(e))
            msg = MIMEText("Your new password id : " + str(s.password))
            print(msg)
            msg['Subject'] = 'Password'
            msg['To'] = email
            msg['From'] = 'hasnareena90@gmail.com'

            print("ok====")

            try:
                gmail.send_message(msg)
            except Exception as e:
                data = {"status": "not"}
                r = json.dumps(data)
                print(r)
                return HttpResponse('''<script>alert(' Invalid');window.location='/'</script>''')
            data = {"status": "vaild"}
            r = json.dumps(data)

            print(r)
            return HttpResponse('''<script>alert('success');window.location='/'</script>''')
    except Exception as e:
        print(e)
        data = {"status": "not"}
        r = json.dumps(data)

        print(r)
        return HttpResponse('''<script>alert(' Invalid');window.location='/'</script>''')


def forgotpassword_flutter(request):
    print(request.POST)
    try:
        print("1")
        print(request.POST)
        email = request.POST['email']
        print(email)
        s = logintbl.objects.get(username=email)
        # qry = "SELECT login.password FROM student  JOIN login ON login.L_id = student.L_id WHERE email=%s"
        # s = selectone(qry, email)
        print(s, "=============")
        if s is None:
            data = {"status": "not"}
            r = json.dumps(data)

            print(r)
            return HttpResponse(r)

            # return jsonify({'task': 'invalid email'})
        else:
            try:
                gmail = smtplib.SMTP('smtp.gmail.com', 587)
                gmail.ehlo()
                gmail.starttls()
                gmail.login('hasnareena90@gmail.com', 'vtiq xdzy froo dqsy')
                print("login=======")
            except Exception as e:
                print("Couldn't setup email!!" + str(e))
            msg = MIMEText("Your new password id : " + str(s.password))
            print(msg)
            msg['Subject'] = 'Password'
            msg['To'] = email
            msg['From'] = 'hasnareena90@gmail.com'

            print("ok====")

            try:
                gmail.send_message(msg)
            except Exception as e:
                data = {"status": "not"}
                r = json.dumps(data)
                print(r)
                return HttpResponse(r)
            data = {"status": "valid"}
            r = json.dumps(data)

            print(r)
            return HttpResponse(r)
    except Exception as e:
        print(e)
        data = {"status": "not"}
        r = json.dumps(data)

        print(r)
        return HttpResponse(r)


# def forgotpasswordpost(request):
#      email = request.POST["email"]
#      s = logintbl.objects.get(username=email)
#      if s is None:
#          return JsonResponse({"status": "Invalid username"})
#      else:
#
#                  subject = 'your mailid '
#                  message = f"Your password: {s.password}"
#                  from_email = 'jaseeljazck6@gmail.com'
#
#
#
#                 send_mail(subject, message, from_email, [email])
#                 return HttpResponse('''<script>alert('Send ');window.location='/'</script>''')


# ===================================================android===========================================


def logincode(request):
    print(request.POST)
    un = request.POST['username']
    pwd = request.POST['password']
    print(un, pwd)

    try:

        ob = logintbl.objects.get(username=un, password=pwd)

        if ob is None:
            data = {"task": "invalid"}
            return JsonResponse({"task": "invalid"})
        else:
            print("in user function")

            return JsonResponse({"task": "valid", "lid": ob.id,"type":ob.type})
    except Exception as e:
        print(e,"--------------")
        return JsonResponse({"task": "no"})

def registrationcode(request):
    try:
        print(request.POST,"uuuki")
        name=request.POST['name']
        email=request.POST['email']
        place = request.POST['place']
        pin = request.POST['pin']
        post = request.POST['post']
        district = request.POST['district']
        phone = request.POST['phone']
        photo=request.FILES['image']
        fs=FileSystemStorage()
        fp=fs.save(photo.name,photo)
        uname=request.POST['username']
        password=request.POST['password']

        lob1=logintbl()
        lob1.username = uname
        lob1.password = password
        lob1.type = 'user'
        lob1.save()

        lob=usertbl()
        lob.name = name
        lob.place = place
        lob.pin = pin
        lob.post = post
        lob.district = district
        lob.email = email
        lob.phone = phone
        lob.LOGIN =lob1
        lob.photo=fp
        lob.save()
        print("uuuuuuuuu",lob)
        return JsonResponse({'task':'valid'})
    except:
        return JsonResponse({"task": "invalid"})

def sendfeedback(request):
        comp = request.POST['review']
        lid = request.POST['lid']
        rating=request.POST['rating']
        lob = feedbacktbl()
        lob.USER = usertbl.objects.get(LOGIN__id=lid)
        lob.feedback = comp
        lob.rating=rating
        lob.date = datetime.datetime.today()
        lob.save()
        return JsonResponse({'task': 'ok'})


def casregistration(request):
    print(request.POST,"lllllllllllll")
    case = request.POST['case']
    lat1=request.POST['lat']
    lon1=request.POST['lon']
    details = request.POST['details']
    incident_place = request.POST['incident_place']
    incident_pin = request.POST['incident_pin']
    incident_post = request.POST['incident_post']
    incident_district = request.POST['incident_district']
    lat, lon = get_lat_lon_opencage(incident_place + ", " + incident_district)
    print(lat, lon, "lllllllll")
    print(lat1, lon1, "<<<<<<<<<<<<<<<<<<<<<<<")
    if lat != None:
        lat1 = lat
        lon1 = lon
    print("==========================")
    print(lat1, lon1, "<<<<<<<<<<<<<<<<<<<<<<<22")
    lid = request.POST['lid']
    lob = casetbl()
    lob.USER = usertbl.objects.get(LOGIN__id=lid)
    lob.case = case
    lob.details = details
    lob.status = "pending"
    lob.incident_place = incident_place
    lob.incident_pin = incident_pin
    lob.incident_post = incident_post
    lob.incident_district = incident_district
    lob.date = datetime.datetime.today()
    lob.latitude=lat1
    lob.longitude=lon1
    lob.save()
    return JsonResponse({'task': 'ok'})

def sendevidencerequest(request):
    lid = request.POST['lid']
    cid = request.POST['cid']
    k=evidence_requesttbl.objects.filter(LOGIN__id=lid,CASEID__id=cid)
    if len(k) == 0:
        lob = evidence_requesttbl()
        lob.LOGIN = logintbl.objects.get(id=lid)
        lob.CASEID = casetbl.objects.get(id=cid)
        lob.status = "pending"
        lob.date = datetime.datetime.today()
        lob.save()
        return JsonResponse({'task': 'ok'})
    else:
        return JsonResponse({'task': 'not'})


def viewpoliceevidence(request):
    ob=evidencetbl.objects.filter(USER=usertbl.objects.get(LOGIN_id=request.POST["lid"]))
    print(ob,"HHHHHHHHHHHHHHH")
    mdata=[]
    for i in ob:
        data={'POLICE':i.stationname,'CASEID':i.case,'evidencename':i.evidencename,'photo':i.photo,'descripition':i.descripition,'date':i.date,'id':i.id}
        mdata.append(data)
        print(mdata)
    return JsonResponse({"status":"ok","data":mdata})


# def viewforensicevidence(request):
#     ob=forensic_evidence.objects.filter(ALLOCID__CASEID_id=id)
#     print(ob,"HHHHHHHHHHHHHHH")
#     mdata=[]
#     for i in ob:
#         data={'evidencename':i.evidencename,'file':i.file,'descripition':i.descripition,'date':i.date,'id':i.id}
#         mdata.append(data)
#         print(mdata)
#     return JsonResponse({"status":"ok","data":mdata})






# def viewforensicevidence(request):
#     print(request.POST, "kkkkkkkkkkkkkkk")
#
#     case_id = request.POST.get("case_id")
#
#     # Fetch data from both    {
#                     "evidencename": i.evidencename,
#               tables
#     forensic_data = forensic_evidence.objects.filter(ALLOCID__CASEID_id=case_id)
#     evidence_data = evidencetbl.objects.filter(CASEID_id=case_id)
#
#     # Combine the data into a single response
#     mdata = [
#                 {
#                     "evidencename": i.evidencename,
#                     "file": str(i.file.url),
#                     "description": i.descripition,
#                     "date": str(i.date),
#                     "id": str(i.id),
#                     "type": "forensic_evidence"
#                 }
#                 for i in forensic_data
#             ] + [
#                    "file": str(i.photo.url),  # Assuming photo field in evidencetbl
#                     "description": i.descripition,
#                     "date": str(i.date),
#                     "id": str(i.id),
#                     "type": "evidencetbl"
#                 }
#                 for i in evidence_data
#             ]
#
#     print(mdata)
#
#     return JsonResponse({"status": "ok", "data": mdata})
#


def viewdonation(request):
    case_id = request.POST.get("case_id")
    data = []
    with open(r'F:\transparent charity (2)\transparent charity\src\node_modules\.bin\build\contracts\Structfund.json') as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    contract = web3.eth.contract(address='0xFF37995F4219d4dd57dd6F1D3602A48460432D11', abi=contract_abi)
    blocknumber = web3.eth.get_block_number()
    for i in range(blocknumber, 2, -1):
        try:
            a = web3.eth.get_transaction_by_block(i, 0)
            decoded_input = contract.decode_function_input(a['input'])
            if decoded_input[1]['eid'] in case_id:
                data.append(decoded_input[1])
        except Exception as e:
            print(e)
            pass
    print(data,"==============================")
    return JsonResponse({"status": "ok", "data": data})















def viewforensicevidence(request):
    case_id = request.POST.get("case_id")
    print(case_id,"jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj")
    res = forensic_evidence.objects.filter(ALLOCID__CASEID_id=case_id)

    kk = evidencetbl.objects.filter(CASEID_id=case_id)

    data = []

    resdata=[]

    if len(kk)>0:
        for p in kk:
            print(p.id)
            # print("------------12")

            with open(
                    r'C:\Users\hp\PycharmProjects\evilock\blockchain\node_modules\.bin\build\contracts\Structreq.json') as file:
                contract_json = json.load(file)  # load contract info as JSON
                contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
            contract = web3.eth.contract(address='0x9d6412E5196fB29402f7D80fd1B61FB127C34BE4', abi=contract_abi)
            blocknumber = web3.eth.get_block_number()
            for i in range(blocknumber, 2, -1):
                try:
                    # print("_-----")
                    a = web3.eth.get_transaction_by_block(i, 0)
                    decoded_input =  contract.decode_function_input(a['input'])
                    # print(decoded_input, "pppppppppppppppppppppp")
                    if str(decoded_input[1]['eid']) == str(p.id)+"e"  :
                        if decoded_input[1] not in data:

                            if decoded_input[1] in data:
                                pass
                            else:
                                data.append(decoded_input[1])
                    # print(data, "*******", decoded_input[1]['eid'])
                except Exception as e:
                    print(e, "===================0000")

            # print(data, "==============================")

    for i in data:
        # print(("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk"))
        # print(i.bidid,"jjjjjjjjjjjj")
        kk = evidencetbl.objects.get(id=i['eid'].replace("e",""))
        row = {
            "evidencename": str(kk.evidencename),
            # "evidencename": str(decoded_input[1]['evd']),
                "file": str(kk.photo.url),
                # "description": str(decoded_input[1]['details']),
                "description": str(kk.descripition),
                "date": str(kk.date),
                "id": str(kk.id),
                "type": "evidence"
       }

        resdata.append(row)


    print("started evidmnbcvkjdbsk")

    if len(res)>0:
        for p in res:
            print(p.id)
            print("------------12")

            with open(
                    r'C:\Users\hp\PycharmProjects\evilock\blockchain\node_modules\.bin\build\contracts\Structreq.json') as file:
                contract_json = json.load(file)  # load contract info as JSON
                contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
            contract = web3.eth.contract(address='0x9d6412E5196fB29402f7D80fd1B61FB127C34BE4', abi=contract_abi)
            blocknumber = web3.eth.get_block_number()
            for i in range(blocknumber, 2, -1):
                try:
                    print("_-----")
                    a = web3.eth.get_transaction_by_block(i, 0)
                    decoded_input = contract.decode_function_input(a['input'])
                    # print(decoded_input, "oooooooooooooooooooooooooooooooooooooooooooooooo")
                    if str(decoded_input[1]['eid']) == str(p.id)+"e":# and decoded_input[1]['status'] == "Winner":
                        if decoded_input[1] not in data:
                            data.append(decoded_input[1])
                        else:
                            pass
                    # print(data, "*******", decoded_input[1]['eid'])
                except Exception as e:
                    print(e, "===================0000")

        print(data, "==============================")
        print(res, "jjjjjjjjjjjjjjjjj")

        for i in data:
            # print(i.bidid,"jjjjjjjjjjjj")
            kk = forensic_evidence.objects.filter(id=i['eid'].replace("f","").replace("e",""))

            if len(kk)>0:
                row = {
                # "evidencename": str(decoded_input[1]['evd']),
                "evidencename": str(kk[0].evidencename),
                    "file": str(kk[0].file.url),
                    "description": str(kk[0].descripition),
                    # "description": str(decoded_input[1]['details']),
                    # "date": str(decoded_input[1]['date']),
                    "date": str(kk[0].date),
                    # "id": str(decoded_input[1]['eid']),
                    "id": str(kk[0].id),
                    "type": "forensic_evidence"

                   }

                resdata.append(row)
            print(res,"jjjjjjjjjjjjjjjjj")

    print("=======**************************************************************888")
    print(resdata)

    # unique_data = {}
    # for item in resdata:
    #
    #     # print(item)
    #     unique_data[item['id']] = item  # Keeps the last occurrence of the id
    #
    # # Convert back to a list
    # distinct_data = list(unique_data.values())

    return JsonResponse({"status": "ok", "data": resdata})







def viewusercasereg(request):
    # ob=casetbl.objects.filter(USER=usertbl.objects.get(LOGIN_id=request.POST["lid"]))
    ob=casetbl.objects.filter(USER__LOGIN_id=request.POST["lid"]).exclude(type='amonymous')
    print(ob,"HHHHHHHHHHHHHHH")
    mdata=[]
    for i in ob:
        data={'case':i.case,'details':i.details,'date':str(i.date),'status':i.status,'incident_place':i.incident_place,'incident_pin':str(i.incident_pin),'incident_post':i.incident_post,'incident_district':i.incident_district,'id':i.id}
        mdata.append(data)
        print(mdata)
    return JsonResponse({"status":"ok","data":mdata})


def requesttblstatus(request):
    ob=evidence_requesttbl.objects.filter(LOGIN_id=request.POST["lid"])
    print(ob, "HHHHHHHHHHHHHHH")
    mdata = []
    for i in ob:
        data = {'case': i.CASEID.case, 'details': i.CASEID.details, 'date': str(i.CASEID.date), 'status': i.CASEID.status,
                'incident_place': i.CASEID.incident_place, 'incident_pin': str(i.CASEID.incident_pin),
                'incident_post': i.CASEID.incident_post, 'incident_district': i.CASEID.incident_district, 'id': i.id,"rdate":i.date,"rstatus":i.status,
                "case_id":i.CASEID.id,"stationname":i.CASEID.POLICE.stationname,"stationplace":i.CASEID.POLICE.place,"stationdistrict":i.CASEID.POLICE.district}
        mdata.append(data)
        print(mdata)
    return JsonResponse({"status": "ok", "data": mdata})

def viewchat(request):
    print(request.POST)
    fromid = request.POST['from_id']
    toid=request.POST['to_id']
    ob1 = chattbl.objects.filter(FROM_ID__id=fromid, TO_ID__id=toid)
    ob2 = chattbl.objects.filter(FROM_ID__id=toid, TO_ID__id=fromid)
    combined_chat = ob1.union(ob2)
    combined_chat = combined_chat.order_by('id')
    res = []
    for i in combined_chat:
        res.append({'msg': i.message, 'fromid': i.FROM_ID.id, 'toid': i.TO_ID.id, 'date':i.date})
    print(res,"===============================++++++++++++++++++++++++++++++++++========================")
    return JsonResponse({"status": "ok", "data": res})


def sendchat(request):
    print(request.POST)
    msg=request.POST['message']
    fromid=request.POST['fromid']
    toid=request.POST['toid']

    ob=chattbl()
    ob.message=msg
    ob.FROM_ID=logintbl.objects.get(id=fromid)
    ob.TO_ID=logintbl.objects.get(id=toid)
    ob.date=datetime.datetime.now().date()
    ob.status="pending"
    ob.save()
    return JsonResponse({"status": "ok"})

#
# def viewchatpolicestation(request):
#     lat1 = float(request.POST['lat'])
#     lon1 = float(request.POST['lon'])
#     from math import sin, cos, sqrt, atan2, radians
#     # ob = location_table.objects.filter(LOGIN__type="rescue")
#     ob = police_stationtbl.objects.all()
#     r = []
#     for i in ob:
#         lat2 = float(i.latitude)
#         lon2 = float(i.longitude)
#
#         print("lat=", lat2, "lon", lon1)
#         # Approximate radius of earth in km
#         R = 6373.0
#
#         # lat1 = radians(lat1)
#         # lon1 = radians(lon1)
#         # lat2 = radians(lat2)
#         # lon2 = radians(lon2)
#
#         dlon = lon2 - lon1
#         dlat = lat2 - lat1
#
#         a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
#         c = 2 * atan2(sqrt(a), sqrt(1 - a))
#
#         distance = R * c
#         print(distance,"dis")
#         if distance < 1000:
#             data = {'stationname': i.stationname, 'place': i.place, 'pin': i.pin, 'post': i.post,
#                     'district': i.district, 'phone': i.phone, 'email': i.email, 'landmark': i.landmark,
#                     'id': i.LOGIN.id}
#             r.append(data)
#     print(r,"rrrrrrrrrr")
#     return JsonResponse({"status": "ok", "data": r})

    # return JsonResponse({"status":"ok","data":mdata})

from math import sin, cos, sqrt, atan2, radians
from django.http import JsonResponse


def viewchatpolicestation(request):
    # Get latitude and longitude from the request
    print(request.POST)
    lat1 = float(request.POST['lat'])
    lon1 = float(request.POST['lon'])
    print(lat1,lon1,"ffffffff")
    # Convert the user's latitude and longitude from degrees to radians
    # lat1 = radians(lat1)
    # lon1 = radians(lon1)

    # Initialize a list to store the nearby police stations
    r = []

    # Assuming police_stationtbl is the table where the police stations are stored
    ob = police_stationtbl.objects.all()

    # Approximate radius of the Earth in kilometers (mean radius)
    R = 6373.0  # Approximate radius of Earth in km

    for i in ob:
        try:
            lat2 = float(i.latitude)  # Convert to float
            lon2 = float(i.longitude)  # Convert to float
        except ValueError:
            print(f"Skipping invalid coordinates: {i.latitude}, {i.longitude}")
            continue  # Skip this case if there's an invalid value

        # lat2 = float(i.lat)
        # lon2 = float(i.lon)

        print("lat=", lat2, "lon", lon2)
        # Approximate radius of earth in km
        R = 6373.0

        # lat1 = radians(lat1)
        # lon1 = radians(lon1)
        # lat2 = radians(lat2)
        # lon2 = radians(lon2)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c

        print(distance, "----------------------")

        # Only include cases within 1000 km
        if distance < 400:
            # Append the police station data to the result list
            data = {
                'stationname': i.stationname,
                'place': i.place,
                'pin': i.pin,
                'post': i.post,
                'district': i.district,
                'phone': i.phone,
                'email': i.email,
                'landmark': i.landmark,
                'id': i.LOGIN.id,
                'distance': distance  # Include the distance for reference
            }
            r.append(data)
    print(r,"rrrrrrrrrrr")
    # Sort the result list by distance (nearest first)
    r.sort(key=lambda x: x['distance'])

    # Return the list of nearby police stations as a JSON response
    return JsonResponse({"status": "ok", "data": r})


def userviewprofile(request):
    lid=request.POST["lid"]
    i=usertbl.objects.get(LOGIN=lid)
    print(i,"HHHHHHHHHHHHHHH",i.photo)

    return JsonResponse({"status":"ok",'name':i.name,'email':i.email,'phone':i.phone,'photo':i.photo.url,'place':i.place,'pin': i.pin,'post':i.post,'district':i.district,'id':i.LOGIN.id})


#
import numpy as np
from django.db.models.functions import ExtractYear
def forecast_case(request):
    case_stats = casetbl.objects.annotate(year=ExtractYear('date')).values('year').annotate(
        total_cases=Count('id')).order_by('year')

    # Convert the query result to a list
    data = list(case_stats)
    print(data,'resuletttt')

    print("case_stats:", case_stats)  # Check if the case_stats is correctly populated
    print("Data List:", data)  # Check if data is correctly converted into a list

    # Handle case where no data is available
    if len(data) == 0:
        return HttpResponse("No data available for forecasting.")
#
    # Convert the case stats to a pandas DataFrame
    import pandas as pd
    df = pd.DataFrame(data)

    # Debugging step: check the content of DataFrame
    print("DataFrame:", df)  # Verify if the DataFrame is populated and structured correctly

    if df.empty:
        return HttpResponse("Data is not properly formatted for forecasting.")

    df.set_index('year', inplace=True)

    # Check if 'total_cases' exists and has data
    if 'total_cases' not in df or df['total_cases'].isnull().all():
        return HttpResponse("No total case data available for forecasting.")

    # Additional check for index and data range
    print("Index:", df.index)  # Check if the index is set properly
    print("Total Cases Series:", df['total_cases'])
    print(" df['total_cases']")
    print( df['total_cases'])# Check if total cases is valid

    try:
        # ARIMA Model for Forecasting with a reduced order
        from statsmodels.tsa.arima.model import ARIMA
        model = ARIMA(df['total_cases'], order=(1, 1, 0))  # Simplified ARIMA model
        model_fit = model.fit()

        # Forecast the next year
        forecast = model_fit.forecast(steps=1)
        next_year = df.index.max() + 1
        print(forecast,"forecast==================")
        forecasted_cases = int(forecast[0])

        # Debugging step: check forecast result
        print("Forecasted Cases:", forecasted_cases)

    except ValueError as e:
        return HttpResponse(f"Error in forecasting: {str(e)}")

    context = {
        'forecast_year': next_year,
        'forecasted_cases': forecasted_cases,
        'case_stats': case_stats,
    }

    return render(request, 'policestation/prediction.html', context)


import matplotlib.pyplot as plt
import io
import base64
from django.http import HttpResponse
# from prophet import Prophet  # Updated import statement
from django.shortcuts import render
from django.db.models import Count
import pandas as pd

def stationforecast_cases1(request):
    # Step 1: Fetch and prepare the data
    cases = casetbl.objects.values('date').annotate(case_count=Count('id'))
    df = pd.DataFrame(list(cases))
    df.rename(columns={'date': 'ds', 'case_count': 'y'}, inplace=True)

    # Step 2: Train the Prophet model
    model = Prophet(yearly_seasonality=True, daily_seasonality=False)
    model.fit(df)

    # Step 3: Forecast for the next year
    future = model.make_future_dataframe(periods=365)
    forecast = model.predict(future)

    # Extract the forecasted cases
    forecasted_cases = forecast[['ds', 'yhat']].tail(365)

    # Step 4: Plot the forecasted data
    plt.figure(figsize=(10, 6))
    plt.plot(forecast['ds'], forecast['yhat'], label='Predicted Cases')
    plt.xlabel('Date')
    plt.ylabel('Predicted Case Count')
    plt.title('Forecasted Cases for the Next Year')
    plt.legend()

    # Convert the plot to a PNG image and then to a base64-encoded string
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    # Encode the image to base64
    graph = base64.b64encode(image_png).decode('utf-8')

    # Step 5: Send data and the graph to the template
    context = {
        'forecasted_cases': forecasted_cases.to_dict(orient='records'),
        'graph': graph  # Pass the base64 graph to the template
    }

    return render(request, 'policestation/station prediction.html', context)
import requests
def get_lat_lon_opencage(address, api_key="ef6b72d9607e40e6a68d4a85b102fbba"):
    url = f"https://api.opencagedata.com/geocode/v1/json?q={address}&key={api_key}"
    response = requests.get(url)
    data = response.json()

    if data['results']:
        location = data['results'][0]['geometry']
        return location['lat'], location['lng']
    return None, None

def casregistrationanonymous(request):
    print(request.POST,"lllllllllllll")
    case = request.POST['case']
    details = request.POST['details']
    incident_place = request.POST['incident_place']
    incident_pin = request.POST['incident_pin']
    incident_post = request.POST['incident_post']
    incident_district = request.POST['incident_district']


    lat = request.POST['lat']
    lon = request.POST['lon']
    lat1,lon1=get_lat_lon_opencage(incident_place+", "+incident_district)
    print(lat,lon,"lllllllll")
    print(lat1,lon1,"<<<<<<<<<<<<<<<<<<<<<<<")
    if lat1!=None:
        lat=lat1
        lon=lon1
    lob = casetbl()
    lob.case = case
    lob.details = details
    lob.type = "amonymous"
    lob.USER_id = 1
    lob.status = "pending"
    lob.incident_place = incident_place
    lob.incident_pin = incident_pin
    lob.incident_post = incident_post
    lob.incident_district = incident_district
    lob.Date = datetime.datetime.today()
    lob.latitude=lat
    lob.longitude=lon
    lob.date=datetime.datetime.now().strftime("%Y-%m-%d")
    lob.save()
    return JsonResponse({'task': 'ok'})



def view_profile(request):
    if request.method == "POST":
        try:
            lid = request.POST.get('lid')
            user = usertbl.objects.get(LOGIN__id=lid)

            data = {
                'name': user.name,
                'email': user.email,
                'phone': user.phone,
                'photo': request.build_absolute_uri(user.photo.url),
                'place': user.place,
                'pin': user.pin,
                'post': user.post,
                'district': user.district,
            }
            return JsonResponse(data)

        except usertbl.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


# def update_profile(request):
#     print(request.FILES,"hhhhhhhhhhhhhh")
#     lid = request.POST['lid']
#     user = usertbl.objects.get(LOGIN__id=lid)
#     photo=request.FILES['photo']
#     fs=FileSystemStorage()
#     fn=fs.save(photo.name,photo)
#     user.image = fn
#     user.name = request.POST['name']
#     user.email = request.POST['email']
#     user.phone = request.POST['phone']
#     user.place = request.POST['place']
#     user.pin = request.POST['pin']
#     user.post = request.POST['post']
#     user.district = request.POST['district']
#     user.save()
#     return JsonResponse({'status': 'success'})



def update_profile(request):
    print(request.FILES, "hhhhhhhhhhhhhh")
    lid = request.POST['lid']
    user = usertbl.objects.get(LOGIN__id=lid)
    if 'photo' in request.FILES:
        photo = request.FILES['photo']
        fs = FileSystemStorage()
        fn = fs.save(photo.name, photo)
        user.photo = fn
        print(f"Image saved: {fn}")
    user.name = request.POST['name']
    user.email = request.POST['email']
    user.phone = request.POST['phone']
    user.place = request.POST['place']
    user.pin = request.POST['pin']
    user.post = request.POST['post']
    user.district = request.POST['district']
    user.save()
    return JsonResponse({'status': 'success'})


def updatelocation(request):
    print(request.POST)
    lat=request.POST["lat"]
    lon=request.POST["lon"]
    lid=request.POST["lid"]
    ob=userlocation.objects.filter(LOGIN=lid)
    if len(ob)>0:
        obx=userlocation.objects.get(LOGIN=lid)
        obx.lat=lat
        obx.lon=lon
        obx.save()
    else:
        obx = userlocation()
        obx.LOGIN_id=lid
        obx.lat = lat
        obx.lon = lon
        obx.save()
    return JsonResponse({"status":"ok"})

