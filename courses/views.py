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



@api_view(['DELETE'])
def delete_student_course_association(request, student_id, course_id):
    
    try:
        
        association = StudentCourse.objects.get(student_id=student_id, course_id=course_id)
        association.delete()
        
        return Response({'message': 'Association supprimée avec succès'}, status=status.HTTP_204_NO_CONTENT)
    except StudentCourse.DoesNotExist:
        return Response({'message': 'Association non trouvée'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)