pipeline {
    agent { label 'ubuntu' }

    environment {
        TOR_USER = credentials('TOR_USER')
        TOR_PASS = credentials('TOR_PASS')
        OTP_KEY = credentials('OTP_KEY')
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    def repoDir = 'TorrentVisitor'
                    def repoExists = fileExists(repoDir)
                    def pipInstalled = sh(script: 'command -v pip', returnStatus: true) == 0

                    if (!repoExists) {
                        echo "Cloning the Git repository..."
                        sh 'git clone https://github.com/david1x/TorrentVisitor.git'
                    } else {
                        echo "Repository already exists. Removing existing repository and cloning a fresh copy."
                        sh "rm -rf ${repoDir}"
                        sh 'git clone https://github.com/david1x/TorrentVisitor.git'
                    }

                    // Install pip if not already installed
                    if (!pipInstalled) {
                        sh 'sudo apt-get update && sudo apt-get install -y python3-pip'
                    }

                    // Install requirements.txt on the Jenkins agent node
                    sh 'sudo pip3 install -r TorrentVisitor/requirements.txt'
                }
            }
        }


        stage('Run') {
            steps {
                script {
                    dir('TorrentVisitor') {
                        sh 'env | grep TOR_'
                        sh "python3 main.py"
                    }
                }
            }
        }

    }
}