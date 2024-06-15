# ДЗ2 

##  Условие:
```text
Реализация скрипта для тестирования MTU в канале
В данной самостоятельной работе:

Нужно реалиозвать простой скрипт для поиска минимального значения MTU в канале между конечными хостами.
Язык программирования - любой.
Для запуска скрипта необходимо подготовить docker контейнер.
Для сдачи работы требуется
Выложить исходник скрипта в GitHub вместе c docker контейнером для запуска и проверки работоспособности.

Критерии оценки:

Расчет оценки по формуле 10 - n

где:

10 максимальное количество баллов

n - стоимость ошибки:

10 - неверен алгоритм. правильный ответ не получен
5 - скрипт работает, однако ответ корректный не во всех ситуациях
1 - не предусмотрены проверки на ввод аргумента
1 - не проверяется корректность аргумента
1 - не проверяется доступность адреса назначения
1 - не отлавливаются исключения
1 - не отлавливается ситуация, при которой icmp заблокирован
1 - скрипт не универсален и работает не во всех операционных системах
```

## Скрипт для проверки

```bash
docker build -t app . && echo "Несуществующий хост: "  &&  docker run app --verbose takogo_hosta_net && echo "Wiki CS: " && docker run app --verbose wiki.cs.hse.ru && echo "GitHub: " && docker run app --verbose github.com
```

Ожидаемый вывод
```text
Несуществующий хост: 
Host name takogo_hosta_net cannot be resolved
Wiki CS: 
Host wiki.cs.hse.ru is unreachable
GitHub: 
Ping host# github.com with payload_size# 1000, returncode=0
Ping host# github.com with payload_size# 1500, returncode=1
Ping host# github.com with payload_size# 1250, returncode=0
Ping host# github.com with payload_size# 1375, returncode=0
Ping host# github.com with payload_size# 1437, returncode=0
Ping host# github.com with payload_size# 1468, returncode=0
Ping host# github.com with payload_size# 1484, returncode=1
Ping host# github.com with payload_size# 1476, returncode=1
Ping host# github.com with payload_size# 1472, returncode=0
Ping host# github.com with payload_size# 1474, returncode=1
Ping host# github.com with payload_size# 1473, returncode=1
MTU to host# github.com = 1472 bytes, packet size with headers = 1500 bytes
```
