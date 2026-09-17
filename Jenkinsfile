pipeline {

    agent any

    environment {

        DOCKER_IMAGE = "sujaygope9939/jenkins-eks-app"

        DOCKER_CREDENTIALS = credentials('docker-hub-creds')

        AWS_REGION = 'eu-north-1'

        EKS_CLUSTER = 'casual-blues-monster'

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
                    export PYTHONPATH="$PWD"
                    pytest -v app/tests --junitxml=test-results.xml
                '''
            }

            post {
                always {
                    junit 'test-results.xml'
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

        stage('Docker Hub Login') {
            steps {
                sh '''
                    echo "${DOCKER_CREDENTIALS_PSW}" | \
                    docker login \
                        --username "${DOCKER_CREDENTIALS_USR}" \
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

        stage('Production Approval') {
            when {
                branch 'main'
            }

            steps {
                input message: 'Deploy this version to production?',
                      ok: 'Deploy'
            }
        }

        stage('Helm Deploy') {
            steps {
                sh '''
                    helm upgrade --install ${HELM_RELEASE} \
                        helm/myapp \
                        --namespace ${K8S_NAMESPACE} \
                        --create-namespace \
                        --set image.repository=${DOCKER_IMAGE} \
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

                    echo "Pods:"
                    kubectl get pods -n ${K8S_NAMESPACE}

                    echo "Services:"
                    kubectl get svc -n ${K8S_NAMESPACE}
                '''
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
