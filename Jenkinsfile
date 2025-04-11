pipeline {
    agent any

    environment {
        IMAGE_NAME = "pet_adoption_app"
        CONTAINER_NAME = "pet_adoption_container"
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/harshaa2312/PetAdoption.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker version'
                    sh "docker build -t $IMAGE_NAME ."
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    sh "docker run -d -p 5000:5000 --name $CONTAINER_NAME $IMAGE_NAME"
                }
            }
        }
    }
}
