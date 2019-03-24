pipeline {
  agent {
    label 'docker'
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
