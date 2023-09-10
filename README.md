# Speech to text server

## Описание

Сервер получает POST запрос, содержащий *.wav файл и отвечает текстом в формате JSON, содержащим распознанную речь пользователя.

Программа ffmpeg конвертирует аудио в подходящий битрейт и сэмплрейт.

Программа whisper.cpp осуществляет инференс нейросети Whisper от OpenAI, на центральном процессоре, с целью распознавания голоса.

## Установка

Сервер требует установленного ПО ffmpeg. Программа доступна по ссылке: https://ffmpeg.org/download.html
После завершения установки, необходимо добавить путь к нему в переменную среды PATH

Так-же для работы сервера требуется ПО Whisper.cpp
Для его установки, выполните следующие инструкции:
```
git clone https://github.com/ggerganov/whisper.cpp
cd whisper.cpp
mkdir build && cd build
cmake ..
cmake --build . --config Release
```
В директории ```whisper.cpp/build/bin``` будет доступен исполняемый файл main (или main.exe), который необходимо скопировать в директорию сервера (содержащую файл main.py)

Так-же необходимо скачать предобученную модель "small" в формате ggml, она доступна по ссылке:
https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.bin
и поместить её так-же в директорию сервера (содержащую файл main.py)

итоговая структура файлов:
```
+-server/
|
+---main.py
+---main
+---ggml-small.bin
+---README.md
```

## Запуск

```
python3 ./main.py
```

## Тест

```
curl --data-binary @myVoice.wav http://localhost:5334/
```
