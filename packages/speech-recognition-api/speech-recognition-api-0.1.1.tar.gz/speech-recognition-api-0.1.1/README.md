[![PyPI - Version](https://img.shields.io/pypi/v/speech-recognition-api?color=%2300CD00)](https://pypi.org/project/speech-recognition-api/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/speech-recognition-api)](https://pypi.org/project/speech-recognition-api/)
[![PyPI - License](https://img.shields.io/pypi/l/speech-recognition-api)](https://pypi.org/project/speech-recognition-api/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/speech-recognition-api)](https://pypi.org/project/speech-recognition-api/)
[![codecov](https://codecov.io/gh/asai95/speech-recognition-api/branch/master/graph/badge.svg)](https://codecov.io/gh/asai95/speech-recognition-api)

## Speech Recognition API

Simple but extensible API for Speech Recognition.

### Installation

From pip:
```bash
pip install speech_recognition_api[all]
```

From git:
```bash
git clone https://github.com/asai95/speech-recognition-api.git
pip install -r requirements.txt
```

### Usage
Simple dev server:
```bash
python -m speech_recognition_api
```

Gunicorn:
```bash
gunicorn "speech_recognition_api:create_app()" -k uvicorn.workers.UvicornWorker -w 1 -b 127.0.0.1:8888
```

Celery worker:
```bash
celery -A speech_recognition_api.extra.celery_bus worker
```

Huey worker:
```bash
huey_consumer speech_recognition_api.extra.huey_bus.huey
```

### Description

This project is aimed to simplify building and deploying of applications that require
Speech Recognition functionality.

It is designed to work as a microservice, so it does not handle stuff like auth and rate limits.

However, it is also designed to be extensible in 3 major areas:

* Models
* File Storages
* Message Busses

There are two types of APIs available.

### Synchronous API

This API is designed for simple workloads, where the machine that runs the server is capable of
running a model. You probably want to limit the payload size for these routes.

**Routes:**

`POST /sync/v1/transcribe`

Accepts an audio file. File type depends on the model that is being used.

Returns an object with transcription.
[Response model](speech_recognition_api/core/sync_api/dto.py).


### Asynchronous API

This API is designed to process files asynchronously, i.e. to create tasks and process them
on separate workers. Typical client flow here is as follows:

* Create a task and receive task id
* Use this task id to periodically check if it is completed.

**Routes:**

`POST /async/v1/transcribe`

Accepts an audio file. File type depends on the model that is being used.

Returns an object with async task id.
[Response model](speech_recognition_api/core/async_api/dto.py).

`GET /async/v1/transcribe/{task_id}`

Returns an object with status and a transcription (if transcription is available).
[Response model](speech_recognition_api/core/async_api/dto.py).

Async API also requires a worker to run the actual work.

### Configuring

Configuration is done by .env file or env variables (they take preference).

The main variables required for the API and worker to run are:

* `MODEL` - model class path (it will do the actual audio-to-text conversion)
* `STORAGE` - storage class path (in Async API it will be responsible for uploading/downloading files)
* `MESSAGE_BUS` - message bus class path (in Async API it will be responsible for sending tasks to
remoted workers and getting the result back from them)

These classes will be imported only when used for the fist time.

Each class may require its own variables. Please refer to config.py of the specific module
to get the config reference.

Built-in classes:

Models:
* [Whisper](speech_recognition_api/extra/whisper_model/whisper_model.py)

Storages:
* [Local file system](speech_recognition_api/extra/local_storage/local_storage.py)
* [Amazon S3](speech_recognition_api/extra/s3_storage/s3_storage.py)
* [Google Cloud Storage](speech_recognition_api/extra/google_cloud_storage/google_cloud_storage.py)

Message Busses:
* [Celery](speech_recognition_api/extra/celery_bus/celery_bus.py)
* [Huey](speech_recognition_api/extra/huey_bus/huey_bus.py)

### Extending

It is easy to extend the API by adding models, storages and message busses.

To do that, one can just create a class that implements an interface:
* [Model](speech_recognition_api/core/common/model/interface.py)
* [Storage](speech_recognition_api/core/async_api/file_storage/interface.py)
* [Message Bus](speech_recognition_api/core/async_api/message_bus/interface.py)

Then just add a path to the class to the config file and that's it!

I suggest to distribute new modules through PyPI, so other people could reuse them.
