# 📚 Kubernetes Day 1: Окружение, Deployment и Service

## 📝 Описание проекта

Это первый день обучения **Kubernetes** на практике. Проект представляет собой простое Flask приложение, развёрнутое в Kubernetes кластере с использованием:

- **Flask** - веб-фреймворк на Python
- **PostgreSQL** - база данных
- **Docker** - контейнеризация
- **Kubernetes** - оркестрация контейнеров

### Цель:
Практическое понимание ключевых концепций Kubernetes:
- Pods (подПрограммы)
- Deployments (управление репликами)
- Services (сетевое взаимодействие)

---

## 🎯 День 1: Итоги

На первый день было выполнено:

✅ **Установка окружения**: Docker, kubectl, Minikube  
✅ **Создание Flask приложения**: простой веб-сервис с тестированием БД  
✅ **Создание Docker образа**: `flask-app:latest`  
✅ **Развёртывание в Kubernetes**:
  - Deployment с 5 репликами
  - Service типа LoadBalancer
  - Проверка функциональности

✅ **Документирование**: этот файл 📄

---

## 🔧 Установка окружения

### Требования
- Windows 10/11 или Linux
- Docker Desktop (с поддержкой Kubernetes)
- kubectl
- Minikube (опционально)

### Шаги установки

#### 1. **Установка Docker Desktop**
```bash
# Скачать с https://www.docker.com/products/docker-desktop
# Установить и перезагрузить систему
# Проверить установку:
docker --version
```

#### 2. **Установка kubectl**
```bash
# На Windows через scoop или choco:
choco install kubernetes-cli

# Проверить:
kubectl version --client
```

#### 3. **Включение Kubernetes в Docker Desktop** (вариант 1)
- Открыть Docker Desktop
- Settings → Kubernetes → Enable Kubernetes
- Подождать инициализации (3-5 минут)

#### 4. **Альтернатива: Запуск Minikube** (вариант 2)
```bash
# Установка (если не установлен)
choco install minikube

# Запуск кластера
minikube start

# Проверка статуса
kubectl cluster-info
```

#### 5. **Проверка готовности окружения**
```bash
kubectl get nodes
kubectl config current-context
```

✅ **Результат**: Кластер Kubernetes запущен и готов к использованию

---

## 🏗️ Архитектура

```
┌─────────────────────────────────────────────┐
│         Kubernetes Cluster                   │
├─────────────────────────────────────────────┤
│                                             │
│  ┌────────────────────────────────────┐    │
│  │    Service (LoadBalancer)          │    │
│  │    my-service:80 → pod:5000        │    │
│  └────────────────────────────────────┘    │
│           ↓↓↓                              │
│  ┌────────────────────────────────────┐    │
│  │   Deployment: flask-deployment     │    │
│  │   Replicas: 5                      │    │
│  │                                    │    │
│  │  ┌──────┐ ┌──────┐ ┌──────┐       │    │
│  │  │ Pod  │ │ Pod  │ │ Pod  │ ...   │    │
│  │  └──────┘ └──────┘ └──────┘       │    │
│  │                                    │    │
│  │  ┌──────┐ ┌──────┐                 │    │
│  │  │ Pod  │ │ Pod  │                 │    │
│  │  └──────┘ └──────┘                 │    │
│  └────────────────────────────────────┘    │
│                                             │
│  Каждый Pod содержит:                      │
│  - Flask приложение (контейнер)            │
│  - External Port: 5000                     │
│                                             │
└─────────────────────────────────────────────┘
```

### Компоненты

| Компонент | Назначение | Файл |
|-----------|-----------|------|
| **Deployment** | Управление репликами, rolling updates | `flask-deployment.yaml` |
| **Service** | Балансировка нагрузки, единая точка входа | `flask-service.yaml` |
| **Pod** | Минимальная единица в Kubernetes, содержит контейнер | автогенерируется Deployment |
| **Container** | Docker образ Flask приложения | `Dockerfile` |

---

## 📦 Структура проекта

```
k8s_day_1/
├── README.md                    # Этот файл
├── app.py                       # Flask приложение
├── requirements.txt             # Зависимости Python
├── Dockerfile                   # Docker образ
├── flask-deployment.yaml        # K8s Deployment
├── flask-service.yaml           # K8s Service
└── ss/                          # Папка со скриншотами (если были)
```

### Содержимое ключевых файлов

#### `app.py` - Flask приложение
```python
from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

@app.route('/')
def index():
    return 'Flask + PostgreSQL in Docker! 🐳'

@app.route('/db-test')
def db_test():
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'db'),
            database=os.getenv('DB_NAME', 'appdb'),
            user=os.getenv('DB_USER', 'user'),
            password=os.getenv('DB_PASSWORD', 'password')
        )
        conn.close()
        return jsonify({'status': 'DB Connected!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

#### `Dockerfile` - Docker образ
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

#### `flask-deployment.yaml` - Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-deployment
  labels:
    app: flask
spec:
  replicas: 5
  selector:
    matchLabels:
      app: flask
  template:
    metadata:
      labels:
        app: flask
    spec:
      containers:
      - name: flask
        image: docker.io/library/flask-app:latest
        imagePullPolicy: Never
        ports:
        - containerPort: 5000
```

#### `flask-service.yaml` - Kubernetes Service
```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app: flask
  ports:
    - protocol: TCP
      targetPort: 5000
      port: 80
  type: LoadBalancer
```

---

## 🚀 Ключевые команды

### Docker команды

```bash
# Сборка Docker образа
docker build -t flask-app:latest .

# Проверка образов
docker images

# Тестирование локально
docker run -p 5000:5000 flask-app:latest

# Проверка логов контейнера
docker logs -f <container_id>
```

### Kubernetes команды

#### Deployment операции
```bash
# Применить Deployment
kubectl apply -f flask-deployment.yaml

# Просмотр развёрнутых Deployments
kubectl get deployments

# Информация о Deployment
kubectl describe deployment flask-deployment

# Просмотр Pods, созданных Deployment
kubectl get pods

# Детальная информация о Pod
kubectl describe pod <pod_name>

# Логи из Pod
kubectl logs -f <pod_name>

# Масштабирование (изменение количества реплик)
kubectl scale deployment flask-deployment --replicas=3

# Удаление Deployment
kubectl delete deployment flask-deployment

# Редактирование Deployment (интерактивно)
kubectl edit deployment flask-deployment
```

#### Service операции
```bash
# Применить Service
kubectl apply -f flask-service.yaml

# Просмотр Services
kubectl get services

# Информация о Service
kubectl describe service my-service

# Получить внешний IP (может быть pending на Minikube)
kubectl get svc my-service

# Порт-форвардинг для доступа (альтернатива LoadBalancer)
kubectl port-forward service/my-service 8080:80

# Удаление Service
kubectl delete service my-service
```

#### Полезные команды
```bash
# Кластер информация
kubectl cluster-info

# Состояние узлов
kubectl get nodes

# Все ресурсы в кластере
kubectl get all

# События в кластере
kubectl get events

# Просмотр логов в реальном времени
kubectl logs -f deployment/flask-deployment

# Выполнить команду в Pod
kubectl exec -it <pod_name> -- /bin/bash

# Удалить все ресурсы
kubectl delete all --all
```

---

## 📉 Запуск и эксплуатация

### Пошаговый запуск

#### Шаг 1: Убедиться, что Kubernetes работает
```bash
kubectl cluster-info
# Результат:
# Kubernetes control plane is running at https://127.0.0.1:6443
# CoreDNS is running at ...
```

#### Шаг 2: Собрать Docker образ
```bash
docker build -t flask-app:latest .
```

**Проверка:**
```bash
docker images | grep flask-app
# Результат: flask-app  latest  <image_id>  <created>
```

#### Шаг 3: Развернуть Deployment
```bash
kubectl apply -f flask-deployment.yaml
```

**Проверка:**
```bash
kubectl get deployments
# Результат:
# NAME                 READY   UP-TO-DATE   AVAILABLE   AGE
# flask-deployment     5/5     5            5           1m
```

#### Шаг 4: Развернуть Service
```bash
kubectl apply -f flask-service.yaml
```

**Проверка:**
```bash
kubectl get services
# Результат:
# NAME         TYPE           CLUSTER-IP    EXTERNAL-IP   PORT(S)        
# my-service   LoadBalancer   10.x.x.x      <pending>     80:31xxx/TCP
```

#### Шаг 5: Проверить Pods
```bash
kubectl get pods
# Результат: 5 работающих Pod'ов

kubectl logs -f deployment/flask-deployment
# Логи приложения
```

#### Шаг 6: Получить доступ к приложению

**Вариант 1: Порт-форвардинг**
```bash
kubectl port-forward service/my-service 8080:80
# Открыть в браузере: http://localhost:8080
```

**Вариант 2: Узнать IP сервиса**
```bash
# Может быть в статусе "pending" на Minikube
kubectl get svc my-service
```

**Вариант 3: На Minikube через команду**
```bash
minikube service my-service
```

### Проверка функциональности

```bash
# Главная страница
curl http://localhost:8080/
# Ответ: "Flask + PostgreSQL in Docker! 🐳"

# Тест подключения к БД
curl http://localhost:8080/db-test
# Ответ: {"error":"..."} (т.к. БД не запущена)
```

---

## ⚠️ Сложности и решения

### Проблема 1: Docker образ не найден
```
Error from server (ErrImagePull): failed to pull image "docker.io/library/flask-app:latest": 
rpc error: code = Unknown desc = Error response from daemon: ...
```

**Причина:** Docker образ не загружен в локальный Docker demon

**Решение:**
```bash
# Собрать образ локально
docker build -t flask-app:latest .

# В Deployment добавить imagePullPolicy: Never (добавлено ✓)
imagePullPolicy: Never
```

---

### Проблема 2: Service остаётся в статусе Pending
```
NAME         TYPE           EXTERNAL-IP   PORT(S)        AGE
my-service   LoadBalancer   <pending>     80:31xxx/TCP
```

**Причина:** На Minikube LoadBalancer типов сервисов требуют дополнительной настройки

**Решение 1:** Использовать порт-форвардинг
```bash
kubectl port-forward service/my-service 8080:80
```

**Решение 2:** На Docker Desktop это работает корректно

**Решение 3:** Запустить Minikube с поддержкой LoadBalancer (отдельный терминал)
```bash
minikube tunnel
```

---

### Проблема 3: Pod'ы не запускаются
```
kubectl get pods
# Status: ImagePullBackOff, ErrImagePull
```

**Причина:** Неправильные версии или отсутствующие образы

**Решение:**
```bash
# Проверить логи Pod'а
kubectl describe pod <pod_name>

# Пересобрать образ
docker build -t flask-app:latest .

# Перезагрузить Deployment (рекреация Pod'ов)
kubectl rollout restart deployment/flask-deployment
```

---

### Проблема 4: Ошибка при подключении к базе
```json
{"error": "could not connect to server: Connection refused"}
```

**Причина:** PostgreSQL не запущена (это ожидаемо в День 1)

**Решение:** В День 2 добавим `docker-compose` с PostgreSQL или запустим в отдельном Pod'е

---

## 📚 Выводы по Kubernetes

### Ключевые концепции, которые были изучены

#### 1. **Pods (Поды)**
- Наименьшая единица в Kubernetes
- Содержит один или несколько контейнеров
- Обычно один контейнер на Pod
- Быстрые (временные), могут быть удалены в любой момент

#### 2. **Deployments (Развёртывания)**
- Управляют Pods через ReplicaSets
- Позволяют масштабировать (replicas: 5 = 5 копий Pod'ов)
- Rolling updates без downtime
- Система самовосстановления (если Pod упадёт, создаст новый)

```bash
# Пример масштабирования:
kubectl scale deployment flask-deployment --replicas=10
# Вместо 5 Pod'ов будет 10
```

#### 3. **Services (Сервисы)**
- Стабильная точка входа для Pods (которые временные)
- Балансировка нагрузки между Pods
- Типы:
  - **ClusterIP**: доступ внутри кластера (по умолчанию)
  - **NodePort**: доступ через порт узла
  - **LoadBalancer**: публичный IP с балансировкой (облака)
  - **ExternalName**: расширенный DNS

#### 4. **Labels и Selectors**
```yaml
# Deployment помечает Pod'ы меткой
labels:
  app: flask

# Service находит Pod'ы по этой метке
selector:
  app: flask
```

### Практические выводы

✅ Kubernetes решает проблемы:
- Масштабирования (много копий сервиса)
- Надёжности (автоматическое восстановление)
- Обновления без остановки (rolling updates)
- Управления ресурсами

⚠️ Сложности на старте:
- Кривая обучения (много новых концепций)
- Множество конфигураций YAML
- Debugging может быть нетривиален
- Docker образы должны быть готовы


---

## 📊 Результаты

| Метрика | Результат |
|---------|-----------|
| Docker образ создан | ✅ `flask-app:latest` |
| Deployment развёрнут | ✅ 5 работающих Pod'ов |
| Service запущен | ✅ LoadBalancer на порту 80 |
| Приложение доступно | ✅ Через port-forward или Minikube service |
| Скейлинг работает | ✅ `kubectl scale` изменяет количество реплик |

---

## 📖 Полезные ссылки

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Kubernetes Concepts](https://kubernetes.io/docs/concepts/)
- [Pod Lifecycle](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/)
- [Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Service](https://kubernetes.io/docs/concepts/services-networking/service/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [Docker Documentation](https://docs.docker.com/)
- [Markdown Guide](https://www.markdownguide.org/)

---

## 🎓 Автор

**День 1 обучения**: установка окружения, первое развёртывание в Kubernetes  
**Дата**: 26 марта 2026

---

