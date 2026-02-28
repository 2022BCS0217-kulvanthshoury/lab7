pipeline {
    agent any

    environment {
        IMAGE_NAME = "2022bcs0217shoury/ml-inference:latest"
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
                REM --- Remove container only if it exists ---
                docker ps -a --format "{{.Names}}" | findstr /I "%CONTAINER_NAME%" >nul
                if %errorlevel%==0 (
                    docker rm -f %CONTAINER_NAME%
                )

                REM --- Run fresh container ---
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
                $ready=$false; ^
                for($i=0;$i -lt $max;$i++){ ^
                  try{ ^
                    $r=Invoke-WebRequest -Uri http://localhost:%PORT%/health -UseBasicParsing; ^
                    if($r.StatusCode -eq 200){ ^
                        Write-Host 'API is ready'; ^
                        $ready=$true; ^
                        break; ^
                    } ^
                  } catch{} ^
                  Start-Sleep -Seconds 2 ^
                }; ^
                if(-not $ready){ exit 1 }"
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

                echo ===== VALID RESPONSE =====
                type valid_response.txt

                REM --- Validate prediction exists ---
                findstr /I "prediction" valid_response.txt >nul
                if %errorlevel% neq 0 exit /b 1
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

                echo ===== INVALID RESPONSE =====
                type invalid_response.txt
                type status.txt
                """
            }
        }

        stage('Stop Container') {
            steps {
                echo "Stopping container..."
                bat """
                docker ps -a --format "{{.Names}}" | findstr /I "%CONTAINER_NAME%" >nul
                if %errorlevel%==0 (
                    docker rm -f %CONTAINER_NAME%
                )
                """
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
        always {
            echo "Pipeline execution completed."
        }
    }
}