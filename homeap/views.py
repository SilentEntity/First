from django.shortcuts import render,render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,JsonResponse

import smtplib
import json
from .models import Users
"""For logging Generation importing logging and saving it to root logger with file name=SilentEntity """
import logging
logging.basicConfig(filename='SilentEntity.log',level=logging.INFO,format='%(asctime)s:%(levelname)s:%(message)s')
# Create your views here.
@csrf_exempt
def Home(request):
    """Home page SignIN function in views ,Creates logs for every activity
        1.accepts json data ,username and password are the keys
        2.response back in json ,with appropriate message
    """
    if request.method == 'POST':
        # data = json.loads(request.body)
        # print(data)
        username=request.POST['username']
        password=request.POST['password']
        obj=Users(username='username',password='password')
        result=Users.objects.filter(username__exact=username).values()
        print('------------->',type(result))
        lis =[i for i in result]
        print(lis)
        if len(lis) > 0 and lis[0]['password'] == password:
            logging.info("User SignedIn with mailId:{}".format('username'))
            print('imhere')
            return render(request,'homeapPages/userhomepage.html',{'data':username})
        else:
            logging.info("Invalid Data provided {},{}".format('username','password'))
            return render(request,'homeapPages/invalidPage.html')
    elif request.method == 'GET':
        logging.info('Someone Visited the Page')
        return render(request,'homeapPages/homepage.html')
        # return pages
        # all can follow people in this page
@csrf_exempt
def getUserData(request):
    print('line 42')
    if request.method == 'POST':
        data=json.loads(request.body)
        print(data)
        result=Users.objects.filter(username__exact=data['username']).values('follower','following')
        mylist=[i for i in result]
        print(mylist)
        availableusers=Users.objects.values('username')
        listofusers=[i for i in availableusers]

        for i in range(len(listofusers)):
            if i<len(listofusers) and listofusers[i]['username'] == data['username']:
               listofusers.remove(listofusers[i])
            for j in range(len(mylist[0]['following'])):
                print(len(mylist[0]['following']))
                print(mylist[0]['following'][j])
                if j<len(mylist[0]['following']) and i<len(listofusers) and listofusers[i]['username']== mylist[0]['following'][j]:
                    listofusers.remove(listofusers[i])

        print(listofusers)

        return JsonResponse({'follower':mylist[0]['follower'],'following':mylist[0]['following'],'userlist':listofusers})



@csrf_exempt
def signup(request):
    """Signup function is for signing up, it creates Logs for every activity
        1.accepts json data username and password are the keys
        2.response back in json data
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        obj=Users(username=data['username'],password=data['password'],follower=[],following=[])
        result=Users.objects.filter(username__exact=data['username']).count()
        if result==1:
            logging.info("Tried to register again with existing email:{}".format(data['username']))
            return JsonResponse({'key':'user Exist'})
        else:
            obj.save()
            logging.info("New User Account Created:{}".format(data['username']))
            return JsonResponse({'key': data['username']})
    elif request.method == 'GET':
        logging.info("Some Tried to SignUP on website")
        return render(request, 'homeapPages/signup.html')
@csrf_exempt
def forgot(request):
    """Forgot password function for retriving password and send it via SMTP to Gmail ,creates logs for every activity
        1.accepts json data username and password is the key
        2.Provide mail to gmail to your registered mail
        3.reposne with json for Approperiate message
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        #obj = Users(username=data['username'], password='')

        result=Users.objects.filter(username__exact=data['username']).values('password')
        l=[i for i in result]
        if len(l)==1:
            #Sending Email for password recovery
            mail = smtplib.SMTP('smtp.gmail.com', 587)
            print('connected')
            mail.ehlo()
            mail.starttls()
            print('here')
            mail.login('entitysilent@gmail.com', 'Myluckon@7')
            print('yes')
            print(data['username'])
            mail.sendmail('entitysilent@gmail.com', data['username'], l[0]['password'])
            logging.info("Forgot Password option ,Password as send to mail:{}".format(data['username']))
            mail.close()
            print(l[0]['password'])
            return JsonResponse({'key':'Check Your Gmail mails for the password'})

        else:
            logging.info("Forgot Password option,Invalid UserId provided:{}".format(data['username']))
            return JsonResponse({'key':'NOT available for this username'})
    elif request.method == 'GET':
        logging.info("Someone tried to recover password")
        return render(request,'homeapPages/forgot.html')
        #return page here
@csrf_exempt
def follower(request):
    """Follower function to give back the person that follow him/her,creates logs for every activity
        1.accepting json data, username is the key
        2.responding back with json data
    """
    if request.method == 'POST':
        data=json.loads(request.body)
        print(data)
        last=Users.objects.filter(username=data['username']).values('follower')
        l=[i for i in last]
        dummy=l[0]['follower']
        result=Users.objects.filter(username=data['username']).update(follower=dummy)
        print(result)
        logging.info("{} user is viewing the list of person that follow him".format(data['username']))
        return JsonResponse({'Your are followed by:':dummy})

    elif request.method == 'GET':

        pass
        #page
@csrf_exempt
def following(request):
    """Follow function enable you to follow people,creates logs for every activity
        1.Takes Json data username and user are the keys
        2.update into followers filed in respective users
    """
    if request.method == 'POST':
        data=json.loads(request.body)
        print(data)
        last=Users.objects.filter(username=data['username']).values('following')
        l=[i for i in last]
        dummy=l[0]['following']
        dummy.append(data['user'])
        print(dummy)
        result=Users.objects.filter(username=data['username']).update(following=dummy)
        print(result)
        for user in dummy:
            last=Users.objects.filter(username=user).values('follower')
            d=[x for x in last]
            dumm=d[0]['follower']
            dumm.append(data['username'])
            update=Users.objects.filter(username=user).update(follower=dumm)
            logging.info("{} user is being followed by {}".format(user,data['username']))
        logging.info("New follower add in:{}".format(data['username']))
        return JsonResponse({'Your are following:':dummy})
    elif request.method == 'GET':
        pass
        #page
