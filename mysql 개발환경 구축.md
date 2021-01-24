# mysql 개발환경 구축

## mysql 설치 및 설정
```
choco update
choco install mysql
```

설치가 모두 끝났으면 mysql.server start 명령어를 이용해 MySQL 서버에 접속합니다.
그 뒤, 간단한 설정을 위해 mysql_secure_installation 명렁어를 실행합니다.

mysql.server start
mysql_secure_installation
이 명령을 실행하면 다음과 같은 설정에 대한 질문이 등장합니다.

Would you like to setup VALIDATE PASSWORD component?
Yes: 복잡한 비밀번호 설정
No: 간단한 비밀번호 설정 V
Remove anonymous users?
Yes: 접속하는 경우 -u 옵션 필요 V
No: 접속하는 경우 -u 옵션 불필요
Disallow root login remotely?
Yes: 원격접속 불가능 V
No: 원격접속 가능
Remove test database and access to it?
Yes: Test 데이터베이스 제거 V
No: Test 데이터베이스 유지
Reload privilege tables now?
Yes: 적용 V
No: 미적용
접속 확인
mysql -uroot -p
status
‘All Done!’과 함께 모든 설정을 마쳤으면 처음에 설정한 비밀번호와 함께 로그인 합니다.
그 후 status 명령어를 실행하여 DB의 character 설정이 모두 UTF-8로 되어 있는지 확인합니다.
아래와 같다면 잘 설정되어 있는 것입니다!
