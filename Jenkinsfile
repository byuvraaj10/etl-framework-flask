pipeline {
    agent any

    stages {
        stage('Setup Environment') {
            steps {
                script {
                    bat '''
                    echo Setting up virtual environment...
                    python -m venv venv
                    call venv\\Scripts\\activate
                    pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('Execute Tests') {
            steps {
                script {
                    bat '''
                    call venv\\Scripts\\activate
                    python -m pytest tests/
                    '''
                }
            }
        }

        stage('Launch Application') {
            steps {
                script {
                    bat '''
                    call venv\\Scripts\\activate
                    start /b python run.py
                    '''
                }
            }
        }
    }

    post {
        always {
            bat 'tasklist | findstr python'
        }
    }
}
