from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import Course, StudentCourse
from django.http import JsonResponse

@api_view(['POST'])
def add_course(request):
    data = request.data
    course = Course.objects.create(
        name=data['name'],
        instructor=data['instructor'],
        category=data['category'],
        schedule=data['schedule']
    )
    return Response(
        {'message': 'Course added successfully', 'id': course.id},
        status=status.HTTP_201_CREATED
    )

@api_view(['PUT'])
def update_course(request, course_id):
    course = Course.objects.get(id=course_id)

    data = request.data
    course.name = data.get('name', course.name)
    course.instructor = data.get('instructor', course.instructor)
    course.category = data.get('category', course.category)
    course.schedule = data.get('schedule', course.schedule)
    course.save()

    return Response({'message': 'Course updated successfully'}, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_course(request, course_id):
    course = Course.objects.get(id=course_id)
    course.delete()
    return Response({'message': 'Course deleted successfully'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def list_courses(request):
    courses = Course.objects.all().values()
    return Response(list(courses), status=status.HTTP_200_OK)

@api_view(['GET'])
def search_courses(request):
    query = request.GET.get('q', '')
    courses = Course.objects.filter(
        Q(name__icontains=query) |
        Q(instructor__icontains=query) |
        Q(category__icontains=query)
    ).values()
    return Response(list(courses), status=status.HTTP_200_OK)

@api_view(['POST'])
def associate_student(request):
    data = request.data
    student_id = data['student_id']
    course_id = data['course_id']

    course = Course.objects.get(id=course_id)
    StudentCourse.objects.create(student_id=student_id, course=course)

    return Response({'message': 'Student associated successfully'}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_courses_by_student(request, student_id):
    student_courses = StudentCourse.objects.filter(student_id=student_id)
    courses = [
        {
            "id": sc.course.id,
            "name": sc.course.name,
            "instructor": sc.course.instructor,
            "category": sc.course.category,
            "schedule": sc.course.schedule
        }
        for sc in student_courses
    ]
    return JsonResponse(courses, safe=False)

# views.py (AJOUTER À LA FIN DU FICHIER)

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import StudentCourse # Assurez-vous que StudentCourse est importé


@api_view(['DELETE'])
def disassociate_all_student_courses(request, student_id):
    """
    Supprime toutes les associations de cours (StudentCourse) pour un étudiant donné.
    Ceci corrige la désélection.
    """
    try:
        # Supprime tous les enregistrements StudentCourse pour cet étudiant
        deleted_count, _ = StudentCourse.objects.filter(student_id=student_id).delete()
        
        # Le code d'état HTTP 204 No Content est approprié ici pour une suppression réussie
        return Response({'message': f'{deleted_count} cours désassociés avec succès.'}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        # En cas d'erreur
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)