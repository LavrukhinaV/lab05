# Лабораторная работа № 5

**Автор:** *Лаврухина Виктория*

--- 
## Цель лабораторной работы
Данная лабораторная работа посвещена изучению Docker и как с ним работать. Эта лабораторная работа послужит подпоркой для старта в выявлении и определении уязвимостей на уровне сканирования контейнеров при сборке приложений.

---

### Структура репозитория лабораторной работы
```
lab05
├── client
│   ├── client.py
│   ├── Dockerfile
│   └── requirements.txt
├── docker-compose.yml
├── README.md
├── server
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
└── source
    ├── Dockerfile
    ├── app.py
    ├── image.tar
    └── requirements.txt
```
---

### Задания

- ✔ 1. Поставьте `Docker` и `buildkit`

```bash
$ brew install buildkit
$ brew install docker
```

- ✔ 2. Перейдите в `source` и выведите на терминале, далее проанализируйте следующие команды консоли

```bash
$ docker buildx build -t hellow-appsec-world .
$ docker run hello-appsec-world
$ docker run --rm -it hello-appsec-world

$ docker save -o hello.tar hello-appsec-world
$ docker load -i hello.tar
$ docker load -i image.tar
```
- ✔ 3. Откройте `Dockerfile` и сделайте его анализ. Сделайте `commit`
- ✔ 4. Замените в `Dockerfile`значение скрипта на `python` тем, который вы сделали ранее в прошлых лабораторных работах. Вложите свой файл `python` в директорию. Сделайте анализ своего измененного `Dockerfile` и внесите изменения. Сделайте `commit`. 

> Пример анализа по текущему `Dockerfile` в репозитории

```dockerfile
# Этап 1: сборка зависимостей
FROM python:3.11-slim AS builder
WORKDIR /hello
# Копируем файл с зависимостями
COPY requirements.txt . 
# Устанавливаем зависимости в отдельную директорию wheelhouse для кеширования
RUN pip install --upgrade pip && pip wheel --wheel-dir=/wheels -r requirements.txt

# Этап 2: запускаемый образ
FROM python:3.11-slim
WORKDIR /hello
# Копируем файл с зависимостями
COPY --from=builder /wheels /wheels # Копируем собранные wheel-пакеты
COPY requirements.txt . 
# Устанавливаем зависимости из wheel-пакетов
RUN pip install --no-index --find-links=/wheels -r requirements.txt
# Копируем исходный код приложения
COPY hello.py .

# Переменные окружения для улучшенной работы Python
ENV PYTHONUNBUFFERED=1
# Запускаем приложение
CMD ["python", "hello.py"] 
```

- ✔ 5. Выведите на терминале и проанализируйте следующие команды консоли. Сравните хеш сумму вашего архива с `image.tar` из репозитория, выведите на терминал.

```bash
$ docker buildx build -t hellow-appsec-world .
$ docker run hello-appsec-world
$ docker save -o hello_ypur_project.tar hello-appsec-world

$ docker load -i hello_ypur_project.tar
$ docker run hello-appsec-world

$ docker load -i image.tar
$ docker run hello-appsec-world
```

- ✔ 6. Доработайте свой `python` скрипт подключаемыми библиотеками, далее их необходимо разместить в `requirements.txt`. Размещение библиотек в следующем формате:

```
flask==2.2.3
requests==2.28.1
```

- ✔ 7. Сделайте `commit`. Повторите сборку приложения по вашему `Dockerfile` для доработанного скрипта `python`. Сохраните `image` в виде .`tar` архива. Сделайте `commit`.
- ✔ 8. Выведите на терминале и проанализируйте следующие команды консоли

```bash
$ docker login
$ docker tag hello-appsec-world yourusername/hello-appsec-world
$ docker push yourusername/hello-appsec-world
$ docker inspect yourusername/hello-appsec-world
$ docker container create --name first hello-appsec-world # выпишите id контейнера

$ docker image pull geminishkv/hello-appsec-world
$ docker inspect geminishkvdev/hello-appsec-world
$ docker container create --name second hello-appsec-world

``` 

- ✔ 9. Выведите на терминале и проанализируйте в консоли процессы, которые запущены, владельцев по пользователям

```bash 
 $ docker container run -it ubuntu /bin/bash
``` 
 
- ✔ 10. Выведите оба контейнера first и second на терминал
- ✔ 11. Перейдите в основной корень `lab05` и выведите на терминале, и проанализируйте

```bash 
$ docker-compose up --build
``` 

- ✔ 12. Откройте соседнее окно терминала и и выведите на терминале

```bash 
$ open -a "Google Chrome" http://localhost:8000
```

- ✔ 13. Остановите работу `docker-compose`.

```bash 
$ docker ps -a
$ docker ps -q
$ docker images

$ docker ps -q | xargs docker stop
$ docker-compose down
```
- ✔ 14. Доработайте `docker-compose` и скрипт, который вы подготовили ранее, что бы вы смогли воспроизвести шаги п.11 по п.13 с демонстрацией. Сделайте `commit`.
- ✔ 15. Залейте изменения в свой удаленный репозиторий, проверьте историю `commit`.
- ✔ 16. Подготовьте отчет `gist`.

---

### Подготовительный этап (перед выполнением)

1. Создать директорию проекта и зайти в нее:
```
mkdir lab05
cd lab05
```

2. Инициализировать git и сделать первый коммит:
```
git init
echo "# lab05" > README.md
git add .
git commit -m "Initial commit"

```

3. Создать и переключиться на ветку dev
```
git checkout -b dev
```

4. Создать удалённый репозиторий на GitHub и привязать origin
```
gh repo create lab05 --private --source=. --remote=origin --push
```
---

### Процесс выполнения заданий
- ✔ 1. Поставьте `Docker` и `buildkit`
```bash
docker version # Проверка корректности установки docker
Client:
 Version:           28.0.1
 API version:       1.48
 Go version:        go1.23.6
 Git commit:        068a01e
 Built:             Wed Feb 26 10:38:16 2025
 OS/Arch:           darwin/arm64
 Context:           desktop-linux

Server: Docker Desktop 4.39.0 (184744)
 Engine:
  Version:          28.0.1
  API version:      1.48 (minimum version 1.24)
  Go version:       go1.23.6
  Git commit:       bbd0a17
  Built:            Wed Feb 26 10:40:57 2025
  OS/Arch:          linux/arm64
  Experimental:     false
 containerd:
  Version:          1.7.25
  GitCommit:        bcc810d6b9066471b0b6fa75f557a15a1cbf31bb
 runc:
  Version:          1.2.4
  GitCommit:        v1.2.4-0-g6c52b3f
 docker-init:
  Version:          0.19.0
  GitCommit:        de40ad0
```
```bash
buildkit version # Проверка корректности установки buildkit
buildctl github.com/moby/buildkit 0.26.2 be1f38efe73c6a93cc429a0488ad6e1db663398c
```
- ✔ 2. Перейдите в `source` и выведите на терминале, далее проанализируйте следующие команды консоли
```bash
cd source # Переход в каталог
docker buildx build -t hello-appsec-world . # Сборка Docker-образа с использованием buildx
[+] Building 13.0s (13/13) FINISHED                                                                                                           docker:desktop-linux
 => [internal] load build definition from Dockerfile                                                                                                          0.0s
 => => transferring dockerfile: 465B                                                                                                                          0.0s
 => [internal] load metadata for docker.io/library/python:3.11-slim                                                                                           4.4s
 => [internal] load .dockerignore                                                                                                                             0.0s
 => => transferring context: 2B                                                                                                                               0.0s
 => [internal] load build context                                                                                                                             0.0s
 => => transferring context: 550B                                                                                                                             0.0s
 => CACHED [builder 1/4] FROM docker.io/library/python:3.11-slim@sha256:158caf0e080e2cd74ef2879ed3c4e697792ee65251c8208b7afb56683c32ea6c                      0.0s
 => => resolve docker.io/library/python:3.11-slim@sha256:158caf0e080e2cd74ef2879ed3c4e697792ee65251c8208b7afb56683c32ea6c                                     0.0s
 => [builder 2/4] WORKDIR /hello                                                                                                                              0.0s
 => [builder 3/4] COPY requirements.txt .                                                                                                                     0.0s
 => [builder 4/4] RUN pip install --upgrade pip && pip wheel --wheel-dir=/wheels -r requirements.txt                                                          7.7s
 => [stage-1 3/6] COPY --from=builder /wheels /wheels                                                                                                         0.0s 
 => [stage-1 4/6] COPY requirements.txt .                                                                                                                     0.0s 
 => [stage-1 5/6] RUN pip install --no-index --find-links=/wheels -r requirements.txt                                                                         0.7s 
 => [stage-1 6/6] COPY hello.py .                                                                                                                             0.0s 
 => exporting to image                                                                                                                                        0.0s 
 => => exporting layers                                                                                                                                       0.0s 
 => => writing image sha256:2a0cbbc6c34e3dccc94ff5bc7f86c0ef543869817243ba88d66e385dcb694650                                                                  0.0s
 => => naming to docker.io/library/hello-appsec-world                                                                                                         0.0s

View build details: docker-desktop://dashboard/build/desktop-linux/desktop-linux/lpdatptjyefkmm5n7l0u18v27

What's next:
    View a summary of image vulnerabilities and recommendations → docker scout quickview 

docker run hello-appsec-world # Запуск контейнера
hello appsec world

docker run --rm -it hello-appsec-world # Интерактивный запуск контейнера с автоудалением
hello appsec world

docker save -o hello.tar hello-appsec-world # Экспорт Docker-образа в файл

docker load -i hello.tar # Импорт Docker-образа из файла
Loaded image: hello-appsec-world:latest

docker load -i image.tar # Загрузка образа из подготовленного архива
Loaded image: hello-appsec-world:latest
```
- ✔ 3. Откройте `Dockerfile` и сделайте его анализ. Сделайте `commit`
```bash
git add Dockerfile
git commit -m "Analyze Dockerfile: multi-stage build, dependency handling, AppSec risks"
```
- ✔ 4. Замените в `Dockerfile`значение скрипта на `python` тем, который вы сделали ранее в прошлых лабораторных работах. Вложите свой файл `python` в директорию. Сделайте анализ своего измененного `Dockerfile` и внесите изменения. Сделайте `commit`. 
- Используется двухстадийная сборка:
  - `builder`: устанавливает зависимости и собирает wheel-пакеты в `/wheels`.
  - `runner`: устанавливает зависимости из локального каталога wheels (`--no-index`), что снижает зависимость от сети на финальном этапе.
- Заменён целевой скрипт контейнера с `hello.py` на `app.py` (скрипт из предыдущей лабораторной работы №1).
- В `CMD` добавлены аргументы для Typer CLI, чтобы контейнер выполнялся без интерактивного ввода и завершался корректно.
- В `requirements.txt` добавлена библиотека `typer` как зависимость скрипта.
```bash
docker buildx build -t hello-appsec-world . # Проверка сборки и запуска
docker run --rm hello-appsec-world
[+] Building 42.2s (13/13) FINISHED                                                                                                           docker:desktop-linux
 => [internal] load build definition from Dockerfile                                                                                                          0.0s
 => => transferring dockerfile: 1.20kB                                                                                                                        0.0s
 => [internal] load metadata for docker.io/library/python:3.11-slim                                                                                          10.4s
 => [internal] load .dockerignore                                                                                                                             0.0s
 => => transferring context: 2B                                                                                                                               0.0s
 => [internal] load build context                                                                                                                             0.0s
 => => transferring context: 723B                                                                                                                             0.0s
 => [builder 1/4] FROM docker.io/library/python:3.11-slim@sha256:158caf0e080e2cd74ef2879ed3c4e697792ee65251c8208b7afb56683c32ea6c                             0.0s
 => => resolve docker.io/library/python:3.11-slim@sha256:158caf0e080e2cd74ef2879ed3c4e697792ee65251c8208b7afb56683c32ea6c                                     0.0s
 => CACHED [builder 2/4] WORKDIR /hello                                                                                                                       0.0s
 => [builder 3/4] COPY requirements.txt .                                                                                                                     0.0s
 => [builder 4/4] RUN pip install --upgrade pip && pip wheel --wheel-dir=/wheels -r requirements.txt                                                         30.5s
 => [stage-1 3/6] COPY --from=builder /wheels /wheels                                                                                                         0.0s
 => [stage-1 4/6] COPY requirements.txt .                                                                                                                     0.0s
 => [stage-1 5/6] RUN pip install --no-index --find-links=/wheels -r requirements.txt                                                                         1.2s
 => [stage-1 6/6] COPY app.py .                                                                                                                               0.0s 
 => exporting to image                                                                                                                                        0.1s 
 => => exporting layers                                                                                                                                       0.1s 
 => => writing image sha256:9f761dcb111c90325f02d3eddf951a5cb0478039bbd2ab44c2e2ac29c670051c                                                                  0.0s
 => => naming to docker.io/library/hello-appsec-world                                                                                                         0.0s 
                                                                                                                                                                   
View build details: docker-desktop://dashboard/build/desktop-linux/desktop-linux/ojnyruyvtbglvv213pc1g1qkk

What's next:
    View a summary of image vulnerabilities and recommendations → docker scout quickview 
Добрый день, Viktoriia Lavrukhina!

```

- ✔ 5. Выведите на терминале и проанализируйте следующие команды консоли. Сравните хеш сумму вашего архива с `image.tar` из репозитория, выведите на терминал.

```bash
docker buildx build -t hello-appsec-world . # Сборка образа
docker run --rm hello-appsec-world # запуск образа
[+] Building 17.2s (13/13) FINISHED                                                                                                           docker:desktop-linux
 => [internal] load build definition from Dockerfile                                                                                                          0.0s
 => => transferring dockerfile: 1.20kB                                                                                                                        0.0s
 => [internal] load metadata for docker.io/library/python:3.11-slim                                                                                          17.1s
 => [internal] load .dockerignore                                                                                                                             0.0s
 => => transferring context: 2B                                                                                                                               0.0s
 => [internal] load build context                                                                                                                             0.0s
 => => transferring context: 137B                                                                                                                             0.0s
 => [builder 1/4] FROM docker.io/library/python:3.11-slim@sha256:158caf0e080e2cd74ef2879ed3c4e697792ee65251c8208b7afb56683c32ea6c                             0.0s
 => => resolve docker.io/library/python:3.11-slim@sha256:158caf0e080e2cd74ef2879ed3c4e697792ee65251c8208b7afb56683c32ea6c                                     0.0s
 => CACHED [builder 2/4] WORKDIR /hello                                                                                                                       0.0s
 => CACHED [builder 3/4] COPY requirements.txt .                                                                                                              0.0s
 => CACHED [builder 4/4] RUN pip install --upgrade pip && pip wheel --wheel-dir=/wheels -r requirements.txt                                                   0.0s
 => CACHED [stage-1 3/6] COPY --from=builder /wheels /wheels                                                                                                  0.0s
 => CACHED [stage-1 4/6] COPY requirements.txt .                                                                                                              0.0s
 => CACHED [stage-1 5/6] RUN pip install --no-index --find-links=/wheels -r requirements.txt                                                                  0.0s
 => CACHED [stage-1 6/6] COPY app.py .                                                                                                                        0.0s
 => exporting to image                                                                                                                                        0.0s
 => => exporting layers                                                                                                                                       0.0s
 => => writing image sha256:9f761dcb111c90325f02d3eddf951a5cb0478039bbd2ab44c2e2ac29c670051c                                                                  0.0s
 => => naming to docker.io/library/hello-appsec-world                                                                                                         0.0s

View build details: docker-desktop://dashboard/build/desktop-linux/desktop-linux/rl9bxs94bjoyvkujchonbtchc

What's next:
    View a summary of image vulnerabilities and recommendations → docker scout quickview 
Добрый день, Viktoriia Lavrukhina!
```
```bash
docker save -o hello_your_project.tar hello-appsec-world # Сохранить образ в tar и посчитать хеш
ls -lh hello_your_project.tar
shasum -a 256 hello_your_project.tar
-rw-------@ 1 aleksandrlavruhin  staff   173M Dec 13 17:13 hello_your_project.tar
136372f55188544eec8d5db86c86241f6acd9b36a5085d49ba998ba7c97d219a  hello_your_project.tar
```
```bash
docker load -i hello_your_project.tar # Загрузить tar обратно и снова запустить
docker run --rm hello-appsec-world

Loaded image: hello-appsec-world:latest
Loaded image: hello-appsec-world:mine
Добрый день, Viktoriia Lavrukhina!
```
```bash
docker load -i image.tar # Запуск образа из image.tar
docker run --rm hello-appsec-world

Loaded image: hello-appsec-world:latest
hello appsec world
```
При загрузке `image.tar` Docker обнаружил, что тег `hello-appsec-world:latest` уже существует локально, поэтому:

* переназначил тег `hello-appsec-world:latest` на образ из `image.tar`;

* предыдущий локальный `образ стал dangling`, но сохранил свой `IMAGE ID`.
```bash
docker image ls --no-trunc | grep 9f761dcb111c # Возврат тега и запуск “моей” версии образа
docker tag 9f761dcb111c90325f02d3eddf951a5cb0478039bbd2ab44c2e2ac29c670051c hello-appsec-world:mine
docker run --rm hello-appsec-world:mine

hello-appsec-world             mine          sha256:9f761dcb111c90325f02d3eddf951a5cb0478039bbd2ab44c2e2ac29c670051c   17 minutes ago   175MB
Добрый день, Viktoriia Lavrukhina!
```
**Вывод сравнения**
* hello-appsec-world:latest (после docker load -i image.tar) — это образ из репозитория, вывод: *hello appsec world*
* hello-appsec-world:mine — моя локальная версия (Typer CLI), вывод: *Добрый день, Viktoriia Lavrukhina!*
- ✔ 6. Доработайте свой python скрипт подключаемыми библиотеками, далее их необходимо разместить в requirements.txt.
В рамках задания Python-скрипт был доработан с использованием подключаемых библиотек:

	- `requests` — для выполнения HTTP-запросов к внешним ресурсам;
	- `flask` — для демонстрации работы приложения в режиме сетевого сервиса;
	- `typer` — для организации CLI-интерфейса управления.

	Зависимости были зафиксированы по версиям в `requirements.txt`, что обеспечивает:
	- воспроизводимость сборки контейнера;
	- снижение риска использования уязвимых или несовместимых версий библиотек;
	- соответствие практикам безопасной контейнеризации.

	Доработанный скрипт поддерживает:
	- CLI-режим (вывод приветствия, HTTP-запросы);
	- сервисный режим (запуск Flask-приложения на порту 8000).
```bash
docker buildx build --no-cache -t hello-appsec-world . # собрать образ
docker run --rm -p 8000:8000 hello-appsec-world python app.py serve # Запуск сервиса Flask

open http://localhost:8000 # в новом терминале, вывод "Hello AppSec World from Flask!
"
```
```bash
git add source/app.py source/requirements.txt
git commit -m "lab05: extend python script with flask and requests dependencies"
```
- ✔ 7. Повторите сборку приложения по вашему Dockerfile для доработанного скрипта python. Сохраните image в виде .tar архива. Сделайте commit.
```bash
docker buildx build --no-cache -t hello-appsec-world . # сборка образа по Dockerfile
[+] Building 17.3s (13/13) FINISHED                                                                                                           docker:desktop-linux
 => [internal] load build definition from Dockerfile                                                                                                          0.0s
 => => transferring dockerfile: 1.20kB                                                                                                                        0.0s
 => [internal] load metadata for docker.io/library/python:3.11-slim                                                                                           2.3s
 => [internal] load .dockerignore                                                                                                                             0.0s
 => => transferring context: 2B                                                                                                                               0.0s
 => [internal] load build context                                                                                                                             0.0s
 => => transferring context: 137B                                                                                                                             0.0s
 => [builder 1/4] FROM docker.io/library/python:3.11-slim@sha256:158caf0e080e2cd74ef2879ed3c4e697792ee65251c8208b7afb56683c32ea6c                             0.0s
 => => resolve docker.io/library/python:3.11-slim@sha256:158caf0e080e2cd74ef2879ed3c4e697792ee65251c8208b7afb56683c32ea6c                                     0.0s
 => CACHED [builder 2/4] WORKDIR /hello                                                                                                                       0.0s
 => [builder 3/4] COPY requirements.txt .                                                                                                                     0.0s
 => [builder 4/4] RUN pip install --upgrade pip && pip wheel --wheel-dir=/wheels -r requirements.txt                                                         13.7s
 => [stage-1 3/6] COPY --from=builder /wheels /wheels                                                                                                         0.0s
 => [stage-1 4/6] COPY requirements.txt .                                                                                                                     0.0s
 => [stage-1 5/6] RUN pip install --no-index --find-links=/wheels -r requirements.txt                                                                         1.1s 
 => [stage-1 6/6] COPY app.py .                                                                                                                               0.0s 
 => exporting to image                                                                                                                                        0.1s 
 => => exporting layers                                                                                                                                       0.1s 
 => => writing image sha256:925ba1f466f21167cd3e13f6056f7111e9adc0e4d3eab5c12a2206a7d386f3de                                                                  0.0s 
 => => naming to docker.io/library/hello-appsec-world                                                                                                         0.0s 
                                                                                                                                                                   
View build details: docker-desktop://dashboard/build/desktop-linux/desktop-linux/twse78kkt33a2mjh4kqszbsm0

What's next:
    View a summary of image vulnerabilities and recommendations → docker scout quickview 
```
```bash
docker run --rm hello-appsec-world python app.py greet --formal # запуск контейнера
Привет, Viktoriia!
```
```bash
docker save -o hello_my_project.tar hello-appsec-world # Сохранить image в .tar архив

ls -lh hello_my_project.tar
-rw-------@ 1 aleksandrlavruhin  staff   193M Dec 13 17:48 hello_my_project.tar
```
```bash
git status
git add Dockerfile app.py requirements.txt hello_my_project.tar
git commit -m "lab05: rebuild image with updated python app and dependencies"
```

- ✔ 8. Выведите на терминале и проанализируйте следующие команды консоли
```bash
docker login
Login Succeeded

docker tag hello-appsec-world:latest lavrukhinav/hello-appsec-world:latest # Тегирование локального образа под Docker Hub

docker push lavrukhinav/hello-appsec-world:latest # Публикация в Docker Hub
The push refers to repository [docker.io/lavrukhinav/hello-appsec-world]
212fda27693d: Pushed 
80fe9ac8c82f: Pushed 
bfc64f3d5421: Pushed 
9a44cf35ca5a: Pushed 
2fed644183cd: Pushed 
ccd7ffd0cc2b: Mounted from library/python 
4d7c3b3e69ba: Mounted from library/python 
631a84bae701: Mounted from library/python 
742b5304df6e: Mounted from library/python 
latest: digest: sha256:74be9d038a7940313a748b1e3eed1ead59e6ff052b8ec4d8a4ac72d5a6c4af8e size: 2201
```
```bash
docker inspect lavrukhinav/hello-appsec-world:latest # Inspect загруженного образа
[
    {
        "Id": "sha256:925ba1f466f21167cd3e13f6056f7111e9adc0e4d3eab5c12a2206a7d386f3de",
        "RepoTags": [
            "lavrukhinav/hello-appsec-world:latest",
            "hello-appsec-world:latest"
        ],
        "RepoDigests": [
            "lavrukhinav/hello-appsec-world@sha256:74be9d038a7940313a748b1e3eed1ead59e6ff052b8ec4d8a4ac72d5a6c4af8e"
        ],
        "Parent": "",
        "Comment": "buildkit.dockerfile.v0",
        "Created": "2025-12-13T14:43:48.093644208Z",
        "DockerVersion": "",
        "Author": "",
        "Config": {
            "Hostname": "",
            "Domainname": "",
            "User": "",
            "AttachStdin": false,
            "AttachStdout": false,
            "AttachStderr": false,
            "Tty": false,
            "OpenStdin": false,
            "StdinOnce": false,
            "Env": [
                "PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
                "LANG=C.UTF-8",
                "GPG_KEY=A035C8C19219BA821ECEA86B64E628F8D684696D",
                "PYTHON_VERSION=3.11.14",
                "PYTHON_SHA256=8d3ed8ec5c88c1c95f5e558612a725450d2452813ddad5e58fdb1a53b1209b78",
                "PYTHONUNBUFFERED=1"
            ],
            "Cmd": [
                "python",
                "app.py",
                "Viktoriia",
                "--lastname",
                "Lavrukhina",
                "--formal"
            ],
            "ArgsEscaped": true,
            "Image": "",
            "Volumes": null,
            "WorkingDir": "/hello",
            "Entrypoint": null,
            "OnBuild": null,
            "Labels": null
        },
        "Architecture": "arm64",
        "Variant": "v8",
        "Os": "linux",
        "Size": 170008151,
        "GraphDriver": {
            "Data": {
                "LowerDir": "/var/lib/docker/overlay2/s2t1klf5qdje4d2em4vxn1guv/diff:/var/lib/docker/overlay2/4zaw8cmyasefy7aytbzwkxyn4/diff:/var/lib/docker/overlay2/rdfzpoaywyxx98ycx7qcv58f9/diff:/var/lib/docker/overlay2/yom7a29qzwevxyxpu3nwq1o16/diff:/var/lib/docker/overlay2/abd632a24a12bbc1d0469865ca04cc1c1a69793fbb9bd893d6f51d303d90d001/diff:/var/lib/docker/overlay2/b22c47a7fe9bd8ce7e685f26a93d129a74e0e1aff1c0879d5d964f1ff965d0ec/diff:/var/lib/docker/overlay2/fb2d4bbf043524347864fb00c4d92c8013f611b4acfecbab92402dac7667a054/diff:/var/lib/docker/overlay2/946268b58df21da0420e9149266b7a9ba5773ac144644758528d451f429ee767/diff",
                "MergedDir": "/var/lib/docker/overlay2/n7h5much8r2vfqbtokbz0hjup/merged",
                "UpperDir": "/var/lib/docker/overlay2/n7h5much8r2vfqbtokbz0hjup/diff",
                "WorkDir": "/var/lib/docker/overlay2/n7h5much8r2vfqbtokbz0hjup/work"
            },
            "Name": "overlay2"
        },
        "RootFS": {
            "Type": "layers",
            "Layers": [
                "sha256:742b5304df6eda388fec80a0fc0a7a95d3e920e61c8d3b9dd32efb0fd8f4c3b7",
                "sha256:631a84bae7017d12a06a9de597f6da7bc5f72e5463d107c2faf54172e281ab17",
                "sha256:4d7c3b3e69ba2a537a08a850ee86b9f94f994d67e484b769b3f913bee9a544fc",
                "sha256:ccd7ffd0cc2be767994e1adb0f348841235c9232ac12604784150aceb2e5a590",
                "sha256:2fed644183cdda2499617817a1ddf71c4af3f35b04c7a7be19ca12251e6d2d28",
                "sha256:9a44cf35ca5a55e1a7c0c8d5c654b1300c027f5d5be55741df088d7d32c22220",
                "sha256:bfc64f3d5421d81c306b9be75d64177412f493834575519fcf9bc2bdae1626de",
                "sha256:80fe9ac8c82fd789dc35b0f4eb26b433e06934958f64f37be70bf7a94472b25a",
                "sha256:212fda27693d411438d63f0e7357b57ddb48dd22dd65decc7e97db881c0dd031"
            ]
        },
        "Metadata": {
            "LastTagTime": "2025-12-13T15:04:35.998792216Z"
        }
    }
]
```
```bash
docker container create --name first hello-appsec-world:latest # Создать контейнер first и выписать ID
682d2a2604ef3373e164ad767d91414287dff301502500de72598d003b5dc5b6
```
```bash
docker image pull geminishkvdev/hello-appsec-world:latest # Скачать образ автора

latest: Pulling from geminishkvdev/hello-appsec-world
b89cf3ec7a3e: Already exists 
89477b9ce6a6: Already exists 
158b441f91fd: Already exists 
44032d6d082a: Already exists 
73c6786ffe40: Pull complete 
602731d4ffe4: Pull complete 
9673dc38d14b: Pull complete 
460204959e1c: Pull complete 
61170947d8ae: Pull complete 
Digest: sha256:f9db3113962ac3bb47d0123dc8f16b2baa3a27fdef5db67b0d1bd0d6c7bdcdf2
Status: Downloaded newer image for geminishkvdev/hello-appsec-world:latest
docker.io/geminishkvdev/hello-appsec-world:latest
```
```bash
docker inspect geminishkvdev/hello-appsec-world
[
    {
        "Id": "sha256:f386bd63aa82e8393bdd081873b60fa5d8938ffb1b7f53bed6bbbd947358f847",
        "RepoTags": [
            "geminishkvdev/hello-appsec-world:latest"
        ],
        "RepoDigests": [
            "geminishkvdev/hello-appsec-world@sha256:f9db3113962ac3bb47d0123dc8f16b2baa3a27fdef5db67b0d1bd0d6c7bdcdf2"
        ],
        "Parent": "",
        "Comment": "buildkit.dockerfile.v0",
        "Created": "2025-11-21T13:46:41.586622834Z",
        "DockerVersion": "",
        "Author": "",
        "Config": {
            "Hostname": "",
            "Domainname": "",
            "User": "",
            "AttachStdin": false,
            "AttachStdout": false,
            "AttachStderr": false,
            "Tty": false,
            "OpenStdin": false,
            "StdinOnce": false,
            "Env": [
                "PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
                "LANG=C.UTF-8",
                "GPG_KEY=A035C8C19219BA821ECEA86B64E628F8D684696D",
                "PYTHON_VERSION=3.11.14",
                "PYTHON_SHA256=8d3ed8ec5c88c1c95f5e558612a725450d2452813ddad5e58fdb1a53b1209b78",
                "PYTHONUNBUFFERED=1"
            ],
            "Cmd": [
                "python",
                "hello.py"
            ],
            "ArgsEscaped": true,
            "Image": "",
            "Volumes": null,
            "WorkingDir": "/hello",
            "Entrypoint": null,
            "OnBuild": null,
            "Labels": null
        },
        "Architecture": "arm64",
        "Os": "linux",
        "Size": 160375439,
        "GraphDriver": {
            "Data": {
                "LowerDir": "/var/lib/docker/overlay2/01ca5f652b65128ef927c4fa0862fa585573b22bf44b1969114b29f66205181c/diff:/var/lib/docker/overlay2/90d4806d2bde214f217dfb1c06536e49e874f4ca5e750d56b2389030b5710c45/diff:/var/lib/docker/overlay2/2b866ecae64b7e309e9374cda1b9155a6db7a41ee23a716a4c1610db09fb316c/diff:/var/lib/docker/overlay2/c9848cea75ee7e2c9143ac7a35e1335c33840ab04758ae0ecab46bf67d067d78/diff:/var/lib/docker/overlay2/7a3f0e9325b7f1de2ca490b24ca9798bdc72360d5c693377afc985fa425b30e0/diff:/var/lib/docker/overlay2/0eb44a672c7dadcf5d61bc0bb53575ef6394b0872ef04f9e3257eddb3ebb192f/diff:/var/lib/docker/overlay2/398bdd040ec525683439dc1b326d08d9d3a72ffcd8157eaa3b368c2262304b50/diff:/var/lib/docker/overlay2/9a10a0b9d50331e4aaafe4fdba75e7ec400e8342afca2d73b7a3ecd63fd840b5/diff",
                "MergedDir": "/var/lib/docker/overlay2/de0e6c31c2a38d386d6e3adb3f4b549692e3b86843b1eb89e9110ce0c549ba87/merged",
                "UpperDir": "/var/lib/docker/overlay2/de0e6c31c2a38d386d6e3adb3f4b549692e3b86843b1eb89e9110ce0c549ba87/diff",
                "WorkDir": "/var/lib/docker/overlay2/de0e6c31c2a38d386d6e3adb3f4b549692e3b86843b1eb89e9110ce0c549ba87/work"
            },
            "Name": "overlay2"
        },
        "RootFS": {
            "Type": "layers",
            "Layers": [
                "sha256:f1b30ab9918326dc2f4c25f16c0e6c13e9a48427441ea41c0e4d8f3e6699da24",
                "sha256:c240010145420619581e4f7b7e4047e460c8555234e3e4db66f890a68e146f24",
                "sha256:7a4b2171e46dd80cd00f895405c44a867a96ab97e17b4e8c9651cc5e4f419369",
                "sha256:591779db32736fe4b356f6cecc88221a5fa8afa34cbced6e719e54584f63ef59",
                "sha256:efd49302dd30654a15a04a446a25ced6b712e90c6dd4e7791700e6cc57052500",
                "sha256:8fe7432c3de3dffd75d5c59ba9c0ab11f79fbafa983ee88df0ace1aa14d4a194",
                "sha256:e687a26fd0a6b3205299a590d71ae34d679adaaf2b653b0707449ebb676354b9",
                "sha256:71299f61dc2b0b021efdcf665174aae82972a5a8d32bc733c4e2fbc6f7c7a10f",
                "sha256:5b8b2e16a223e538a7cde134a8d2da34674bea14b95915fc1314cd8af5805608"
            ]
        },
        "Metadata": {
            "LastTagTime": "0001-01-01T00:00:00Z"
        }
    }
]
```
```bash
docker container create --name second hello-appsec-world # Создать контейнер second

79f455b42d034fd3cfe16f1960fa8b5862ad9ee2b50d8223fb939213fcfac492
source$ docker ps -a --filter "name=first|second"

CONTAINER ID   IMAGE                       COMMAND                  CREATED          STATUS    PORTS     NAMES
79f455b42d03   hello-appsec-world          "python app.py Vikto…"   14 seconds ago   Created             second
682d2a2604ef   hello-appsec-world:latest   "python app.py Vikto…"   5 minutes ago    Created             first
```

- ✔ 9. Выведите на терминале и проанализируйте в консоли процессы, которые запущены, владельцев по пользователям

```bash 
docker container run --rm -it ubuntu /bin/bash
 whoami
id
ps aux
ps -p 1 -o pid,user,comm,args
root
uid=0(root) gid=0(root) groups=0(root)
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.0   4296  3596 pts/0    Ss   15:19   0:00 /bin/bash
root        11  0.0  0.0   7628  3532 pts/0    R+   15:20   0:00 ps aux
  PID USER     COMMAND         COMMAND
    1 root     bash            /bin/bash
exit
``` 
- ✔ 10. Выведите оба контейнера first и second на терминал
```bash
docker ps -a # Вывод контейнеров first и second

CONTAINER ID   IMAGE                              COMMAND                  CREATED             STATUS                    PORTS                      NAMES
79f455b42d03   hello-appsec-world                 "python app.py Vikto…"   7 minutes ago       Created                                              second
682d2a2604ef   hello-appsec-world:latest          "python app.py Vikto…"   12 minutes ago      Created                                              first
```
- ✔ 11. Перейдите в основной корень `lab05` и выведите на терминале, и проанализируйте

```bash 
docker compose up --build

WARN[0000] /Users/aleksandrlavruhin/phystech/AppSec/lab05/docker-compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion 
Compose now can delegate build to bake for better performances
Just set COMPOSE_BAKE=true
[+] Building 21.1s (26/26) FINISHED                                                                                                           docker:desktop-linux
 => [server internal] load build definition from Dockerfile                                                                                                   0.0s
 => => transferring dockerfile: 456B                                                                                                                          0.0s
 => [client internal] load metadata for docker.io/library/python:3.11-slim                                                                                    2.4s
 => [server auth] library/python:pull token for registry-1.docker.io                                                                                          0.0s
 => [server internal] load .dockerignore                                                                                                                      0.0s
 => => transferring context: 2B                                                                                                                               0.0s
 => [server internal] load build context                                                                                                                      0.0s
 => => transferring context: 915B                                                                                                                             0.0s
 => [client builder 1/4] FROM docker.io/library/python:3.11-slim@sha256:158caf0e080e2cd74ef2879ed3c4e697792ee65251c8208b7afb56683c32ea6c                      0.0s
 => => resolve docker.io/library/python:3.11-slim@sha256:158caf0e080e2cd74ef2879ed3c4e697792ee65251c8208b7afb56683c32ea6c                                     0.0s
 => CACHED [client builder 2/4] WORKDIR /app                                                                                                                  0.0s
 => [server builder 3/4] COPY requirements.txt .                                                                                                              0.0s
 => [server builder 4/4] RUN pip install --upgrade pip && pip wheel --wheel-dir=/wheels -r requirements.txt                                                   8.4s
 => [server stage-1 3/6] COPY --from=builder /wheels /wheels                                                                                                  0.0s 
 => [server stage-1 4/6] COPY requirements.txt .                                                                                                              0.0s 
 => [server stage-1 5/6] RUN pip install --no-index --find-links=/wheels -r requirements.txt                                                                  0.9s 
 => [server stage-1 6/6] COPY app.py .                                                                                                                        0.0s 
 => [server] exporting to image                                                                                                                               0.1s 
 => => exporting layers                                                                                                                                       0.0s 
 => => writing image sha256:a19d7c086053c5e60263c3d68c26a17188eb331626a447742c73b7b495876407                                                                  0.0s
 => => naming to docker.io/library/lab05-server                                                                                                               0.0s
 => [server] resolving provenance for metadata file                                                                                                           0.0s 
 => [client internal] load build definition from Dockerfile                                                                                                   0.0s
 => => transferring dockerfile: 462B                                                                                                                          0.0s
 => [client internal] load .dockerignore                                                                                                                      0.0s
 => => transferring context: 2B                                                                                                                               0.0s
 => [client internal] load build context                                                                                                                      0.0s
 => => transferring context: 649B                                                                                                                             0.0s
 => [client builder 3/4] COPY requirements.txt .                                                                                                              0.0s
 => [client builder 4/4] RUN pip install --upgrade pip && pip wheel --wheel-dir=/wheels -r requirements.txt                                                   8.0s
 => [client stage-1 3/6] COPY --from=builder /wheels /wheels                                                                                                  0.0s
 => [client stage-1 4/6] COPY requirements.txt .                                                                                                              0.0s 
 => [client stage-1 5/6] RUN pip install --no-index --find-links=/wheels -r requirements.txt                                                                  0.9s 
 => [client stage-1 6/6] COPY client.py .                                                                                                                     0.0s 
 => [client] exporting to image                                                                                                                               0.0s 
 => => exporting layers                                                                                                                                       0.0s 
 => => writing image sha256:1d5d8d78600aa5ab35d5a182bfd88113a0459e5428e7965715f85bde24b91d44                                                                  0.0s
 => => naming to docker.io/library/lab05-client                                                                                                               0.0s
 => [client] resolving provenance for metadata file                                                                                                           0.0s 
[+] Running 5/5
 ✔ client                    Built                                                                                                                            0.0s 
 ✔ server                    Built                                                                                                                            0.0s 
 ✔ Network lab05_app_net     Created                                                                                                                          0.0s 
 ✔ Container lab05-server-1  Created                                                                                                                          0.0s 
 ✔ Container lab05-client-1  Created                                                                                                                          0.0s 
Attaching to client-1, server-1
server-1  |  * Serving Flask app 'app'
server-1  |  * Debug mode: off
server-1  | WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
server-1  |  * Running on all addresses (0.0.0.0)
server-1  |  * Running on http://127.0.0.1:8000
server-1  |  * Running on http://172.20.0.2:8000
server-1  | Press CTRL+C to quit
server-1  | 172.20.0.3 - - [13/Dec/2025 15:25:17] "GET / HTTP/1.1" 200 -
client-1  | 
client-1  |     <html>
client-1  |     <head><title>Colorful Output</title></head>
client-1  |     <body style="font-family: monospace; font-size: 24px;">
server-1  | 192.168.65.1 - - [13/Dec/2025 15:26:27] "GET / HTTP/1.1" 200 -
``` 

- ✔ 12. Откройте соседнее окно терминала и и выведите на терминале

```bash 
open http://localhost:8000 # Текст в окне браузера "hello appsec world"
```

- ✔ 13. Остановите работу `docker-compose`.

```bash 
 docker compose down

[+] Running 2/2
 ✔ Container lab05-web-1  Removed                                                                                                                            10.2s 
 ✔ Network lab05_default  Removed   

```
- ✔ 14. Доработайте `docker-compose` и скрипт, который вы подготовили ранее, что бы вы смогли воспроизвести шаги п.11 по п.13 с демонстрацией. Сделайте `commit`.
В рамках доработки docker-compose реализован воспроизводимый стенд демонстрации:
	- при запуске `docker compose up --build` автоматически собирается образ и поднимается сервис `web`;
	- сервис публикует порт `8000:8000`, доступен по `http://localhost:8000`;
	- подтверждение работоспособности: эндпоинты `/health` (OK) и `/ip` (вызов внешнего API через requests);
	- остановка выполняется через `Ctrl+C` и `docker compose down`, после чего контейнеры удаляются.
```bash
docker compose up --build # Запуск
Compose now can delegate build to bake for better performances
Just set COMPOSE_BAKE=true
[+] Building 30.0s (12/12) FINISHED                                                                                                           docker:desktop-linux
 => [web internal] load build definition from Dockerfile                                                                                                      0.0s
 => => transferring dockerfile: 240B                                                                                                                          0.0s
 => [web internal] load metadata for docker.io/library/python:3.11-slim                                                                                      10.0s
 => [web auth] library/python:pull token for registry-1.docker.io                                                                                             0.0s
 => [web internal] load .dockerignore                                                                                                                         0.0s
 => => transferring context: 2B                                                                                                                               0.0s
 => [web 1/5] FROM docker.io/library/python:3.11-slim@sha256:158caf0e080e2cd74ef2879ed3c4e697792ee65251c8208b7afb56683c32ea6c                                 0.0s
 => => resolve docker.io/library/python:3.11-slim@sha256:158caf0e080e2cd74ef2879ed3c4e697792ee65251c8208b7afb56683c32ea6c                                     0.0s
 => [web internal] load build context                                                                                                                         0.0s
 => => transferring context: 1.07kB                                                                                                                           0.0s
 => CACHED [web 2/5] WORKDIR /app                                                                                                                             0.0s
 => [web 3/5] COPY requirements.txt .                                                                                                                         0.0s
 => [web 4/5] RUN pip install --no-cache-dir -r requirements.txt                                                                                             20.0s
 => [web 5/5] COPY app.py .                                                                                                                                   0.0s
 => [web] exporting to image                                                                                                                                  0.1s
 => => exporting layers                                                                                                                                       0.1s
 => => writing image sha256:a76b69d48050423d337afae24ee3fa962c03cc999e5f7407a16054e10fddfc91                                                                  0.0s
 => => naming to docker.io/library/lab05-web                                                                                                                  0.0s
 => [web] resolving provenance for metadata file                                                                                                              0.0s 
WARN[0030] Found orphan containers ([lab05-client-1 lab05-server-1]) for this project. If you removed or renamed this service in your compose file, you can run this command with the --remove-orphans flag to clean it up. 
[+] Running 3/3
 ✔ web                    Built                                                                                                                               0.0s 
 ✔ Network lab05_default  Created                                                                                                                             0.0s 
 ✔ Container lab05-web-1  Created                                                                                                                             0.0s 
Attaching to web-1
web-1  | 'FLASK_ENV' is deprecated and will not be used in Flask 2.3. Use 'FLASK_DEBUG' instead.
web-1  | 'FLASK_ENV' is deprecated and will not be used in Flask 2.3. Use 'FLASK_DEBUG' instead.
web-1  | 'FLASK_ENV' is deprecated and will not be used in Flask 2.3. Use 'FLASK_DEBUG' instead.
web-1  |  * Serving Flask app 'app'
web-1  |  * Debug mode: off
web-1  | WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
web-1  |  * Running on all addresses (0.0.0.0)
web-1  |  * Running on http://127.0.0.1:8000
web-1  |  * Running on http://172.21.0.2:8000
web-1  | Press CTRL+C to quit
web-1  | 192.168.65.1 - - [13/Dec/2025 15:31:17] "GET / HTTP/1.1" 200 -
web-1  | 192.168.65.1 - - [13/Dec/2025 15:31:22] "GET /health HTTP/1.1" 200 -
```
```bash
curl -s http://localhost:8000/health # демонстрация
{"status":"ok"}
```
```bash
git add docker-compose.yml server/app.py server/Dockerfile server/requirements.txt
git commit -m "lab05: add compose demo with flask service"
```
- ✔ 15. Залейте изменения в свой удаленный репозиторий, проверьте историю `commit`.
```bash
git log --oneline
5e7ef62 (HEAD -> dev) lab05: add compose demo with flask service
aed35ca lab05: extend python script with flask and requests dependencies
65e2ac0 lab05: replace hello script with Typer CLI and pin dependencies
c53e53f Analyze Dockerfile: multi-stage build, dependency handling, AppSec risks
be8e1c7 (origin/dev, main) Initial commit
```
- ✔ 16. Составить `gist` отчет и отправить ссылку личным сообщением
```bash
gh gist create lab05.md --public --desc "lab05 report"
```