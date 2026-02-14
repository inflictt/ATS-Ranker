from django.urls import path
from .views import ResumeUploadView, JobRankingView, home

# These are the APP-level URL patterns.
# They are included in the project's root urls.py under the "/api/" prefix,
# which is what the JS fetch("/api/upload-resume/") call expects.
#
# In your project's urls.py make sure you have:
#
#   from django.urls import path, include
#   from django.conf import settings
#   from django.conf.urls.static import static
#
#   urlpatterns = [
#       path("admin/", admin.site.urls),
#       path("",        include("resumechecker.urls")),   # home view at /
#       path("api/",    include("resumechecker.urls")),   # API views at /api/
#   ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#
# OR use a dedicated api_urls.py — see README.

urlpatterns = [
    path("",                      home,                name="home"),
    path("upload-resume/",        ResumeUploadView.as_view(), name="upload-resume"),
    path("rankings/<int:job_id>/", JobRankingView.as_view(),  name="job-rankings"),
]