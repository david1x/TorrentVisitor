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
                    checkout scm
                }
            }
        }

        stage('Create Virtual Environment') {
            steps {
                script {
                    // Install pip if not already installed
                    def pipInstalled = sh(script: 'command -v pip', returnStatus: true) == 0
                    if (!pipInstalled) {
                        sh 'sudo apt-get update && sudo apt-get install -y python3-pip'
                    }

                    // Create a virtual environment in the TorrentVisitor directory
                    sh 'python3 -m venv venv'

                    // Activate the virtual environment
                    sh '. venv/bin/activate'

                    // Install requirements.txt within the virtual environment
                    sh 'pip3 install -r requirements.txt'
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
                script {
                    cleanupFolders(['/tmp/workspace/TorrentHeadless', '/tmp/workspace/TorrentHeadless@tmp'])
                }
            }
        }
    }

    post {
        always {
            script {
                // Deactivate the virtual environment
                sh 'deactivate'
            }
            cleanupFolders(['/tmp/workspace/TorrentHeadless', '/tmp/workspace/TorrentHeadless@tmp'])
        }
    }
}

// Function to check if a file or folder exists
def fileExists(String path) {
    return file(path).exists()
}

// Function to cleanup folders
def cleanupFolders(List<String> folders) {
    // Loop through each folder
    folders.each { targetFolder ->
        // Check if the folder exists before attempting cleanup
        if (fileExists(targetFolder)) {
            sh "rm -rf ${targetFolder}"
            echo "Cleanup for ${targetFolder} completed successfully."
        } else {
            echo "Folder ${targetFolder} does not exist. No cleanup needed."
        }
    }
}
