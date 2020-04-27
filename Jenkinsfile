pipeline {
    agent {
        dockerfile {
            args '-u root --net=host -v $HOME/docker_volumes/.cache/:/root/.cache/'
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
                sh '''cd src 
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
                sh 'rm -f doc/sphinx-build.log'
                sh '''cd doc
                pipenv run make html'''
                sh 'tar -C doc/build/html -czf docs-${BUILD_TAG}.tar.gz .'
            }
            post {
                success {
                    archiveArtifacts artifacts: "docs-${env.BUILD_TAG}.tar.gz", fingerprint: true
                }
                failure {
                    sh 'cat doc/sphinx-build.log'
                }
            }
        }

        stage('Deploy Documentation') {
            environment {
                TAG_NAME = "${TAG_NAME}"
            }
            when {
                anyOf {
                    branch 'stable'
                    branch 'master'
                    buildingTag()
                }
            }
            steps {
                sh 'rm -f rsync.log'
                sshagent(credentials: ['1cf72f47-b70c-4f90-a958-020956099d19']) {
                    sh 'echo ${TAG_NAME:-GIT_BRANCH#*/}'
                    sh 'echo ${DEPLOY_HOST}:${DEPLOY_PATH}${TAG_NAME:-GIT_BRANCH#*/}/ >> debug.log'
                    sh 'ssh -o StrictHostKeyChecking=no -o BatchMode=yes ${DEPLOY_HOST} mkdir -p ${DEPLOY_PATH}${TAG_NAME:-GIT_BRANCH#*/}/'
                    sh '''rsync -aze 'ssh -o StrictHostKeyChecking=no -o BatchMode=yes' \
                    --log-file=rsync.log \
                    --delete \
                    doc/build/html/ ${DEPLOY_HOST}:${DEPLOY_PATH}${TAG_NAME:-GIT_BRANCH#*/}/'''
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
