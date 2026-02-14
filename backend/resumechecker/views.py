from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from .serializers import ResumeSerializer
from .models import JobDescription, ResumeScore
from .analyzer import extract_text_from_pdf, calculate_similarity


class ResumeUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):

        serializer = ResumeSerializer(data=request.data)
        job_id = request.data.get("job_id")

        if not job_id:
            return Response(
                {"error": "job_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            job = JobDescription.objects.get(id=job_id)
        except JobDescription.DoesNotExist:
            return Response(
                {"error": f"No job found with id={job_id}"},
                status=status.HTTP_404_NOT_FOUND
            )

        if serializer.is_valid():
            resume_obj = serializer.save()

            resume_path = resume_obj.resume.path
            extracted_text = extract_text_from_pdf(resume_path)

            result = calculate_similarity(
                extracted_text,
                job.job_description
            )

            ResumeScore.objects.create(
                resume=resume_obj,
                job_description=job,
                score=result["score"]
            )

            return Response(
                {
                    "success": True,
                    "score": result["score"],
                    "tfidf_score": result["tfidf_score"],
                    "skill_score": result["skill_score"],
                    "matched_keywords": result["matched_keywords"],
                    "missing_keywords": result["missing_keywords"],
                    "suggestions": result["suggestions"],
                    "resume_id": resume_obj.id,
                    "job_id": job.id,
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {"error": "Invalid data", "details": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


class JobRankingView(APIView):

    def get(self, request, job_id):

        if not JobDescription.objects.filter(id=job_id).exists():
            return Response(
                {"error": f"No job found with id={job_id}"},
                status=status.HTTP_404_NOT_FOUND
            )

        scores = ResumeScore.objects.filter(
            job_description_id=job_id
        ).select_related("resume").order_by("-score")

        data = [
            {
                "rank": idx + 1,
                "resume_id": score.resume.id,
                "resume_name": score.resume.resume.name.split("/")[-1],
                "score": score.score,
                # created_at lives on ResumeScore (exists) not Resume (doesn't)
                "submitted_at": score.created_at.strftime("%Y-%m-%d %H:%M"),
            }
            for idx, score in enumerate(scores)
        ]

        return Response(
            {
                "job_id": job_id,
                "total": len(data),
                "rankings": data,
            }
        )


# def home(request):
#     return render(request, "resumechecker/index.html")

def home(request):
    return HttpResponse("Working ✅")
