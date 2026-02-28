pipeline {
    agent any

    environment {
        IMAGE_NAME = "<YOUR_DOCKER_USERNAME>/ml-inference:latest"
        CONTAINER_NAME = "ml-inference-test"
        PORT = "8000"
    }

    stages {

        stage('Pull Image') {
            steps {
                echo "Pulling Docker image..."
                bat "docker pull %IMAGE_NAME%"
            }
        }

        stage('Run Container') {
            steps {
                echo "Starting container..."
                bat """
                docker rm -f %CONTAINER_NAME% || exit 0
                docker run -d -p %PORT%:8000 --name %CONTAINER_NAME% %IMAGE_NAME%
                """
            }
        }

        stage('Wait for Service Readiness') {
            steps {
                echo "Waiting for API..."
                bat """
                powershell -Command ^
                "$max=30; ^
                for($i=0;$i -lt $max;$i++){ ^
                  try{ ^
                    $r=Invoke-WebRequest -Uri http://localhost:%PORT%/health -UseBasicParsing; ^
                    if($r.StatusCode -eq 200){ exit 0 } ^
                  } catch{} ^
                  Start-Sleep -Seconds 2 ^
                }; ^
                exit 1"
                """
            }
        }

        stage('Send Valid Inference Request') {
            steps {
                echo "Testing valid input..."
                bat """
                curl -X POST http://localhost:%PORT%/predict ^
                  -H "Content-Type: application/json" ^
                  -d @valid_input.json > valid_response.txt

                type valid_response.txt
                findstr prediction valid_response.txt
                """
            }
        }

        stage('Send Invalid Request') {
            steps {
                echo "Testing invalid input..."
                bat """
                curl -o invalid_response.txt -w "%%{http_code}" ^
                  -X POST http://localhost:%PORT%/predict ^
                  -H "Content-Type: application/json" ^
                  -d @invalid_input.json > status.txt

                type invalid_response.txt
                type status.txt
                """
            }
        }

        stage('Stop Container') {
            steps {
                echo "Stopping container..."
                bat "docker rm -f %CONTAINER_NAME% || exit 0"
            }
        }
    }

    post {
        success {
            echo "Pipeline Passed"
        }
        failure {
            echo "Pipeline Failed"
        }
    }
}