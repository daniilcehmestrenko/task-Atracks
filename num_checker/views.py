from django.shortcuts import render

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .tasks import register_files
from .forms import NumberForm
from .serializers import RegistrySerializer
from .models import Registry


def check_number(request):
    mess = ''
    if request.method == 'POST':
        form = NumberForm(request.POST)

        if form.is_valid():
            number = form.cleaned_data['number']
            
            if not number.isdigit():
                mess = 'Используйте цифры'

                return render(request, 'num_checker/number_form.html', {'form': form, 'mess': mess})

            num_code = int(number[1:4])
            num_body = int(number[4:])

            registry_obj = Registry.objects.filter(
                code=num_code,
                range_from__lte=num_body,
                range_to__gte=num_body,
            ).first()

            if registry_obj is None:
                mess = 'Номер не найден'
            else:
                mess = f'Номер - {number}\n \
                        Оператор - {registry_obj.operator}\n \
                        Регион - {registry_obj.region}'
    else:
        form = NumberForm()
        mess = 'Формат номера 7XXXXXXXXXX'

    return render(request, 'num_checker/number_form.html', {'form': form, 'mess': mess})


class GetInfoNumberAPIView(APIView):
    def post(self, request: Request):
        number = request.data.get('number')

        if number is None:
            return Response({'mess': 'number не указан'})

        if len(number) != 11:
            return Response({'mess': 'неправильный формат номера'})

        number = number if type(number) == str else str(number)
        num_code = int(number[1:4])
        num_body = int(number[4:])

        registry_obj = Registry.objects.filter(
            code=num_code,
            range_from__lte=num_body,
            range_to__gte=num_body,
        ).first()

        if registry_obj is None:
            return Response({'mess': 'Номер не найден'})

        serializer = RegistrySerializer(registry_obj)
        data = serializer.data

        return Response({
            'operator': data['operator'],
            'region': data['region']
        })


class StartDatabaseFilling(APIView):
    def get(self, request: Request):
        register_files.delay()

        return Response({'mess': 'tasks is running'})
