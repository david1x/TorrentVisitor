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
                    
                    echo '*************'
                    echo 'before'
                    sh 'whoami && pwd'
                    echo '*************'

                    if (!repoExists) {
                        echo "Cloning the Git repository..."
                        sh 'git clone https://github.com/david1x/TorrentVisitor.git'
                    } else {
                        echo "Repository already exists. Removing existing repository and cloning a fresh copy."
                        sh "rm -rf ${repoDir}"
                        sh 'git clone https://github.com/david1x/TorrentVisitor.git'
                    }

                    echo '*************'
                    echo 'after'
                    sh 'whoami && pwd'
                    echo '*************'
                }
            }
        }

        stage('Create Virtual Environment') {
            steps {
                script {
                    echo '*************'
                    echo 'before'
                    sh 'whoami && pwd'
                    echo '*************'
                    dir('TorrentVisitor') {
                        echo '*************'
                        echo 'after and before venv'
                        sh 'whoami && pwd'
                        echo '*************'
                        // Install pip if not already installed
                        def pipInstalled = sh(script: 'command -v pip', returnStatus: true) == 0
                        if (!pipInstalled) {
                            sh 'sudo apt-get update && sudo apt-get install -y python3-pip'
                        }

                        // Create a virtual environment in the TorrentVisitor directory
                        sh 'python3 -m venv venv'
                        sh 'ls -lha'
                        // Activate the virtual environment
                        sh 'source venv/bin/activate'

                        // Install requirements.txt within the virtual environment
                        sh 'pip3 install -r requirements.txt'

                        echo '*************'
                        echo 'after venv'
                        sh 'whoami && pwd'
                        echo '*************'
                    }
                }
            }
        }

        stage('Run') {
            steps {
                script {
                    echo '*************'
                    echo 'before'
                    sh 'whoami && pwd'
                    echo '*************'
                    dir('TorrentVisitor') {
                        echo '*************'
                        echo 'after'
                        sh 'whoami && pwd'
                        echo '*************'
                        sh "python3 main.py"
                    }
                }
            }
        }

    }
}