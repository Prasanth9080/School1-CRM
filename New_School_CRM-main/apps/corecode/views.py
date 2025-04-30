# new.... 

# functions


# view.py  29-07-24   6.19pm updated





from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import (
    AcademicSessionForm,
    AcademicTermForm,
    CurrentSessionForm,
    SiteConfigForm,
    StudentClassForm,
    SubjectForm,
)
from .models import (
    AcademicSession,
    AcademicTerm,
    SiteConfig,
    StudentClass,
    Subject,
)


# class IndexView(LoginRequiredMixin, TemplateView):
#     template_name = "index.html"


from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.students.models import Student
from apps.staffs.models import Staff
from apps.finance.models import Invoice

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_students'] = Student.objects.count()
        context['total_staff'] = Staff.objects.count()
        context['total_invoice'] = Invoice.objects.count()
        return context


####### new Indexview function ###########


# from django.shortcuts import render
# from django.views.generic import TemplateView
# from django.contrib.auth.mixins import LoginRequiredMixin
# from apps.students.models import Student
# from apps.staffs.models import Staff
# from apps.finance.models import Invoice

# class IndexView(LoginRequiredMixin, TemplateView):
#     template_name = "index.html"
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['total_students'] = Student.objects.count()
#         context['total_staff'] = Staff.objects.count()
#         context['total_invoice'] = Invoice.objects.count()
#         context['current_session'] = getattr(self.request, 'current_session', None)
#         context['current_term'] = getattr(self.request, 'current_term', None)
#         return context






### sub admin:

# views.py
# views.py

# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import update_session_auth_hash
# from django.contrib import messages
# from django.contrib.auth.forms import PasswordChangeForm
# from .forms import UserUpdateForm, ProfileUpdateForm
# from django.contrib.auth.models import User
# from .models import Profile

# @login_required
# def profile_view(request):
#     user = request.user  # Retrieve the current logged-in user

#     if request.method == 'POST':
#         user_form = UserUpdateForm(request.POST, instance=user)
#         profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=user.profile)
#         password_form = PasswordChangeForm(user, request.POST)

#         if user_form.is_valid() and profile_form.is_valid() and password_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             user = user_form.instance  # Get updated user instance
#             password_form.save()
#             update_session_auth_hash(request, user)  # Update session with new password hash
#             messages.success(request, 'Your profile was successfully updated!')
#             return redirect('profile')
#         else:
#             messages.error(request, 'Please correct the error below.')
#     else:
#         user_form = UserUpdateForm(instance=user)
#         profile_form = ProfileUpdateForm(instance=user.profile)
#         password_form = PasswordChangeForm(user)

#     context = {
#         'user_form': user_form,
#         'profile_form': profile_form,
#         'password_form': password_form,
#     }

#     return render(request, 'profile.html', context)




###### profile and edit profile....

# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import PasswordChangeForm
# from django.contrib.auth import update_session_auth_hash
# from django.shortcuts import render, redirect
# from .forms import UserForm, ProfileForm


# @login_required
# def profile_view(request):
#     return render(request, 'profile.html', {
#         'user': request.user,
#     })

# @login_required
# def edit_profile_view(request):
#     if request.method == 'POST':
#         if 'old_password' in request.POST:
#             password_form = PasswordChangeForm(request.user, request.POST)
#             if password_form.is_valid():
#                 user = password_form.save()
#                 update_session_auth_hash(request, user)
#                 messages.success(request, 'Your password was successfully updated!')
#                 return redirect('edit_profile')
#             else:
#                 messages.error(request, 'Please correct the error below.')
#         else:
#             user_form = UserForm(request.POST, instance=request.user)
#             profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
#             if user_form.is_valid() and profile_form.is_valid():
#                 user_form.save()
#                 profile_form.save()
#                 messages.success(request, 'Your profile was successfully updated!')
#                 return redirect('edit_profile')
#             else:
#                 messages.error(request, 'Please correct the error below.')
#     else:
#         user_form = UserForm(instance=request.user)
#         profile_form = ProfileForm(instance=request.user.profile)
#         password_form = PasswordChangeForm(request.user)

#     return render(request, 'edit_profile.html', {
#         'user_form': user_form,
#         'profile_form': profile_form,
#         'password_form': password_form
#     })




from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from .forms import UserForm, ProfileForm



@login_required
def profile_view(request):
    return render(request, 'profile.html', {
        'user': request.user,
    })


##### old views.py funtion for without input field

# @login_required
# def edit_profile_view(request):
#     user_form = UserForm(instance=request.user)
#     profile_form = ProfileForm(instance=request.user.profile)
#     password_form = PasswordChangeForm(request.user)

#     if request.method == 'POST':
#         if 'old_password' in request.POST:
#             password_form = PasswordChangeForm(request.user, request.POST)
#             if password_form.is_valid():
#                 user = password_form.save()
#                 update_session_auth_hash(request, user)
#                 messages.success(request, 'Your password was successfully updated!')
#                 return redirect('edit_profile')
#             else:
#                 messages.error(request, 'Please correct the error below / pls enter the stronge password.')
#         else:
#             user_form = UserForm(request.POST, instance=request.user)
#             profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
#             if user_form.is_valid() and profile_form.is_valid():
#                 user_form.save()
#                 profile_form.save()
#                 messages.success(request, 'Your profile was successfully updated!')
#                 return redirect('edit_profile')
#             else:
#                 messages.error(request, 'Please correct the error below.')

#     return render(request, 'edit_profile.html', {
#         'user_form': user_form,
#         'profile_form': profile_form,
#         'password_form': password_form
#     })



# @login_required
# def edit_profile_view(request):
#     if request.method == 'POST':
#         if 'old_password' in request.POST:
#             # Handle password change
#             password_form = PasswordChangeForm(request.user, request.POST)
#             if password_form.is_valid():
#                 user = password_form.save()
#                 update_session_auth_hash(request, user)
#                 messages.success(request, 'Your password was successfully updated!')
#                 return redirect('edit_profile')
#             else:
#                 messages.error(request, 'Please correct the error below.')
#         else:
#             # Handle profile update
#             user_form = UserForm(request.POST, instance=request.user)
#             profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
#             if user_form.is_valid() and profile_form.is_valid():
#                 user_form.save()
#                 profile_form.save()
#                 messages.success(request, 'Your profile was successfully updated!')
#                 return redirect('edit_profile')
#             else:
#                 messages.error(request, 'Please correct the error below.')
#     else:
#         user_form = UserForm(instance=request.user)
#         profile_form = ProfileForm(instance=request.user.profile)
#         password_form = PasswordChangeForm(request.user)

#     return render(request, 'edit_profile.html', {
#         'user_form': user_form,
#         'profile_form': profile_form,
#         'password_form': password_form
#     })




@login_required
def edit_profile_view(request):
    # Initialize forms
    user_form = UserForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)
    password_form = PasswordChangeForm(request.user)

    if request.method == 'POST':
        if 'old_password' in request.POST:
            # Handle password change
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                return redirect('edit_profile')
            else:
                messages.error(request, 'Please correct the error below.')
        else:
            # Handle profile update
            user_form = UserForm(request.POST, instance=request.user)
            profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, 'Your profile was successfully updated!')
                return redirect('edit_profile')
            else:
                messages.error(request, 'Please correct the error below.')

    # Render the template with forms
    return render(request, 'edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'password_form': password_form
    })




#### forgot password:: view function for success message:
### not working.....,

# from django.contrib.auth.views import PasswordResetConfirmView
# from django.contrib import messages
# from django.urls import reverse_lazy

# class CustomPasswordResetConfirmView(PasswordResetConfirmView):
#     template_name = 'password_reset_confirm.html'
#     success_url = reverse_lazy('password_reset_complete')

#     def form_valid(self, form):
#         messages.success(self.request, 'Password changed successfully.')
#         return super().form_valid(form)


# views.py    newly added..............................................
# from django.contrib.auth.views import PasswordResetView
# from django.contrib.auth.models import User
# from django.http import JsonResponse
# from django.urls import reverse_lazy
# from django.core.mail import send_mail
# from django.template.loader import render_to_string
# from django.utils.html import strip_tags
# from django.conf import settings

# class CustomPasswordResetView(PasswordResetView):
#     template_name = 'password-reset.html'
#     email_template_name = 'password_reset_email.html'
#     subject_template_name = 'password_reset_subject.txt'
#     success_url = reverse_lazy('password_reset_done')

#     def form_valid(self, form):
#         email = form.cleaned_data.get('email')
#         if User.objects.filter(email=email).exists():
#             # Call the parent class's form_valid method to send the email
#             return super().form_valid(form)
#         else:
#             # Return error response if the email is not registered
#             if self.request.is_ajax():
#                 return JsonResponse({'error': 'Email address not found.'}, status=400)
#             else:
#                 return super().form_invalid(form)
    
#     def form_invalid(self, form):
#         if self.request.is_ajax():
#             return JsonResponse({'error': form.errors}, status=400)
#         return super().form_invalid(form)





from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import PasswordResetForm

@csrf_exempt
def custom_password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Your email is incorrect.'}, status=400)

        # Prepare password reset email
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        domain = get_current_site(request).domain
        reset_link = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
        full_link = f"http://{domain}{reset_link}"

        subject = 'Password Reset Requested'
        message = render_to_string('password_reset_email.html', {
            'user': user,
            'protocol': 'http',
            'domain': domain,
            'uid': uid,
            'token': token,
        })
        
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

        return JsonResponse({'message': 'Password reset email has been sent.'})

    return JsonResponse({'error': 'Invalid request method.'}, status=405)








##### new views function for, forgotpassword updated sucess message
### not working..... below function..;
 
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm

def password_reset_confirm(request, uidb64=None, token=None):
    uid = urlsafe_base64_decode(uidb64).decode()
    user = User.objects.get(pk=uid)
    
    if default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your password has been changed successfully.')
                return redirect('password_reset_complete')
        else:
            form = SetPasswordForm(user)
    else:
        form = None

    return render(request, 'password_reset_confirm.html', {'form': form})





####### newly function for forgot password.............................


# from django.contrib.auth.views import PasswordResetView
# from django.urls import reverse_lazy
# from django.contrib import messages

# class CustomPasswordResetView(PasswordResetView):
#     template_name = 'password-reset.html'
#     email_template_name = 'registration/password_reset_email.html'
#     subject_template_name = 'registration/password_reset_subject.txt'
#     success_url = reverse_lazy('password_reset')

#     def form_valid(self, form):
#         response = super().form_valid(form)
#         messages.success(self.request, 'Password reset email has been sent.')
#         return response

# from django.contrib.auth.views import PasswordResetView
# from django.http import JsonResponse
# from django.urls import reverse_lazy

# class CustomPasswordResetView(PasswordResetView):
#     template_name = 'corecode/password-reset.html'
#     email_template_name = 'password_reset_email.html'
#     subject_template_name = 'password_reset_subject.txt'
#     success_url = reverse_lazy('password_reset_done')

#     def form_valid(self, form):
#         if self.request.is_ajax():
#             return JsonResponse({'message': 'Password reset email has been sent.'})
#         return super().form_valid(form)
    
#     def form_invalid(self, form):
#         if self.request.is_ajax():
#             return JsonResponse({'error': form.errors}, status=400)
#         return super().form_invalid(form)








# #### new default profile picture added views.py functions:







##################################
   ###################################################################
                     ##############################################################

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib import messages
from django.urls import reverse_lazy

User = get_user_model()

def password_reset_confirm(request, uidb64, token):
    user = None
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        if not default_token_generator.check_token(user, token):
            user = None
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None:
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Password has been reset successfully.")
                return redirect('password_reset_complete')
        else:
            form = SetPasswordForm(user)
        return render(request, 'passwordreset-confirm.html', {'form': form, 'uid': uidb64, 'token': token})
    else:
        messages.error(request, "The link is invalid or has expired.")
        return redirect('password_reset_done')

def password_reset_complete(request):
    return render(request, 'password-reset-done.html')



















# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import PasswordChangeForm
# from django.contrib.auth import update_session_auth_hash
# from django.shortcuts import render, redirect
# from django.templatetags.static import static
# from .forms import UserForm, ProfileForm

# @login_required
# def profile_view(request):
#     profile_picture_url = request.user.profile.profile_picture.url if request.user.profile.profile_picture else static('dist/img/avatar.png')
#     return render(request, 'profile.html', {
#         'user': request.user,
#         'profile_picture_url': profile_picture_url,
#     })

# @login_required
# def edit_profile_view(request):
#     if request.method == 'POST':
#         if 'old_password' in request.POST:
#             password_form = PasswordChangeForm(request.user, request.POST)
#             if password_form.is_valid():
#                 user = password_form.save()
#                 update_session_auth_hash(request, user)
#                 messages.success(request, 'Your password was successfully updated!')
#                 return redirect('edit_profile')
#             else:
#                 messages.error(request, 'Please correct the error below.')
#         else:
#             user_form = UserForm(request.POST, instance=request.user)
#             profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
#             if user_form.is_valid() and profile_form.is_valid():
#                 user_form.save()
#                 profile_form.save()
#                 messages.success(request, 'Your profile was successfully updated!')
#                 return redirect('edit_profile')
#             else:
#                 messages.error(request, 'Please correct the error below.')
#     else:
#         user_form = UserForm(instance=request.user)
#         profile_form = ProfileForm(instance=request.user.profile)
#         password_form = PasswordChangeForm(request.user)

#     profile_picture_url = request.user.profile.profile_picture.url if request.user.profile.profile_picture else static('dist/img/avatar.png')
    
#     return render(request, 'edit_profile.html', {
#         'user_form': user_form,
#         'profile_form': profile_form,
#         'password_form': password_form,
#         'profile_picture_url': profile_picture_url,
#     })
 




##### old sign-up view function:


from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib import messages

class SignupView(View):
    def get(self, request):
        return render(request, 'corecode/signup.html')
    

    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('signup')
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        # Create UserProfile instance and link to the User
        UserProfile.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            email=email
            # Add other fields as needed
        )

        messages.success(request, 'Signup successful! Please login.')
        return redirect('login')


### Login view

# from django.contrib.auth import authenticate, login
# from django.shortcuts import render, redirect
# from django.contrib import messages

# def custom_login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']

#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('home')  # Change 'home' to your dashboard or desired URL
#         else:
#             messages.error(request, "Your username and password didn't match. Please try again.")
#             return redirect('login')

#     return render(request, 'corecode/login.html')

##### ///////////// ##### this is working good and login with username and email address


# from django.contrib.auth import authenticate, login
# from django.contrib.auth.models import User
# from django.shortcuts import render, redirect
# from django.contrib import messages

# def custom_login_view(request):
#     if request.method == 'POST':
#         login_input = request.POST['username']
#         password = request.POST['password']

#         # Try to find user by username or email
#         try:
#             user = User.objects.get(username=login_input)
#         except User.DoesNotExist:
#             try:
#                 user = User.objects.get(email=login_input)
#             except User.DoesNotExist:
#                 user = None

#         # Authenticate only if user was found
#         if user is not None:
#             user = authenticate(request, username=user.username, password=password)
#             if user is not None:
#                 login(request, user)
#                 messages.success(request, f"welcome {user.username} 👍")
#                 return redirect('home')  # Change this to your landing page after login
#             else:
#                 messages.error(request, "Incorrect password. Please try again.")
#         else:
#             messages.error(request, "No account found with that username or email.")
#         return redirect('login')

#     return render(request, 'corecode/login.html')


###### //////////////// ########### end .....


# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .decorators import role_required
from .models import UserProfile

from django.contrib.auth.decorators import login_required
from .decorators import role_required

def custom_login_view(request):
    if request.method == "POST":
        username_or_email = request.POST['username']
        password = request.POST['password']

        # Try login with username or email
        user = authenticate(request, username=username_or_email, password=password)
        if user is None:
            try:
                user_obj = User.objects.get(email=username_or_email)
                user = authenticate(request, username=user_obj.username, password=password)
            except:
                user = None

        if user is not None:
            login(request, user)
            role = user.userprofile.role
            if role == "principal":
                messages.success(request, f"Hi welcome, {user.get_full_name() or user.username}")
                return redirect("principal_index")
            elif role == "teacher":
                messages.success(request, f"Hi welcome, {user.get_full_name() or user.username}")
                return redirect("staff_index")
            elif role == "student":
                messages.success(request, f"Hi welcome, {user.get_full_name() or user.username}")
                return redirect("student_index")
            else:
                return redirect("home")
        else:
            messages.error(request, "Invalid credentials. Please try again.")

    return render(request, "corecode/login.html")

@login_required
@role_required('principal')
def principal_index(request):
    # return render(request, 'corecode/student_dashboard.html')s
    return render(request, 'principal/principal_index.html')

@login_required
@role_required('teacher')
def staff_index(request):
    # return render(request, 'corecode/teacher_dashboard.html')
    return render(request, 'staffs/staff_index.html')

@login_required
@role_required('student')
def student_index(request):
    # return render(request, 'corecode/student_dashboard.html')
    # return render(request, 'index.html')
    return render(request, 'students/student_index.html')








# from django.contrib.auth import login, authenticate
# from django.contrib.auth.forms import UserCreationForm
# from django.shortcuts import render, redirect
# from django.urls import reverse

# def signup(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=password)
#             login(request, user)
#             return redirect('desired_redirect_url')  # Change this to your desired redirect URL
#     else:
#         form = UserCreationForm()
#     return render(request, 'corecode/signup.html', {'form': form})























class SiteConfigView(LoginRequiredMixin, View):
    """Site Config View"""

    form_class = SiteConfigForm
    template_name = "corecode/siteconfig.html"

    def get(self, request, *args, **kwargs):
        formset = self.form_class(queryset=SiteConfig.objects.all())
        context = {"formset": formset}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        formset = self.form_class(request.POST)
        if formset.is_valid():
            formset.save()
            messages.success(request, "Configurations successfully updated")
        context = {"formset": formset, "title": "Configuration"}
        return render(request, self.template_name, context)


class SessionListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = AcademicSession
    template_name = "corecode/session_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = AcademicSessionForm()
        return context


class SessionCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = AcademicSession
    form_class = AcademicSessionForm
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("sessions")
    success_message = "New session successfully added"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add new session"
        return context


class SessionUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = AcademicSession
    form_class = AcademicSessionForm
    success_url = reverse_lazy("sessions")
    success_message = "Session successfully updated."
    template_name = "corecode/mgt_form.html"

    def form_valid(self, form):
        obj = self.object
        if obj.current == False:
            terms = (
                AcademicSession.objects.filter(current=True)
                .exclude(name=obj.name)
                .exists()
            )
            if not terms:
                messages.warning(self.request, "You must set a session to current.")
                return redirect("session-list")
        return super().form_valid(form)


class SessionDeleteView(LoginRequiredMixin, DeleteView):
    model = AcademicSession
    success_url = reverse_lazy("sessions")
    template_name = "corecode/core_confirm_delete.html"
    success_message = "The session {} has been deleted with all its attached content"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.current == True:
            messages.warning(request, "Cannot delete session as it is set to current")
            return redirect("sessions")
        messages.success(self.request, self.success_message.format(obj.name))
        return super(SessionDeleteView, self).delete(request, *args, **kwargs)


class TermListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = AcademicTerm
    template_name = "corecode/term_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = AcademicTermForm()
        return context
 

class TermCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = AcademicTerm
    form_class = AcademicTermForm
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("terms")
    success_message = "New term successfully added"


class TermUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = AcademicTerm
    form_class = AcademicTermForm
    success_url = reverse_lazy("terms")
    success_message = "Term successfully updated."
    template_name = "corecode/mgt_form.html"

    def form_valid(self, form):
        obj = self.object
        if obj.current == False:
            terms = (
                AcademicTerm.objects.filter(current=True)
                .exclude(name=obj.name)
                .exists()
            )
            if not terms:
                messages.warning(self.request, "You must set a term to current.")
                return redirect("term")
        return super().form_valid(form)


class TermDeleteView(LoginRequiredMixin, DeleteView):
    model = AcademicTerm
    success_url = reverse_lazy("terms")
    template_name = "corecode/core_confirm_delete.html"
    success_message = "The term {} has been deleted with all its attached content"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.current == True:
            messages.warning(request, "Cannot delete term as it is set to current")
            return redirect("terms")
        messages.success(self.request, self.success_message.format(obj.name))
        return super(TermDeleteView, self).delete(request, *args, **kwargs)


class ClassListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = StudentClass
    template_name = "corecode/class_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = StudentClassForm()
        return context


class ClassCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = StudentClass
    form_class = StudentClassForm
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("classes")
    success_message = "New class successfully added"


class ClassUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = StudentClass
    fields = ["name"]
    success_url = reverse_lazy("classes")
    success_message = "class successfully updated."
    template_name = "corecode/mgt_form.html"


class ClassDeleteView(LoginRequiredMixin, DeleteView):
    model = StudentClass
    success_url = reverse_lazy("classes")
    template_name = "corecode/core_confirm_delete.html"
    success_message = "The class {} has been deleted with all its attached content"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        print(obj.name)
        messages.success(self.request, self.success_message.format(obj.name))
        return super(ClassDeleteView, self).delete(request, *args, **kwargs)


class SubjectListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = Subject
    template_name = "corecode/subject_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SubjectForm()
        return context


class SubjectCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("subjects")
    success_message = "New subject successfully added"


class SubjectUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Subject
    fields = ["name"]
    success_url = reverse_lazy("subjects")
    success_message = "Subject successfully updated."
    template_name = "corecode/mgt_form.html"


class SubjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Subject
    success_url = reverse_lazy("subjects")
    template_name = "corecode/core_confirm_delete.html"
    success_message = "The subject {} has been deleted with all its attached content"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message.format(obj.name))
        return super(SubjectDeleteView, self).delete(request, *args, **kwargs)


class CurrentSessionAndTermView(LoginRequiredMixin, View):
    """Current SEssion and Term"""

    form_class = CurrentSessionForm
    template_name = "corecode/current_session.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class(
            initial={
                "current_session": AcademicSession.objects.get(current=True),
                "current_term": AcademicTerm.objects.get(current=True),
            }
        )
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_Class(request.POST)
        if form.is_valid():
            session = form.cleaned_data["current_session"]
            term = form.cleaned_data["current_term"]
            AcademicSession.objects.filter(name=session).update(current=True)
            AcademicSession.objects.exclude(name=session).update(current=False)
            AcademicTerm.objects.filter(name=term).update(current=True)

        return render(request, self.template_name, {"form": form})

#################################### signup


# from django.shortcuts import render,HttpResponse,redirect
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate,login,logout
# from django.contrib.auth.decorators import login_required
# # Create your views here.
# @login_required(login_url='login')
# def HomePage(request):
#     # return render (request,'home.html')
#     return render (request,'index.html')

# def SignupPage(request):
#     if request.method=='POST':
#         uname=request.POST.get('username')
#         email=request.POST.get('email')
#         pass1=request.POST.get('password1')
#         pass2=request.POST.get('password2')

#         if pass1!=pass2:
#             return HttpResponse("Your password and confrom password are not Same!!")
#         else:

#             my_user=User.objects.create_user(uname,email,pass1)
#             my_user.save()
#             return redirect('login')
        



#     return render (request,'signup.html')

# def LoginPage(request):
#     if request.method=='POST':
#         username=request.POST.get('username')
#         pass1=request.POST.get('pass')
#         user=authenticate(request,username=username,password=pass1)
#         if user is not None:
#             login(request,user)
#             return redirect('home')
#         else:
#             return HttpResponse ("Username or Password is incorrect!!!")

#     return render (request,'login.html')

# def LogoutPage(request):
#     logout(request)
#     return redirect('login')