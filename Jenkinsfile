pipeline {
    agent none
    stages {
        stage('Test') { 
            agent {
                docker {
                    image 'python:3.7' 
                }
            }
            steps {
                sh "pip install --user pipenv"
                sh "pipenv sync"
                sh 'pipenv run pytest -p no:warnings --junit-xml test-reports/results.xml' 
            }
            post {
                always {
                    junit 'test-reports/results.xml' 
                }
            }
        }
    }
}
