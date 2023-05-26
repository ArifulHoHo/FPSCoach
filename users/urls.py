from django.urls import path
from . import views

urlpatterns = [
    path('',views.coachPage,name='coaches'),
    path('coach/<str:pk>',views.showcoachProfile,name='coach-profile'),

    path('login/',views.loginUser,name='login'),
    path('logout/',views.logoutUser,name='logout'),
    path('register/',views.registerUser,name='register'),

    path('account/',views.userAccount,name='account'),
    path('edit-account/',views.editAccount,name='edit-account'),
    path('create-skill/',views.createSkill,name='create-skill'),
    path('upgrade-user/',views.requestUpgradeToCoach,name='upgrade-user'),
    path('new-coach-info',views.upgradeCoach, name='new-coach-info'),

    path('book-coach/<str:pk>/',views.bookSession,name = 'book-coach'),
    path('cancel-session/<str:pk>/',views.cancelSession,name='cancel-session'),

    path('inbox/',views.inbox,name='inbox'),
    path('message/<str:pk>/',views.viewMessage,name='message'),
    path('create-message/<str:pk>',views.createMessage,name='create-message'),

    path('notifications/',views.showNotifications,name='notifications'),

    path('news-portal/',views.showNews,name='news-portal'),
    path('single-post/<str:pk>/',views.showSinglePost,name='single-post'),

    path('add-post/',views.addPost,name='add-post'),
    
]