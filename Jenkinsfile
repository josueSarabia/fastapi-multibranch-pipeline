pipeline {
    environment {
        imageName = "mrbluetoo/fastapi-demo-app:${env.BUILD_ID}"
        customImage = ''
    }

    agent any
    stages {


        stage('Start Container for Testing') {
            steps {
                script {
                    sh 'docker compose rm -f; docker compose up -d images'
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    sh '''
                        #!/bin/bash
                        cd api/
                        pip3 install virtualenv
                        python3 -m virtualenv venv
                        source ./venv/bin/activate
                        pip3 install -r requirements.txt
                        python3 -m pytest
                    '''
                }
            }
            post {
                success {
                    script {
                        sh 'docker-compose down'
                    }
                }
                failure {
                    script {
                        sh 'docker-compose down'
                    }
                }
            }
        }

        stage('Build Image') {
            steps {
                script {
                    customImage = docker.build(imageName)
                }
            }
        }

        stage('Push to Registry') {
            when {
                branch "master"
            }
            steps {
                script {
                    docker.withRegistry('', 'DockerHub') {
                        customImage.push()
                    }
                }
            }
        }
    }
}