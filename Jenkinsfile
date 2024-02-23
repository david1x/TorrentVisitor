properties([pipelineTriggers([cron('20 11,14,18 * * *')])])
pipeline {
    agent { label 'ubuntu' }

    environment {
        TOR_USER = credentials('TOR_USER')
        TOR_PASS = credentials('TOR_PASS')
        OTP_KEY = credentials('OTP_KEY')
    }

    stages {
        // stage('Checkout') {
        //     steps {
        //         script {
        //             def repoDir = 'TorrentHeadless'
        //             def repoExists = fileExists(repoDir)
        //             def pipInstalled = sh(script: 'command -v pip', returnStatus: true) == 0

        //             if (!repoExists) {
        //                 echo "Cloning the Git repository..."
        //                 sh 'git clone https://gitea.amarsphere.com/davidamar/TorrentHeadless.git'
        //             } else {
        //                 echo "Repository already exists. Removing existing repository and cloning a fresh copy."
        //                 sh "rm -rf ${repoDir}"
        //                 sh 'git clone https://gitea.amarsphere.com/davidamar/TorrentHeadless.git'
        //             }
        //         }
        //     }
        // }

        stage('Create Virtual Environment') {
            steps {
                script {
                    // dir('TorrentHeadless') {
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
                    // }
                    
                }
            }
        }

        stage('Run') {
            steps {
                // dir('TorrentHeadless') {
                    script {
                        // Use double quotes to interpolate variables
                        sh "python3 main.py"
                    }
                    
                // }
            }
        }

        stage('Cleanup') {
            steps {
                script {
                    sh 'pwd'
                    def repoDir = 'TorrentHeadless'
                    sh 'pwd'
                    echo "Deleting Running Folder..."
                    sh "rm -rf ${repoDir}"
                    sh "rm -rf ${repoDir}@tmp"
                }
            }
        }
    }

    post {
        always {
            script {
                // Check if virtual environment is activated before deactivating
                if (sh(script: '[[ -n "$VIRTUAL_ENV" ]]', returnStatus: true) == 0) {
                    sh 'deactivate'
                    echo 'Deactivated the virtual environment.'
                } else {
                    echo 'No virtual environment is currently activated. Skipping deactivation.'
                }
                cleanWs(cleanWhenNotBuilt: false,
                        deleteDirs: true,
                        disableDeferredWipeout: true,
                        notFailBuild: true,
                        patterns: [[pattern: '.gitignore', type: 'INCLUDE'],
                                   [pattern: '.propsfile', type: 'EXCLUDE']])
            }
        }
    }
}

