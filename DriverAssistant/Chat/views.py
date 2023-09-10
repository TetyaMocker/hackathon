import json
import requests
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

import pyaudio
import wave

from Authorization.models import UserFlag
from urllib.parse import quote


def update_flag(request):
    user_flag = UserFlag.objects.get(user=request.user)
    user_flag.user = request.user
    user_flag.flag = 'False'
    user_flag.save()
    return JsonResponse('Запись завершена и сохранена в файле recorded.wav', safe=False)


def record_view(request):
    params = json.loads(request.body)

    user_flag = UserFlag.objects.get(user=request.user)

    user_flag.user = request.user
    user_flag.flag = params['flag']

    user_flag.save()

    filename = 'static/wav/recorded.wav'

    speech2text, response_answer = record_audio(filename, request)

    return JsonResponse({'speech2text': speech2text, 'response_answer': response_answer}, safe=False)


def record_audio(filename, request):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    frames = []

    while UserFlag.objects.get(user=request.user).flag:
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    url = 'http://31.200.229.112:5334/'

    speech2text = ""

    try:
        with open(filename, 'rb') as file:
            response = requests.post(url, data=file)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return JsonResponse(e, safe=False)

    result = response.content.decode("UTF8")
    result = json.loads(result)

    for text in result["transcription"]:
        speech2text += text["text"]

    # Текстовой ответ Зины
    encoded_query = quote(speech2text, safe='')

    url = f'http://31.200.229.112:8990/?q={encoded_query}'

    response = requests.get(url)
    response.raise_for_status()
    response_answer = response.content.decode('UTF8')

    # Голосовой ответ Зины
    file_url = 'http://31.200.229.112:3333/test.wav'

    file_name = 'static/wav/recorded_answer.wav'

    response = requests.get(file_url)

    if response.status_code == 200:

        with open(file_name, 'wb') as file:
            file.write(response.content)
    else:
        print(f'Ошибка при скачивании файла. Код статуса: {response.status_code}')

    return speech2text, response_answer


@csrf_exempt
def add_message(request):
    if request.method == 'POST':

        params = json.loads(request.body)

        url = f'http://31.200.229.112:8990/?q={params["message"]}'

        response = requests.get(url)
        response.raise_for_status()
        response_answer = response.content.decode('UTF8')

        # Голосовой ответ Зины
        file_url = 'http://31.200.229.112:3333/test.wav'

        file_name = 'static/wav/recorded_answer.wav'

        response = requests.get(file_url)

        if response.status_code == 200:
            with open(file_name, 'wb') as file:
                file.write(response.content)
        else:
            return JsonResponse(response.status_code)

        return JsonResponse(response_answer, safe=False)

    else:
        pass


def chat_generator(request):
    return render(request, 'Chat/Chat.html')
