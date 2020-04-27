pipeline {
    agent {
        dockerfile {
            args '-u root --net=host -v $HOME/docker_volumes/.cache/:/root/.cache/'
        }
    }
    environment {
        SPHINXOPTS = '-w sphinx-build.log'
        DEPLOY_HOST = 'docs@moriya.zapto.org'
        PROJECT_NAME = 'bot-base'
        DEPLOY_DOC_PATH = "www/docs/${env.PROJECT_NAME}/"
        DEPLOY_REL_PATH = "www/releases/${env.PROJECT_NAME}/"
        TAG_NAME = """${TAG_NAME ?: ""}"""
        ARTIFACTS = "${WORKSPACE}/.artifacts"
    }
    stages {
        stage('Generate release archives') {
            steps {
                sh 'git clean -fxd'
                sh 'mkdir -p ${ARTIFACTS}/build'
                sh 'mkdir -p /tmp/build'
                sh 'pipenv lock -r | tee requirements.txt'
                sh 'echo .artifacts >> .releaseignore'
                sh 'rsync -avr --exclude-from=.releaseignore ./ /tmp/build'
                sh 'tar -C /tmp/build -cvzf ${ARTIFACTS}/build/${TAG_NAME:-${GIT_BRANCH#*/}}.tar.gz --owner=0 --group=0 .'
                sh 'cd /tmp/build && zip ${ARTIFACTS}/build/${TAG_NAME:-${GIT_BRANCH#*/}}.zip -r .'            
            }
            post {
                always {
                    archiveArtifacts artifacts: ".artifacts/build/*", fingerprint: true
                }
            }
        }

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
                sh '''cd doc
                pipenv run make html'''
                sh 'mkdir -p ${ARTIFACTS}/doc'
                sh 'tar -C doc/build/html -czf ${ARTIFACTS}/doc/html.tar.gz .'
            }
            post {
                success {
                    archiveArtifacts artifacts: ".artifacts/doc/*", fingerprint: true
                }
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
                    buildingTag()
                }
            }
            steps {
                sshagent(credentials: ['1cf72f47-b70c-4f90-a958-020956099d19']) {
                    sh 'echo ${TAG_NAME:-${GIT_BRANCH#*/}}'
                    sh 'echo ${DEPLOY_HOST}:${DEPLOY_DOC_PATH}${TAG_NAME:-${GIT_BRANCH#*/}}/'
                    sh 'ssh -o StrictHostKeyChecking=no -o BatchMode=yes ${DEPLOY_HOST} mkdir -p ${DEPLOY_DOC_PATH}${TAG_NAME:-${GIT_BRANCH#*/}}/'
                    sh '''rsync -aze 'ssh -o StrictHostKeyChecking=no -o BatchMode=yes' \
                    --log-file=rsync-doc.log \
                    --delete \
                    doc/build/html/ ${DEPLOY_HOST}:${DEPLOY_DOC_PATH}${TAG_NAME:-${GIT_BRANCH#*/}}/'''
                }
            }
            post {
                failure {
                    sh 'cat rsync-doc.log'
                }
            }
        }
        
        stage('Deploy Release Files') {
            when {
                anyOf {
                    branch 'stable'
                    branch 'master'
                    buildingTag()
                }
            }
            steps {
                sshagent(credentials: ['1cf72f47-b70c-4f90-a958-020956099d19']) {
                    sh 'echo ${TAG_NAME:-${GIT_BRANCH#*/}}'
                    sh 'echo ${DEPLOY_HOST}:${DEPLOY_REL_PATH}${TAG_NAME:-${GIT_BRANCH#*/}}/'
                    sh 'ssh -o StrictHostKeyChecking=no -o BatchMode=yes ${DEPLOY_HOST} mkdir -p ${DEPLOY_REL_PATH}${TAG_NAME:-${GIT_BRANCH#*/}}/'
                    sh '''rsync -aze 'ssh -o StrictHostKeyChecking=no -o BatchMode=yes' \
                    --log-file=rsync-rel.log \
                    --delete \
                    ${ARTIFACTS}/ ${DEPLOY_HOST}:${DEPLOY_REL_PATH}${TAG_NAME:-${GIT_BRANCH#*/}}/'''
                }
            }
            post {
                failure {
                    sh 'cat rsync-rel.log'
                }
            }
        }
    }
    post {
        always {
            sh 'git clean -fxd'
        }
    }
}
