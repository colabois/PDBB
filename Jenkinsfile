pipeline {
    agent {
        dockerfile {
            args '-u root -v $HOME/docker_volumes/.cache/:/root/.cache/'
        }
    }
    environment {
        SPHINXOPTS = '-w sphinx-build.log'
        DEPLOY_HOST = 'docs@moriya.zapto.org'
        DEPLOY_PATH = 'www/docs/bot-base/'
    }

    stages {
        stage('Install Dependencies') {
            steps {
                sh 'pipenv sync --verbose --sequential --dev'
            }
        }

        stage('Run Tests') { 
            steps {
                sh '''export PYTHONPATH=$(pwd)/python
                cd src 
                pipenv run pytest -p no:warnings --junit-xml test-reports/results.xml'''
            }
            post {
                always {
                    junit 'src/test-reports/results.xml' 
                }
            }
        }

        stage('Build Documentation') {
            steps {
                sh '''export PYTHONPATH=$(pwd)/python
                cd doc
                rm -f sphinx-build.log
                pipenv run make html'''
            }
            post {
                failure {
                    sh 'cat doc/sphinx-build.log'
                }
            }
        }

        stage('Deploy Documentation') {
            when {
                anyOf {
                    branch 'stable'
                    branch 'master'
                }
            }
            steps {
                sshagent(credentials: ['1cf72f47-b70c-4f90-a958-020956099d19']) {
                    sh '''cd doc
                    rm -f rsync.log
                    echo ${DEPLOY_HOST}:${DEPLOY_PATH}${GIT_BRANCH#*/}/ >> debug.log
                    ssh -o StrictHostKeyChecking=no -o BatchMode=yes ${DEPLOY_HOST} mkdir -p ${DEPLOY_PATH}{GIT_BRANCH#*/}/
                    rsync -aze 'ssh -o StrictHostKeyChecking=no -o BatchMode=yes' \
                    --log-file=rsync.log \
                    --delete \
                    ./build/html/ ${DEPLOY_HOST}:${DEPLOY_PATH}${GIT_BRANCH#*/}/'''
                }
            }
            post {
                failure {
                    sh 'cat doc/debug.log doc/rsync.log'
                }
            }
        }
    }
}
