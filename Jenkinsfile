pipeline {
  agent {
    kubernetes {
      label 'docker'
      defaultContainer 'jnlp'
      yaml """
apiVersion: v1
kind: Pod
metadata:
  name: jenkins-slave
  labels:
    app: jenkins
    role: slave
    component: ci-cd
spec:
  containers:
    - name: dind
      image: docker:18.05-dind
      securityContext:
        privileged: true
      volumeMounts:
        - name: dind-storage
          mountPath: /var/lib/docker
  volumes:
    - name: dind-storage
      emptyDir: {}
"""
    }
  }
  stages {
    stage('Build') {
      steps {
        container('dind') {
          sh 'docker build -t nthienan/db-backup .'
        }
        container('busybox') {
          sh 'docker image'
        }
      }
    }
  }
}
