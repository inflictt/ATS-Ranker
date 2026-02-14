from rest_framework import serializers
from .models import Resume, JobDescription


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Resume
        fields = ["id", "resume"]
        read_only_fields = ["id"]

    def validate_resume(self, value):
        if not value.name.lower().endswith(".pdf"):
            raise serializers.ValidationError(
                "Only PDF files are accepted. Please upload a .pdf resume."
            )
        max_bytes = 5 * 1024 * 1024
        if value.size > max_bytes:
            raise serializers.ValidationError("Resume file exceeds the 5 MB limit.")
        return value


class JobDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model  = JobDescription
        # Only fields that exist in the current DB — no created_at column
        fields = ["id", "job_title", "job_description"]
        read_only_fields = ["id"]