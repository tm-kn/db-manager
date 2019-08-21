#!/bin/sh
set -xe

PROJECT_NAME=$1

PROJECT_DIR=/vagrant
VIRTUALENV_DIR=/home/vagrant/.virtualenvs/$PROJECT_NAME

PYTHON=$VIRTUALENV_DIR/bin/python
PIP=$VIRTUALENV_DIR/bin/pip


apt-get update -y

apt-get install -y apt-transport-https ca-certificates curl gnupg2 software-properties-common
curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -

add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"
apt-get update -y
apt-get install -y docker-ce docker-ce-cli containerd.io
systemctl enable docker
systemctl start docker

usermod -aG docker vagrant

# Create database (let it fail because database may exist)
set +e
su - vagrant -c "createdb $PROJECT_NAME"
set -e


# Virtualenv setup for project
su - vagrant -c "virtualenv --python=python3 $VIRTUALENV_DIR"

su - vagrant -c "echo $PROJECT_DIR > $VIRTUALENV_DIR/.project"

# Upgrade PIP itself
su - vagrant -c "$PIP install --upgrade pip"

# Upgrade setuptools (for example html5lib needs 1.8.5+)
su - vagrant -c "$PIP install --upgrade six setuptools"

# Install PIP requirements
su - vagrant -c "cd $PROJECT_DIR && $PIP install -r requirements.txt"

# Set execute permissions on manage.py as they get lost if we build from a zip file
chmod a+x $PROJECT_DIR/manage.py


# running migrations here is typically not necessary because of fab pull_data
# su - vagrant -c "$PYTHON $PROJECT_DIR/manage.py migrate --noinput"

# Install Heroku CLI
curl -sSL https://cli-assets.heroku.com/install-ubuntu.sh | sh

# Install AWS CLI
apt-get update -y
apt-get install -y unzip
rm -rf /tmp/awscli-bundle || true
rm -rf /tmp/awscli-bundle.zip || true
curl -sSL "https://s3.amazonaws.com/aws-cli/awscli-bundle.zip" -o "/tmp/awscli-bundle.zip"
unzip -q /tmp/awscli-bundle.zip -d /tmp
/tmp/awscli-bundle/install -i /usr/local/aws -b /usr/local/bin/aws

# Add a couple of aliases to manage.py into .bashrc
cat << EOF >> /home/vagrant/.bashrc
export PYTHONPATH=$PROJECT_DIR
export DJANGO_SETTINGS_MODULE=$PROJECT_NAME.settings
export DATABASE_URL=postgres:///$PROJECT_NAME
export CELERY_BROKER_URL=redis://127.0.0.1:6379/2

alias dj="django-admin.py"
alias djrun="dj runserver 0.0.0.0:8000"
alias djrunp="dj runserver_plus 0.0.0.0:8000"
alias celeryrun="celery -A db_manager worker --loglevel=info"

source $VIRTUALENV_DIR/bin/activate
export PS1="[$PROJECT_NAME \W]\\$ "
cd $PROJECT_DIR
EOF
