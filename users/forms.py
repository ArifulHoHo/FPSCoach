from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Skill, Profile, CoachProfile, Review, BookSession, Message, NewsPortalPost, ValorantData
from django.forms.widgets import DateInput, TimeInput

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {'first_name':'Name'}

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user','is_coach']
        labels = {'social_instagram':'Instagram Link','social_twitter':'Twitter Link','social_youtube':'Youtube channel link','social_twitch':'Twitch link'}

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})



class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'
        exclude = ['owner']
        labels = {'name':'Skill Name'}

    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})

class CoachForm(ModelForm):
    class Meta:
        model = CoachProfile
        fields = ['session_price','experience']
        labels = {'experience':'Coached Before? How long in years?','session_price':'Session fee (be reasonable please)'}

    def __init__(self, *args, **kwargs):
        super(CoachForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value','body']
        labels = {
            'value':'Place your vote',
            'body':'Add you comment with your vote'
        }
    
    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})

class BookSessionForm(ModelForm):
    class Meta:
        model = BookSession
        fields = ['session_date','session_time','payment_id']
        labels = {'payment_id':'Enter the payment ID to confirm booking session'}
        widgets = {
            'session_date': DateInput(attrs={'placeholder': 'yyyy-mm-dd'}),
            'session_time': TimeInput(attrs={'placeholder': 'hh:mm'}),
        }

    def __init__(self, *args, **kwargs):
        super(BookSessionForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['name','email','subject','body']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})


class PlayerReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['body']
        labels = {
            
            'body':'Provide feedback based on coaching session'
        }
    
    def __init__(self, *args, **kwargs):
        super(PlayerReviewForm, self).__init__(*args, **kwargs)

        

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})

class PostForm(ModelForm):
    class Meta:
        model = NewsPortalPost
        fields = ['title','description','post_image','tags']

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)

        

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})

