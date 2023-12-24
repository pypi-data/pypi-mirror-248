-- 힌국어
이 라이브러리는 파이썬에서 더 쉬운 소켓 프로그래밍을 위한 라이브러리입니다. 
server 클래스와 Client 클래스를 생성해 프로그래밍을 하고, 프로토콜 부분과 데이터 부분을 나눠서 전송하고 받을 수 있습니다. 
대신, 프로토콜 부분이나 데이터 부분에 '__' 문자열을 넣지 마십시요. __ 문자열은 프로토콜과 데이터 부분을 나누는 문자열이기 때문에
프로토콜과 데이터가 의도치 않게 나누어지거나 밀릴 수 있습니다.

-- English
This library is for easier socket programming. 
It has server class and client class, we use that classes.
We can split protocol and data when program is sending or receiving.
But, you shouldn't use the '__' string in protocol or data.
because the protocol and data will be split or pushed, unintentionally.
