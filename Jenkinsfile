pipeline {
    agent none
    stages {
        stage('Test') { 
            agent {
                docker {
                    image 'python:3.8' 
                }
            }
            steps {
                sh "pip install --no-cache-dir -t python pipenv"
                sh "PYTHONPATH=\$(pwd)/python PIPENV_VENV_IN_PROJECT=true python/bin/pipenv sync --sequential --dev"
                sh "export PYTHONPATH=\$(pwd)/python && cd src && PIPENV_VENV_IN_PROJECT=true \${PYTHONPATH}/bin/pipenv run pytest -p no:warnings --junit-xml test-reports/results.xml"
            }
            post {
                always {
                    junit 'src/test-reports/results.xml' 
                }
            }
        }
    }
}
