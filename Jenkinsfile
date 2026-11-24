pipeline {
    agent any

    environment {
        IMAGE_NAME   = 'cicd-assignment'
        STAGING_PORT = '8090'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'ls -l'
            }
        }

        stage('Package') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .'
            }
        }

        stage('Start Staging') {
            steps {
                sh '''
                    docker rm -f a3-staging || true
                    docker run -d --name a3-staging -p ${STAGING_PORT}:80 ${IMAGE_NAME}:${BUILD_NUMBER}
                    sleep 3
                    curl -sf http://localhost:${STAGING_PORT}/ > /dev/null
                '''
            }
        }

        stage('Test') {
            agent {
                dockerfile {
                    dir 'tests'
                    args '--network host'
                    reuseNode true
                }
            }
            environment {
                HOME     = '/tmp'
                BASE_URL = "http://localhost:${STAGING_PORT}"
            }
            steps {
                sh 'pytest tests/test_site.py -v --junitxml=test-results.xml'
            }
            post {
                always {
                    archiveArtifacts artifacts: 'test-results.xml,screenshot.png', allowEmptyArchive: true
                    script {
                        if (fileExists('test-results.xml')) {
                            try {
                                junit 'test-results.xml'
                            } catch (err) {
                                echo "junit step unavailable; results archived as test-results.xml"
                            }
                        }
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                echo 'All tests passed. Deploying to production on port 80'
                sh '''
                    docker rm -f a3-prod || true
                    docker run -d --name a3-prod --restart unless-stopped -p 80:80 ${IMAGE_NAME}:${BUILD_NUMBER}
                '''
            }
        }
    }

    post {
        always {
            sh 'docker rm -f a3-staging || true'
        }
        success {
            echo "Build ${BUILD_NUMBER} deployed successfully"
        }
        failure {
            echo "Build ${BUILD_NUMBER} failed. Nothing new was deployed"
        }
    }
}
