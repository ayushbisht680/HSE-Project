# from rest_framework.response import Response
# from rest_framework import status
# from functools import wraps
# from .models import HSE

# def check_hse_form_status(view_func):
#     @wraps(view_func)

#     def _wrapped_view(self,request, *args, **kwargs):
#         data=self.request.data
#         week_number = data.get("week_number")
#         year = data.get("year")
#         hse = HSE.objects.filter(week_number=week_number, year=year).first()

#         if hse and hse.form_status == 1:
#             return Response('Form already submitted', status=status.HTTP_400_BAD_REQUEST)
#         return view_func(request, *args, **kwargs)
    
#     return _wrapped_view
