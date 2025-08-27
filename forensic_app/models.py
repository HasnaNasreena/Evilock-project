from django.db import models

# Create your models here.
class logintbl(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    type=models.CharField(max_length=100)

class courttbl(models.Model):
    LOGIN=models.ForeignKey(logintbl, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    pin=models.BigIntegerField()
    post=models.CharField(max_length=100)
    district=models.CharField(max_length=100)
    phone=models.BigIntegerField()
    email=models.CharField(max_length=100)
    type=models.CharField(max_length=100)

class forensicstafftbl(models.Model):
    LOGIN=models.ForeignKey(logintbl, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    photo=models.FileField()
    regno=models.BigIntegerField()
    forensicplace=models.CharField(max_length=100)
    forensicpin = models.CharField(max_length=100)
    forensicpost = models.CharField(max_length=100)
    district= models.CharField(max_length=100)


class usertbl(models.Model):
    LOGIN = models.ForeignKey(logintbl, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.BigIntegerField()
    photo = models.FileField()
    place = models.CharField(max_length=100)
    pin = models.BigIntegerField()
    post = models.CharField(max_length=100)
    district = models.CharField(max_length=100)


class feedbacktbl(models.Model):
    USER=models.ForeignKey(usertbl,on_delete=models.CASCADE)
    date=models.DateField()
    rating=models.FloatField()
    feedback=models.CharField(max_length=100)





class police_stationtbl(models.Model):
    LOGIN = models.ForeignKey(logintbl, on_delete=models.CASCADE)
    stationname = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    pin = models.BigIntegerField()
    post = models.CharField(max_length=100)
    district=models.CharField(max_length=100)
    phone = models.BigIntegerField()
    email = models.CharField(max_length=100)
    landmark=models.CharField(max_length=100)
    latitude=models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)

class casetbl(models.Model):
    USER=models.ForeignKey(usertbl,on_delete=models.CASCADE,blank=True,null=True )
    POLICE=models.ForeignKey(police_stationtbl,on_delete=models.CASCADE,blank=True,null=True )
    case = models.CharField(max_length=100)
    details=models.CharField(max_length=100)
    date=models.DateField()
    type=models.CharField(max_length=100)
    status=models.CharField(max_length=100)
    incident_place=models.CharField(max_length=100)
    incident_pin=models.BigIntegerField()
    incident_post=models.CharField(max_length=100)
    incident_district=models.CharField(max_length=100)
    latitude=models.CharField(max_length=100)
    longitude=models.CharField(max_length=100)


class case_alloctbl(models.Model):
    STAFFID = models.ForeignKey(forensicstafftbl, on_delete=models.CASCADE)
    CASEID=models.ForeignKey(casetbl,on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=100)


class evidencetbl(models.Model):
    POLICE = models.ForeignKey(police_stationtbl, on_delete=models.CASCADE)
    CASEID=models.ForeignKey(casetbl,on_delete=models.CASCADE)
    evidencename = models.CharField(max_length=100)
    photo = models.FileField()
    descripition=models.CharField(max_length=1000)
    date = models.DateField()


class forensic_evidence(models.Model):
    ALLOCID=models.ForeignKey(case_alloctbl,on_delete=models.CASCADE)
    evidencename = models.CharField(max_length=100)
    file=models.FileField()
    descripition = models.CharField(max_length=1000)
    date = models.DateField()


class chattbl(models.Model):
    FROM_ID=models.ForeignKey(logintbl, on_delete=models.CASCADE,related_name="fromid")
    TO_ID=models.ForeignKey(logintbl, on_delete=models.CASCADE,related_name="toid")
    message=models.CharField(max_length=100)
    date = models.DateField()
    status = models.CharField(max_length=100)

class evidence_requesttbl(models.Model):
    CASEID=models.ForeignKey(casetbl,on_delete=models.CASCADE)
    LOGIN=models.ForeignKey(logintbl, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=100)
    COURT =models.ForeignKey(courttbl,on_delete=models.CASCADE,null=True,blank=True)


class userlocation(models.Model):
    LOGIN = models.ForeignKey(logintbl, on_delete=models.CASCADE)
    lat = models.CharField(max_length=100)
    lon = models.CharField(max_length=100)


class anony_casetbl(models.Model):
    POLICE=models.ForeignKey(police_stationtbl,on_delete=models.CASCADE,blank=True,null=True )
    case = models.CharField(max_length=100)
    details=models.CharField(max_length=100)
    date=models.DateField()
    status=models.CharField(max_length=100)
    incident_place=models.CharField(max_length=100)
    incident_pin=models.BigIntegerField()
    incident_post=models.CharField(max_length=100)
    incident_district=models.CharField(max_length=100)
    latitude=models.CharField(max_length=100)
    longitude=models.CharField(max_length=100)



class firtbl(models.Model):
    CASEID=models.ForeignKey(casetbl,on_delete=models.CASCADE)
    fir=models.FileField()
























