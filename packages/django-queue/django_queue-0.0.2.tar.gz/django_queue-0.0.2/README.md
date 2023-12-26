django-queue
=====

Django-queue is a Django app to add task queues to Django. It is based on the Django ORM. It uses concepts like proxy models to define tasks.

Note that this app is far from complete. It is currently a proof-of-concept of the Django ORM API only. See below for future goals.

Design goals include:
- Transactional Enqueueing like what the following two provide for Golang and Elixir:
  - [Riverqueue](https://news.ycombinator.com/item?id=38349716)
  - [Oban](https://github.com/sorentwo/oban)
- Installation simplicity (`pip install django-queue`).
- Tight integration with Django ORM so if you know the ORM, you know how to use this tool.
- Operational simplicity and flexibility.

## Quick Start

1. Add to your `INSTALLED_APPS` setting like this::
```python3
    INSTALLED_APPS = [
        ...,
        "django_queue",
    ]
```

2. Run ``python manage.py migrate`` to create the task models.

3. Add a new task to your app:
```python3
import requests
from django.db import models

from django_queue.models import Task


class GetPokemonTask(Task):
    """
    Gets a pokemon from the Pokemon API pokeapi.co.
    """
    # app_name.model_name
    base_type = "pokemon.GetPokemonTask"

    class Meta:
        proxy = True

    def task(self):
        """Fetch the api response."""
        pokemon = self.args[0]
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon}"
        response = requests.get(url)
        response.raise_for_status()
        self.result = response.json()
        self.save()

```
3. Create a task:
For example, run from the django shell (`./manage.py shell`):
```python3
>>> from pokemon import models
>>> task = models.GetPokemonTask.objects.delay('ditto')
```
5. Run the task:
For example, run from the django shell (`./manage.py shell`):
```python3
>>> task = models.GetPokemonTask.objects.first()
>>> task
<GetPokemonTask: GetPokemonTask object (5)>
>>> task.args
['ditto']
>>> task.task()
>>> task.result
{'abilities': ...}
```

## Wish list of future features
This is my scratchpad for brainstorming what could be useful. Some of these could be actual features implemented in the app. Others could be examples to provide.

- Actual concurrency mechanisms to allow multiple workers to work on one task definition.
- Statuses, e.g., `scheduled`, `running`, `done`, `error`
- Ability to have one worker run all kinds of tasks or a subset of them.
- Support SQLite
- Support Postgres
  - Maybe something from https://blog.sequin.io/all-the-ways-to-capture-changes-in-postgres/.
- Management command to run workers.
- Examples of:
  - Running with uWSGI background offloader
  - Running as a Docker container
  - Running as a K8s pod with an HPA
  - Running as an AWS Lambda
  - Running as a GCS cloud function
- Documentation.
- Examples directory.
- Benchmarking.

## Contributing
If you're interested in contributing, file an issue or DM me!
