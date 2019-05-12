pipeline {
  agent {
    kubernetes {
      label 'db-backup'
      yamlFile 'builder-pod.yaml'
    }
  }
  stages {
    stage('Build') {
      steps {
        container('docker') {
          sh 'docker build -t nthienan/db-backup .'
        }
      }
    }
    stage('Archive') {
      steps {
        container('docker') {
          sh 'docker images'
        }
      }
    }
  }
}
