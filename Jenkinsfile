pipeline {
    agent any

    environment {
        IMAGE_NAME = "pet_adoption_app"
        CONTAINER_NAME = "pet_adoption_container"
    }

    stages {
      

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t $IMAGE_NAME ."
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    sh """
                        docker stop $CONTAINER_NAME || true
                        docker rm $CONTAINER_NAME || true
                        docker run -d -p 5000:5000 --name $CONTAINER_NAME $IMAGE_NAME
                    """
                }
            }
        }
    }
}
