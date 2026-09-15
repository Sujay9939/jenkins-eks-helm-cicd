pipeline {

    agent {
        label 'docker-agent'
    }

    environment {

        DOCKER_IMAGE = "YOUR_DOCKERHUB_USERNAME/jenkins-eks-app"

        DOCKER_CREDENTIALS = credentials('dockerhub-credentials')

        AWS_REGION = 'ap-south-1'

        EKS_CLUSTER = 'YOUR-EKS-CLUSTER-NAME'

        HELM_RELEASE = 'myapp'

        K8S_NAMESPACE = 'production'
    }

    stages {

        stage('Checkout') {

            steps {

                echo 'Checking out source code...'

                checkout scm
            }
        }


        stage('Install Dependencies') {

            steps {

                sh '''
                    python3 -m venv venv

                    . venv/bin/activate

                    pip install --upgrade pip

                    pip install -r app/requirements.txt
                '''
            }
        }


        stage('Unit Tests') {

            steps {

                sh '''
                    . venv/bin/activate

                    pytest \
                    app/tests \
                    --junitxml=test-results.xml
                '''
            }

            post {

                always {

                    junit 'test-results.xml'
                }
            }
        }


        stage('SonarQube Analysis') {

            steps {

                withSonarQubeEnv('sonarqube') {

                    sh '''
                        . venv/bin/activate

                        pip install coverage

                        coverage run -m pytest app/tests

                        coverage xml

                        sonar-scanner \
                          -Dsonar.projectKey=jenkins-eks-helm-app \
                          -Dsonar.sources=app \
                          -Dsonar.tests=app/tests \
                          -Dsonar.python.coverage.reportPaths=coverage.xml
                    '''
                }
            }
        }


        stage('Quality Gate') {

            steps {

                timeout(time: 5, unit: 'MINUTES') {

                    waitForQualityGate abortPipeline: true
                }
            }
        }


        stage('Docker Build') {

            steps {

                sh '''
                    docker build \
                    -t ${DOCKER_IMAGE}:${BUILD_NUMBER} \
                    -t ${DOCKER_IMAGE}:latest \
                    .
                '''
            }
        }


        stage('Trivy Security Scan') {

            steps {

                sh '''
                    trivy image \
                    --exit-code 1 \
                    --severity CRITICAL,HIGH \
                    --ignore-unfixed \
                    ${DOCKER_IMAGE}:${BUILD_NUMBER}
                '''
            }
        }


        stage('Docker Hub Login') {

            steps {

                sh '''
                    echo "${DOCKER_CREDENTIALS_PSW}" | \
                    docker login \
                    -u "${DOCKER_CREDENTIALS_USR}" \
                    --password-stdin
                '''
            }
        }


        stage('Push Docker Image') {

            steps {

                sh '''
                    docker push ${DOCKER_IMAGE}:${BUILD_NUMBER}

                    docker push ${DOCKER_IMAGE}:latest
                '''
            }
        }


        stage('Configure EKS Access') {

            steps {

                sh '''
                    aws eks update-kubeconfig \
                    --region ${AWS_REGION} \
                    --name ${EKS_CLUSTER}

                    kubectl get nodes
                '''
            }
        }


        stage('Helm Lint') {

            steps {

                sh '''
                    helm lint helm/myapp
                '''
            }
        }


        stage('Helm Deploy') {

            steps {

                sh '''
                    helm upgrade --install ${HELM_RELEASE} \
                    helm/myapp \
                    --namespace ${K8S_NAMESPACE} \
                    --create-namespace \
                    --set image.tag=${BUILD_NUMBER} \
                    --wait \
                    --timeout 5m \
                    --rollback-on-failure
                '''
            }
        }


        stage('Deployment Verification') {

            steps {

                sh '''
                    kubectl rollout status \
                    deployment/${HELM_RELEASE} \
                    -n ${K8S_NAMESPACE} \
                    --timeout=180s

                    kubectl get pods \
                    -n ${K8S_NAMESPACE}

                    kubectl get svc \
                    -n ${K8S_NAMESPACE}
                '''
            }
        }


        stage('Production Approval') {

            when {

                branch 'main'
            }

            steps {

                input message: 'Deploy this version to production?', \
                      ok: 'Deploy'
            }
        }
    }


    post {

        success {

            echo 'CI/CD pipeline completed successfully.'
        }

        failure {

            echo 'Pipeline failed. Check the Jenkins console output.'
        }

        always {

            sh '''
                docker logout || true

                docker system prune -f || true
            '''
        }
    }
}
