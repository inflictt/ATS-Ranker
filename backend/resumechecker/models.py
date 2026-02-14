from django.db import models


class Resume(models.Model):
    # upload_to kept as original "resume" to match existing DB/migration.
    # Files continue to be stored under media/resume<filename> as before.
    resume = models.FileField(upload_to="resume")

    def __str__(self):
        return self.resume.name.split("/")[-1]


class JobDescription(models.Model):
    # EXACTLY matches original schema — no extra columns, no migration needed.
    job_title       = models.CharField(max_length=100)
    job_description = models.TextField()

    def __str__(self):
        return self.job_title


class ResumeScore(models.Model):
    resume          = models.ForeignKey(Resume,         on_delete=models.CASCADE, related_name="scores")
    job_description = models.ForeignKey(JobDescription, on_delete=models.CASCADE, related_name="scores")
    score           = models.FloatField()
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-score"]

    def __str__(self):
        return f"{self.resume} → {self.job_description} ({self.score}%)"