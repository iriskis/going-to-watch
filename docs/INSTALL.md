# Installing project for developing on local PC

You have to have the following tools installed prior initializing the project:

- [docker](https://docs.docker.com/engine/installation/)
- [docker-compose](https://docs.docker.com/compose/install/)
- [pack-cli](https://buildpacks.io/docs/tools/pack/)
- [pyenv](https://github.com/pyenv/pyenv)
- [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)

## Backend

### Task runner

For easier running of everyday tasks, like:

* run dev server
* run all tests
* run linters
* run celery workers
* ...

We use [invoke](https://pypi.org/project/invoke/).

It provides shortcuts for most of the tasks, so it's like collection of bash scrips
or makefile or `npm scripts`.

To enable autocomletion of invoke commands add this line to your `~/.zshrc`

```
source <(inv --print-completion-script zsh)
```

### Python interpreter

Also `invoke` abstract "python interpreter", so you can use both `virtual env` and
`dockerized` python interpreter for working with project (see `.invoke` file).

* `virtualenv` is the default approach that requires python interpreter,
virtualenv, etc.
* `dockerized` is simpler for quick starting project and for experienced
developers

Suggested approach is using `virtualenv`

### Services

Project may use external services like Database (postgres), message broker,
cache (redis). For easier set up they are defined in `docker-compose.yml` file,
and they are automatically prepared / started when using `invoke`.


# Prepare python env using virtualenv

1. Set up aliases for docker hosts in `/etc/hosts`:

```
127.0.0.1 postgres
127.0.0.1 redis
```

2. Create separate python virtual environment if you are going to run it in
local:

```bash
pyenv install 3.10.4
pyenv virtualenv 3.10.4 going-to-watch-backend
pyenv local going-to-watch-backend
pyenv activate going-to-watch-backend
```

3. Set up packages for using `invoke`

```bash
pip install -r requirements/local_build.txt
```

4. Start project initialization that will set up docker containers,
python/system env:

```bash
inv project.init
```

5. Run the project and go to `localhost:8000` page in browser to check whether
it was started:

```bash
$ inv django.run
```

That's it. After these steps, the project will be successfully set up.

Once you run `project.init` initially you can start web server with
`inv django.run` command without executing `project.init` call.

# PyCharm console
Open Pycharm `settings`->`Build,Execution,Deployment`->`Console`->`Django Console` then
copy below into Starting script

```python
from django_extensions.management.shells import import_objects
from django.core.management.color import no_style

globals().update(
    import_objects({"dont_load": [], "quiet_load": False}, no_style())
)
```

# Devops tools
You will need:
* [kubectl](https://kubernetes.io/docs/tasks/tools/)
* [teleport](https://goteleport.com/docs/getting-started/)

Most of needed shortcuts can be called via invoke `inv k8s.###`. Just make sure that you log in with
`inv k8s.login`

```
k8s.logs
k8s.python-shell
```

# Add social app in Django admin
Go to the admin page, open "Sites" and create (or modify an existing) site "127.0.0.1:8000".
![](https://user-images.githubusercontent.com/61578484/183415693-f0b8a332-8d1a-4ca8-9bd4-87b235e1f188.png)

Then open tab "Social applications" and create new application.
Be sure to enter your project's client_id and secret_key in ["google console"](https://console.cloud.google.com)

![](https://user-images.githubusercontent.com/61578484/183416323-8cb33fd6-238b-4383-b2a9-15d6b3d7d624.png)
