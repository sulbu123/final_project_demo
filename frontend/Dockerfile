FROM node:18-alpine

WORKDIR /app

# 필요한 빌드 도구 설치
RUN apk add --no-cache python3 make g++

# package.json과 package-lock.json 복사
COPY package*.json ./

# 글로벌 및 로컬 react-scripts 설치
RUN npm install -g react-scripts
RUN npm install

# 애플리케이션 소스 복사
COPY . .

# 빌드
RUN npm run build

# 프로덕션 서버 설치
RUN npm install -g serve

# 포트 노출
EXPOSE 3000

# 애플리케이션 실행
CMD ["serve", "-s", "build", "-l", "3000"] 