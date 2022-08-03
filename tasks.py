from invoke import Collection

from provision import (
    celery,
    ci,
    data,
    django,
    docker,
    git,
    k8s,
    linters,
    open_api,
    project,
    tests,
)

ns = Collection(
    celery,
    ci,
    django,
    docker,
    data,
    linters,
    project,
    tests,
    git,
    open_api,
    k8s,
)

# Configurations for run command
ns.configure(
    dict(
        run=dict(
            pty=True,
            echo=True,
        ),
    ),
)
