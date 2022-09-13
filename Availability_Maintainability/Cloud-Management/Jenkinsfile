pipeline {
    environment {
        destBucket = "mnc-rule-bucket"
        masterDestPath = "REAN-ManagedCloud-DEV/Master"
        developDestPath = "REAN-ManagedCloud-DEV/Develop"
        crossaccount_role_arn = "arn:aws:iam::107339370656:role/mncPipelineRole"
        git_tag = "v0.1"
    }

    agent {
        node {
            label 'master'
            customWorkspace 'workspace/REAN-ManagedCloud/REAN-ManagedCloud-DEV/'
        }
    }

    stages{
        stage('Clean the workspace before build'){
            steps{
                script{
                    step([$class: 'WsCleanup'])
                }
            }
        }

        stage('Clone the REAN Managed Cloud repository') {
            steps {
                echo "Cloning REAN-Managed-Cloud Repo"
                script {
                    try {
	                dir('REAN-Managed-Cloud') {
	                    git 'git@github.com:reancloud/REAN-Managed-Cloud.git'
                        }
                    }
                    catch (Exception e) {
                        println "Not able to clone the REAN Managed Cloud repository"
                        println e
                        sh 'exit 1'
                    }
                }         
            }
        } 
          
        stage('Archive the branch have Latest commit') {
            steps {
                echo "finding the branch have latest commit"
                script {
                    try {
                        sh '''
	                    #!/bin/bash
	                    bash "$WORKSPACE/REAN-Managed-Cloud/archive_scripts.sh"
                        '''
                    }
                    catch (Exception e) {
                        println "Not able to Archive the REAN Managed Cloud repository"
                        println e
                        sh 'exit 1'
                    }
                }         
            }
        } 

        stage('Upload artifacts to s3') {
            steps {
                echo "uploading artifacts"
                script {
                    try {
                        sh '''
	                    #!/bin/bash
	                    bash "$WORKSPACE/REAN-Managed-Cloud/artifacts_scripts.sh"
                        '''
                    }
                    catch (Exception e) {
                        println "Not able to Upload artifacts to s3"
                        println e
                        sh 'exit 1'
                    }
                }           
            }
        } 
    
        stage('Clean the workspace after build'){
            steps{
                step([$class: 'WsCleanup'])
            }
        }
    }
}
