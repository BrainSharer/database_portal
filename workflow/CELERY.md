## Working with the celery pipeline
Here is a starter for celery: https://docs.celeryproject.org/en/stable/getting-started/first-steps-with-celery.html
1. Make sure there are no other existing celery processes.
1. Open up a terminal in the base dir of the activebrainatlas admin project
1. Source the correct virtualenv: `source /usr/local/share/pipeline/bin/activate`
1. Run celery: `celery -A workflow worker -P threads -l info` This needs to be restarted every time you make a change in the code.
1. Open up the page: http://localhost:8000/admin/workflow/task/pipeline