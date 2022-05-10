# Instruction Manual

* `git clone git@github.com:nahidsaikat/video-analyzer.git`
* `cd terraform`
  * `terraform init`
  * `terraform plan`
  * `terraform apply`
* `cd backend`
  * `python -m venv .venv`
  * `source .venv/bin/activate`
  * `pip install -r requirements.txt`
  * `python manage.py makemigrations`
  * `python manage.py migrate`
  * `python manage.py runserver`
