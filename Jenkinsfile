#!/usr/bin/env groovy
def dockerImage

pipeline {
    environment {
    registry = "leonvzd/spring-petclinic:latest"
    registryCredential = 'dockerHubCredentials'
    dockerImage = ''
  }
    agent {
        label 'docker'
    }
    options {
        ansiColor('xterm')
        timestamps()
        timeout(30)
        disableConcurrentBuilds()
        buildDiscarder logRotator(numToKeepStr: '5')
    }
    triggers {
        cron '@daily'
    }

    stages {
        stage('Maven Build') {
            steps {
                script {
                    docker.image('maven:3-jdk-8-slim').inside {
                        sh 'mvn clean package --batch-mode'
                    }
                }
//                publishCoverage adapters: [jacocoAdapter('target/jacoco.exec')]
//                findbugs pattern: '**/target/findbugsXml.xml'
//                checkstyle pattern: '**/target/checkstyle-result.xml'
//                junit allowEmptyResults: true, testResults: '**/target/surefire-reports/**/*.xml'
                archiveArtifacts artifacts: '**/target/*.jar,**/target/*.war', fingerprint: true
            }
        }
        stage('Docker Build') {
            steps {
                script {
                    dockerImage = docker.build registry
                }
            }
        }
        stage('Deploy to Staging Server') {
            steps {
             //   createDynatraceDeploymentEvent(envId: 'cloud', tagMatchRules: tagMatchRules) {
                 createDynatraceDeploymentEvent(entityIds: 
                 [
                    [$class: 'Service', entityId: 'SERVICE-6D8644AEFD7A7A5D']
                     
                     ], envId: 'cloud', tagMatchRules: [[meTypes: [[meType: 'SERVICE']], tags: [[context: 'CONTEXTLESS', key: 'app', value: '"test"']]]]) {
    // some block
                 
                    sh 'docker-compose down'
                    sh 'docker-compose up -d'
                }
            }
        }
        stage('Performance Test') {
            steps {
                recordDynatraceSession(entityIds: [ [$class: 'Service', entityId: 'SERVICE-6D8644AEFD7A7A5D']], envId: 'cloud', testCase: 'loadtest') {
                //    performanceTest(readFile('performanceTest.json'))
                     bzt "blaze.yml"
                }
                perfSigDynatraceReports envId: 'cloud', specFile: 'specfile.json', nonFunctionalFailure: 2
            }
        }
        stage('Docker Push') {
            steps {
                 echo 'Docker Push!'
              /**  script {
                    docker.withRegistry('', registryCredential) {
                        dockerImage.push()
                    }
                } **/
            }
        }
        stage('deploy to Production') {
            steps {
                echo 'deploy to Production!'
            }
        }
    }
    post {
        always {
          echo 'done!'  
//          step([$class: 'Mailer', notifyEveryUnstableBuild: true, recipients: 'notify@me', sendToIndividuals: false])
        }
    }
}