from django.contrib import admin
from django.urls import path

from forensic_app import views

urlpatterns = [
    path('',views.login,name='login'),
    path('logout',views.logout),
    path('admin_add_court',views.admin_add_court),
    path('admin_view_court',views.admin_view_court),
    path('admin_view_policestation',views.admin_view_policestation),
    path('admin_view_allocationhistory',views.admin_view_allocationhistory),
    path('admin_view_casehistory',views.admin_view_casehistory),
    path('admin_view_feedback',views.admin_view_feedback),
    path('admin_view_staff_verify',views.admin_view_staff_verify),
    path('adminhome',views.adminhome),
    path('loginpost',views.loginpost),
    path('forgotpassword', views.forgotpassword),

    path('forgotpasswordpost', views.forgotpasswordpost),
    path('/forgotpassword_flutter', views.forgotpassword_flutter),
    path('addcourtpost',views.addcourtpost),
    path('searchFeedback',views.searchFeedback),
    path('searchcasehistory', views.searchcasehistory),
    path('searchallocationhistory', views.searchallocationhistory),
    path('acceptstaff/<id>', views.acceptstaff),
    path('rejectstaff/<id>', views.rejectstaff),
    path('editcourt/<id>', views.editcourt),
    path('rejectstaff/<id>', views.rejectstaff),
    path('editcourtpost', views.editcourtpost),
    path('delete/<id>', views.delete),


    path('policestation',views.policestation),
    path('stationforecast_cases1',views.stationforecast_cases1),
    path('policestation_addnewevidence', views.policestation_addnewevidence),
    path('policestation_case_reg', views.policestation_case_reg),
    path('policestation_evidence_requ_forwa_to_court', views.policestation_evidence_requ_forwa_to_court),
    path('policestation_manageevidence', views.policestation_manageevidence),
    path('forwardcourtpost/<id>', views.forwardcourtpost),
    path('forwardcourt', views.forwardcourt),
    path('policestation_view_anonymous_report',views.policestation_view_anonymous_report),
    path('registration',views.registration),
    path('viewverifiedcase',views.viewverifiedcase),
    path('fir',views.fir),
    path('firrequest',views.firrequest),
    path('firview/<id>',views.firview),
    path('registrationpost', views.registrationpost),
    path('policestation_addnewevidencepost', views.policestation_addnewevidencepost),
    path('editpolicestation/<id>',views.editpolicestation),
    path('editpolicestationpost', views.editpolicestationpost),
    path('delete_manageevidence/<id>',views.delete_manageevidence),
    path('acceptcasereg/<id>', views.acceptcasereg),
    path('rejectcasereg/<id>', views.rejectcasereg),
    path('acceptrequestcase/<id>', views.acceptrequestcase),
    path('rejectreuestevidence/<id>', views.rejectreuestevidence),
    path('policeloc', views.policeloc),
    path('admin_view_evidance_history/<id>', views.admin_view_evidance_history),
    path('forensicstaff_view_uploadevidence_police/<id>', views.forensicstaff_view_uploadevidence_police),
    # path('forwardcourt/<id>', views.forwardcourt),

    path('courthome', views.courthome),
    path('court_staffassign_case', views.court_staffassign_case),
    path('court_staff_assign_to_case_2', views.court_staff_assign_to_case_2),
    path('verify_evidence_request', views.verify_evidence_request),
    path('court_verify_policestation', views.court_verify_policestation),
    path('acceptpolicestation/<id>', views.acceptpolicestation),
    path('rejectpolicestation/<id>', views.rejectpolicestation),
    path('assign_staff/<id>', views.assign_staff),
    path('assign_staff_post', views.assign_staff_post),
    path('rejectevidence/<id>', views.rejectevidence),
    path('acceptevidence/<id>', views.acceptevidence),

    path('forensichome', views.forensichome),
    path('forensicstaff_forensicreg', views.forensicstaff_forensicreg),
    path('forensicregpost', views.forensicregpost),
    path('forensicstaff_uploadevidence/<id>', views.forensicstaff_uploadevidence),
    path('forensic_addevidence', views.forensic_addevidence),
    path('forensic_addnewevidencepost', views.forensic_addnewevidencepost),

    path('forensicstaff_view_alloc_case', views.forensicstaff_view_alloc_case),


    path('chatwithuser', views.chatwithuser, name='chatwithuser'),
    path('profilestaff', views.profilestaff, name='profilestaff'),
    path('chatview', views.chatview, name='chatview'),
    path('coun_msg/<int:id>', views.coun_msg, name='coun_msg'),
    path('coun_insert_chat/<str:msg>/<int:id>', views.coun_insert_chat, name='coun_insert_chat'),

    path('chatfuserview', views.chatfuserview, name='chatfuserview'),
    path('chatfuserview_load', views.chatfuserview_load, name='chatfuserview_load'),
    path('coun_fmsg2/<id>', views.coun_fmsg2, name='coun_fmsg2'),

    path('chatwithfstaff', views.chatwithfstaff, name='chatwithfstaff'),
    path('chatfstaffview', views.chatfstaffview, name='chatfstaffview'),
    path('coun_fmsg/<int:id>', views.coun_fmsg, name='coun_fmsg'),
    path('coun_insert_fstaff/<str:msg>/<int:id>', views.coun_insert_fstaff, name='coun_insert_fstaff'),


    # ================android==========================================================






    path('/logincode', views.logincode, name='logincode'),
    path('registrationcode', views.registrationcode),
    path('sendfeedback', views.sendfeedback),
    path('casregistration', views.casregistration),
    path('sendevidencerequest', views.sendevidencerequest),
    path('viewforensicevidence', views.viewforensicevidence),
    path('viewpoliceevidence', views.viewpoliceevidence),
    path('/viewusercasereg', views.viewusercasereg),
    path('/requesttblstatus', views.requesttblstatus),

    path('viewchat', views.viewchat),
    path('/view_profile', views.view_profile),
    # path('/update_profile', views.update_profile),
    path('sendchat', views.sendchat),
    path('viewchatpolicestation', views.viewchatpolicestation),
    path('userviewprofile', views.userviewprofile),
    path('/userviewprofile', views.userviewprofile),
    path('/updateprofile', views.update_profile),
    path('casregistrationanonymous', views.casregistrationanonymous),
    path('updatelocation', views.updatelocation),
    path('approve_case/<id>', views.approve_case),
    path('reject_case/<id>', views.reject_case),
]

