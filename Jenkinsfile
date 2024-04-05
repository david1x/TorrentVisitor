properties([pipelineTriggers([cron('20 11,14,18 * * *')])])
pipeline {
    agent { label 'deepin' }

    environment {
        TOR_USER = credentials('TOR_USER')
        TOR_PASS = credentials('TOR_PASS')
        OTP_KEY = credentials('OTP_KEY')
    }

    stages {

        stage('Create Virtual Environment') {
            steps {
                script {
                        // Install pip if not already installed
                        def pipInstalled = sh(script: 'command -v pip', returnStatus: true) == 0
                        if (!pipInstalled) {
                            sh 'sudo apt-get update && sudo apt-get install -y python3-pip'
                        }
    
                        // Create a virtual environment in the TorrentHeadless directory
                        sh 'python3 -m venv venv'
    
                        // Activate the virtual environment
                        sh '. venv/bin/activate'
    
                        // Install requirements.txt within the virtual environment
                        sh 'sudo pip3 install -r requirements.txt'                    
                }
            }
        }

        stage('Run') {
            steps {
                    script {
                        // Use double quotes to interpolate variables
                        sh "python3 main.py"
                    }
            }
        }

        stage('Cleanup') {
            steps {
                deleteDir()
            }
        }
    }
    post{
        failure{
            emailext to: "davidamar1x@gmail.com",
            subject: "[${currentBuild.currentResult}] Jenkins Build: ${env.JOB_NAME}",
            body: "${currentBuild.currentResult}: Job ${env.JOB_NAME}\nMore Info can be found here: ${env.BUILD_URL}"
        }
    }

}

