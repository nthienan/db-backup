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
        container('docker-18.05') {
          sh 'docker build -t nthienan/db-backup .'
        }
      }
    }
    stage('Archive') {
      steps {
        container('docker-18.05') {
          sh 'docker images'
        }
      }
    }
  }
}
