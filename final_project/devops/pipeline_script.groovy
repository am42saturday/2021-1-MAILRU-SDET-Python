pipeline {

    agent any

    stages {

        stage("Clear directory") {
            steps {
                cleanWs()
            }
        }

        stage('Clone repo with devops and tests') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: 'master']],
                    userRemoteConfigs: [[
                        credentialsId: 'b562eea5-2921-42ee-8ee1-0fa3b8750da6',
                        url: 'git@github.com:am42saturday/final_project_all.git']]
                ])
            }
        }

        stage('Run and configure myapp via docker-compose') {
            steps {
                step([
                    $class: 'DockerComposeBuilder',
                    dockerComposeFile: 'devops/docker-compose.yml',
                    option: [$class: 'StartAllServices'],
                    useCustomDockerComposeFile: true
                ])
            }
        }

        stage('Run tests') {
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE'){
                    script{
                        sh 'cd tests && python3 -m pytest -n ${NUM} ${MARK_TESTS}'
                    }
                }
            }
        }

        stage('Stop myapp') {
            steps {
                step([
                    $class: 'DockerComposeBuilder',
                    dockerComposeFile: 'devops/docker-compose.yml',
                    option: [$class: 'StopAllServices'],
                    useCustomDockerComposeFile: true
                ])
            }
        }
    }

    post {
        always{
            dir("tests"){
                allure ( commandline: '2.13.9',
                    includeProperties: false,
                    jdk: '',
                    results: [[path: 'report']])
            }
        }
    }
}
