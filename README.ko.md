### English (영어 설명서)
English README can be found [here](README.md).


# 트위치 -> 유튜브로 생방송 릴레이
트위치에서 방송이 시작하면 자동으로 그 방송을 그대로 유튜브에 비공개 라이브스트림으로 똑같이 전달합니다. 방송이 종료되면 다음 방송까지 대기하고 있다 다음 방송 시작 때 자동으로 유튜브 라이브스트림에 새 방송을 전달합니다.

# 사용법
```plaintext
main.py [-h] -c CHANNEL -s STREAM_KEY
  -c CHANNEL, --channel CHANNEL       
                        트위치 채널 영어 이름
  -s STREAM_KEY, --stream-key STREAM_KEY
                        유튜브 라이브스트림 준비하기 섹션의 #6번 단계에서 복사한 "OOOO-OOOO-OOOO-OOOO" 형식의 스트림키
```

# 유튜브 라이브스트림 준비하기
유튜브 정책상 라이브스트림 신청 후 24시간이 지나야 스트림키를 얻을 수 있습니다.
1. https://youtube.com/livestreaming 접속
2. 라이브스트림 신청 후 24시간동안 대기
3. https://youtube.com/livestreaming 에서 대시보드 가기
4. "새 스트림 키 만들기" 클릭
5. 새 스트림 키 설정
    a. **Name**: 유튜브 방송에 쓰일 제목. 나중에 수정 가능함
    b. **Streaming Protocol**: 꼭 "HLS" 여야 함
6. 스트림키를 스크립트 실행 시에 사용하기 위해 복사


# 기술적 세부 사항
## HLS pull/push
트위치는 [HLS (HTTP Live Streaming)](https://en.wikipedia.org/wiki/HTTP_Live_Streaming) 를 사용하여 생방송을 사용자들에게 전송하고, 유튜브에서도 HLS push를 사용하여 스트리머가 방송을 할 수 있습니다.

HLS는 (1) .m3u8 플레이리스트 와 (2) .ts 세그먼트 두 종류 파일로 이루어져 있습니다. 스크립트는 트위치에서 플레이리스트와 세그먼트를 다운받고, 유튜브용 플레이리스트를 만든 후 세그먼트 파일과 함께 업로드합니다.
## 재인코딩 없음 (FFMPEG 사용 안함)
트위치와 유튜브가 둘 다 HLS를 사용하기 때문에 별다른 인코딩 없이 유튜브에 그대로 세그먼트 파일을 업로드합니다. 따라서 CPU의 성능이 중요하지는 않습니다.
## Python 버전
이 코드는 Python 3.9에서 테스트하였습니다.