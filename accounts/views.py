from django.conf import settings
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.views.generic import FormView, View
from .forms import SignUpForm, LoginForm, ForgotPasswordForm, ResetPasswordForm
from .token import generate_user_token, generate_password_reset_token, verify_user_token, verify_password_reset_token
from django.http import HttpResponse
from django.core.mail import send_mail
from .mixins import AnonymousRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class CreateUserView(AnonymousRequiredMixin, FormView):
    model = User
    form_class = SignUpForm
    template_name = "accounts/signup.html"

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        user = User.objects.create_user(username=email, email=email, password=password)

        user.is_active = False
        user.save()

        token = generate_user_token(user_id=user.pk)

        verification_link = self.request.build_absolute_uri(reverse("activate_user", kwargs={"token": token}))

        if settings.DEBUG:
            print(f"\nVERIFICATION URL:\n{verification_link}\n")

        send_mail(
            subject="Verify your email",
            message=(
                "Please verify your email using this link:\n\n"
                f"{verification_link}\n\n"
                "This link expires in 24 hours."
            ),
            from_email="noreply@example.com",
            recipient_list=[user.email],
            fail_silently=False,
        )

        return render(self.request,"accounts/verify-user.html")

    def form_invalid(self, form):
        return super().form_invalid(form)
            
class ActivateUserView(AnonymousRequiredMixin, View):
    def get(self, request, token):
        verified = verify_user_token(token)
        if verified is None:
            return HttpResponse("Invalid link or link has expired.", status=400)

        user_id = verified.get("user_id")

        if user_id is None:
            return HttpResponse("Invalid link or link has expired.", status=400)
        
        try:
            user = User.objects.get(pk=user_id)
        except:
            return HttpResponse("User does not exist", status=400)
        
        if user.is_active:
            return HttpResponse("User has already been activated", status=400)
        
        user.is_active = True
        user.save(update_fields=["is_active"])

        messages.success(self.request, "You are now verified! You can now log in.")

        return redirect("login-form")
    
class LoginView(AnonymousRequiredMixin, FormView):
    model = User
    form_class = LoginForm
    template_name = "accounts/login.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        login(self.request, form.user)
        return redirect("/")

    def form_invalid(self, form):
        return super().form_invalid(form)
    
class LogoutView(LoginRequiredMixin, View):
    template_name = "accounts/logout.html"

    def post(self, request):
        logout(request)
        return redirect("login-form")
    

class ForgotPasswordView(AnonymousRequiredMixin, FormView):
    template_name = "accounts/forgot-password.html"
    form_class = ForgotPasswordForm

    def form_valid(self, form):
        email = form.cleaned_data["email"]

        user = User.objects.filter(
            email__iexact=email,
            is_active=True,
        ).first()

        if user:
            token = generate_password_reset_token(user_id=user.pk)

            reset_url = self.request.build_absolute_uri(
                reverse(
                    "reset-password",
                    kwargs={"token": token},
                )
            )

            if settings.DEBUG:
                print(f"\nPASSWORD RESET URL:\n{reset_url}\n")

            send_mail(
                subject="Reset your password",
                message=(
                    "Use the following link to reset your password:\n\n"
                    f"{reset_url}\n\n"
                    "This link expires in 24 hours."
                ),
                from_email="noreply@example.com",
                recipient_list=[user.email],
                fail_silently=False,
            )

        messages.success(
            self.request,
            "Password reset email has been sent!",
        )

        return redirect("forgot-password")
        
class ResetPasswordView(AnonymousRequiredMixin, FormView):
    template_name = "accounts/reset-password.html"
    form_class = ResetPasswordForm

    def form_valid(self, form):
        token = self.kwargs["token"]
        verified = verify_password_reset_token(token)

        if verified is None:
            return HttpResponse("Invalid link or link has expired.", status=400)
        
        user_id = verified.get("user_id")
        
        if user_id is None:
            return HttpResponse("Invalid link or link has expired.2", status=400)

        user = User.objects.filter(pk=user_id, is_active=True,).first()

        if user is None:
            return HttpResponse("Invalid link or link has expired.", status=400)

        password = form.cleaned_data["password"]
        user.set_password(password)
        user.save()

        messages.success(self.request, "Password changed successfully! You can now log in.")

        return redirect("login-form")

    def form_invalid(self, form):
        return super().form_invalid(form)