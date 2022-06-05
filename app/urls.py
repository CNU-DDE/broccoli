from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = format_suffix_patterns([
    path('user', views.UserResponse.as_view()),
    path('user/token', views.UserTokenResponse.as_view()),
    path('cover-letter', views.CoverLetterResponse.as_view()),
    path('position', views.PositionResponse.as_view()),
    path('position/<int:position_id>', views.PositionDetailResponse.as_view()),
    path('claim', views.ClaimResponse.as_view()),
    path('claim/<int:claim_id>', views.ClaimDetailResponse.as_view()),
    path('resume', views.ResumeResponse.as_view()),
    path('resume/all', views.ResumeAllResponse.as_view()),
    path('resume/<int:resume_id>', views.ResumeDetailResponse.as_view()),
    path('resume/submission', views.ResumeSubmissionResponse.as_view()),
])
