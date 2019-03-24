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
        container('dind') {
          sh 'docker build -t nthienan/db-backup .'
        }
      }
    }
    stage('Archive') {
      steps {
        container('dind') {
          sh 'docker images'
        }
      }
    }
  }
}
