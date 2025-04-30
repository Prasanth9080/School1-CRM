from .models import AcademicSession, AcademicTerm


class SiteWideConfigs:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_session = AcademicSession.objects.get(current=True)
        current_term = AcademicTerm.objects.get(current=True)

        request.current_session = current_session
        request.current_term = current_term

        response = self.get_response(request)

        return response




#### new code ####
# from .models import AcademicSession, AcademicTerm

# class SiteWideConfigs:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         try:
#             current_session = AcademicSession.objects.get(current=True)
#         except AcademicSession.DoesNotExist:
#             current_session = None

#         try:
#             current_term = AcademicTerm.objects.get(current=True)
#         except AcademicTerm.DoesNotExist:
#             current_term = None

#         request.current_session = current_session
#         request.current_term = current_term

#         response = self.get_response(request)
#         return response





##################

# from .models import AcademicSession, AcademicTerm

# class SiteWideConfigs:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         from django.core.exceptions import ObjectDoesNotExist

#         # Safely get current session
#         try:
#             current_session = AcademicSession.objects.get(current=True)
#         except ObjectDoesNotExist:
#             current_session = None

#         # Safely get current term
#         try:
#             current_term = AcademicTerm.objects.get(current=True)
#         except ObjectDoesNotExist:
#             current_term = None

#         request.current_session = current_session
#         request.current_term = current_term

#         return self.get_response(request)
