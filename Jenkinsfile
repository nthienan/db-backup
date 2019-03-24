pipeline {
  agent {
    label 'docker'
  }
  stages {
    stage('Build') {
      steps {
        container('builder') {
          sh 'docker build -t nthienan/db-backup .'
        }
      }
    }
    stage('Archive') {
      steps {
        container('builder') {
          sh 'docker image'
        }
      }
    }
  }
}
