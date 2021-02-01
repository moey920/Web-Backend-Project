# 파이썬 웹 백엔드 구현을 위한 레포지토리입니다.

웹 백엔드 구현을 위한 프로젝트입니다. Flask와 MySQL, Azure 서버를 활용하여 배포까지 진행합니다.(예정)

> 현재는 Azure 연동은 진행하지 않았습니다.

- MySQL을 이용하여 DB를 생성하고 Flask 웹 서버에 연결하였습니다.
- board, boardArticle api를 강의를 토대로 구성하였습니다.
- user api를 Flask 기반으로 구현하였으며 
    - register 기능은 localhost:5000/register에서 정상적으로 form의 입력값을 가져와 DB에 저장하였습니다.
    - 회원가입 완료시 /login 페이지로 이동합니다
    - login 기능은 이메일과 패스워드를 받아 로그인 성공시 index.html로 이동합니다.
        - 로그인 기능이 작동하는 것은 확인하였으나 패스워드를 검사하는 기능에 오류가 있습니다.
        - 현재는 이메일만 존재하면 어떠한 패스워드로도 접속이 가능합니다.
- dashboard api는 /dashboart/```<intnum>```로 접속할 수 있습니다.
