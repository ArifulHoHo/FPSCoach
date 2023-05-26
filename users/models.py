from django.db import models
from django.contrib.auth.models import User

import uuid
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True,blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    short_intro = models.CharField(max_length=200,blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(blank=True, null=True, upload_to = 'profiles/',default='profiles/user-default.png')
    is_coach = models.BooleanField(default=False)
    
    social_twitter = models.CharField(max_length=200, blank=True, null=True)
    social_instagram = models.CharField(max_length=200, blank=True, null=True)
    social_youtube = models.CharField(max_length=200, blank=True, null=True)
    social_twitch = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True, editable=False)


    def __str__(self):
        return str(self.username)
    
    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()

        ratio = (upVotes / totalVotes ) * 100
        self.vote_total = totalVotes
        self.vote_ratio = ratio

        self.save()


class Skill(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True, editable=False)

    def __str__(self):
        return str(self.name)
    
class CoachProfile(models.Model):
    PRICE_CHOICES = [
        (500,'500 Tk'),
        (1000,'1000 Tk'),
        (2000,'2000 Tk'),
    ]
    coach = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True)
    session_price = models.IntegerField(choices=PRICE_CHOICES)
    vote_total = models.IntegerField(default=0)
    vote_ratio = models.IntegerField(default=0)
    experience = models.IntegerField(default=0)
    coached_students = models.IntegerField(default=0)
    id = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True, editable=False)

    def __str__(self):
        return str(self.coach)
    
    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()

        ratio = (upVotes / totalVotes ) * 100
        self.vote_total = totalVotes
        self.vote_ratio = ratio

        self.save()

    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset

    
class Review(models.Model):
    VOTE_TYPE = (
        ('up','Up Vote'),
        ('down','Down Vote'),
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    coach = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name='reviews')
    coachID = models.ForeignKey(CoachProfile, on_delete=models.CASCADE, null=True)
    body = models.TextField(null=True,blank=True)
    value = models.CharField(max_length=200,choices=VOTE_TYPE,null=True,blank=True,default='up')
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True, editable=False)

    class Meta:
        unique_together = [['owner','coach']]

    def __str__(self):
        return self.value


class BookSession(models.Model):
    
    coachBooked = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    bookUser = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name='bookuser')
    session_price = models.IntegerField()
    payment_id = models.CharField(max_length=10,null=True, blank=True)
    session_date = models.DateField(null=True)
    session_time = models.TimeField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True, editable=False)

    def __str__(self):
        return str(self.bookUser)
    
class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages')
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True, editable=False)

    def __str__(self):
        return self.subject
    
    class Meta:
        ordering = ['is_read','-created']


class NewsPortalPost(models.Model):

    creator = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True,blank=True)
    post_image = models.ImageField(blank=True, null=True,default='default.jpg')
    tags = models.ManyToManyField('Tag',blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True, editable=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']

class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True, editable=False)

    def __str__(self):
        return self.name


class ValorantData(models.Model):
    username = models.CharField(max_length=200)
    userID = models.CharField(max_length=4)
    user = models.OneToOneField(Profile,on_delete= models.SET_NULL,null=True,blank=True)
    peak_rank = models.CharField(max_length=20,default='Iron 1')
    rank = models.CharField(max_length=20,default='Iron 1')
    matches_played = models.IntegerField(default=0)
    matches_won = models.IntegerField(default=0)
    k_d = models.CharField(max_length=5,default='0.0')
    hs_percent = models.CharField(max_length=5,default='0.0')
    damage_per_round = models.CharField(max_length=5,default='0.0')

    def __str__(self):
        return str(self.user)
    
    